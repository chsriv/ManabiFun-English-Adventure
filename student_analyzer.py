#!/usr/bin/env python3
"""
📊 Advanced Student Report Generator for ManabiFun
Generates comprehensive ML-powered student analysis reports
"""

import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

class StudentAnalyzer:
    def __init__(self):
        """Initialize the student analyzer with trained models"""
        try:
            # Load enhanced weakness detector
            with open('models/enhanced_weakness_detector.pkl', 'rb') as f:
                self.weakness_model_data = pickle.load(f)
                self.weakness_model = self.weakness_model_data['model']
                self.feature_columns = self.weakness_model_data['feature_columns']
            
            # Load progress predictor
            with open('models/progress_predictor.pkl', 'rb') as f:
                self.progress_model_data = pickle.load(f)
                self.progress_model = self.progress_model_data['model']
            
            print("✅ Advanced ML models loaded successfully")
            
        except FileNotFoundError as e:
            print(f"⚠️ Model file not found: {e}")
            self.weakness_model = None
            self.progress_model = None

    def extract_learning_features(self, progress_data):
        """Extract comprehensive learning features from user progress"""
        if not progress_data['completed_chapters']:
            return None
        
        # Calculate comprehensive metrics
        all_scores = []
        all_attempts = []
        realm_performance = {'grammar': [], 'articles': [], 'synonyms': [], 'antonyms': [], 'sentences': []}
        
        total_questions = progress_data['total_questions']
        total_correct = progress_data['total_correct']
        
        # Extract detailed performance data
        for realm, difficulties in progress_data['completed_chapters'].items():
            for difficulty, data in difficulties.items():
                all_scores.append(data['percentage'])
                all_attempts.append(data['attempts'])
                realm_performance[realm].append(data['percentage'])
        
        # Calculate realm averages (fill missing realms with overall average)
        overall_avg = np.mean(all_scores) if all_scores else 0.7
        realm_scores = {}
        for realm in ['grammar', 'articles', 'synonyms', 'antonyms', 'sentences']:
            if realm_performance[realm]:
                realm_scores[realm] = np.mean(realm_performance[realm]) / 100
            else:
                realm_scores[realm] = overall_avg / 100
        
        # Advanced metrics
        chapters_completed = len(all_scores)
        avg_time_per_question = 12.0  # Default estimate
        session_frequency = chapters_completed / max(1, len(progress_data['learning_path'])) * 7
        score_variance = np.var(all_scores) if len(all_scores) > 1 else 0
        overall_accuracy = overall_avg / 100
        
        # Create feature vector matching training data
        features = [
            realm_scores['grammar'],
            realm_scores['articles'],
            realm_scores['synonyms'],
            realm_scores['antonyms'],
            realm_scores['sentences'],
            avg_time_per_question,
            chapters_completed,
            session_frequency,
            score_variance,
            overall_accuracy,
            total_questions
        ]
        
        return {
            'features': features,
            'realm_scores': realm_scores,
            'metrics': {
                'chapters_completed': chapters_completed,
                'overall_accuracy': overall_accuracy,
                'score_variance': score_variance,
                'total_questions': total_questions,
                'avg_attempts': np.mean(all_attempts) if all_attempts else 1,
                'consistency': 1 - (score_variance / 100) if score_variance > 0 else 1
            }
        }

    def predict_weakness_advanced(self, progress_data):
        """Advanced weakness prediction with confidence scores"""
        if not self.weakness_model:
            return None
        
        feature_data = self.extract_learning_features(progress_data)
        if not feature_data:
            return None
        
        try:
            # Get prediction with probabilities
            features_array = np.array(feature_data['features']).reshape(1, -1)
            prediction = self.weakness_model.predict(features_array)[0]
            probabilities = self.weakness_model.predict_proba(features_array)[0]
            
            topics = ['grammar', 'articles', 'synonyms', 'antonyms', 'sentences']
            
            # Get confidence scores for all areas
            weakness_analysis = {}
            for i, topic in enumerate(topics):
                weakness_analysis[topic] = {
                    'weakness_probability': probabilities[i],
                    'current_score': feature_data['realm_scores'][topic],
                    'needs_attention': probabilities[i] > 0.3
                }
            
            # Sort by weakness probability
            sorted_weaknesses = sorted(weakness_analysis.items(), 
                                     key=lambda x: x[1]['weakness_probability'], 
                                     reverse=True)
            
            return {
                'primary_weakness': topics[prediction],
                'weakness_analysis': weakness_analysis,
                'sorted_weaknesses': sorted_weaknesses,
                'confidence': max(probabilities),
                'feature_data': feature_data
            }
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return None

    def predict_learning_trajectory(self, progress_data):
        """Predict student's learning progression"""
        if not self.progress_model or not progress_data['completed_chapters']:
            return None
        
        try:
            feature_data = self.extract_learning_features(progress_data)
            current_score = feature_data['metrics']['overall_accuracy']
            chapters_completed = feature_data['metrics']['chapters_completed']
            avg_attempts = feature_data['metrics']['avg_attempts']
            
            # Prepare features for progress model
            prog_features = [current_score, chapters_completed, 180, avg_attempts]  # 180 = 3 min avg
            prog_prediction = self.progress_model.predict([prog_features])[0]
            prog_probabilities = self.progress_model.predict_proba([prog_features])[0]
            
            categories = ['decline', 'stable', 'improve']
            
            return {
                'prediction': categories[prog_prediction],
                'probabilities': {categories[i]: prob for i, prob in enumerate(prog_probabilities)},
                'trajectory_score': prog_probabilities[2]  # Improvement probability
            }
            
        except Exception as e:
            print(f"⚠️ Trajectory prediction error: {e}")
            return None

    def generate_student_report(self, student_name, progress_data):
        """Generate comprehensive student analysis report"""
        if not progress_data['completed_chapters']:
            return {"error": "No progress data available for analysis"}
        
        # Get advanced predictions
        weakness_analysis = self.predict_weakness_advanced(progress_data)
        trajectory = self.predict_learning_trajectory(progress_data)
        
        if not weakness_analysis:
            return {"error": "Unable to generate ML analysis"}
        
        feature_data = weakness_analysis['feature_data']
        metrics = feature_data['metrics']
        
        # Calculate learning insights
        total_chapters = sum(len(difficulties) for difficulties in progress_data['completed_chapters'].values())
        mastery_count = sum(1 for score in progress_data['realm_mastery'].values() if score >= 89)
        
        # Generate report
        report = {
            'student_name': student_name,
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'summary': {
                'total_chapters': total_chapters,
                'overall_accuracy': metrics['overall_accuracy'] * 100,
                'realms_mastered': mastery_count,
                'consistency_score': metrics['consistency'] * 100,
                'total_questions': metrics['total_questions']
            },
            'ml_analysis': {
                'primary_weakness': weakness_analysis['primary_weakness'],
                'confidence': weakness_analysis['confidence'],
                'weakness_breakdown': weakness_analysis['weakness_analysis'],
                'learning_trajectory': trajectory['prediction'] if trajectory else 'stable',
                'improvement_probability': trajectory['trajectory_score'] if trajectory else 0.5
            },
            'detailed_performance': progress_data['realm_mastery'],
            'recommendations': self._generate_recommendations(weakness_analysis, trajectory, metrics),
            'learning_insights': self._generate_insights(weakness_analysis, metrics, total_chapters)
        }
        
        return report

    def _generate_recommendations(self, weakness_analysis, trajectory, metrics):
        """Generate personalized recommendations"""
        recommendations = []
        
        primary_weakness = weakness_analysis['primary_weakness']
        confidence = weakness_analysis['confidence']
        
        # Primary recommendation based on ML analysis
        if confidence > 0.7:
            recommendations.append({
                'priority': 'HIGH',
                'action': f'Focus intensively on {primary_weakness.title()}',
                'reason': f'ML model is {confidence:.1%} confident this is your weakest area',
                'timeline': '1-2 weeks'
            })
        
        # Secondary recommendations based on detailed analysis
        sorted_weaknesses = weakness_analysis['sorted_weaknesses']
        for topic, data in sorted_weaknesses[1:3]:  # Top 2 secondary weaknesses
            if data['needs_attention']:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'action': f'Practice {topic.title()} regularly',
                    'reason': f'{data["weakness_probability"]:.1%} probability of needing attention',
                    'timeline': '2-3 weeks'
                })
        
        # Study pattern recommendations
        if trajectory and trajectory['prediction'] == 'improve':
            recommendations.append({
                'priority': 'LOW',
                'action': 'Continue current study pattern',
                'reason': f'{trajectory["trajectory_score"]:.1%} probability of continued improvement',
                'timeline': 'Ongoing'
            })
        elif trajectory and trajectory['prediction'] == 'decline':
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Increase study frequency and review fundamentals',
                'reason': 'ML model predicts performance decline risk',
                'timeline': 'Immediate'
            })
        
        return recommendations

    def _generate_insights(self, weakness_analysis, metrics, total_chapters):
        """Generate learning insights"""
        insights = []
        
        # Progress insights
        if total_chapters >= 10:
            insights.append(f"🎯 Extensive learner with {total_chapters} chapters completed")
        elif total_chapters >= 5:
            insights.append(f"📚 Dedicated learner with {total_chapters} chapters completed")
        else:
            insights.append(f"🌱 Beginning learner with {total_chapters} chapters completed")
        
        # Consistency insights
        consistency = metrics['consistency']
        if consistency > 0.9:
            insights.append("⭐ Highly consistent performance across topics")
        elif consistency > 0.7:
            insights.append("👍 Good consistency with some variation")
        else:
            insights.append("📊 Variable performance - focus on consistency")
        
        # ML-specific insights
        weakness_data = weakness_analysis['weakness_analysis']
        strong_areas = [topic for topic, data in weakness_data.items() 
                       if data['current_score'] > 0.85]
        weak_areas = [topic for topic, data in weakness_data.items() 
                     if data['current_score'] < 0.7]
        
        if strong_areas:
            insights.append(f"💪 Strong in: {', '.join(strong_areas)}")
        if weak_areas:
            insights.append(f"🎯 Needs work: {', '.join(weak_areas)}")
        
        return insights

# Global instance
student_analyzer = StudentAnalyzer()