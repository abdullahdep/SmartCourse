import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import random

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
tfidf_matrix = load_npz("models/tfidf_features.npz")

def tfidf_recommend(query, df, top_k=10):
    query_vec = vectorizer.transform([query]).toarray()  # must use SAME vectorizer
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_idx = similarity.argsort()[::-1][:top_k]

    def convert_nan(val):
        """Convert NaN values to None for JSON serialization"""
        if isinstance(val, float) and np.isnan(val):
            return None
        return val

    results = []
    for i in top_idx:
        results.append({
            "title": convert_nan(df.iloc[i]["University"]),
            "department": convert_nan(df.iloc[i]["Department"]),
            "city": convert_nan(df.iloc[i]["City/Cities"]),
            "description": convert_nan(df.iloc[i]["Course Description"]),
            "shifts": convert_nan(df.iloc[i]["shifts"]),
            "online": convert_nan(df.iloc[i]["online"]),
            "admission_dates": convert_nan(df.iloc[i]["Admission dates"]),
            "marks_required": convert_nan(df.iloc[i]["Marks required"]),
            "labs_available": convert_nan(df.iloc[i]["Labs Avalible"]),
            "course_title": convert_nan(df.iloc[i]["Course title"]),
            "score": round(float(similarity[i] * 100), 2)
        })
    return results
