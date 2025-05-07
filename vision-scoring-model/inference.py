from transformers import AutoTokenizer
from train_scibert_regressor import SciBERTRegressor, MODEL_NAME, DEVICE
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import CATEGORY_MAP
import torch
import json

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = SciBERTRegressor(MODEL_NAME)
model.load_state_dict(torch.load("checkpoints/scibert_regressor.pt", map_location=DEVICE))
model.eval().to(DEVICE)

analyzer = SentimentIntensityAnalyzer()

# Load data
input_path = "synthetic_vision_ideas_filled.jsonl"

results = []
with open(input_path, "r") as f:
    for line in f:
        entry = json.loads(line)
        abstract = entry["abstract"]
        cat_codes = entry["categories"]
        novelty_score = entry["novelty_score"]

        if novelty_score > 0.6:
            label = "Visionary" 
        elif 0.3 < novelty_score <= 0.6:
            label = "Mid"
        else:
            label = "Skill"
            
        cat_names = [CATEGORY_MAP.get(code, code) for code in cat_codes]
        cat_text = " ".join(cat_names)
        input_text = f"{abstract.strip()} [SEP] categories: {cat_text}"

        # Tokenize input
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512
        )

        # Predict novelty score from our model
        with torch.no_grad():
            vision_score = model(
                input_ids=inputs["input_ids"].to(DEVICE),
                attention_mask=inputs["attention_mask"].to(DEVICE)
            ).item()

        # Sentiment score using VADER
        raw_sentiment = analyzer.polarity_scores(abstract)["compound"]
        sentiment_score = (raw_sentiment + 1) / 2  # Normalize to [0, 1]

        # Final score is based on sentiment score (how passionate they are about the project? Given a low weightage) and novelty score (from the trained model)
        predicted_score = 0.9 * vision_score + 0.1 * sentiment_score

        results.append({
            "abstract": abstract,
            "categories": cat_codes,
            "true_novelty_score": round(novelty_score, 4),
            "predicted_novelty_score": round(predicted_score, 4),
            "true_label" : label
        })


results_sorted = sorted(results, key=lambda r: r["predicted_novelty_score"], reverse=True)

print("\nInference Results (sorted by predicted score):")
for r in results_sorted:
    print(f"- True Label: {r['true_label']} | Predicted: {r['predicted_novelty_score']} | Abstract: {r['abstract'][:60]}...")

# # Save output
# with open(output_path, "w") as f:
#     for r in results:
#         f.write(json.dumps(r) + "\n")


