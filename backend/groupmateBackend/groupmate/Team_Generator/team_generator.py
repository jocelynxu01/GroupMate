import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import torch
import torch.nn as nn
from itertools import cycle
from transformers import AutoTokenizer, AutoModel


class SciBERTRegressor(nn.Module):
    
        
    def __init__(self, model_name: str):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        hidden_size = self.encoder.config.hidden_size
        self.regressor = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 1),
            nn.Sigmoid()  # output ∈ [0,1]
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        return self.regressor(pooled).squeeze(1)


def run_model(
    students,
    model_checkpoint: str = "groupmate/Team_Generator/data/scibert_regressor.pt",
    skills_file: str = "groupmate/Team_Generator/data/skills_list.txt",
    output_file: str = "groups_output.json",
    device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    api_key: str = "AIzaSyB6KoDBjmmXKojcYnLX69gL84LENQr-dmI"
):
    # ------------------------
    # Step 0: Load student data
    # ------------------------
    # with open(student_file, "r") as f:
    #     students = json.load(f)

    # ------------------------
    # Step 1: Predict vision scores
    # ------------------------
    MODEL_NAME = "allenai/scibert_scivocab_uncased"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model_sci = SciBERTRegressor(MODEL_NAME).to(device)
    model_sci.load_state_dict(torch.load(model_checkpoint, map_location=device))
    model_sci.eval()

    for student in students:
        print('student:',student)
        essay = student["project_proposal"]
        inputs = tokenizer(
            essay,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512
        )
        with torch.no_grad():
            score = model_sci(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device)
            ).item()
        student["vision_score"] = score

    # sort and split into tiers
    students_sorted = sorted(students, key=lambda x: x["vision_score"], reverse=True)
    n = len(students_sorted)
    third = n // 3
    visionaries = students_sorted[:third]
    collaborators = students_sorted[third:2*third]
    enablers = students_sorted[2*third:]

    print(f"Visionaries: {len(visionaries)}, Collaborators: {len(collaborators)}, Enablers: {len(enablers)}")

    # ------------------------
    # Step 2: Initialize groups
    # ------------------------
    groups = [
        {"members": [v], "needed_skills": [], "current_skills": []}
        for v in visionaries
    ]

    # ------------------------
    # Step 3: Infer needed skills
    # ------------------------
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel("models/gemini-1.5-flash")

    with open(skills_file, "r") as f:
        total_skills = [line.strip() for line in f]

    def infer_skills(essays: str):
        prompt = (
            "Based on these group vision essays, pick 5–7 skills from the list:\n\n"
            f"{', '.join(total_skills)}\n\n"
            f"Essays:\n{essays}\n\n"
            "Respond with a comma-separated list of chosen skills."
        )
        try:
            resp = llm.generate_content([prompt]).text
            picks = [s.strip() for s in resp.split(",")]
            return [s for s in picks if s in total_skills]
        except Exception:
            # fallback
            np.random.seed(hash(essays) % 2**32)
            return list(np.random.choice(total_skills, size=3, replace=False))

    for grp in groups:
        essays = " ".join([m["project_proposal"] for m in grp["members"]])
        grp["needed_skills"] = infer_skills(essays)

    # ------------------------
    # Step 4: Assign collaborators
    # ------------------------
    def missing(grp):
        return set(grp["needed_skills"]) - set(grp["current_skills"])

    grp_cycle = cycle(groups)

    while collaborators:
        assigned = False
        for _ in range(len(groups)):
            grp = next(grp_cycle)
            miss = missing(grp)
            for c in collaborators[:]:
                if miss.intersection(c["skills"]):
                    grp["members"].append(c)
                    grp["current_skills"].extend(c["skills"])
                    collaborators.remove(c)
                    assigned = True
                    break
        if not any(missing(g) for g in groups):
            break
        if not assigned:
            # just fill smallest groups
            while collaborators:
                tgt = min(groups, key=lambda g: len(g["members"]))
                c = collaborators.pop(0)
                tgt["members"].append(c)
                tgt["current_skills"].extend(c["skills"])
            break

    # ------------------------
    # Step 5: Assign enablers to fill
    # ------------------------
    for grp in sorted(groups, key=lambda g: len(g["members"])):
        while len(grp["members"]) < 4 and enablers:
            e = enablers.pop(0)
            grp["members"].append(e)
            grp["current_skills"].extend(e["skills"])

    # ------------------------
    # Step 6: Suggest project ideas
    # ------------------------
    def suggest_projects(essays: str, skills: list[str]):
        prompt = (
            "Based on the following vision essays and skills, suggest two project ideas:\n\n"
            f"Essays:\n{essays}\n\n"
            f"Skills: {', '.join(skills)}\n\n"
            "Return as a numbered list."
        )
        return llm.generate_content([prompt]).text.strip()

    for grp in groups:
        essays = " ".join([m["project_proposal"] for m in grp["members"]])
        grp["project_ideas"] = suggest_projects(essays, grp["current_skills"])

    # ------------------------
    # Final output
    # ------------------------
    

    with open(output_file, "w") as f:
        json.dump({"groups": groups}, f, indent=4)

    return groups


