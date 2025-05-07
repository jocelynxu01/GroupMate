import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import AutoTokenizer, AutoModel
from torch.optim import AdamW
from tqdm import tqdm
import numpy as np
import os 

from config import CATEGORY_MAP, MODEL_NAME, BATCH_SIZE, EPOCHS, LR, DEVICE, PATIENCE

# data path
DATA_PATH = "training-dataset.jsonl"
CHECKPOINT_PATH = "checkpoints/scibert_regressor.pt"

# ----- Dataset -----
# Take abstract+categories to predict final score
class NoveltyDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_len=512):
        self.samples = []
        with open(file_path, "r") as f:
            for line in f:
                d = json.loads(line)
                if "abstract" in d and "final_novelty_score" in d and "categories" in d:
                    abstract = d["abstract"].strip()
                    # Map category codes to readable names
                    full_names = [CATEGORY_MAP.get(cat, cat) for cat in d["categories"]]
                    categories_text = " ".join(full_names)
                    # Combine abstract and mapped categories
                    full_input = f"{abstract} [SEP] categories: {categories_text}"
                    self.samples.append((full_input, float(d["final_novelty_score"])))
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        text, score = self.samples[idx]
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "score": torch.tensor(score, dtype=torch.float)
        }


# ----- Model -----
class SciBERTRegressor(nn.Module):
    def __init__(self, model_name):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.regressor = nn.Sequential(
            nn.Linear(self.encoder.config.hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Ensure output ∈ [0,1]
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        return self.regressor(pooled).squeeze(1)

# ----- Training Loop -----
def train():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    dataset = NoveltyDataset(DATA_PATH, tokenizer)
    total_len = len(dataset)
    val_len = int(0.2 * total_len)
    train_len = total_len - val_len

    train_set, val_set = random_split(dataset, [train_len, val_len])
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=BATCH_SIZE)

    model = SciBERTRegressor(MODEL_NAME).to(DEVICE)
    optimizer = AdamW(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()

    best_val_loss = float("inf")
    patience_counter = 0

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]"):
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            scores = batch["score"].to(DEVICE)

            preds = model(input_ids, attention_mask)
            loss = loss_fn(preds, scores)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        avg_train_loss = total_loss / len(train_loader)

        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in tqdm(val_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Val]"):
                input_ids = batch["input_ids"].to(DEVICE)
                attention_mask = batch["attention_mask"].to(DEVICE)
                scores = batch["score"].to(DEVICE)

                preds = model(input_ids, attention_mask)
                val_loss += loss_fn(preds, scores).item()
        avg_val_loss = val_loss / len(val_loader)

        print(f" Epoch {epoch+1} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

        # Early stopping and checkpointing
        if avg_val_loss < best_val_loss:
            print("Validation improved! Saving checkpoint...")
            torch.save(model.state_dict(), CHECKPOINT_PATH)
            best_val_loss = avg_val_loss
            patience_counter = 0
        else:
            patience_counter += 1
            print(f" No improvement. Patience: {patience_counter}/{PATIENCE}")
            if patience_counter >= PATIENCE:
                print("Early stopping triggered.")
                break

    print(f"\nBest Validation Loss: {best_val_loss:.4f}")
    print(f"Final model saved to {CHECKPOINT_PATH}")

if __name__ == "__main__":
    train()
