import json
import numpy as np
import pandas as pd
from itertools import cycle
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# ------------------------
# CONFIGURATION
# ------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Models for vision‐score regression (SciBERT) and embeddings (MPNet)
REGRESSOR_NAME = "allenai/scibert_scivocab_uncased"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"


def run_model(
    student_file: str = "data/vision_students.json",
    model_checkpoint: str = "model_checkpoint/scibert_regressor.pt",
    skills_file: str = "data/skills_list.txt",
    output_file: str = "groups_output.json",
    device: torch.device = DEVICE,
    api_key: str = "YOUR_API_KEY"
):
    # ------------------------
    # LOAD TOKENIZERS & MODELS
    # ------------------------
    class SciBERTRegressor(nn.Module):
        def __init__(self, model_name):
            super().__init__()
            self.encoder = AutoModel.from_pretrained(model_name)
            self.regressor = nn.Sequential(
                nn.Linear(self.encoder.config.hidden_size, 128),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(128, 1),
                nn.Sigmoid()
            )
        def forward(self, input_ids, attention_mask):
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
            return self.regressor(out.pooler_output).squeeze(1)

    tokenizer_reg = AutoTokenizer.from_pretrained(REGRESSOR_NAME)
    model_reg = SciBERTRegressor(REGRESSOR_NAME).to(device)
    model_reg.load_state_dict(
        torch.load(model_checkpoint, map_location=device)
    )
    model_reg.eval()

    tokenizer_emb = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
    model_emb = AutoModel.from_pretrained(EMBEDDING_MODEL_NAME).to(device)
    model_emb.eval()

    # ------------------------
    # LOAD STUDENT DATA
    # ------------------------
    with open(student_file) as f:
        students = json.load(f)

    # ------------------------
    # STEP 1: Compute vision_score & embeddings
    # ------------------------
    for student in students:
        text = student["vision"]

        # vision score
        inputs = tokenizer_reg(text, return_tensors="pt",
                               truncation=True, padding="max_length", max_length=512)
        with torch.no_grad():
            vs = model_reg(
                input_ids=inputs.input_ids.to(device),
                attention_mask=inputs.attention_mask.to(device)
            ).item()
        student["vision_score"] = vs

        # embedding
        emb_inputs = tokenizer_emb(text, return_tensors="pt",
                                   truncation=True, padding="max_length", max_length=256)
        with torch.no_grad():
            emb_out = model_emb(**{k: v.to(device) for k, v in emb_inputs.items()})
        if hasattr(emb_out, "pooler_output"):
            emb = emb_out.pooler_output.cpu().numpy()
        else:
            emb = emb_out.last_hidden_state.mean(dim=1).cpu().numpy()
        student["embedding"] = emb

    # ------------------------
    # STEP 2: Sort & split into pools
    # ------------------------
    students_sorted = sorted(students, key=lambda x: x["vision_score"], reverse=True)
    n = len(students_sorted)
    third = n // 3
    visionaries  = students_sorted[:third]
    collaborators = students_sorted[third:2*third]
    enablers      = students_sorted[2*third:]

    groups = [
        {"members": [v], "needed_skills": [], "current_skills": []}
        for v in visionaries
    ]

    # ------------------------
    # STEP 3: Infer skills needed (LLM)
    # ------------------------
    genai.configure(api_key=api_key)
    model_llm = genai.GenerativeModel("models/gemini-1.5-flash")

    with open(skills_file) as f:
        all_skills = [l.strip() for l in f]

    def infer_needed_skills(essays: str):
        prompt = f"""
Based on these vision essays, select 5–7 skills from:
{', '.join(all_skills)}

Essays:
{essays}

Return a comma-separated list of chosen skills.
"""
        try:
            resp = model_llm.generate_content([prompt]).text
            skills = [s.strip() for s in resp.split(",") if s.strip() in all_skills]
            if skills:
                return skills
        except:
            pass
        np.random.seed(hash(essays) & 0xffffffff)
        return list(np.random.choice(all_skills, size=3, replace=False))

    for grp in groups:
        essays = " ".join([m["vision"] for m in grp["members"]])
        needed = infer_needed_skills(essays)
        grp["needed_skills"] = needed

    # ------------------------
    # STEP 4: Assign collaborators with weighted scoring
    # ------------------------
    def group_embedding(group):
        embs = np.vstack([m["embedding"] for m in group["members"]])
        return embs.mean(axis=0, keepdims=True)

    remaining = collaborators[:]
    assigned = True

    while remaining and assigned:
        assigned = False
        for grp in groups:
            needed = set(grp["needed_skills"]) - set(grp["current_skills"])
            if not needed:
                continue

            g_emb = group_embedding(grp)
            scores = []
            for c in remaining:
                v_sim      = cosine_similarity(g_emb, c["embedding"])[0,0]
                skill_frac = len(needed & set(c["skills"])) / len(needed)
                score      = 0.3 * v_sim + 0.7 * skill_frac
                scores.append((c, score))

            best_c, best_score = max(scores, key=lambda x: x[1])
            if needed & set(best_c["skills"]):
                grp["members"].append(best_c)
                grp["current_skills"].extend(best_c["skills"])
                remaining.remove(best_c)
                assigned = True

    for c in remaining:
        grp_smallest = min(groups, key=lambda g: len(g["members"]))
        grp_smallest["members"].append(c)
        grp_smallest["current_skills"].extend(c["skills"])
    remaining.clear()

    # STEP 5: Assign enablers by skill until all slots filled
    remaining_enablers = enablers[:]
    for grp in sorted(groups, key=lambda g: len(g["members"])):
        while len(grp["members"]) < 4 and remaining_enablers:
            missing = set(grp["needed_skills"]) - set(grp["current_skills"])   
            scores = [(e, len(missing & set(e["skills"])) / (len(missing) if missing else 1))
                      for e in remaining_enablers]
            best_e, best_score = max(scores, key=lambda x: x[1])
            grp["members"].append(best_e)
            grp["current_skills"].extend(best_e["skills"])
            remaining_enablers.remove(best_e)

    for e in remaining_enablers:
        grp_smallest = min(groups, key=lambda g: len(g["members"]))
        grp_smallest["members"].append(e)
        grp_smallest["current_skills"].extend(e["skills"])

    # ------------------------
    # STEP 6: Suggest project ideas (LLM)
    # ------------------------
    def suggest_projects(essays: str, skills: list[str]):
        prompt = f"""
Vision Essays:
{essays}

Skills:
{', '.join(skills)}

Suggest:
1. One project based on the essays.
2. One project leveraging the skills.
"""
        return model_llm.generate_content([prompt]).text.strip()

    for grp in groups:
        essays = " ".join([m["vision"] for m in grp["members"]])
        skills = grp["current_skills"]
        grp["project_ideas"] = suggest_projects(essays, skills)

    # ------------------------
    # OUTPUT RESULTS
    # ------------------------

    for i, grp in enumerate(groups, 1):
        member_ids = [m["id"] for m in grp["members"]]
        print(f"\n--- Group {i} ---")
        print("Members:", member_ids)
        print("Skills:", grp["current_skills"])
        print("Projects:", grp["project_ideas"])

    def convert_ndarrays(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if isinstance(v, np.ndarray):
                    obj[k] = v.tolist()
                else:
                    convert_ndarrays(v)
        elif isinstance(obj, list):
            for item in obj:
                convert_ndarrays(item)

    convert_ndarrays(groups)

    with open(output_file, "w") as f:
        json.dump({"groups": groups}, f, indent=4)


if __name__ == "__main__":
    run_model()
