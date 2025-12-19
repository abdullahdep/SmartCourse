import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz

vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
tfidf_matrix = load_npz("models/tfidf_features.npz")

def tfidf_recommend(query, df, top_k=10):
    query_vec = vectorizer.transform([query]).toarray()  # must use SAME vectorizer
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_idx = similarity.argsort()[::-1][:top_k]

    results = []
    for i in top_idx:
        results.append({
            "title": df.iloc[i]["University"],
            "department": df.iloc[i]["Department"],
            "description": df.iloc[i]["Course Description"],
            "score": round(float(similarity[i] * 100), 2)
        })
    return results
