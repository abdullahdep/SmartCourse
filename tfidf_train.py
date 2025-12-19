import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

# Load your dataset
df = pd.read_csv("data/courses_preprocessed.csv")  # or your extended dataset
corpus = df['Course Description'].fillna('').tolist()

# Train TF-IDF vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
tfidf_matrix = vectorizer.fit_transform(corpus)

# Save both
os.makedirs("models", exist_ok=True)
np.savez_compressed("models/tfidf_features.npz", tfidf_matrix.toarray())  # matrix
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")  # vectorizer

print("TF-IDF vectorizer and matrix saved successfully!")
