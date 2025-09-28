#!/usr/bin/env python3
"""
🌟 English Adventure Explorer 
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
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Cinzel+Decorative:wght@400;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(145deg, #f4f1e8, #e8dcc0);
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 108, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(120, 119, 108, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(160, 120, 80, 0.05) 0%, transparent 50%);
        font-family: 'Crimson Text', serif;
    }
    
    /* Book title styling */
    .book-title {
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        color: #2c1810;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f9f7f1, #ede4d0);
        border: 3px solid #8b7355;
        border-radius: 15px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Chapter headings */
    .chapter-heading {
        font-family: 'Cinzel Decorative', cursive;
        font-size: 2.2rem;
        color: #654321;
        text-align: center;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background: rgba(255, 248, 240, 0.8);
        border-left: 8px solid #cd853f;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Story text styling */
    .story-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.3rem;
        line-height: 1.8;
        color: #2c2416;
        background: rgba(255, 252, 245, 0.9);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #d4af37;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        position: relative;
    }
    
    .story-text::before {
        content: '"';
        font-size: 4rem;
        color: #cd853f;
        position: absolute;
        top: -10px;
        left: 15px;
        font-family: 'Crimson Text', serif;
        opacity: 0.6;
    }
    
    /* Question box styling */
    .question-box {
        background: linear-gradient(135deg, #fdfbf7, #f5f0e8);
        border: 3px solid #8b6f47;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
    }
    
    .question-box::before {
        content: "⚡";
        font-size: 2rem;
        position: absolute;
        top: -15px;
        left: 20px;
        background: #f9f7f1;
        padding: 0 10px;
        border-radius: 50%;
    }
    
    /* Option buttons styling */
    .stButton > button {
        background: linear-gradient(135deg, #f4f1e8, #e8dcc0) !important;
        border: 2px solid #8b6f47 !important;
        border-radius: 10px !important;
        color: #2c1810 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #e8dcc0, #d4c4a0) !important;
        border-color: #654321 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Progress styling */
    .adventure-progress {
        background: linear-gradient(90deg, #cd853f, #daa520);
        border-radius: 25px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(205, 133, 63, 0.3);
    }
    
    /* Realm cards */
    .realm-card {
        background: linear-gradient(135deg, rgba(255,248,240,0.95), rgba(250,240,230,0.95));
        border: 3px solid #8b6f47;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .realm-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border-color: #cd853f;
    }
    
    .realm-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(218,165,32,0.1) 0%, transparent 70%);
        transition: all 0.4s ease;
        z-index: 0;
    }
    
    .realm-card:hover::before {
        transform: scale(1.5) rotate(180deg);
    }
    
    .realm-content {
        position: relative;
        z-index: 1;
    }
    
    /* Adventure stats */
    .adventure-stat {
        background: rgba(139, 111, 71, 0.1);
        border-left: 5px solid #cd853f;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        font-family: 'Crimson Text', serif;
    }
    
    /* Success/failure messages */
    .success-message {
        background: linear-gradient(135deg, #d4f6d4, #a8e6a8);
        border: 2px solid #4caf50;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #2e7d32;
        font-weight: 600;
    }
    
    .gentle-redirect {
        background: linear-gradient(135deg, #fff3cd, #ffeeba);
        border: 2px solid #ffc107;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #856404;
        font-weight: 600;
    }
    
    /* Decorative elements */
    .ornament {
        text-align: center;
        font-size: 2rem;
        color: #cd853f;
        margin: 2rem 0 1rem 0;
    }
    
    /* Analytics dashboard styling */
    .analytics-scroll {
        background: rgba(255, 248, 240, 0.95);
        border: 3px solid #8b6f47;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .analytics-scroll::before {
        content: "📜";
        font-size: 2rem;
        position: absolute;
        top: -15px;
        left: 20px;
        background: #f9f7f1;
        padding: 0 8px;
        border-radius: 50%;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(248, 243, 235, 0.95);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ========================================
# DATA LOADING & CONFIGURATION
# ========================================

# Adventure realm configuration
ADVENTURE_REALMS = {
    "grammar": {
        "name": "🌳 Grammar Grove", 
        "emoji": "🌳",
        "description": "Ancient woods where verb sprites dance and pronoun pixies play",
        "welcome": "Welcome to Grammar Grove, where the wise old Oak teaches the secrets of perfect sentences!",
        "mentor": "Professor Syntax, the Grammar Guardian",
        "difficulty_chapters": {
            "easy": "The Whispering Woods",
            "medium": "The Enchanted Clearing", 
            "hard": "The Sacred Grove"
        }
    },
    "articles": {
        "name": "📜 Article Academy", 
        "emoji": "📜",
        "description": "Ancient library with mysterious scrolls missing crucial words",
        "welcome": "Enter the hallowed halls of Article Academy, where ancient scrolls await completion!",
        "mentor": "Librarian Articula, Keeper of the Scrolls",
        "difficulty_chapters": {
            "easy": "The Reading Room",
            "medium": "The Manuscript Hall",
            "hard": "The Sacred Archive"
        }
    },
    "synonyms": {
        "name": "🦋 Synonym Sanctuary", 
        "emoji": "🦋",
        "description": "Magical garden where creatures speak only in similar words",
        "welcome": "Welcome to Synonym Sanctuary, where every word has a twin waiting to be discovered!",
        "mentor": "The Wordweaver, Guardian of Meanings",
        "difficulty_chapters": {
            "easy": "The Garden Gates",
            "medium": "The Butterfly Meadow",
            "hard": "The Heart of the Sanctuary"
        }
    },
    "antonyms": {
        "name": "🪞 Antonym Archipelago", 
        "emoji": "🪞",
        "description": "Mirror islands where everything means the opposite",
        "welcome": "Cross the waters to Antonym Archipelago, where opposites attract and mirrors reveal truth!",
        "mentor": "Captain Contrary, Master of Opposites",
        "difficulty_chapters": {
            "easy": "Mirror Bay",
            "medium": "Reflection Ridge",
            "hard": "The Opposite Observatory"
        }
    },
    "sentences": {
        "name": "🏰 Sentence Citadel", 
        "emoji": "🏰",
        "description": "Magnificent fortress where perfect sentences unlock magical doors",
        "welcome": "Behold the Sentence Citadel, where Alex must master the art of perfect construction!",
        "mentor": "The Grand Architect of Language",
        "difficulty_chapters": {
            "easy": "The Outer Courtyard",
            "medium": "The Great Hall",
            "hard": "The Throne Room"
        }
    }
}

@st.cache_data
def load_adventure_data():
    """Load the CSV data and organize by adventure realms"""
    if not os.path.exists("data/manabifun_questions.csv"):
        st.error("📚 The ancient scrolls seem to be missing! Please ensure the question database exists.")
        return None
    
    try:
        df = pd.read_csv("data/manabifun_questions.csv")
        
        # Clean and organize data
        df['topic'] = df['topic'].str.lower().str.strip()
        df['difficulty'] = df['difficulty'].str.lower().str.strip()
        df['correct_answer'] = df['correct_answer'].str.upper().str.strip()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['question']).reset_index(drop=True)
        
        return df
    except Exception as e:
        st.error(f"📚 The ancient scrolls are damaged! Error: {str(e)}")
        return None

@st.cache_resource
def load_adventure_model():
    """Load the ML model for Alex's weakness detection"""
    if os.path.exists("models/weakness_detector.pkl"):
        try:
            with open("models/weakness_detector.pkl", "rb") as f:
                model_data = pickle.load(f)
            
            if isinstance(model_data, dict):
                return model_data['model'], model_data['topics']
            return model_data, list(ADVENTURE_REALMS.keys())
        except Exception:
            return None, None
    return None, None

