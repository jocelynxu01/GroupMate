import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import itertools
import json


team_size = 3  #add field in the UI

with open("data/vision_students.json", "r") as f:
    students = json.load(f)

df = pd.DataFrame(students)
embed_model = SentenceTransformer('all-mpnet-base-v2')
vision_embeddings = embed_model.encode(df['vision'].tolist(), normalize_embeddings=True)

mlb_skills = MultiLabelBinarizer().fit(df['skills'])
skills_bin = mlb_skills.transform(df['skills'])
mlb_courses = MultiLabelBinarizer().fit(df['courses'])
courses_bin = mlb_courses.transform(df['courses'])


def compute_pair_score(i, j):
    vision_sim = cosine_similarity([vision_embeddings[i]], [vision_embeddings[j]])[0][0]

    skill_i, skill_j = set(df.loc[i, 'skills']), set(df.loc[j, 'skills'])
    course_i, course_j = set(df.loc[i, 'courses']), set(df.loc[j, 'courses'])

    skill_overlap = len(skill_i & skill_j) / len(skill_i | skill_j) if skill_i | skill_j else 0
    course_overlap = len(course_i & course_j) / len(course_i | course_j) if course_i | course_j else 0

    skill_score = 1 - skill_overlap
    course_score = 1 - course_overlap

    return 0.8 * vision_sim + 0.1 * skill_score + 0.1 * course_score


n = len(df)
similarity = np.zeros((n, n))
for i, j in itertools.combinations(range(n), 2):
    score =compute_pair_score(i, j)
    similarity[i][j]=similarity[j][i]=score

# Greedy for now
def score_group(group):
    pairs = list(itertools.combinations(group, 2))
    return sum(similarity[i][j] for i, j in pairs) / len(pairs)

unassigned = set(range(n))
teams = []

while len(unassigned) >= team_size:
    best_group=None
    best_score=-1
    for group in itertools.combinations(unassigned, team_size):
        score=score_group(group)
        if score > best_score:
            best_score=score
            best_group=group
    for idx in best_group:
        unassigned.remove(idx)
    teams.append(list(best_group))

# leftover students
if unassigned:
    teams.append(list(unassigned))

for idx, team in enumerate(teams):
    print("=" * 40)
    print(f"Team {idx + 1}")
    print("=" * 40)
    for i in team:
        row = df.loc[i]
        print(f"ID: {row['id']}")
        print(f"Name: {row['first_name']}")
        print(f"Vision:\n  {row['vision']}")
        print(f"Skills:\n  {', '.join(row['skills'])}")
        print(f"Courses:\n  {', '.join(row['courses'])}")
        print("-" * 40)
