from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
import numpy as np

# Precompute embeddings
course_embeddings = np.load("models/course_embeddings.npy")

def neural_recommend(query, df):
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, course_embeddings)[0]

    top_k = scores.topk(10)

    results = []
    for score, idx in zip(top_k.values, top_k.indices):
        i = int(idx)
        results.append({
            "title": df.iloc[i]["Course Name"],
            "department": df.iloc[i]["Department"],
            "description": df.iloc[i]["Course Description"],
            "score": float(score * 100)
        })

    return results
