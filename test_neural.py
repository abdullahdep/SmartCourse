#!/usr/bin/env python
"""Test neural model consistency"""

from neural_model import neural_recommend
from preprocessing import preprocess_text
import pandas as pd

df = pd.read_csv('data/courses_cleaned.csv')
query = 'web development'
clean_query = preprocess_text(query)

print("Testing Neural Model Consistency")
print("=" * 60)

# Get neural results twice to verify consistency
try:
    neural1 = neural_recommend(clean_query, df)
    print('First search completed')
    for r in neural1[:3]:
        print(f"  {r['title']}: {r['score']}")
    
    neural2 = neural_recommend(clean_query, df)
    print('\nSecond search completed')
    for r in neural2[:3]:
        print(f"  {r['title']}: {r['score']}")
    
    if neural1[0]['title'] == neural2[0]['title'] and neural1[0]['score'] == neural2[0]['score']:
        print('\n✓ Neural model results are CONSISTENT')
    else:
        print('\n✗ Neural model results are DIFFERENT')
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
