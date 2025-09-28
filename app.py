import streamlit as st
import pandas as pd
import numpy as np
import random
import pickle
import os
from datetime import datetime
import plotly.express as px

# ------------------------
# Load Data
# ------------------------
QUESTIONS_CSV = "data/manabifun_questions.csv"
SCORES_CSV = "data/student_scores.csv"
MODEL_PATH = "models/weakness_detector.pkl"

# Load questions
if os.path.exists(QUESTIONS_CSV):
    questions_df = pd.read_csv(QUESTIONS_CSV)
    print(f"✅ Loaded {len(questions_df)} questions from CSV")
else:
    st.error("❌ Questions dataset not found! Please run train_model.py first.")
    st.stop()

# Load model - handle both old and new model formats
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)
        
    # Check if it's the new format with model_data dict or old format with just model
    if isinstance(model_data, dict):
        model = model_data['model']
        TOPICS = model_data['topics'].tolist()
        topic_to_idx = model_data['topic_to_idx']
        feature_names = model_data['feature_names']
        print("✅ Loaded enhanced model with topic mapping")
    else:
        # Old format fallback
        model = model_data
        TOPICS = ["grammar", "articles", "synonyms", "antonyms", "sentences"]
        topic_to_idx = {topic: idx for idx, topic in enumerate(TOPICS)}
        feature_names = TOPICS + ['time_spent']
        print("⚠️ Using fallback model format")
else:
    st.error("❌ Model not found! Please run train_model.py first.")
    st.stop()

# Ensure student score log exists
if not os.path.exists(SCORES_CSV):
    pd.DataFrame(columns=[
        "student_id","student_name","timestamp","quiz_type","topic",
        "score","total_questions","correct_answers","time_spent_minutes",
        "difficulty_level","xp_earned","streak_day"
    ]).to_csv(SCORES_CSV, index=False)

# ------------------------
# Helper Functions
# ------------------------
def fisher_yates_shuffle(questions_list):
    """
    Implement Fisher-Yates shuffle algorithm for randomizing quiz questions.
    
    Algorithm: Fisher-Yates (also known as Knuth shuffle)
    - Start with the last element
    - Generate a random index from 0 to current index (inclusive)
    - Swap current element with the randomly selected element
    - Move to the previous element and repeat
    
    Time Complexity: O(n)
    Space Complexity: O(1) - in-place shuffling
    """
    n = len(questions_list)
    for i in range(n - 1, 0, -1):
        # Generate random index between 0 and i (inclusive)
        j = random.randint(0, i)
        # Swap elements at indices i and j
        questions_list[i], questions_list[j] = questions_list[j], questions_list[i]
    
    return questions_list

def get_questions(topic, num=10):
    """Get shuffled questions for a specific topic using Fisher-Yates algorithm"""
    topic_df = questions_df[questions_df["topic"] == topic]
    
    if len(topic_df) < num:
        # If we don't have enough questions, use all available
        selected_questions = topic_df.to_dict(orient="records")
    else:
        # Sample questions and convert to list for shuffling
        selected_questions = topic_df.sample(n=num, random_state=None).to_dict(orient="records")
    
    # Apply Fisher-Yates shuffle for randomization
    shuffled_questions = fisher_yates_shuffle(selected_questions)
    
    print(f"🔀 Applied Fisher-Yates shuffle to {len(shuffled_questions)} questions for topic: {topic}")
    return shuffled_questions

def calculate_xp(score, total):
    return score * 10  # 10 XP per correct answer

def log_score(student_id, student_name, topic, score, total, correct, difficulty, xp):
    df = pd.read_csv(SCORES_CSV)
    new_row = {
        "student_id": student_id,
        "student_name": student_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quiz_type": "island",
        "topic": topic,
        "score": score,
        "total_questions": total,
        "correct_answers": correct,
        "time_spent_minutes": random.randint(5,15),  # dummy time
        "difficulty_level": difficulty,
        "xp_earned": xp,
        "streak_day": random.randint(1,7)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(SCORES_CSV, index=False)

def predict_weakness(scores_row):
    """Predict student weakness based on performance scores"""
    try:
        prediction = model.predict([scores_row])[0]
        weak_topic = TOPICS[prediction] if prediction < len(TOPICS) else TOPICS[0]
        return prediction, weak_topic
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        return 0, TOPICS[0]

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="🌸 ManabiFun", layout="centered")

