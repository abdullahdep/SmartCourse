import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

df = pd.read_csv("../data/courses_preprocessed.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

corpus = df["clean_text"].tolist()

embeddings = []
for text in tqdm(corpus):
    emb = model.encode(text)
    embeddings.append(emb)


tqdm.pandas()
embeddings = np.array(embeddings)
np.save("../models/course_embeddings.npy", embeddings)

print("Neural embeddings saved.")
