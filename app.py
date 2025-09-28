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
from student_analyzer import student_analyzer

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

def update_user_progress(realm_key, difficulty, score, total_questions):
    """Update comprehensive user progress tracking"""
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Initialize realm progress if not exists
    if realm_key not in st.session_state.player_progress['completed_chapters']:
        st.session_state.player_progress['completed_chapters'][realm_key] = {}
    
    # Update chapter progress
    st.session_state.player_progress['completed_chapters'][realm_key][difficulty] = {
        'score': score,
        'total': total_questions,
        'percentage': percentage,
        'attempts': st.session_state.player_progress['completed_chapters'][realm_key].get(difficulty, {}).get('attempts', 0) + 1,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Update global stats
    st.session_state.player_progress['total_questions'] += total_questions
    st.session_state.player_progress['total_correct'] += score
    
    # Track learning path
    chapter_key = f"{realm_key}_{difficulty}"
    if chapter_key not in st.session_state.player_progress['learning_path']:
        st.session_state.player_progress['learning_path'].append(chapter_key)
    
    # Calculate realm mastery
    realm_scores = []
    for diff_data in st.session_state.player_progress['completed_chapters'][realm_key].values():
        realm_scores.append(diff_data['percentage'])
    st.session_state.player_progress['realm_mastery'][realm_key] = sum(realm_scores) / len(realm_scores)
    
    # Update weak/strong areas
    if percentage < 60:
        if realm_key not in st.session_state.player_progress['weak_areas']:
            st.session_state.player_progress['weak_areas'].append(realm_key)
    elif percentage >= 85:
        if realm_key not in st.session_state.player_progress['strong_areas']:
            st.session_state.player_progress['strong_areas'].append(realm_key)
        # Remove from weak areas if now strong
        if realm_key in st.session_state.player_progress['weak_areas']:
            st.session_state.player_progress['weak_areas'].remove(realm_key)

def show_progress_dashboard():
    """Display comprehensive progress dashboard with charts"""
    progress = st.session_state.player_progress
    
    if not progress['completed_chapters']:
        st.info("🌱 Complete your first chapter to see your progress dashboard!")
        return
    
    st.subheader("📊 Your Learning Journey Dashboard")
    
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_chapters = sum(len(difficulties) for difficulties in progress['completed_chapters'].values())
        st.metric("Chapters Completed", total_chapters)
    with col2:
        overall_accuracy = (progress['total_correct'] / progress['total_questions'] * 100) if progress['total_questions'] > 0 else 0
        st.metric("Overall Accuracy", f"{overall_accuracy:.1f}%")
    with col3:
        mastered_realms = sum(1 for score in progress['realm_mastery'].values() if score >= 89)
        st.metric("Mastered Realms", mastered_realms)
    with col4:
        st.metric("Total Questions", progress['total_questions'])
    
    # Realm mastery chart
    if progress['realm_mastery']:
        st.subheader("🏆 Realm Mastery Overview")
        
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Create realm mastery bar chart
        realm_names = [ADVENTURE_REALMS[key]['name'] for key in progress['realm_mastery'].keys()]
        realm_scores = list(progress['realm_mastery'].values())
        realm_colors = ['#28a745' if score >= 89 else '#ffc107' if score >= 70 else '#dc3545' for score in realm_scores]
        
        fig = go.Figure(data=[
            go.Bar(
                x=realm_names,
                y=realm_scores,
                marker_color=realm_colors,
                text=[f"{score:.1f}%" for score in realm_scores],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Realm Mastery Levels",
            xaxis_title="Realms",
            yaxis_title="Average Score (%)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        # Add mastery threshold line
        fig.add_hline(y=89, line_dash="dash", line_color="green", annotation_text="Mastery Threshold (89%)")
        fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Good Progress (70%)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Chapter-level progress
        st.subheader("📚 Detailed Chapter Progress")
        for realm_key, difficulties in progress['completed_chapters'].items():
            realm_info = ADVENTURE_REALMS[realm_key]
            st.write(f"**{realm_info['emoji']} {realm_info['name']}**")
            
            chapter_cols = st.columns(len(difficulties))
            for i, (diff, data) in enumerate(difficulties.items()):
                with chapter_cols[i]:
                    chapter_name = realm_info['difficulty_chapters'][diff]
                    color = "green" if data['percentage'] >= 89 else "orange" if data['percentage'] >= 70 else "red"
                    st.markdown(f"""
                    <div style="border: 2px solid {color}; border-radius: 10px; padding: 10px; margin: 5px 0;">
                        <h5>{chapter_name}</h5>
                        <p><strong>{data['percentage']:.1f}%</strong></p>
                        <p>{data['score']}/{data['total']} correct</p>
                        <p>Attempts: {data['attempts']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Recommendations based on progress
    st.subheader("🎯 Personalized Recommendations")
    
    weak_realms = [realm for realm, score in progress['realm_mastery'].items() if score < 70]
    strong_realms = [realm for realm, score in progress['realm_mastery'].items() if score >= 89]
    
    if weak_realms:
        weak_realm_key = weak_realms[0]  # Focus on weakest
        weak_realm = ADVENTURE_REALMS[weak_realm_key]
        st.warning(f"🎯 **Priority Focus**: {weak_realm['emoji']} {weak_realm['name']} - Current average: {progress['realm_mastery'][weak_realm_key]:.1f}%")
    
    if strong_realms:
        st.success(f"🌟 **Strong Areas**: {', '.join([ADVENTURE_REALMS[r]['name'] for r in strong_realms])}")
    
    # Learning path visualization
    if len(progress['learning_path']) > 1:
        st.subheader("🛤️ Your Learning Journey")
        journey_text = " → ".join([
            f"{ADVENTURE_REALMS[path.split('_')[0]]['emoji']} {path.split('_')[1].title()}" 
            for path in progress['learning_path']
        ])
        st.write(journey_text)

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
    
    if st.button("🚀 Begin My Adventure!", type="primary", use_container_width=True, key="begin_adventure"):
        if player_name.strip():
            st.session_state.player_name = player_name.strip()
            st.rerun()
        else:
            st.warning("Please enter your name to begin the adventure!")
    
    if st.session_state.player_name:
        st.markdown(f"""
        <div class="story-text">
            <h4>Welcome, {st.session_state.player_name}! </h4>
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
    
    # Initialize comprehensive progress tracking system
    if 'player_progress' not in st.session_state:
        st.session_state.player_progress = {
            'completed_chapters': {},  # {realm: {difficulty: {score: X, attempts: Y, date: Z}}}
            'realm_mastery': {},       # {realm: average_score}
            'total_questions': 0,
            'total_correct': 0,
            'learning_path': [],       # Track which realms/chapters completed in order
            'weak_areas': [],          # Track consistently weak topics
            'strong_areas': []         # Track consistently strong topics
        }
    
    # Initialize session state
    if 'current_realm' not in st.session_state:
        st.session_state.current_realm = None
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = None
    
    # Player introduction
    if not show_player_introduction():
        return
    
    # Navigation logic with error handling
    try:
        if st.session_state.current_realm is None:
            # Show realm selection
            show_realm_selection()
        elif st.session_state.current_chapter is None:
            # Show selected realm
            if st.session_state.current_realm in ADVENTURE_REALMS:
                show_realm_adventure(st.session_state.current_realm)
            else:
                st.error("❌ Invalid realm selected. Returning to realm selection.")
                st.session_state.current_realm = None
                st.rerun()
        else:
            # Show quiz questions
            show_quiz_question(st.session_state.current_realm, st.session_state.current_chapter)
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("🔄 Returning to the beginning of your adventure...")
        # Reset session state on error
        st.session_state.current_realm = None
        st.session_state.current_chapter = None
        if st.button("🚀 Restart Adventure"):
            st.rerun()

def show_realm_selection():
    """Display the five mystical realms for selection"""
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    
    # Progress dashboard toggle
    if st.session_state.player_progress['completed_chapters']:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 View My Progress Dashboard", type="secondary", use_container_width=True):
                show_progress_dashboard()
                st.markdown("---")
        with col2:
            if st.button("🎓 Generate Student Report", type="primary", use_container_width=True):
                show_student_report()
                st.markdown("---")
    
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

def show_realm_adventure(realm_key):
    """Display the adventure within a selected realm"""
    realm_info = ADVENTURE_REALMS[realm_key]
    
    # Realm header with back button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="chapter-heading">
            {realm_info['emoji']} Welcome to {realm_info['name']}!
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Return to Realms", use_container_width=True, key="realm_adventure_return"):
            st.session_state.current_realm = None
            st.session_state.current_chapter = None
            st.rerun()
    
    # Story introduction for the realm
    st.markdown(f"""
    <div class="story-text">
        <h4>🌟 You have entered {realm_info['name']}! 🌟</h4>
        <p>{realm_info['description']}</p>
        <p>Dear {st.session_state.player_name}, three mystical chapters await your exploration in this realm. 
        Each chapter tests your knowledge with questions that grow more challenging as you progress.</p>
        <p><strong>🎯 Your Mission:</strong> Answer questions correctly to prove your mastery! 
        The AI Oracle will watch your performance and guide you to areas where you can grow stronger.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    
    # Chapter selection
    st.markdown("""
    <div class="chapter-heading">
        📚 Choose Your Chapter
    </div>
    """, unsafe_allow_html=True)
    
    # Display chapter options
    for difficulty, chapter_name in realm_info['difficulty_chapters'].items():
        # Get appropriate emoji for difficulty
        difficulty_emoji = {'easy': '🌱', 'medium': '🌿', 'hard': '🌳'}[difficulty]
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f4f1e8, #e8dcc0);
            border: 2px solid #cd853f;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <h4 style="color: #8b4513; margin-bottom: 0.5rem;">
                {difficulty_emoji} {chapter_name}
            </h4>
            <p style="color: #2c1810; font-style: italic;">
                Difficulty: {difficulty.title()}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📖 Begin {chapter_name}", 
                    key=f"chapter_{realm_key}_{difficulty}", 
                    use_container_width=True):
            st.session_state.current_chapter = difficulty
            start_chapter_quiz(realm_key, difficulty)
            st.rerun()

def start_chapter_quiz(realm_key, difficulty):
    """Start a quiz for the selected realm and difficulty"""
    try:
        # Get questions for this realm and difficulty
        realm_questions = questions_df[
            (questions_df['topic'] == realm_key) & 
            (questions_df['difficulty'] == difficulty)
        ].head(10)  # Limit to 10 questions
        
        if len(realm_questions) == 0:
            st.error(f"❌ No questions found for {realm_key} - {difficulty}. Please try another difficulty level.")
            return
        
        # Initialize quiz session state safely
        st.session_state.quiz_questions = []
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        
        # Apply Fisher-Yates shuffle to questions
        questions_list = realm_questions.to_dict('records')
        
        # Validate questions have required fields
        valid_questions = []
        for q in questions_list:
            if all(key in q for key in ['question', 'correct_answer']) and q['question'].strip():
                valid_questions.append(q)
        
        if len(valid_questions) == 0:
            st.error("❌ No valid questions available. Please try another realm.")
            return
            
        shuffled_questions = fisher_yates_shuffle(valid_questions.copy())
        st.session_state.quiz_questions = shuffled_questions
        
        print(f"🔀 Applied Fisher-Yates shuffle to {len(shuffled_questions)} questions for topic: {realm_key}")
        
    except Exception as e:
        st.error(f"❌ Error starting quiz: {str(e)}")
        print(f"Error in start_chapter_quiz: {e}")
        return

def show_quiz_question(realm_key, difficulty):
    """Display the current quiz question"""
    realm_info = ADVENTURE_REALMS[realm_key]
    
    # Initialize all quiz session state variables
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    
    if len(st.session_state.quiz_questions) == 0:
        st.error("No quiz questions available! Please return to realm selection.")
        if st.button("🏠 Return to Realms", key="no_questions_return"):
            st.session_state.current_realm = None
            st.session_state.current_chapter = None
            st.rerun()
        return
    
    # Validate quiz_index bounds
    if st.session_state.quiz_index >= len(st.session_state.quiz_questions):
        show_quiz_results(realm_key, difficulty)
        return
    
    # Ensure quiz_index is not negative
    if st.session_state.quiz_index < 0:
        st.session_state.quiz_index = 0
    
    current_q = st.session_state.quiz_questions[st.session_state.quiz_index]
    total_questions = len(st.session_state.quiz_questions)
    
    # Question header
    st.markdown(f"""
    <div class="chapter-heading">
        {realm_info['emoji']} Question {st.session_state.quiz_index + 1} of {total_questions}
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (st.session_state.quiz_index + 1) / total_questions
    st.progress(progress, text=f"Progress: {st.session_state.quiz_index + 1}/{total_questions}")
    
    # Question display - with error handling for missing question
    question_text = current_q.get('question', 'Question text not available')
    st.markdown(f"""
    <div class="story-text">
        <h4>📝 {question_text}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options with validation
    options = []
    for opt_key in ['option_a', 'option_b', 'option_c', 'option_d']:
        option_text = current_q.get(opt_key, '')
        if option_text and option_text.strip():
            options.append(option_text.strip())
    
    if len(options) == 0:
        st.error("❌ No answer options available for this question!")
        if st.button("⏭️ Skip Question", key="skip_question"):
            st.session_state.quiz_index += 1
            st.rerun()
        return
    
    # User answer selection with validation
    user_answer = st.radio(
        "Choose your answer:",
        options,
        key=f"answer_{st.session_state.quiz_index}"
    )
    
    # Submit button with answer validation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Submit Answer", use_container_width=True, type="primary", key="submit_answer"):
            # Validate user has selected an answer
            if not user_answer or user_answer.strip() == "":
                st.warning("⚠️ Please select an answer before submitting!")
                return
            
            # Safely get correct answer with fallback
            correct_letter = current_q.get('correct_answer', '').strip().upper()
            if not correct_letter:
                st.error("❌ Question data error: No correct answer found!")
                return
                
            # Map correct answer letter to actual option text
            option_map = {
                'A': current_q.get('option_a', '').strip(),
                'B': current_q.get('option_b', '').strip(), 
                'C': current_q.get('option_c', '').strip(),
                'D': current_q.get('option_d', '').strip()
            }
            correct_answer = option_map.get(correct_letter, '')
            
            # Validate correct answer exists
            if not correct_answer:
                st.error(f"❌ Question data error: Correct answer '{correct_letter}' not found!")
                return
            
            is_correct = user_answer.strip() == correct_answer.strip()
            
            if is_correct:
                st.success(f"✅ Excellent! That's correct!")
                st.session_state.quiz_score += 1
            else:
                st.error(f"❌ Not quite right. The correct answer is: {correct_answer}")
            
            # Move to next question or finish
            st.session_state.quiz_index += 1
            
            if st.session_state.quiz_index >= len(st.session_state.quiz_questions):
                show_quiz_results(realm_key, difficulty)
            else:
                st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏰 Return to Chapter Selection", use_container_width=True, key="quiz_chapter_return"):
            st.session_state.current_chapter = None
            st.rerun()
    with col2:
        if st.button("🏠 Return to Realms", use_container_width=True, key="quiz_realm_return"):
            st.session_state.current_realm = None
            st.session_state.current_chapter = None
            st.rerun()

def show_quiz_results(realm_key, difficulty):
    """Show the results after completing a quiz with comprehensive progress tracking and ML analysis"""
    realm_info = ADVENTURE_REALMS[realm_key]
    total_questions = len(st.session_state.quiz_questions)
    score = st.session_state.quiz_score
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Update comprehensive progress tracking
    update_user_progress(realm_key, difficulty, score, total_questions)
    
    st.markdown(f"""
    <div class="chapter-heading">
        🎉 Chapter Complete!
    </div>
    """, unsafe_allow_html=True)
    
    # Use simple Streamlit components instead of complex HTML
    st.success(f"🌟 Congratulations, {st.session_state.player_name}! 🌟")
    st.write(f"You have successfully completed the **{realm_info['difficulty_chapters'][difficulty]}** in **{realm_info['name']}**!")
    
    # Results display
    st.subheader("📊 Your Results")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Score",
            value=f"{score}/{total_questions}",
            delta=f"{percentage:.1f}% Accuracy"
        )
    # 🧠 Progressive ML Oracle Based on Learning Journey Stage
    st.subheader("🧠 ML Oracle's Wisdom")
    
    try:
        progress = st.session_state.player_progress
        current_performance = percentage / 100
        total_chapters_completed = sum(len(difficulties) for difficulties in progress['completed_chapters'].values())
        
        # Progressive recommendations based on learning journey stage
        if total_chapters_completed == 1:
            # First chapter completed - encouragement and basic guidance
            st.info("🌱 Analyzing your first adventure...")
            if current_performance >= 0.89:
                ml_insight = f"Outstanding debut! You've mastered **{realm_info['name']}** with {percentage:.1f}%! Ready to explore new realms?"
                weak_realm_key = None  # No specific recommendation yet
                recommendation = "🎉 **Excellent start!** You're ready to explore any realm that interests you. All paths are open!"
            elif current_performance >= 0.70:
                ml_insight = f"Great first chapter! {percentage:.1f}% shows solid understanding. Consider trying a few more chapters to build confidence."
                weak_realm_key = realm_key  # Suggest same realm for confidence building
                recommendation = f"💪 **Good progress!** Try another chapter in **{realm_info['name']}** to build mastery, or explore a new realm!"
            else:
                ml_insight = f"Good effort on your first chapter! {percentage:.1f}% is a solid foundation to build upon."
                weak_realm_key = realm_key
                recommendation = f"📚 **Keep practicing!** Try the same chapter again or an easier difficulty in **{realm_info['name']}** to build confidence."
        
        elif total_chapters_completed <= 3:
            # 2-3 chapters completed - exploration phase
            st.info("🔮 Analyzing your early adventures...")
            
            # Check if they're exploring different realms or focusing on one
            realms_visited = len(progress['completed_chapters'])
            
            if realms_visited == 1:
                # Focused on one realm - suggest exploration
                avg_score = progress['realm_mastery'][realm_key]
                if avg_score >= 85:
                    unvisited = set(ADVENTURE_REALMS.keys()) - {realm_key}
                    weak_realm_key = list(unvisited)[0] if unvisited else realm_key
                    ml_insight = f"Excellent focus! You're excelling in **{realm_info['name']}** (avg: {avg_score:.1f}%)."
                    recommendation = f"🌟 **Time to explore!** Try **{ADVENTURE_REALMS[weak_realm_key]['name']}** to broaden your skills!"
                else:
                    weak_realm_key = realm_key
                    ml_insight = f"Building mastery in **{realm_info['name']}** (avg: {avg_score:.1f}%). Keep strengthening this foundation!"
                    recommendation = f"🎯 **Focus mode!** Continue with **{realm_info['name']}** until you reach 89% mastery."
            else:
                # Exploring multiple realms - general encouragement
                best_realm = max(progress['realm_mastery'].items(), key=lambda x: x[1])
                worst_realm = min(progress['realm_mastery'].items(), key=lambda x: x[1])
                
                weak_realm_key = worst_realm[0]
                ml_insight = f"Great exploration! Your strongest area is **{ADVENTURE_REALMS[best_realm[0]]['name']}** ({best_realm[1]:.1f}%)."
                recommendation = f"🎨 **Balanced explorer!** Consider revisiting **{ADVENTURE_REALMS[weak_realm_key]['name']}** ({worst_realm[1]:.1f}%) for improvement."
        
        else:
            # 4+ chapters completed - detailed analysis with specific chapter recommendations
            st.info("🧠 Performing deep analysis of your learning journey...")
            
            # Find chapters that need revisiting (below 89%)
            chapters_needing_work = []
            for realm_key_check, difficulties in progress['completed_chapters'].items():
                for diff, data in difficulties.items():
                    if data['percentage'] < 89:
                        chapter_name = ADVENTURE_REALMS[realm_key_check]['difficulty_chapters'][diff]
                        chapters_needing_work.append({
                            'realm': realm_key_check,
                            'difficulty': diff,
                            'chapter_name': chapter_name,
                            'score': data['percentage'],
                            'realm_name': ADVENTURE_REALMS[realm_key_check]['name']
                        })
            
            if chapters_needing_work:
                # Sort by lowest score - recommend weakest chapter
                chapters_needing_work.sort(key=lambda x: x['score'])
                weakest_chapter = chapters_needing_work[0]
                
                weak_realm_key = weakest_chapter['realm']
                ml_insight = f"Analysis complete! I've identified {len(chapters_needing_work)} chapters below mastery level (89%)."
                recommendation = f"🎯 **Priority Chapter:** Revisit **{weakest_chapter['chapter_name']}** in **{weakest_chapter['realm_name']}** (current: {weakest_chapter['score']:.1f}%)"
                
                if len(chapters_needing_work) > 1:
                    recommendation += f"\n\n📋 **Also consider:** {len(chapters_needing_work)-1} other chapters need attention for full mastery."
            else:
                # All chapters mastered - suggest new exploration
                visited_realms = set(progress['completed_chapters'].keys())
                all_realms = set(ADVENTURE_REALMS.keys())
                unvisited = all_realms - visited_realms
                
                if unvisited:
                    weak_realm_key = list(unvisited)[0]
                    ml_insight = f"🏆 **Incredible mastery!** All {total_chapters_completed} completed chapters are above 89%!"
                    recommendation = f"🚀 **New frontier:** Explore **{ADVENTURE_REALMS[weak_realm_key]['name']}** for fresh challenges!"
                else:
                    weak_realm_key = realm_key
                    ml_insight = f"🎖️ **LEGENDARY STATUS!** You've mastered all realms with 89%+ scores!"
                    recommendation = "👑 **Master of All Realms!** Try harder difficulties or help others on their journey!"
        
        # Display progressive ML recommendations
        st.write(f"**📈 Current Performance:** {percentage:.1f}% in {realm_info['name']}")
        st.success(f"🧠 **ML Insight:** {ml_insight}")
        
        if 'weak_realm_key' in locals() and weak_realm_key and weak_realm_key != realm_key:
            weak_realm_info = ADVENTURE_REALMS.get(weak_realm_key)
            if weak_realm_info:
                st.write(f"**🎯 Recommended Focus Area:** {weak_realm_info['emoji']} **{weak_realm_info['name']}**")
                st.write(f"*\"{weak_realm_info['description']}\"*")
        
        st.info(recommendation)
        
        # Show mini progress dashboard after each quiz
        st.subheader("📈 Your Progress So Far")
        show_progress_dashboard()
        
    except Exception as e:
        st.error(f"🤖 ML Oracle is temporarily unavailable: {str(e)}")
        st.info("🔮 The mystical analysis will be ready for your next adventure!")
        print(f"ML Analysis Error: {e}")
    
    # Performance feedback with 89% mastery threshold
    if percentage >= 89:
        st.balloons()
        st.success("🎊 Outstanding mastery! You've truly conquered this chapter!")
    elif percentage >= 70:
        st.success("🎯 Well done! You've shown good understanding of this topic!")
    else:
        st.info("📚 Keep practicing! Every challenge makes you stronger!")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Try Another Chapter", use_container_width=True, key="results_try_another"):
            # Reset quiz state
            st.session_state.quiz_questions = []
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.current_chapter = None
            st.rerun()
    
    with col2:
        if st.button("🏠 Return to Realm Selection", use_container_width=True, key="results_realm_selection"):
            # Reset all state
            st.session_state.quiz_questions = []
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.current_realm = None
            st.session_state.current_chapter = None
            st.rerun()

def show_student_report():
    """Display comprehensive ML-powered student analysis report"""
    st.markdown('<div class="ornament">🎓 ✨ 📊 ✨ 🎓</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chapter-heading">
        🧠 AI-Powered Student Analysis Report
    </div>
    """, unsafe_allow_html=True)
    
    progress_data = st.session_state.player_progress
    
    if not progress_data['completed_chapters']:
        st.warning("📝 Complete at least one chapter to generate your personalized student report!")
        return
    
    # Generate comprehensive report using ML models
    with st.spinner("🤖 AI Oracle analyzing your learning patterns..."):
        report = student_analyzer.generate_student_report(
            st.session_state.player_name,
            progress_data
        )
    
    if 'error' in report:
        st.error(f"❌ {report['error']}")
        return
    
    # Display report header
    st.markdown(f"""
    <div class="story-text">
        <h3>📋 Student Report for {report['student_name']}</h3>
        <p><em>Generated on: {report['report_date']}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
    st.subheader("📊 Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Chapters Completed",
            report['summary']['total_chapters'],
            help="Total number of chapters you've completed across all realms"
        )
    
    with col2:
        st.metric(
            "Overall Accuracy",
            f"{report['summary']['overall_accuracy']:.1f}%",
            help="Your average performance across all questions"
        )
    
    with col3:
        st.metric(
            "Realms Mastered",
            f"{report['summary']['realms_mastered']}/5",
            help="Number of realms where you've achieved 89%+ mastery"
        )
    
    with col4:
        st.metric(
            "Consistency Score",
            f"{report['summary']['consistency_score']:.1f}%",
            help="How consistent your performance is across topics"
        )
    
    # ML Analysis Section
    st.subheader("🧠 AI Machine Learning Analysis")
    
    ml_analysis = report['ml_analysis']
    
    # Primary weakness with confidence
    confidence_color = "green" if ml_analysis['confidence'] > 0.8 else "orange" if ml_analysis['confidence'] > 0.6 else "red"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-left: 5px solid {confidence_color}; padding: 15px; margin: 10px 0; border-radius: 5px;">
        <h4>🎯 Primary Focus Area: {ml_analysis['primary_weakness'].title()}</h4>
        <p><strong>AI Confidence:</strong> {ml_analysis['confidence']:.1%}</p>
        <p><strong>Learning Trajectory:</strong> {ml_analysis['learning_trajectory'].title()}</p>
        <p><strong>Improvement Probability:</strong> {ml_analysis['improvement_probability']:.1%}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed weakness breakdown
    st.subheader("🔍 Detailed Area Analysis")
    
    weakness_data = ml_analysis['weakness_breakdown']
    
    # Create visualization for weakness probabilities
    topics = list(weakness_data.keys())
    weakness_probs = [data['weakness_probability'] * 100 for data in weakness_data.values()]
    current_scores = [data['current_score'] * 100 for data in weakness_data.values()]
    
    fig = go.Figure()
    
    # Add current performance bars
    fig.add_trace(go.Bar(
        name='Current Performance',
        x=topics,
        y=current_scores,
        marker_color='lightblue',
        yaxis='y'
    ))
    
    # Add weakness probability line
    fig.add_trace(go.Scatter(
        name='Needs Attention (%)',
        x=topics,
        y=weakness_probs,
        mode='lines+markers',
        marker_color='red',
        line=dict(width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Performance vs. Areas Needing Attention',
        xaxis_title='Learning Areas',
        yaxis=dict(title='Current Performance (%)', side='left', range=[0, 100]),
        yaxis2=dict(title='Attention Needed (%)', side='right', range=[0, 100], overlaying='y'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations section
    st.subheader("💡 Personalized Recommendations")
    
    for rec in report['recommendations']:
        priority_color = {"HIGH": "red", "MEDIUM": "orange", "LOW": "green"}[rec['priority']]
        
        st.markdown(f"""
        <div style="border-left: 4px solid {priority_color}; padding: 10px; margin: 5px 0; background: #f8f9fa;">
            <h5>🎯 {rec['action']} <span style="color: {priority_color};">({rec['priority']} Priority)</span></h5>
            <p><strong>Why:</strong> {rec['reason']}</p>
            <p><strong>Timeline:</strong> {rec['timeline']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Learning insights
    st.subheader("🌟 Learning Insights")
    
    for insight in report['learning_insights']:
        st.markdown(f"- {insight}")
    
    # Detailed performance table
    with st.expander("📈 Detailed Performance Breakdown"):
        performance_df = pd.DataFrame([
            {
                'Area': area.title(),
                'Current Score': f"{data['current_score']*100:.1f}%",
                'Needs Attention': "Yes" if data['needs_attention'] else "No",
                'Weakness Probability': f"{data['weakness_probability']*100:.1f}%"
            }
            for area, data in weakness_data.items()
        ])
        st.dataframe(performance_df, use_container_width=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Practice Weak Areas", type="primary", use_container_width=True):
            # Navigate to the weakest realm
            weakest_realm = ml_analysis['primary_weakness']
            st.session_state.current_realm = weakest_realm
            st.rerun()
    
    with col2:
        if st.button("📊 View Progress Dashboard", use_container_width=True):
            show_progress_dashboard()
    
    with col3:
        if st.button("🏠 Back to Adventure", use_container_width=True):
            st.rerun()

# Run the adventure!
if __name__ == "__main__":
    main()

