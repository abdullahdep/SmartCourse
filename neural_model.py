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
            "title": df.iloc[i]["University"],
            "department": df.iloc[i]["Department"],
            "city": df.iloc[i]["City/Cities"],
            "description": df.iloc[i]["Course Description"],
            "shifts": df.iloc[i]["shifts"],
            "online": df.iloc[i]["online"],
            "admission_dates": df.iloc[i]["Admission dates"],
            "marks_required": df.iloc[i]["Marks required"],
            "labs_available": df.iloc[i]["Labs Avalible"],
            "score": float(score * 100)
        })

    return results
