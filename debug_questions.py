#!/usr/bin/env python3
"""Debug script to check question distribution"""

import pandas as pd

# Load data
df = pd.read_csv("data/manabifun_questions.csv")

print("=== QUESTION DISTRIBUTION DEBUG ===")
print(f"Total questions: {len(df)}")
print()

for topic in df['topic'].unique():
    print(f"🌟 {topic.upper()} REALM:")
    topic_df = df[df['topic'] == topic]
    
    for difficulty in ['easy', 'medium', 'hard']:
        difficulty_df = topic_df[topic_df['difficulty'] == difficulty]
        count = len(difficulty_df)
        print(f"   {difficulty.capitalize()}: {count} questions")
        
        if count > 0 and count <= 3:
            print(f"   ⚠️  WARNING: Only {count} questions - will complete too quickly!")
    
    print(f"   Total: {len(topic_df)} questions")
    print()

print("=== ANALYSIS ===")
for topic in df['topic'].unique():
    topic_df = df[df['topic'] == topic]
    for difficulty in ['easy', 'medium', 'hard']:
        difficulty_df = topic_df[topic_df['difficulty'] == difficulty]
        count = len(difficulty_df)
        if count == 1:
            print(f"🚨 CRITICAL: {topic}/{difficulty} has only 1 question!")
        elif count <= 3:
            print(f"⚠️  Warning: {topic}/{difficulty} has only {count} questions")