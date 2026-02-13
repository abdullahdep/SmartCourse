#!/usr/bin/env python
"""Test consistency of search results"""

from tfidf_model import tfidf_recommend
from neural_model import neural_recommend
from preprocessing import preprocess_text
import pandas as pd

df = pd.read_csv('data/courses_cleaned.csv')
query = 'web development'
clean_query = preprocess_text(query)

print("=" * 60)
print("Testing TF-IDF Consistency")
print("=" * 60)

# Get TF-IDF results twice to verify consistency
tfidf1 = tfidf_recommend(clean_query, df, top_k=3)
tfidf2 = tfidf_recommend(clean_query, df, top_k=3)

print('First search:')
for r in tfidf1:
    print(f"  {r['title']}: {r['score']}")

print('\nSecond search:')
for r in tfidf2:
    print(f"  {r['title']}: {r['score']}")

if tfidf1[0]['title'] == tfidf2[0]['title'] and tfidf1[0]['score'] == tfidf2[0]['score']:
    print('✓ TF-IDF results are CONSISTENT\n')
else:
    print('✗ TF-IDF results are DIFFERENT\n')

print("=" * 60)
print("Testing Neural Model Consistency")
print("=" * 60)

# Get neural results twice to verify consistency
neural1 = neural_recommend(clean_query, df)
neural2 = neural_recommend(clean_query, df)

print('First search:')
for r in neural1[:3]:
    print(f"  {r['title']}: {r['score']}")

print('\nSecond search:')
for r in neural2[:3]:
    print(f"  {r['title']}: {r['score']}")

if neural1[0]['title'] == neural2[0]['title'] and neural1[0]['score'] == neural2[0]['score']:
    print('✓ Neural model results are CONSISTENT')
else:
    print('✗ Neural model results are DIFFERENT')

