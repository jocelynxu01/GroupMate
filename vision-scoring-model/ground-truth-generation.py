CLEAN_DATA_PATH = "arxiv_data_2023.jsonl"
OUTPUT_PATH = "training-dataset.jsonl"

'''
Heuristic 1: skill entropy score:
To capture how different the 

What Does Category Entropy Mean? Entropy here measures how diverse the co-authors' research backgrounds are, based on the categories they've published in.
If a paper has a high Category Entropy it means, the authors who worked on the paper have published across many different arXiv categories. Their experience is broad and interdisciplinary. (More visionary). And low category entropy means the authors publish mostly in the same few categories.
their expertise is narrow or domain-specific. (More skill based)

I'm hoping this heuristic will proxy for: 
Detecting interdisciplinary collaborations.
Scoring papers on diversity of expertise in author teams.
Correlated with innovation, impact, or novelty.
'''
import json
from collections import defaultdict, Counter
from tqdm import tqdm
from scipy.stats import entropy

import unicodedata
import re



# Clean author name function (taken from pre proecesiing dataset code)

MAX_FIRST_LEN = 15
MAX_MIDDLE_LEN = 15
MAX_LAST_LEN = 20
def normalize_author_name(name: str) -> str:
    """Lowercase and collapse whitespace for consistent lookup."""
    return re.sub(r'\s+', ' ', name.strip().lower())

def clean_author_name(parsed_entry):
    parsed_entry = (parsed_entry + ["", "", ""])[:3]
    last, first, middle = parsed_entry
    first = unicodedata.normalize("NFC", first.strip())
    middle = unicodedata.normalize("NFC", middle.strip())
    last = unicodedata.normalize("NFC", last.strip())
    if len(first) > MAX_FIRST_LEN or len(middle) > MAX_MIDDLE_LEN or len(last) > MAX_LAST_LEN:
        return None
    name = f"{first} {last} {middle}".strip()
    return re.sub(r'\s+', ' ', name)

# Author → {category → count}
author_category_counts = defaultdict(lambda: defaultdict(int))
FULL_DATA_PATH = "arxiv-metadata-oai-snapshot.json"

with open(FULL_DATA_PATH, 'r') as f:
    for line in tqdm(f, desc="Building author-category counts"):
        try:
            entry = json.loads(line)
        except:
            continue
        if not all(k in entry for k in ["authors_parsed", "categories"]):
            continue
        raw_cats = entry["categories"].split()
        cleaned_authors = set()
        for a in entry["authors_parsed"]:
            cleaned = clean_author_name(a)
            if cleaned:
                cleaned_authors.add(cleaned)

        for author in cleaned_authors:
            norm_author = normalize_author_name(author)
            for cat in raw_cats:
                author_category_counts[norm_author][cat] += 1            


def compute_entropy_from_author_category_union(authors, author_category_counts):
    total_cat_counts = Counter()

    for author in authors:
        cat_counts = author_category_counts.get(normalize_author_name(author), {})

        for cat, count in cat_counts.items():
            total_cat_counts[cat] += count

    values = list(total_cat_counts.values())
    if not values or sum(values) == 0:
        return 0.0
    return entropy(values, base=2)


with open(CLEAN_DATA_PATH, 'r') as f_in, open(OUTPUT_PATH, 'w') as f_out:
    for line in tqdm(f_in, desc="Computing entropy per paper"):
        entry = json.loads(line)
        authors = entry["authors"]
        categories = entry["categories"]
        h = compute_entropy_from_author_category_union(authors, author_category_counts)
        entry["category_entropy"] = h

        f_out.write(json.dumps(entry) + '\n')

'''
Heuristic 2: Semantic Score
Through this score I wanna capture how semantically different a paper is from the "central idea" of its category distribution cluster.

First Clustre papers from similar category sitributions. We treat this category distribution as a soft label (like a topic mixture or probability distribution). 
I am generating only 20 clusters for now (very small compared to our dataset), but I don't ahve enough compute to generate more clusters.
First task:
    Compute category distribution vectors for each paper (similar to what we did in the first heuristic)
    Calculate pairwise Jensen–Shannon divergences, this was giving better scores than cosine distances. This is a standard metric used to compare distributions.
    Cluster papers into 20 category-based clusters
    Show you which paper belongs to which cluster

Second Task:
    Map each paper_id to cluster_id from the category mixture clustering in Task 1
    Map each paper_id to SPECTER embedding from the abstract
    For each cluster_id, compute its centroid embedding
    For each paper:
        Compute cosine_distance(embedding, cluster_centroid)
    This cosine distance is teh semantic score
'''

import json
import numpy as np
from collections import defaultdict, Counter
from tqdm import tqdm
from scipy.spatial.distance import pdist, squareform, jensenshannon
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize



from config import arxiv_cs_categories, arxiv_all_categories\


import unicodedata
import re

category_index = {cat: i for i, cat in enumerate(arxiv_all_categories)}

# Load cleaned papers
paper_vectors = []
paper_ids = []
abstracts = []

