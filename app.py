#!/usr/bin/env python3
"""
🌟 The Explorer's English Adventure 
An Enid Blyton-style interactive learning adventure
Transform English learning into a magical journey through enchanted realms!
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import pickle
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ========================================
# PAGE CONFIGURATION & STYLING
# ========================================

st.set_page_config(
    page_title="English Adventure Explorer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Enid Blyton book styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f4f1e8 0%, #e8dcc0 100%);
        font-family: 'Times New Roman', serif;
    }
    
    .book-title {
        background: linear-gradient(135deg, #2c1810, #8b4513, #cd853f);
        color: #f4f1e8;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 2rem 0;
        padding: 2rem;
        border: 3px solid #cd853f;
        border-radius: 15px;
        background: linear-gradient(135deg, #2c1810, #8b4513);
        box-shadow: 0 8px 25px rgba(205, 133, 63, 0.3);
    }
    
    .chapter-heading {
        background: linear-gradient(135deg, #2c1810, #8b4513);
        color: #f4f1e8;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1.5rem 0;
        border: 2px solid #cd853f;
        box-shadow: 0 4px 15px rgba(205, 133, 63, 0.3);
    }
    
    .story-text {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #cd853f;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-style: italic;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2c1810;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .ornament {
        text-align: center;
        font-size: 1.5rem;
        margin: 1rem 0;
        color: #cd853f;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# ADVENTURE REALMS CONFIGURATION
# ========================================

ADVENTURE_REALMS = {
    'grammar': {
        'name': 'The Grammar Grove',
        'emoji': '🌳',
        'description': 'Ancient trees whisper the secrets of sentence structure',
        'difficulty_chapters': {
            'easy': 'Whispering Saplings',
            'medium': 'Sturdy Oak Circle', 
            'hard': 'Ancient Elder Council'
        }
    },
    'articles': {
        'name': 'The Article Archipelago',
        'emoji': '🏝️',
        'description': 'Mysterious islands where "a", "an", and "the" guard hidden treasures',
        'difficulty_chapters': {
            'easy': 'Gentle Tide Pools',
            'medium': 'Coral Reef Gardens',
            'hard': 'Deep Ocean Mysteries'
        }
    },
    'synonyms': {
        'name': 'The Synonym Sanctuary',
        'emoji': '🦋',
        'description': 'Enchanted meadow where words dance with their kindred spirits',
        'difficulty_chapters': {
            'easy': 'Butterfly Meadow',
            'medium': 'Wildflower Fields',
            'hard': 'Rainbow Garden Peak'
        }
    },
    'antonyms': {
        'name': 'The Antonym Arena',
        'emoji': '⚔️',
        'description': 'Training grounds where opposite words clash in epic battles',
        'difficulty_chapters': {
            'easy': 'Practice Grounds',
            'medium': 'Combat Circle',
            'hard': 'Champions Arena'
        }
    },
    'sentences': {
        'name': 'The Sentence Stronghold',
        'emoji': '🏰',
        'description': 'Majestic castle where words unite to form powerful declarations',
        'difficulty_chapters': {
            'easy': 'Courtyard Gardens',
            'medium': 'Great Hall',
            'hard': 'Royal Throne Room'
        }
    }
}

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

# ========================================
# ADVENTURE FUNCTIONS
# ========================================

def show_adventure_title():
    """Display the main book title"""
    # Use player's name if available, otherwise use default
    if 'player_name' in st.session_state and st.session_state.player_name:
        title_name = f"{st.session_state.player_name}'s"
    else:
        title_name = "The Explorer's"
    
    st.markdown(f"""
    <div class="book-title">
         {title_name} English Adventure 
        <br><span style="font-size: 1.2rem; font-weight: 400; font-style: italic;">
            A Magical Journey Through the Five Realms of Language
        </span>
    </div>
    """, unsafe_allow_html=True)

def show_player_introduction():
    """Show player name input with adventure story"""
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ""
    
    st.markdown("""
    <div class="story-text">
        <h3>🌟 Welcome, brave adventurer! 🌟</h3>
        <p>Deep in the heart of the Enchanted Learning Lands, five mystical realms await your discovery. 
        Each realm holds ancient secrets of the English language, guarded by wise creatures and magical challenges.</p>
        <p>Before you begin this grand adventure, please tell us your name, so the realm guardians may know you...</p>
    </div>
    """, unsafe_allow_html=True)
    
    player_name = st.text_input(
        "✨ What shall the realm guardians call you?",
        value=st.session_state.player_name,
        placeholder="Enter your adventurer name here..."
    )
    
    if st.button("🚀 Begin My Adventure!", type="primary", use_container_width=True):
        if player_name.strip():
            st.session_state.player_name = player_name.strip()
            st.rerun()
        else:
            st.warning("Please enter your name to begin the adventure!")
    
    if st.session_state.player_name:
        st.markdown(f"""
        <div class="story-text">
            <h4>Welcome, {st.session_state.player_name}! �</h4>
            <p><em>The ancient scrolls whisper your name across the realms...</em></p>
            <p>Your reputation as a word-master has spread across the land, {st.session_state.player_name}! 
            The five realm guardians eagerly await your arrival. Choose your first destination wisely, 
            for each realm will test your knowledge and reward your wisdom with magical powers!</p>
        </div>
        """, unsafe_allow_html=True)
        return True
    return False

# ========================================
# MAIN ADVENTURE INTERFACE  
# ========================================

def main():
    """Main adventure application"""
    show_adventure_title()
    
    # Initialize session state
    if 'current_realm' not in st.session_state:
        st.session_state.current_realm = None
    
    # Player introduction
    if not show_player_introduction():
        return
    
    # Show realm selection
    show_realm_selection()

def show_realm_selection():
    """Display the five mystical realms for selection"""
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chapter-heading">
        🗺️ Choose Your Realm of Adventure
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="story-text">
        Behold, {st.session_state.player_name}! The five mystical realms stretch before you, 
        each offering unique challenges and ancient wisdom. The ML Oracle has been watching your journey 
        and will guide you to strengthen any weak areas you encounter.
        <br><br>
        <strong>🎯 Your Mission:</strong> Master each realm by achieving 89% accuracy or higher! 
        Only then will you unlock the title of "Language Master" and gain access to the ultimate treasure!
    </div>
    """, unsafe_allow_html=True)
    
    # Display realm cards
    cols = st.columns(2)
    
    for idx, (realm_key, realm_info) in enumerate(ADVENTURE_REALMS.items()):
        with cols[idx % 2]:
            # Create realm card
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f4f1e8, #e8dcc0);
                border: 2px solid #cd853f;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                text-align: center;
                box-shadow: 0 4px 15px rgba(205, 133, 63, 0.2);
                transition: transform 0.2s ease;
            ">
                <h3 style="color: #8b4513; margin-bottom: 1rem;">
                    {realm_info['emoji']} {realm_info['name']}
                </h3>
                <p style="color: #2c1810; font-style: italic; margin-bottom: 1rem;">
                    {realm_info['description']}
                </p>
                <div style="font-size: 0.9rem; color: #8b6f47;">
                    <strong>Chapters Available:</strong><br>
                    🌱 {realm_info['difficulty_chapters']['easy']}<br>
                    🌿 {realm_info['difficulty_chapters']['medium']}<br>
                    🌳 {realm_info['difficulty_chapters']['hard']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 Enter {realm_info['name']}", 
                        key=f"realm_{realm_key}", 
                        use_container_width=True):
                st.session_state.current_realm = realm_key
                st.rerun()

# Run the adventure!
if __name__ == "__main__":
    main()

