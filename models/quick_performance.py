#!/usr/bin/env python3
"""
🌸 ManabiFun Model Performance Checker
Simple and clean performance evaluation
"""

import pickle
import numpy as np
from sklearn.metrics import accuracy_score
import os

def check_model_performance():
    """Simple model performance check with essential metrics only"""
    print("🌸 ManabiFun Model Performance")
    print("=" * 40)
    
    # Load model
    if os.path.exists("models/weakness_detector.pkl"):
        with open("models/weakness_detector.pkl", "rb") as f:
            model_data = pickle.load(f)
        model = model_data['model']
        topics = model_data['topics']
    else:
        print("❌ Model file not found!")
        return
    
    # Generate quick test data
    np.random.seed(42)
    X_test, y_test = [], []
    
    for _ in range(200):  # Small test set
        weak_topic_idx = np.random.randint(0, len(topics))
        scores = np.random.normal(70, 12, len(topics))
        scores = np.clip(scores, 30, 95)
        scores[weak_topic_idx] = np.random.normal(40, 8)
        scores[weak_topic_idx] = np.clip(scores[weak_topic_idx], 20, 65)
        
        time_spent = max(5, np.random.normal(15, 4))
        X_test.append(list(scores) + [time_spent])
        y_test.append(weak_topic_idx)
    
    # Test model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Show results
    print(f"🎯 Model Accuracy: {accuracy:.1%}")
    print(f"🏝️ Topics: {len(topics)} categories")
    
    if accuracy >= 0.90:
        status = "✅ Very Good"
    elif accuracy >= 0.80:
        status = "👍 Good"
    else:
        status = "⚠️ Needs Work"
    
    print(f"🏆 Status: {status}")
    print("=" * 40)

if __name__ == "__main__":
    check_model_performance()