# ========================================
# XP SYSTEM AND ADVENTURE MOTIVATION
# ========================================

def award_xp(amount, reason):
    """Award XP and adventure points with tracking"""
    st.session_state.total_xp += amount
    st.session_state.adventure_points += amount
    
def get_xp_for_correct_answer():
    """XP for each correct answer"""
    return 15

def get_xp_for_chapter_pass():
    """XP for passing a chapter (89%+)"""
    return 150

def get_xp_for_realm_mastery():
    """XP for mastering an entire realm"""
    return 500

def generate_encouragement_message(realm_key, accuracy, is_passed):
    """Generate Enid Blyton-style encouragement messages"""
    realm_info = ADVENTURE_REALMS[realm_key]
    mentor = realm_info['mentor']
    
    if is_passed:
        success_messages = [
            f"🌟 'Magnificent work, brave explorer!' exclaimed {mentor} with sparkling eyes. 'You've achieved {accuracy:.1f}% mastery - truly worthy of the ancient halls of learning!'",
            f"⚡ The magical crystals of {realm_info['name']} glow with approval! {mentor} beams proudly: 'With {accuracy:.1f}% accuracy, you've proven yourself a true word-warrior!'",
            f"🎭 'Splendid adventure, young scholar!' {mentor} declares. 'Your {accuracy:.1f}% mastery has unlocked new mysteries in our realm!'",
            f"🏆 The entire {realm_info['name']} celebrates your triumph! {mentor} bows respectfully: 'Such wisdom at {accuracy:.1f}% - the ancient texts sing your praises!'"
        ]
        return random.choice(success_messages)
    else:
        encouragement_messages = [
            f"🌱 'Fear not, dear adventurer!' {mentor} says kindly. 'With {accuracy:.1f}%, you've shown great promise! Every master explorer needs practice - return when you feel ready to strengthen your skills!'",
            f"📚 {mentor} smiles warmly: 'Your {accuracy:.1f}% shows excellent progress, but the ancient magic requires 89% mastery. Take time to study the scrolls and return stronger!'",
            f"🔮 'The crystals whisper of your potential!' {mentor} encourages. 'You achieved {accuracy:.1f}% - so close to unlocking the full mysteries! Practice your craft and return when ready!'",
            f"🌟 'Every great explorer faces challenges!' {mentor} says with twinkling eyes. 'Your {accuracy:.1f}% proves you have the heart of a scholar. Strengthen your knowledge and return triumphant!'"
        ]
        return random.choice(encouragement_messages)

def get_weakness_recommendation_message(player_name, weak_realm, confidence):
    """Generate ML-powered weakness recommendation in adventure style"""
    realm_info = ADVENTURE_REALMS.get(weak_realm, {})
    realm_name = realm_info.get('name', weak_realm)
    mentor = realm_info.get('mentor', 'The Ancient Oracle')
    
    return f"""
    🔮 **The Ancient Oracle's Vision**
    
    "{player_name}, the mystical currents reveal your greatest opportunity for growth! 
    The magical essence suggests focusing your next adventures in **{realm_name}**. 
    
    The spirits whisper with {confidence:.1f}% certainty that treasures of knowledge 
    await you there. {mentor} is prepared to guide your learning journey!
    
    *Remember, young explorer - every master was once a beginner. 
    Your path to linguistic mastery leads through dedicated practice!"*
    """

# ========================================
# ML-POWERED QUESTION SHUFFLING
# ========================================

def fisher_yates_shuffle(questions_list):
    """Fisher-Yates shuffle algorithm for unbiased question randomization"""
    questions = questions_list.copy()
    n = len(questions)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        questions[i], questions[j] = questions[j], questions[i]
    return questions

def get_chapter_questions(questions_df, realm_key, difficulty, max_questions=10):
    """Get shuffled questions for a chapter with ML-powered selection"""
    # Filter questions for current realm and difficulty
    filtered_questions = questions_df[
        (questions_df['topic'] == realm_key) & 
        (questions_df['difficulty'] == difficulty)
    ]
    
    if len(filtered_questions) == 0:
        return []
    
    # Convert to list and shuffle with Fisher-Yates
    questions_list = filtered_questions.to_dict('records')
    shuffled_questions = fisher_yates_shuffle(questions_list)
    
    # Limit to max_questions (10)
    return shuffled_questions[:max_questions]

def calculate_chapter_accuracy(realm_key, difficulty):
    """Calculate accuracy for a specific chapter"""
    chapter_stats = st.session_state.chapter_stats[realm_key][difficulty]
    if chapter_stats['total_questions'] == 0:
        return 0
    return (chapter_stats['correct_answers'] / chapter_stats['total_questions']) * 100

def is_chapter_passed(realm_key, difficulty, pass_threshold=89):
    """Check if chapter meets 89% pass threshold"""
    accuracy = calculate_chapter_accuracy(realm_key, difficulty)
    total_questions = st.session_state.chapter_stats[realm_key][difficulty]['total_questions']
    
    # Need at least 10 questions attempted AND 89% accuracy
    return total_questions >= 10 and accuracy >= pass_threshold

def is_realm_mastered(realm_key, questions_df):
    """Check if entire realm is mastered (all available chapters passed)"""
    mastered_chapters = 0
    available_chapters = 0
    
    for difficulty in ['easy', 'medium', 'hard']:
        chapter_questions = questions_df[
            (questions_df['topic'] == realm_key) & 
            (questions_df['difficulty'] == difficulty)
        ]
        
        if len(chapter_questions) > 0:  # Chapter exists
            available_chapters += 1
            if is_chapter_passed(realm_key, difficulty):
                mastered_chapters += 1
    
    return available_chapters > 0 and mastered_chapters == available_chapters

