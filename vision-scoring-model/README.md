# Vision Scoring Model

This repository contains a complete pipeline for scoring student vision essays using a fine-tuned SciBERT regressor. The model is trained on synthetic and heuristic-labeled data derived from research-style vision essays and outputs a continuous novelty score between 0 and 1.

## Objective

To evaluate how novel, visionary, and conceptually rich student project ideas are, based on freeform vision essays. This score is then used for intelligent team formation, enabling grouping of Visionaries, Collaborators, and Enablers in academic settings.

---

## Repository Structure
```
vision-scoring-model/
│
├── config.py # Configuration for model and paths
├── data_preprocessing.py # Cleans and prepares input data from JSONL to structured format
├── ground-truth-generation.py # Generates heuristic ground truth labels using novelty heuristics
├── train_scibert_regressor.py # Trains the SciBERT-based regressor on vision essay data
├── inference.py # Runs inference on new vision essays using the trained model
├── synthetic_vision_ideas_filled.jsonl # JSONL file of synthetic or collected vision essays with metadata
```
---
## Dataset

Before running any scripts, download the arXiv Metadata Dataset from Kaggle [Here](https://www.kaggle.com/datasets/Cornell-University/arxiv).

Place the downloaded file (e.g., arxiv-metadata-oai-snapshot.json) into the root of this repository.

## Quickstart

### 1. Install Requirements

```bash
pip install -r requirements.txt
```
2. Preprocess Data
```bash
python data_preprocessing.py
```
3. Generate Ground Truth Labels
```bash
python ground-truth-generation.py
```
This uses heuristic scoring metrics like semantic distance, lexical novelty, and entropy to assign weak labels.

4. Train the Vision Scoring Model
```bash
python train_scibert_regressor.py
```
This will fine-tune a SciBERT model to predict continuous novelty scores.

5. Run Inference
```bash
python inference.py --input_file path_to_essays.jsonl --output_file predictions.jsonl
```

## Heuristic Signals Used

Semantic Distance: Measured by comparing essay embeddings to domain centroids.

Lexical Novelty: Based on TF-IDF similarity to common essay patterns.

Entropy of Tags: Captures interdisciplinary depth using category entropy.

These are used as weak supervision for training the regressor.

## Input Format

Each vision essay should be a JSONL entry like:

```
{
  "student_id": "stu_3005",
  "essay": "I want to build a decentralized platform for refugee credential verification using blockchain and NLP...",
  "skills": ["blockchain", "NLP", "React", "Firebase"],
  "courses": ["AI Ethics", "Crypto Systems"]
}
```
## Output Format
```
{
  "student_id": "stu_3005",
  "predicted_score": 0.87
}
```
Notes
Uses SciBERT for domain-sensitive text embeddings.
Can be extended to include sentiment scores (e.g., via VADER) to incorporate passion or emotional tone in future iterations.
Ideal for classroom group formation tasks or research mentorship matching.
