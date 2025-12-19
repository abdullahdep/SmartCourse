import numpy as np
import pandas as pd
import joblib
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

df = pd.read_csv("../data/courses_preprocessed.csv")

vectorizer = joblib.load("../models/tfidf_vectorizer.joblib")
tfidf_matrix = load_npz("../models/tfidf_features.npz")
neural_emb = np.load("../models/course_embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

sample_queries = [
    "I want to learn python for data science",
    "courses for machine learning beginner",
    "web development with javascript",
    "database fundamentals"
]

def evaluate_tfidf(query, k=10):
    q_vec = vectorizer.transform([query])
    sim = cosine_similarity(q_vec, tfidf_matrix).flatten()
    return sim.argsort()[::-1][:k]

def evaluate_neural(query, k=10):
    q_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(q_emb, neural_emb)[0]
    return scores.topk(k).indices.cpu().numpy()

def precision_at_k(pred_idx, true_idx, k):
    return len(set(pred_idx[:k]) & set(true_idx[:k])) / k

print("\n===== Model Evaluation =====\n")

for q in sample_queries:
    print(f"\nQuery: {q}")

    tfidf_results = evaluate_tfidf(q)
    neural_results = evaluate_neural(q)

    print("TF-IDF Top Result:", df.iloc[tfidf_results[0]]["Course Name"])
    print("Neural Top Result:", df.iloc[neural_results[0]]["Course Name"])

    overlap = len(set(tfidf_results) & set(neural_results))
    print("Overlap in top 10:", overlap)