# ========================================
# ADVENTURE SESSION MANAGEMENT
# ========================================

def initialize_adventure():
    """Initialize Alex's adventure session"""
    if 'adventure_initialized' not in st.session_state:
        st.session_state.adventure_initialized = True
        st.session_state.player_name = ""
        st.session_state.current_realm = None
        st.session_state.current_chapter = None
        st.session_state.adventure_points = 0
        st.session_state.total_xp = 0
        st.session_state.quest_streak = 0
        st.session_state.completed_realms = set()
        st.session_state.mastered_realms = set()  # Realms with 89%+ accuracy
        st.session_state.current_question_idx = 0
        
        # New progress tracking: {realm: {difficulty: {'questions_taken': [], 'correct_answers': 0, 'total_questions': 0, 'accuracy': 0, 'passed': False}}}
        st.session_state.chapter_stats = {}
        for realm in ADVENTURE_REALMS.keys():
            st.session_state.chapter_stats[realm] = {
                'easy': {'questions_taken': [], 'correct_answers': 0, 'total_questions': 0, 'accuracy': 0, 'passed': False, 'attempts': 0},
                'medium': {'questions_taken': [], 'correct_answers': 0, 'total_questions': 0, 'accuracy': 0, 'passed': False, 'attempts': 0},
                'hard': {'questions_taken': [], 'correct_answers': 0, 'total_questions': 0, 'accuracy': 0, 'passed': False, 'attempts': 0}
            }
        
        st.session_state.answers_log = []
        st.session_state.show_question = False
        st.session_state.question_answered = False
        st.session_state.last_answer_correct = None
        st.session_state.current_question_set = []  # Shuffled questions for current chapter

def save_adventure_progress():
    """Save Alex's progress to CSV"""
    try:
        progress_data = {
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'player_name': [st.session_state.player_name],
            'adventure_points': [st.session_state.adventure_points],
            'quest_streak': [st.session_state.quest_streak],
            'completed_realms': [len(st.session_state.completed_realms)],
            'total_questions': [len(st.session_state.answers_log)]
        }
        
        progress_df = pd.DataFrame(progress_data)
        
        if os.path.exists("data/student_scores.csv"):
            existing_df = pd.read_csv("data/student_scores.csv")
            progress_df = pd.concat([existing_df, progress_df], ignore_index=True)
        
        progress_df.to_csv("data/student_scores.csv", index=False)
    except Exception as e:
        st.warning(f"Could not save progress: {e}")

# ========================================
# STORY GENERATION FUNCTIONS
# ========================================

def generate_story_intro(realm_name, difficulty):
    """Generate story introduction for each chapter"""
    realm_info = ADVENTURE_REALMS[realm_name]
    chapter_name = realm_info['difficulty_chapters'][difficulty]
    
    intros = {
        "grammar": {
            "easy": f"Alex stepped into {chapter_name}, where gentle sunbeams danced through ancient oak leaves. The Grammar Guardian smiled warmly, 'Young explorer, master these simple challenges and the forest spirits will guide you deeper!'",
            "medium": f"Deeper in the grove, Alex reached {chapter_name}. Here, the trees whispered more complex riddles, and Professor Syntax appeared with twinkling eyes, 'The magic grows stronger here, brave Alex!'",
            "hard": f"At last, Alex stood before {chapter_name}, where the most ancient trees held the deepest secrets. The Grammar Guardian's voice echoed solemnly, 'Only true mastery will unlock these mysteries, dear adventurer!'"
        },
        "articles": {
            "easy": f"Alex pushed open the great oak doors to enter {chapter_name}. Librarian Articula gestured to glowing scrolls, 'Welcome, young scholar! These simple texts await your wisdom.'",
            "medium": f"Ascending the marble stairs, Alex entered {chapter_name}. Ancient manuscripts floated in the air, and Articula nodded approvingly, 'You're ready for greater challenges now!'",
            "hard": f"Through golden doors, Alex entered {chapter_name}. Here, the most sacred texts pulsed with magical energy. 'Few reach this chamber,' whispered Articula reverently."
        },
        "synonyms": {
            "easy": f"Alex wandered into {chapter_name}, where colorful butterflies danced around blooming flowers. The Wordweaver laughed melodically, 'Each flower here speaks in different voices - listen carefully!'",
            "medium": f"In {chapter_name}, magical creatures fluttered around Alex with knowing smiles. 'The deeper mysteries await,' sang the Wordweaver, 'where words dance as one!'",
            "hard": f"Alex reached {chapter_name}, where ethereal beings communicated in perfect harmony. The Wordweaver's voice grew mystical: 'Here, you must understand the deepest connections of language.'"
        },
        "antonyms": {
            "easy": f"Alex's boat touched the shores of {chapter_name}. Captain Contrary grinned and pointed to simple mirrors, 'Start with these reflecting pools, young navigator!'",
            "medium": f"On {chapter_name}, Alex found mirrors that showed curious reversals. Captain Contrary chuckled, 'The islands grow stranger as you journey deeper!'",
            "hard": f"At {chapter_name}, reality itself seemed to bend and twist. Captain Contrary spoke seriously, 'Here, young explorer, only those who truly understand opposites may pass.'"
        },
        "sentences": {
            "easy": f"Alex entered {chapter_name} of the magnificent citadel. The Grand Architect smiled warmly, 'Begin with these foundation stones of language, young builder!'",
            "medium": f"In {chapter_name}, Alex marveled at intricate grammatical architecture. 'Now we construct more complex structures,' declared the Grand Architect proudly.",
            "hard": f"Finally reaching {chapter_name}, Alex gasped at the breathtaking mastery required. The Grand Architect spoke with reverence: 'Here lies the ultimate test of linguistic artistry.'"
        }
    }
    
    return intros[realm_name][difficulty]

def generate_question_story(question_text, realm_name, difficulty):
    """Transform a CSV question into story narrative"""
    realm_info = ADVENTURE_REALMS[realm_name]
    mentor = realm_info['mentor']
    
    story_frames = {
        "grammar": [
            "The ancient oak rustled its leaves and posed a riddle to Alex: ",
            f"{mentor} appeared in a shimmer of golden light, asking: ",
            "A friendly forest sprite giggled and challenged Alex: ",
            "The Grammar Guardian's voice echoed through the trees: "
        ],
        "articles": [
            "A glowing scroll unfurled before Alex, missing crucial words: ",
            f"{mentor} presented an ancient manuscript to Alex: ",
            "A floating parchment danced in the air, asking Alex: ",
            "The mystical tome opened to reveal: "
        ],
        "synonyms": [
            "A butterfly with shimmering wings whispered to Alex: ",
            "The magical garden flowers began to sing: ",
            f"{mentor} smiled knowingly and asked: ",
            "A chorus of woodland creatures chimed together: "
        ],
        "antonyms": [
            "The mirror showed Alex a reflection with a riddle: ",
            f"{mentor} pointed across the waters, asking: ",
            "An opposite-speaking parrot squawked at Alex: ",
            "The magical mirror portal shimmered with the question: "
        ],
        "sentences": [
            "The citadel's great door displayed golden letters: ",
            f"{mentor} gestured to architectural blueprints, saying: ",
            "Magical building blocks rearranged themselves to ask: ",
            "The throne room's enchanted voice resonated: "
        ]
    }
    
    frame = random.choice(story_frames[realm_name])
    return f'"{frame}{question_text}"'

