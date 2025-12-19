import pandas as pd
import spacy
import re
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    text = text.lower()
    text = re.sub('<.*?>', '', text)
    text = re.sub('[^a-zA-Z ]', ' ', text)
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc if not t.is_stop]
    return " ".join(tokens)

df = pd.read_csv("../data/courses_cleaned.csv")

tqdm.pandas()
df["clean_text"] = df["Course Description"].progress_apply(preprocess)

df.to_csv("../data/courses_preprocessed.csv", index=False)

print("Preprocessing complete.")
