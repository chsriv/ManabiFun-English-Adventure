#!/usr/bin/env python3
"""
🌸 ManabiFun Model Performance Check
Simple evaluation with essential metrics
"""

import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import os

def check_performance():
    """Simple model performance evaluation"""
    print("🌸 ManabiFun Model Performance")
    print("=" * 40)
    
    # Load model
    if os.path.exists("models/weakness_detector.pkl"):
        with open("models/weakness_detector.pkl", "rb") as f:
            model_data = pickle.load(f)
        model = model_data['model']
        topics = model_data['topics']
        print(f"✅ Model: {model.__class__.__name__}")
        print(f"🏝️ Topics: {len(topics)} categories")
    else:
        print("❌ Model file not found!")
        return
    
    # Generate test data (same format as training)
    np.random.seed(42)
    X, y = [], []
    
    for _ in range(500):
        weak_topic_idx = np.random.randint(0, len(topics))
        scores = np.random.normal(70, 12, len(topics))
        scores = np.clip(scores, 30, 95)
        scores[weak_topic_idx] = np.random.normal(40, 8)
        scores[weak_topic_idx] = np.clip(scores[weak_topic_idx], 20, 65)
        
        time_spent = max(5, np.random.normal(15, 4))
        X.append(list(scores) + [time_spent])
        y.append(weak_topic_idx)
    
    X, y = np.array(X), np.array(y)
    
    # Split and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Show results
    print()
    print("📊 Basic Metrics:")
    print(f"   🎯 Accuracy:  {accuracy:.1%}")
    print(f"   📊 Precision: {precision:.3f}")
    print(f"   📋 Recall:    {recall:.3f}")
    print(f"   ⚖️  F1-Score:  {f1:.3f}")
    
    # Status
    if accuracy >= 0.90:
        status = "✅ Very Good"
    elif accuracy >= 0.80:
        status = "👍 Good"
    else:
        status = "⚠️ Needs Work"
    
    print(f"   🏆 Status:    {status}")
    print("=" * 40)

if __name__ == "__main__":
    check_performance()