def generate_success_story(realm_name, is_correct=True):
    """Generate story responses for correct/incorrect answers"""
    if is_correct:
        success_stories = {
            "grammar": [
                "✨ The forest spirits cheered as Alex's answer rang true! Golden leaves swirled around in celebration.",
                "🌟 'Excellent!' beamed Professor Syntax. 'Your grammatical wisdom grows stronger!'",
                "⭐ The ancient oak's branches glowed with approval, opening a new path deeper into the grove.",
                "🎉 Forest creatures emerged from behind trees, applauding Alex's linguistic prowess!"
            ],
            "articles": [
                "📚 The scroll glowed with mystical light and rolled itself up with satisfaction!",
                "✨ 'Marvelous!' exclaimed Librarian Articula. 'The ancient texts approve of your wisdom!'",
                "🌟 The manuscript's missing words filled themselves in with golden ink, completing the magic!",
                "⭐ Ancient books on nearby shelves hummed with harmonious approval!"
            ],
            "synonyms": [
                "🦋 Butterflies danced in joyous spirals around Alex, their wings shimmering with delight!",
                "🌺 The garden bloomed even more magnificently, flowers singing in perfect harmony!",
                "✨ 'Beautiful!' sang the Wordweaver. 'You've captured the essence of meaning perfectly!'",
                "🌟 Magical creatures throughout the sanctuary nodded with wise approval!"
            ],
            "antonyms": [
                "🪞 The mirror cracked with joy, revealing a treasure chest on the opposite shore!",
                "⚡ 'Precisely opposite!' laughed Captain Contrary. 'You've mastered the mirror's magic!'",
                "✨ The reflection world shimmered and revealed new islands to explore!",
                "🌟 Opposite-birds flew in formation, creating rainbow patterns in the sky!"
            ],
            "sentences": [
                "🏰 The citadel's doors swung open majestically, revealing chambers of linguistic gold!",
                "⚡ 'Magnificent construction!' declared the Grand Architect. 'Your sentence sparkles with perfection!'",
                "✨ Golden mortar filled the gaps between words, strengthening Alex's grammatical foundations!",
                "🌟 The entire citadel resonated with harmonic approval, walls glowing with warm light!"
            ]
        }
        return random.choice(success_stories[realm_name])
    else:
        gentle_redirects = {
            "grammar": [
                "🍃 'Not quite!' smiled a helpful pixie. 'But the scenic route through the Syntax Woods teaches much!' The forest spirits guided Alex along a beautiful winding path.",
                "🌿 Professor Syntax chuckled kindly, 'Every explorer takes detours! Let me show you a secret shortcut that teaches even more grammar magic!'",
                "🦋 'The forest has many paths,' whispered the Grammar Guardian gently. 'This alternative route will strengthen your skills beautifully!'",
                "🌸 A wise old owl hooted softly, 'Mistakes are stepping stones to mastery, young Alex. Follow the moonbeam trail to discover new insights!'"
            ],
            "articles": [
                "📖 'Ah, a learning moment!' Librarian Articula smiled warmly. 'Let's explore this fascinating manuscript wing together - it holds the answer!'",
                "📜 The scroll chuckled (if scrolls could chuckle) and unfurled a helpful study guide. 'Every scholar needs reference materials!'",
                "🔍 'The great detectives of grammar all made such discoveries!' Articula winked. 'This research path will illuminate the truth!'",
                "✨ Ancient books whispered encouragingly, 'The longest journeys teach the most, brave scholar!' and glowed to light Alex's way."
            ],
            "synonyms": [
                "🌼 'Close, but not quite the same bloom!' giggled the garden sprites. 'Follow the butterfly trail to find the perfect twin word!'",
                "🦋 The Wordweaver sang softly, 'Each word has its perfect partner! Let's dance through the meadow to find yours!'",
                "🌺 'Words are shy creatures,' whispered a flower fairy. 'Sometimes they hide! Let's search together in the synonym sanctuary!'",
                "✨ Magical creatures formed a helpful parade, leading Alex through a garden maze full of word treasures!"
            ],
            "antonyms": [
                "🪞 'Opposites can be tricky!' laughed Captain Contrary. 'But this scenic route around the reflection lake teaches much more!'",
                "⚡ The mirror world shimmered with amusement. 'Every navigator needs practice reading the opposite currents! This way to understanding!'",
                "🌊 'The tides of language ebb and flow!' called the Captain wisely. 'Follow the reverse current to discover the truth!'",
                "🔮 Mirror-dolphins splashed playfully, leading Alex on an underwater adventure full of opposite treasures!"
            ],
            "sentences": [
                "🏗️ 'Even master builders adjust their blueprints!' smiled the Grand Architect kindly. 'Let's examine the foundation stones together!'",
                "⚡ The citadel's walls glowed encouragingly. 'Strong structures need careful planning! Follow the architectural tour for insights!'",
                "🔧 'Every great constructor learns through experimentation!' The Grand Architect opened a workshop full of sentence-building tools.",
                "✨ Helpful construction sprites appeared with tiny hammers and measuring tools, ready to assist Alex's grammatical building!"
            ]
        }
        return random.choice(gentle_redirects[realm_name])

# ========================================
# MAIN APPLICATION FUNCTIONS
# ========================================

