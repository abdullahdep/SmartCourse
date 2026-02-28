from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch
import random
import os

# Set random seeds FIRST before any imports that use randomness
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

# Set PyTorch to deterministic mode
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Disable TensorFlow GPU to ensure deterministic behavior
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_DETERMINISTIC_OPS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

model = SentenceTransformer("all-MiniLM-L6-v2")
# Set model to eval mode for deterministic behavior
model.eval()

# Precompute embeddings
course_embeddings = np.load("models/course_embeddings.npy")

def neural_recommend(query, df):
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, course_embeddings)[0]

    top_k = scores.topk(10)

    def convert_nan(val):
        """Convert NaN values to None for JSON serialization"""
        if isinstance(val, float) and np.isnan(val):
            return None
        return val

    results = []
    for score, idx in zip(top_k.values, top_k.indices):
        i = int(idx)
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
            "score": round(float(score) * 100, 2)
        })

    return results