with open(CLEAN_DATA_PATH, "r") as f:
    for line in tqdm(f, desc="Processing papers"):
        entry = json.loads(line)
        paper_id = entry["id"]
        authors = entry["authors"]
        abstract = entry["abstract"]

        vector = np.zeros(len(arxiv_all_categories))
        for author in authors:
            a_norm = author.strip().lower()
            if a_norm in author_category_counts:
                for cat, count in author_category_counts[a_norm].items():
                    if cat in category_index:
                        vector[category_index[cat]] += count

        if vector.sum() == 0:
            continue 
        vector /= vector.sum()  # normalize to make it a distribution

        paper_ids.append(paper_id)
        paper_vectors.append(vector)
        abstracts.append(abstract)

paper_matrix = np.vstack(paper_vectors)

sample_size = 20000  
indices = np.random.choice(len(paper_matrix), size=sample_size, replace=False)
paper_matrix = paper_matrix[indices]
paper_ids = [paper_ids[i] for i in indices]

print("Computing Jensen-Shannon divergence matrix...")
jsd_matrix = squareform(pdist(paper_matrix, metric='jensenshannon'))

print("Clustering papers...")
clusterer = AgglomerativeClustering(n_clusters=40, affinity='precomputed', linkage='average')
labels = clusterer.fit_predict(jsd_matrix)

paper_clusters = {pid: int(label) for pid, label in tqdm(zip(paper_ids, labels), total=len(paper_ids), desc="Assigning clusters")}

# Save to JSON
with open("paper_clusters.json", "w") as f:
    json.dump(paper_clusters, f, indent=2)

print("Saved paper_clusters.json with", len(paper_clusters), "entries.")


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("allenai/specter2_base")
paper_embeddings = model.encode(abstracts, convert_to_numpy=True)

paper_id_to_embedding = {}
for i in range(len(paper_ids)):
    paper_id_to_embedding[paper_id[i]] = paper_embeddings[i]

from collections import defaultdict
import numpy as np

cluster_embeddings = defaultdict(list)

for paper_id, cluster_id in paper_clusters.items():
    if paper_id in paper_id_to_embedding:
        cluster_embeddings[cluster_id].append(paper_id_to_embedding[paper_id])

# Compute centroid per cluster
cluster_centroids = {
    cid: np.mean(embeds, axis=0) for cid, embeds in cluster_embeddings.items()
}


from sklearn.metrics.pairwise import cosine_distances

semantic_novelty = {}

for paper_id, cluster_id in paper_clusters.items():
    if paper_id not in paper_id_to_embedding:
        continue
    emb = paper_id_to_embedding[paper_id]
    centroid = cluster_centroids[cluster_id]
    dist = cosine_distances([emb], [centroid])[0][0]
    semantic_novelty[paper_id] = dist


with open(OUTPUT_PATH, 'w') as f_out:
    for line in tqdm(f_out, desc="Addding Semantic novelty scores"):
        entry = json.loads(line)
        paper_id = entry["paper_id"]
        entry["semantic_novelty"] = semantic_novelty[paper_id]
        f_out.write(json.dumps(entry) + '\n')

'''
Heuristic 3: Lexical  Similar Encoding using a TFIDF, very low weight assigned in final novelty score computation
Captures: How different is a paper’s wording vs its peer cluster
'''

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
from tqdm import tqdm


vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
X = vectorizer.fit_transform(abstracts)

k = 40  # there are 40 cs categories
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(X)

centroids = kmeans.cluster_centers_
lexical_novelty = {}

for i, pid in enumerate(paper_ids):
    cluster_id = clusters[i]
    vector = X[i]
    centroid = centroids[cluster_id]
    dist = cosine_distances(vector, centroid.reshape(1, -1))[0][0]
    lexical_novelty[pid] = dist


with open(OUTPUT_PATH, 'w') as f_out:
    for line in tqdm(f_out, desc="Addding Semantic novelty scores"):
        entry = json.loads(line)
        paper_id = entry["paper_id"]
        entry["lexical_novelty"] = lexical_novelty[paper_id]
        f_out.write(json.dumps(entry) + '\n')

'''
Normalise and compute final vision score as:
0.5*semantic novelty + 0.4*categorical entropy + 0.1*lexical novelty
'''
import json
from tqdm import tqdm


print("Loading training-dataset.jsonl...")
with open(OUTPUT_PATH, "r") as f:
    data = [json.loads(line) for line in tqdm(f, desc="Loading data")]

def normalize_field(data, field_name):
    print(f"Normalizing field: {field_name}")
    values = [p[field_name] for p in data if p[field_name] is not None]
    min_val, max_val = min(values), max(values)
    for p in tqdm(data, desc=f"Normalizing {field_name}"):
        p[f"{field_name}_norm"] = (p[field_name] - min_val) / (max_val - min_val)


normalize_field(updated_data, "semantic_novelty")
normalize_field(updated_data, "lexical_novelty")
normalize_field(updated_data, "category_entropy")

print("Computing final_novelty_score...")
for p in tqdm(data, desc="Scoring"):
    semantic = p.get("semantic_novelty_norm", 0)
    entropy = p.get("category_entropy_norm", 0)
    lexical = p.get("lexical_novelty_norm", 0)

    p["final_novelty_score"] = (
        0.5 * semantic +
        0.4 * entropy +
        0.1 * lexical
    )

print("Saving updated dataset...")
with open(OUTPUT_PATH, "w") as f:
    for p in tqdm(data, desc="Writing"):
        f.write(json.dumps(p) + "\n")

print(f"\nDone. Saved {len(data)} papers to {INPUT_PATH}")