def show_adventure_title():
    """Display the main book title"""
    # Use player's name if available, otherwise use default
    if hasattr(st.session_state, 'player_name') and st.session_state.player_name:
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
    """Handle player name input and adventure setup"""
    st.markdown("""
    <div class="story-text">
        Once upon a time, in a world where words held magical power and grammar could unlock secret doors, 
        there lived a brave young explorer with an insatiable curiosity for language and adventure...
        
        <br><br>
        
        But every great adventurer needs a name! What shall we call our intrepid explorer?
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        player_name = st.text_input(
            "✨ Enter the explorer's name:", 
            value=st.session_state.player_name,
            placeholder="Alex the Adventurer",
            help="Choose a name worthy of epic adventures!"
        )
        
        if st.button("🚀 Begin the Adventure!", use_container_width=True):
            if player_name.strip():
                st.session_state.player_name = player_name.strip()
                st.rerun()
            else:
                st.warning("Every great explorer needs a name!")

def show_realm_selection(questions_df):
    """Display the magical realm selection"""
    st.markdown(f"""
    <div class="chapter-heading">
        Welcome, {st.session_state.player_name}! 🌟
    </div>
    
    <div class="story-text">
        Your reputation as a word-master has spread across the land, {st.session_state.player_name}! 
        Five magical realms await your expertise, each guarded by ancient puzzles that only a true 
        language explorer can solve.
        
        <br><br>
        
        Choose your first destination wisely - though fear not, for all paths lead to greater wisdom!
    </div>
    """, unsafe_allow_html=True)
    
    # Adventure progress summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="adventure-stat">
            <strong>🌟 Adventure Points:</strong><br>
            {st.session_state.adventure_points}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="adventure-stat">
            <strong>🔥 Quest Streak:</strong><br>
            {st.session_state.quest_streak}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="adventure-stat">
            <strong>🏰 Realms Conquered:</strong><br>
            {len(st.session_state.completed_realms)}/5
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="adventure-stat">
            <strong>📚 Challenges Faced:</strong><br>
            {len(st.session_state.answers_log)}
        </div>
        """, unsafe_allow_html=True)
    
    # Realm selection
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    for idx, (realm_key, realm_info) in enumerate(ADVENTURE_REALMS.items()):
        with cols[idx % 2]:
            # 🎯 Calculate with 10-question limit per chapter
            realm_chapters = []
            total_possible = 0
            for diff in ['easy', 'medium', 'hard']:
                chapter_q = len(questions_df[(questions_df['topic'] == realm_key) & 
                                           (questions_df['difficulty'] == diff)].head(10))
                if chapter_q > 0:
                    realm_chapters.append((diff, chapter_q))
                    total_possible += chapter_q
            
            # Calculate progress using new chapter_stats system
            mastered_chapters = sum(1 for diff in ['easy', 'medium', 'hard'] 
                                  if is_chapter_passed(realm_key, diff))
            available_chapters = len(realm_chapters)
            progress_percentage = (mastered_chapters / available_chapters * 100) if available_chapters > 0 else 0
            
            # 🎨 Dynamic completion status with colors  
            if realm_key in st.session_state.mastered_realms:
                completion_status = "🏆 MASTERED! All chapters at 89%+"
                status_color = "#28a745"
                border_color = "#4caf50"
                glow = "0 0 20px rgba(76, 175, 80, 0.3)"
            elif mastered_chapters > 0:
                completion_status = f"⚡ Progress: {mastered_chapters}/{available_chapters} chapters mastered"
                status_color = "#ffc107"
                border_color = "#ffc107"
                glow = "0 0 15px rgba(255, 193, 7, 0.2)"
            else:
                completion_status = "🔮 Awaiting Discovery"
                status_color = "#6f42c1"
                border_color = "#8b6f47"
                glow = "0 0 10px rgba(139, 111, 71, 0.1)"
            
            # 🎨 Super cool realm card with dynamic styling
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,248,240,0.95), rgba(250,240,230,0.95));
                border: 3px solid {border_color};
                border-radius: 20px;
                padding: 2rem;
                margin: 1rem 0;
                text-align: center;
                cursor: pointer;
                transition: all 0.4s ease;
                box-shadow: {glow};
                position: relative;
                overflow: hidden;
            ">
                <h3 style="color: {status_color}; margin-bottom: 1rem; font-family: 'Cinzel Decorative', cursive;">
                    {realm_info['emoji']} {realm_info['name']}
                </h3>
                <p style="font-style: italic; margin-bottom: 1rem; color: #2c2416;">
                    {realm_info['description']}
                </p>
                <p style="font-weight: 600; color: {status_color}; margin-bottom: 1rem;">
                    {completion_status}
                </p>
                <div style="background: rgba(0,0,0,0.1); border-radius: 10px; height: 8px; margin-top: 15px;">
                    <div style="background: {status_color}; height: 8px; border-radius: 10px; width: {progress_percentage}%; transition: width 0.8s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                f"🚪 Enter {realm_info['name']}",
                key=f"realm_{realm_key}",
                use_container_width=True
            ):
                st.session_state.current_realm = realm_key
                st.session_state.show_question = False
                st.session_state.question_answered = False
                st.rerun()

def show_chapter_selection(questions_df, realm_key):
    """Display chapter selection with 89% pass threshold system"""
    realm_info = ADVENTURE_REALMS[realm_key]
    
    st.markdown(f"""
    <div class="chapter-heading">
        {realm_info['emoji']} {realm_info['name']}
    </div>
    
    <div class="story-text">
        {realm_info['welcome']}
        
        <br><br>
        
        To master this realm, brave {st.session_state.player_name}, you must achieve at least 89% accuracy 
        in each chapter through dedicated practice and wisdom!
    </div>
    """, unsafe_allow_html=True)
    
    # Show chapters with new progress system
    for difficulty in ['easy', 'medium', 'hard']:
        available_questions = questions_df[
            (questions_df['topic'] == realm_key) & 
            (questions_df['difficulty'] == difficulty)
        ]
        
        if len(available_questions) == 0:
            continue  # Skip chapters with no questions
            
        chapter_stats = st.session_state.chapter_stats[realm_key][difficulty]
        chapter_name = realm_info['difficulty_chapters'][difficulty]
        
        accuracy = calculate_chapter_accuracy(realm_key, difficulty)
        is_passed = is_chapter_passed(realm_key, difficulty)
        total_attempted = chapter_stats['total_questions']
        attempts = chapter_stats['attempts']
        
        # Determine status
        if is_passed:
            status_icon = "🏆"
            status_text = f"MASTERED! ({accuracy:.1f}%)"
            status_color = "#28a745"
            button_disabled = False
        elif total_attempted >= 10 and accuracy < 89:
            status_icon = "📚"
            status_text = f"Needs Practice ({accuracy:.1f}% - Try Again!)"
            status_color = "#ffc107"
            button_disabled = False
        elif total_attempted > 0:
            status_icon = "⚡"
            status_text = f"In Progress ({total_attempted}/10 questions, {accuracy:.1f}%)"
            status_color = "#17a2b8"
            button_disabled = False
        else:
            status_icon = "🔮"
            status_text = "Ready to Begin Adventure"
            status_color = "#6f42c1"
            button_disabled = False
        
        col1, col2 = st.columns([3, 1])
        with col1:
            chapter_button_text = f"{status_icon} {chapter_name}\n{status_text}"
            if attempts > 1:
                chapter_button_text += f"\n(Attempt #{attempts})"
            
            if st.button(
                chapter_button_text,
                key=f"chapter_{realm_key}_{difficulty}",
                use_container_width=True,
                disabled=button_disabled
            ):
                st.session_state.current_chapter = difficulty
                st.session_state.show_question = True
                st.session_state.question_answered = False
                
                # Generate new shuffled question set for this attempt
                st.session_state.current_question_set = get_chapter_questions(
                    questions_df, realm_key, difficulty, max_questions=10
                )
                st.session_state.current_question_idx = 0
                
                # Increment attempt counter
                st.session_state.chapter_stats[realm_key][difficulty]['attempts'] += 1
                
                st.rerun()
        
        with col2:
            # Progress indicator
            if total_attempted > 0:
                progress_value = min(total_attempted / 10, 1.0)
                st.progress(progress_value, text=f"{total_attempted}/10")
    
    # Show realm mastery status
    if is_realm_mastered(realm_key, questions_df):
        st.success("� **REALM MASTERED!** 🎉\nYou have achieved mastery in all chapters of this realm!")
        st.session_state.mastered_realms.add(realm_key)
    
    # Back button
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    if st.button("🏠 Return to Realm Selection"):
        st.session_state.current_realm = None
        st.rerun()