st.title("🌸 ManabiFun - Learn English the Fun Way! 🌸")

# Student login (simple)
student_name = st.text_input("Enter your name:", "")
if student_name:
    student_id = student_name[:2].upper() + str(random.randint(100,999))

    # Pick topic
    topic = st.selectbox("🏝️ Choose your Learning Island:", TOPICS)

    # Session state for quiz
    if "quiz" not in st.session_state:
        st.session_state.quiz = []
        st.session_state.q_index = 0
        st.session_state.correct = 0
        st.session_state.finished = False

    if st.button("Start Quiz", type="primary"):
        st.session_state.quiz = get_questions(topic, 10)
        st.session_state.q_index = 0
        st.session_state.correct = 0
        st.session_state.finished = False

    if st.session_state.quiz and not st.session_state.finished:
        q = st.session_state.quiz[st.session_state.q_index]

        st.subheader(f"Q{st.session_state.q_index+1}: {q['question']}")
        
        # Create options list from the CSV columns
        options = [
            q['option_a'],
            q['option_b'], 
            q['option_c'],
            q['option_d']
        ]
        
        choice = st.radio(
            "Select your answer:",
            options,
            key=f"q_{st.session_state.q_index}"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Previous") and st.session_state.q_index > 0:
                st.session_state.q_index -= 1
                st.rerun()
        with col2:
            if st.button("Next ➡"):
                # Determine correct answer
                correct_letter = q['correct_answer'].upper()
                correct_option_map = {
                    'A': q['option_a'],
                    'B': q['option_b'], 
                    'C': q['option_c'],
                    'D': q['option_d']
                }
                correct_answer = correct_option_map.get(correct_letter, q['option_a'])
                
                # Check if answer is correct
                if choice == correct_answer:
                    st.session_state.correct += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! The correct answer was: {correct_answer}")

                if st.session_state.q_index < len(st.session_state.quiz) - 1:
                    st.session_state.q_index += 1
                    st.rerun()
                else:
                    st.session_state.finished = True
                    score = st.session_state.correct
                    total_questions = len(st.session_state.quiz)
                    xp = calculate_xp(score, total_questions)
                    st.success(f"🎉 Quiz Complete! You scored {score}/{total_questions} and earned {xp} XP")

                    # Log result
                    log_score(student_id, student_name, topic, score, total_questions, score, q.get('difficulty', 'medium'), xp)
                    st.rerun()

    # ------------------------
    # Analytics
    # ------------------------
    st.subheader("📊 Your Progress")
    if os.path.exists(SCORES_CSV):
        df = pd.read_csv(SCORES_CSV)
        student_df = df[df['student_name'] == student_name]

        if not student_df.empty:
            # Pie chart of performance by topic
            fig = px.pie(student_df, names="topic", values="score", title="Performance by Topic")
            st.plotly_chart(fig)

            # Weakness prediction using the trained model
            avg_scores = []
            for topic in TOPICS:
                topic_scores = student_df[student_df['topic'] == topic]['score']
                avg_score = topic_scores.mean() if len(topic_scores) > 0 else 70
                avg_scores.append(avg_score)
            
            # Add dummy time spent (you could enhance this by tracking actual time)
            avg_scores.append(15)  
            
            weak_topic_idx, weak_topic_name = predict_weakness(avg_scores)
            st.warning(f"🤖 AI Suggests: Focus more on **{weak_topic_name}**")
            
            # Display confidence and feature importance if available
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba([avg_scores])[0]
                confidence = max(probabilities) * 100
                st.info(f"📊 Prediction confidence: {confidence:.1f}%")

            # Line chart: Weekly progress (dummy data for demo)
            student_df['timestamp'] = pd.to_datetime(student_df['timestamp'])
            weekly = student_df.groupby(student_df['timestamp'].dt.isocalendar().week)['score'].mean().reset_index()
            fig_line = px.line(weekly, x='week', y='score', title="Weekly Average Score")
            st.plotly_chart(fig_line)

        else:
            st.info("Take a quiz to start tracking your progress!")

    st.markdown("---")
    st.caption("🌸 ManabiFun - Fun Learning for Kids | Track your progress and improve daily!")
    st.caption("🔀 **Shuffling Algorithm**: Fisher-Yates shuffle ensures fair randomization of quiz questions")
    st.caption("🤖 **AI Model**: Random Forest trained on student performance patterns for weakness detection")