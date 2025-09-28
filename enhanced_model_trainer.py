#!/usr/bin/env python3
"""
🧠 Enhanced ML Model Trainer for ManabiFun
Trains models on user progress patterns for truly personalized learning recommendations
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os
from datetime import datetime, timedelta

def generate_enhanced_training_data(n_samples=5000):
    """Generate enhanced training data based on realistic user learning patterns"""
    np.random.seed(42)
    
    data = []
    
    # Simulate diverse learning patterns
    for i in range(n_samples):
        # Generate realistic user profile
        user_type = np.random.choice(['beginner', 'intermediate', 'advanced'], p=[0.4, 0.4, 0.2])
        
        if user_type == 'beginner':
            base_skill = np.random.uniform(0.3, 0.6)
            improvement_rate = np.random.uniform(0.02, 0.08)
        elif user_type == 'intermediate': 
            base_skill = np.random.uniform(0.5, 0.8)
            improvement_rate = np.random.uniform(0.01, 0.05)
        else:  # advanced
            base_skill = np.random.uniform(0.7, 0.95)
            improvement_rate = np.random.uniform(0.001, 0.02)
        
        # Simulate skill correlation (some skills are related)
        grammar_base = base_skill + np.random.normal(0, 0.1)
        sentences_score = grammar_base + np.random.normal(0, 0.05)  # Highly correlated with grammar
        articles_score = grammar_base + np.random.normal(0, 0.08)   # Moderately correlated
        
        # Synonyms and antonyms are vocabulary-based (different skill set)
        vocab_base = base_skill + np.random.normal(0, 0.15)
        synonyms_score = vocab_base + np.random.normal(0, 0.06)
        antonyms_score = vocab_base + np.random.normal(0, 0.06)
        
        # Ensure scores are within valid range
        scores = {
            'grammar': np.clip(grammar_base, 0.1, 0.98),
            'articles': np.clip(articles_score, 0.1, 0.98),
            'synonyms': np.clip(synonyms_score, 0.1, 0.98),
            'antonyms': np.clip(antonyms_score, 0.1, 0.98),
            'sentences': np.clip(sentences_score, 0.1, 0.98)
        }
        
        # Simulate learning patterns (chapters attempted, time spent)
        chapters_completed = np.random.randint(1, 15)  # Total chapters across all realms
        avg_time_per_question = np.random.uniform(5, 25)  # seconds
        session_frequency = np.random.uniform(1, 7)  # sessions per week
        
        # Determine weakest area based on scores
        weakest_skill = min(scores.items(), key=lambda x: x[1])[0]
        weakest_idx = ['grammar', 'articles', 'synonyms', 'antonyms', 'sentences'].index(weakest_skill)
        
        # Additional features for enhanced prediction
        score_variance = np.var(list(scores.values()))  # How consistent across skills
        total_questions = chapters_completed * np.random.randint(4, 8)
        overall_accuracy = np.mean(list(scores.values()))
        
        # Create feature vector
        feature_row = [
            scores['grammar'],
            scores['articles'], 
            scores['synonyms'],
            scores['antonyms'],
            scores['sentences'],
            avg_time_per_question,
            chapters_completed,
            session_frequency,
            score_variance,
            overall_accuracy,
            total_questions
        ]
        
        data.append(feature_row + [weakest_idx])
    
    # Create DataFrame
    columns = [
        'grammar_score', 'articles_score', 'synonyms_score', 'antonyms_score', 'sentences_score',
        'avg_time_per_question', 'chapters_completed', 'session_frequency', 'score_variance', 
        'overall_accuracy', 'total_questions', 'weakness_prediction'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    return df

def train_enhanced_model():
    """Train enhanced ML model for personalized recommendations"""
    print("🧠 Generating enhanced training data...")
    df = generate_enhanced_training_data()
    
    # Features and target
    feature_columns = [
        'grammar_score', 'articles_score', 'synonyms_score', 'antonyms_score', 'sentences_score',
        'avg_time_per_question', 'chapters_completed', 'session_frequency', 'score_variance', 
        'overall_accuracy', 'total_questions'
    ]
    
    X = df[feature_columns]
    y = df['weakness_prediction']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"📊 Training set: {len(X_train)} samples")
    print(f"📊 Test set: {len(X_test)} samples")
    
    # Train enhanced Random Forest
    print("🌳 Training Enhanced Random Forest...")
    enhanced_rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'  # Handle class imbalance
    )
    
    enhanced_rf.fit(X_train, y_train)
    
    # Evaluate model
    train_pred = enhanced_rf.predict(X_train)
    test_pred = enhanced_rf.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)
    
    print(f"✅ Training Accuracy: {train_accuracy:.3f}")
    print(f"✅ Test Accuracy: {test_accuracy:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(enhanced_rf, X, y, cv=5, scoring='accuracy')
    print(f"🎯 Cross-validation Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': enhanced_rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔍 Top Feature Importances:")
    print(feature_importance.head(8))
    
    # Save enhanced model
    topics = ['grammar', 'articles', 'synonyms', 'antonyms', 'sentences']
    
    model_data = {
        'model': enhanced_rf,
        'topics': np.array(topics),
        'feature_columns': feature_columns,
        'training_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'feature_importance': feature_importance,
        'training_date': datetime.now().isoformat(),
        'model_version': '2.0_enhanced',
        'sample_size': len(df)
    }
    
    model_path = 'models/enhanced_weakness_detector.pkl'
    os.makedirs('models', exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"💾 Enhanced model saved to {model_path}")
    print(f"🎉 Model size: {len(df)} training samples")
    print(f"🧠 Enhanced features: {len(feature_columns)}")
    
    return enhanced_rf, model_data

def create_user_progress_predictor():
    """Create additional model to predict learning progression patterns"""
    print("\n🚀 Creating User Progress Predictor...")
    
    # Generate progress prediction data
    np.random.seed(123)
    progress_data = []
    
    for i in range(3000):
        # User characteristics
        initial_skill = np.random.uniform(0.2, 0.8)
        motivation = np.random.uniform(0.3, 1.0)
        consistency = np.random.uniform(0.4, 1.0)
        
        # Current session data
        current_score = np.random.uniform(0.1, 0.95)
        questions_attempted = np.random.randint(5, 15)
        time_spent = np.random.uniform(60, 600)  # seconds
        previous_attempts = np.random.randint(0, 10)
        
        # Predict improvement in next session
        # Higher motivation and consistency lead to better improvement
        base_improvement = motivation * consistency * 0.1
        score_factor = (1 - current_score) * 0.3  # More room for improvement if low score
        
        next_session_improvement = base_improvement + score_factor + np.random.normal(0, 0.05)
        next_session_improvement = np.clip(next_session_improvement, -0.2, 0.4)
        
        # Categorize improvement: 0=decline, 1=stable, 2=improve
        if next_session_improvement < -0.02:
            improvement_category = 0
        elif next_session_improvement < 0.05:
            improvement_category = 1
        else:
            improvement_category = 2
        
        progress_data.append([
            current_score, questions_attempted, time_spent, previous_attempts,
            motivation, consistency, improvement_category
        ])
    
    # Train progress predictor
    progress_df = pd.DataFrame(progress_data, columns=[
        'current_score', 'questions_attempted', 'time_spent', 'previous_attempts',
        'motivation', 'consistency', 'improvement_category'
    ])
    
    X_prog = progress_df[['current_score', 'questions_attempted', 'time_spent', 'previous_attempts']]
    y_prog = progress_df['improvement_category']
    
    progress_model = RandomForestClassifier(n_estimators=100, random_state=42)
    progress_model.fit(X_prog, y_prog)
    
    progress_accuracy = cross_val_score(progress_model, X_prog, y_prog, cv=5).mean()
    print(f"📈 Progress Predictor Accuracy: {progress_accuracy:.3f}")
    
    # Save progress predictor
    progress_model_data = {
        'model': progress_model,
        'accuracy': progress_accuracy,
        'feature_columns': ['current_score', 'questions_attempted', 'time_spent', 'previous_attempts'],
        'categories': ['decline', 'stable', 'improve']
    }
    
    with open('models/progress_predictor.pkl', 'wb') as f:
        pickle.dump(progress_model_data, f)
    
    print("💾 Progress predictor saved to models/progress_predictor.pkl")
    
    return progress_model

if __name__ == "__main__":
    print("🌟 ManabiFun Enhanced ML Model Training")
    print("="*50)
    
    # Train main weakness detection model
    enhanced_model, model_data = train_enhanced_model()
    
    # Train progress predictor
    progress_model = create_user_progress_predictor()
    
    print("\n🎉 All models trained successfully!")
    print("🚀 Ready for enhanced personalized learning!")