def show_adventure_question(questions_df, realm_key, difficulty):
    """Display questions using new 89% threshold system"""
    realm_info = ADVENTURE_REALMS[realm_key]
    chapter_name = realm_info['difficulty_chapters'][difficulty]
    
    # Get current question set (shuffled when chapter was started)
    if not hasattr(st.session_state, 'current_question_set') or not st.session_state.current_question_set:
        st.error("No questions loaded! Please return to chapter selection.")
        return
    
    current_question_idx = st.session_state.current_question_idx
    chapter_stats = st.session_state.chapter_stats[realm_key][difficulty]
    
    # Check if we've completed 10 questions
    if current_question_idx >= len(st.session_state.current_question_set) or chapter_stats['total_questions'] >= 10:
        show_chapter_results(realm_key, difficulty, questions_df)
        return
    
    current_question = st.session_state.current_question_set[current_question_idx]
    
    # Story introduction
    if not st.session_state.show_question:
        st.session_state.show_question = True
        st.session_state.question_answered = False
    
    story_intro = generate_story_intro(realm_key, difficulty)
    st.markdown(f"""
    <div class="chapter-heading">
        {realm_info['emoji']} {chapter_name} - Question {current_question_idx + 1}/10
    </div>
    
    <div class="story-text">
        {story_intro}
    </div>
    """, unsafe_allow_html=True)
    
    # Question presentation
    question_story = generate_question_story(current_question['question'], realm_key, difficulty)
    
    st.markdown(f"""
    <div class="question-box">
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            {question_story}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    progress = (current_question_idx + 1) / 10
    st.progress(progress, text=f"Chapter Progress: {current_question_idx + 1}/10 questions")
    
    # Answer options
    if not st.session_state.question_answered:
        options = [
            current_question['option_a'],
            current_question['option_b'],
            current_question['option_c'],
            current_question['option_d']
        ]
        
        correct_answer = current_question['correct_answer']
        correct_index = ord(correct_answer) - ord('A')
        
        st.markdown("**Choose your answer, brave explorer:**")
        
        for i, option in enumerate(options):
            if st.button(f"{chr(65+i)}) {option}", key=f"option_{i}", use_container_width=True):
                is_correct = (i == correct_index)
                
                # Update chapter statistics
                chapter_stats['total_questions'] += 1
                if is_correct:
                    chapter_stats['correct_answers'] += 1
                    xp_earned = get_xp_for_correct_answer()
                    award_xp(xp_earned, "Correct Answer")
                    st.session_state.quest_streak += 1
                else:
                    st.session_state.quest_streak = 0
                
                # Recalculate accuracy
                chapter_stats['accuracy'] = (chapter_stats['correct_answers'] / chapter_stats['total_questions']) * 100
                
                # Record answer
                st.session_state.answers_log.append({
                    'realm': realm_key,
                    'difficulty': difficulty,
                    'question': current_question['question'],
                    'selected_answer': chr(65+i),
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'timestamp': datetime.now()
                })
                
                st.session_state.question_answered = True
                st.session_state.last_answer_correct = is_correct
                
                # Save progress
                save_adventure_progress()
                st.rerun()
    
    else:
        # Show result and story continuation
        success_story = generate_success_story(realm_key, st.session_state.last_answer_correct)
        
        if st.session_state.last_answer_correct:
            st.success(success_story)
        else:
            st.info(success_story)
        
        # Continue button
        if st.button("➡️ Continue the Adventure!", use_container_width=True):
            st.session_state.current_question_idx += 1
            st.session_state.question_answered = False
            st.session_state.show_question = False
            st.rerun()
    
    # Navigation
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    if st.button("🔙 Return to Chapter Selection"):
        st.session_state.show_question = False
        st.session_state.question_answered = False
        st.session_state.current_chapter = None
        st.rerun()

def show_chapter_results(realm_key, difficulty, questions_df):
    """Show chapter completion results with 89% threshold evaluation"""
    realm_info = ADVENTURE_REALMS[realm_key]
    chapter_name = realm_info['difficulty_chapters'][difficulty]
    chapter_stats = st.session_state.chapter_stats[realm_key][difficulty]
    
    accuracy = chapter_stats['accuracy']
    total_questions = chapter_stats['total_questions']
    correct_answers = chapter_stats['correct_answers']
    is_passed = is_chapter_passed(realm_key, difficulty)
    
    st.markdown("""
    <div class="chapter-heading">
        📊 Chapter Results
    </div>
    """, unsafe_allow_html=True)
    
    # Show results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Completed", f"{total_questions}/10")
    with col2:
        st.metric("Correct Answers", correct_answers)
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    # Pass/Fail evaluation with adventure messaging
    if is_passed:
        # Chapter passed!
        st.balloons()
        chapter_stats['passed'] = True
        
        # Award XP
        xp_reward = get_xp_for_chapter_pass()
        award_xp(xp_reward, f"Chapter Mastery: {chapter_name}")
        
        encouragement = generate_encouragement_message(realm_key, accuracy, True)
        st.success(encouragement)
        
        st.success(f"🎉 **+{xp_reward} XP Awarded for Chapter Mastery!** 🎉")
        
        # Check if realm is now mastered
        if is_realm_mastered(realm_key, questions_df):
            st.session_state.mastered_realms.add(realm_key)
            realm_xp = get_xp_for_realm_mastery()
            award_xp(realm_xp, f"Realm Mastery: {realm_info['name']}")
            
            st.success(f"""
            🏆 **REALM MASTERY ACHIEVED!** 🏆
            
            You have completely mastered {realm_info['name']}!
            The {realm_info['mentor']} bows with deep respect for your linguistic prowess!
            
            💎 **Realm Mastery Bonus: +{realm_xp} XP!** 💎
            """)
    else:
        # Need more practice
        encouragement = generate_encouragement_message(realm_key, accuracy, False)
        st.info(encouragement)
        
        st.info(f"""
        📚 **Practice Makes Perfect!** 📚
        
        You achieved {accuracy:.1f}% accuracy - keep practicing to reach the 89% mastery threshold!
        Every great explorer faces challenges on their journey to wisdom.
        
        Return when you feel ready to strengthen your skills!
        """)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            # Reset for new attempt
            st.session_state.current_question_idx = 0
            st.session_state.show_question = False
            st.session_state.question_answered = False
            
            # Generate new shuffled questions
            st.session_state.current_question_set = get_chapter_questions(
                questions_df, realm_key, difficulty, max_questions=10
            )
            
            # Increment attempt counter
            st.session_state.chapter_stats[realm_key][difficulty]['attempts'] += 1
            
            # Reset stats for new attempt
            st.session_state.chapter_stats[realm_key][difficulty].update({
                'correct_answers': 0,
                'total_questions': 0,
                'accuracy': 0
            })
            
            st.rerun()
    
    with col2:
        if st.button("🏠 Return to Chapter Selection", use_container_width=True):
            st.session_state.current_chapter = None
            st.session_state.show_question = False
            st.session_state.question_answered = False
            st.rerun()

    st.markdown("---")
    </div>
    
    <div class="story-text">
        {story_intro}
    </div>
    """, unsafe_allow_html=True)
    
    # Question presentation
    question_story = generate_question_story(current_question['question'], realm_key, difficulty)
    
    st.markdown(f"""
    <div class="question-box">
        <div style="font-size: 1.2rem; margin-bottom: 1rem;">
            {question_story}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    if not st.session_state.question_answered:
        options = [
            current_question['option_a'],
            current_question['option_b'],
            current_question['option_c'],
            current_question['option_d']
        ]
        
        correct_answer = current_question['correct_answer']
        correct_index = ord(correct_answer) - ord('A')
        
        st.markdown("**Choose your answer, brave explorer:**")
        
        for i, option in enumerate(options):
            if st.button(f"{chr(65+i)}) {option}", key=f"option_{i}", use_container_width=True):
                is_correct = (i == correct_index)
                
                # Record answer
                st.session_state.answers_log.append({
                    'realm': realm_key,
                    'difficulty': difficulty,
                    'question': current_question['question'],
                    'selected_answer': chr(65+i),
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'timestamp': datetime.now()
                })
                
                # Update progress and scores
                if is_correct:
                    st.session_state.adventure_points += 10
                    st.session_state.quest_streak += 1
                else:
                    st.session_state.quest_streak = 0
                
                # Progress is automatically tracked when question is added to questions_taken list
                # No need to manually increment progress counter
                st.session_state.question_answered = True
                st.session_state.last_answer_correct = is_correct
                
                # Save progress
                save_adventure_progress()
                st.rerun()
    
    else:
        # Show result and story continuation
        success_story = generate_success_story(realm_key, st.session_state.last_answer_correct)
        
        if st.session_state.last_answer_correct:
            st.success(success_story)
        else:
            st.info(success_story)
        
        # Continue button
        if st.button("➡️ Continue the Adventure!", use_container_width=True):
            st.session_state.question_answered = False
            st.session_state.show_question = False
            st.rerun()
    
    # 🎨 Super cool progress indicator
    total_questions = len(st.session_state.current_question_set)
    questions_completed = current_question_idx + (1 if st.session_state.question_answered else 0)
    progress = questions_completed / total_questions if total_questions > 0 else 0
    
    # Progress visualization with gradient
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f4f1e8, #e8dcc0);
        border: 2px solid #cd853f;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    ">
        <h4 style="color: #654321; margin-bottom: 15px; font-family: 'Cinzel Decorative', cursive;">
            ⚡ Chapter Progress ⚡
        </h4>
        <p style="font-size: 1.2rem; font-weight: 600; color: #2c1810; margin-bottom: 15px;">
            Question {questions_completed} of {total_questions} • {int(progress * 100)}% Complete
        </p>
        <div style="background: rgba(0,0,0,0.1); border-radius: 15px; height: 15px; margin: 0 auto; max-width: 300px;">
            <div style="
                background: linear-gradient(90deg, #cd853f, #daa520, #ffd700);
                height: 15px;
                border-radius: 15px;
                width: {progress * 100}%;
                transition: all 0.8s ease;
                box-shadow: 0 2px 10px rgba(205, 133, 63, 0.4);
            "></div>
        </div>
        <p style="font-style: italic; color: #8b6f47; margin-top: 10px;">
            {"🎉 Chapter nearly complete!" if progress > 0.8 else "Keep exploring, brave adventurer!" if progress > 0.5 else "The journey begins!"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown('<div class="ornament">⚡ ✨ 🌟 ✨ ⚡</div>', unsafe_allow_html=True)
    if st.button("🔙 Return to Chapter Selection"):
        st.session_state.show_question = False
        st.session_state.question_answered = False
        st.session_state.current_chapter = None
        st.rerun()

def show_chapter_completion(realm_key, difficulty, questions_df):
    """Show chapter completion celebration"""
    realm_info = ADVENTURE_REALMS[realm_key]
    chapter_name = realm_info['difficulty_chapters'][difficulty]
    
    st.markdown("""
    <div class="chapter-heading">
        🎉 Chapter Complete! 🎉
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"""
    🌟 **Congratulations, {st.session_state.player_name}!** 🌟
    
    You have successfully conquered {chapter_name} in {realm_info['name']}!
    
    Your wisdom grows stronger with each challenge overcome!
    
    ⭐ **Chapter Bonus: +50 Adventure Points!** ⭐
    """)
    
    # Award bonus points
    if f"{realm_key}_{difficulty}_bonus" not in st.session_state:
        st.session_state.adventure_points += 50
        st.session_state[f"{realm_key}_{difficulty}_bonus"] = True
        save_adventure_progress()
    
    # Check if realm is completed (with 10-question limit)
    realm_progress = st.session_state.realm_progress[realm_key]
    total_chapters = sum(1 for diff in ['easy', 'medium', 'hard'] 
                        if len(questions_df[(questions_df['topic'] == realm_key) & 
                                          (questions_df['difficulty'] == diff)].head(10)) > 0)  # 🎯 10-question limit
    completed_chapters = sum(1 for diff in ['easy', 'medium', 'hard']
                           if realm_progress[diff] > 0 and 
                           len(questions_df[(questions_df['topic'] == realm_key) & 
                                          (questions_df['difficulty'] == diff)].head(10)) <= realm_progress[diff])  # 🎯 10-question limit
    
    if completed_chapters >= total_chapters:
        st.session_state.completed_realms.add(realm_key)
        st.balloons()
        
        st.markdown(f"""
        <div class="success-message" style="text-align: center; font-size: 1.4rem;">
            <p>🏆 REALM MASTERY ACHIEVED! 🏆</p>
            
            <p style="margin-top: 20px;">You have completely mastered {realm_info['name']}!<br>
            The {realm_info['mentor']} bows with deep respect for your linguistic prowess!</p>
            
            <p style="margin-top: 20px;">💎 Realm Mastery Bonus: +100 Adventure Points! 💎</p>
        </div>
        """, unsafe_allow_html=True)
        
        if f"{realm_key}_realm_bonus" not in st.session_state:
            st.session_state.adventure_points += 100
            st.session_state[f"{realm_key}_realm_bonus"] = True
            save_adventure_progress()
    
    # Navigation options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Return to Chapter Selection", use_container_width=True):
            st.session_state.show_question = False
            st.session_state.current_chapter = None
            st.rerun()
    
    with col2:
        if st.button("🏠 Return to Realm Selection", use_container_width=True):
            st.session_state.current_realm = None
            st.session_state.show_question = False
            st.rerun()

