import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz

df = pd.read_csv("../data/courses_preprocessed.csv")

corpus = df["clean_text"].astype(str).tolist()

vectorizer = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(corpus)

joblib.dump(vectorizer, "../models/tfidf_vectorizer.joblib")
save_npz("../models/tfidf_features.npz", tfidf_matrix)

print("TF-IDF model trained.")