def show_adventure_analytics():
    """Show Alex's Adventure Journal (analytics dashboard)"""
    st.markdown("""
    <div class="chapter-heading">
        📜 Alex's Adventure Journal
    </div>
    
    <div class="story-text">
        Let us examine the chronicles of your brave exploits, {name}! 
        Each challenge faced and every triumph achieved has been carefully recorded 
        in this magical journal...
    </div>
    """.format(name=st.session_state.player_name), unsafe_allow_html=True)
    
    if not st.session_state.answers_log:
        st.info("📖 Your adventure journal awaits the first entry! Begin exploring to see your progress here.")
        return
    
    # Convert answers to DataFrame for analysis
    answers_df = pd.DataFrame(st.session_state.answers_log)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="analytics-scroll">
            <h4>🏆 Adventure Statistics</h4>
        </div>
        """, unsafe_allow_html=True)
        
        total_questions = len(answers_df)
        correct_answers = len(answers_df[answers_df['is_correct']])
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        st.metric("📚 Total Challenges", total_questions)
        st.metric("✅ Successful Solutions", correct_answers)
        st.metric("🎯 Adventure Accuracy", f"{accuracy:.1f}%")
        st.metric("🌟 Adventure Points", st.session_state.adventure_points)
    
    with col2:
        st.markdown("""
        <div class="analytics-scroll">
            <h4>🗺️ Realm Progress</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Create realm progress chart
        realm_stats = answers_df.groupby('realm')['is_correct'].agg(['count', 'sum']).reset_index()
        realm_stats.columns = ['Realm', 'Total', 'Correct']
        realm_stats['Accuracy'] = (realm_stats['Correct'] / realm_stats['Total'] * 100).round(1)
        
        # Map realm keys to display names
        realm_stats['Display_Name'] = realm_stats['Realm'].map(
            lambda x: ADVENTURE_REALMS[x]['name'] if x in ADVENTURE_REALMS else x
        )
        
        if len(realm_stats) > 0:
            fig = px.bar(
                realm_stats, 
                x='Display_Name', 
                y='Accuracy',
                title='📊 Mastery by Realm',
                color='Accuracy',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                paper_bgcolor='rgba(255,248,240,0.8)',
                plot_bgcolor='rgba(255,248,240,0.8)',
                font_family="Crimson Text"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ML Model Insights (Alex's Wise Mentor Guidance)
    model, topics = load_adventure_model()
    if model is not None and len(answers_df) >= 5:
        st.markdown("""
        <div class="analytics-scroll">
            <h4>🔮 The Wise Mentor's Guidance</h4>
            <p><em>Ancient wisdom reveals patterns in your learning journey...</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Prepare data for ML model
            realm_scores = {}
            for realm in ADVENTURE_REALMS.keys():
                realm_answers = answers_df[answers_df['realm'] == realm]
                if len(realm_answers) > 0:
                    realm_scores[realm] = realm_answers['is_correct'].mean() * 100
                else:
                    realm_scores[realm] = 70  # Default score
            
            # Create feature vector (same format as training)
            feature_vector = [realm_scores.get(topic, 70) for topic in topics] + [15]  # Add time_spent
            
            # Get prediction
            prediction = model.predict([feature_vector])[0]
            probabilities = model.predict_proba([feature_vector])[0]
            
            predicted_weakness = topics[prediction]
            confidence = max(probabilities) * 100
            
            weakness_realm = ADVENTURE_REALMS.get(predicted_weakness, {}).get('name', predicted_weakness)
            
            st.info(f"""
            🔮 **The Ancient Oracle Speaks:**
            
            "Young {st.session_state.player_name}, the magical currents suggest focusing your next adventures 
            in the realm of **{weakness_realm}**. The spirits whisper with {confidence:.1f}% certainty 
            that great treasures of knowledge await you there!"
            
            *Remember, every great explorer has areas to strengthen - this is the path to true mastery!*
            """)
            
        except Exception:
            st.info("🔮 The Oracle's crystal ball grows cloudy... More adventures needed for clearer visions!")

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application function"""
    # Initialize adventure
    initialize_adventure()
    
    # Load data
    questions_df = load_adventure_data()
    if questions_df is None:
        st.stop()
    
    # Show title
    show_adventure_title()
    
    # Navigation logic
    if not st.session_state.player_name:
        show_player_introduction()
    
    elif st.session_state.current_realm is None:
        # Create sidebar navigation
        with st.sidebar:
            st.markdown("### 🧭 Adventure Navigation")
            if st.button("📜 Adventure Journal", use_container_width=True):
                st.session_state.show_analytics = not st.session_state.get('show_analytics', False)
            
            if st.button("🔄 New Adventure", use_container_width=True):
                # Reset adventure
                for key in list(st.session_state.keys()):
                    if key.startswith(('adventure_', 'current_', 'realm_', 'answers_', 'show_', 'question_', 'last_')):
                        del st.session_state[key]
                st.rerun()
        
        # Show analytics if requested
        if st.session_state.get('show_analytics', False):
            show_adventure_analytics()
        else:
            show_realm_selection(questions_df)
    
    elif st.session_state.current_chapter is None:
        show_chapter_selection(questions_df, st.session_state.current_realm)
    
    else:
        show_adventure_question(questions_df, st.session_state.current_realm, st.session_state.current_chapter)

if __name__ == "__main__":
    main()