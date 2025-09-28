# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os
import random

def load_questions_dataset():
    """Load and analyze the manabifun_questions.csv dataset"""
    print("📚 Loading manabifun_questions.csv dataset...")
    
    questions_df = pd.read_csv("data/manabifun_questions.csv")
    print(f"✅ Loaded {len(questions_df)} questions from dataset")
    
    # Analyze dataset structure
    topics = questions_df['topic'].unique()
    print(f"📊 Topics found: {list(topics)}")
    
    for topic in topics:
        count = len(questions_df[questions_df['topic'] == topic])
        print(f"  - {topic}: {count} questions")
    
    return questions_df

def create_training_data_from_csv():
    """Create training data based on the actual CSV dataset structure"""
    np.random.seed(42)
    random.seed(42)
    
    # Load the questions dataset
    questions_df = load_questions_dataset()
    
    # Get unique topics and create label encoding
    topics = questions_df['topic'].unique()
    topic_to_idx = {topic: idx for idx, topic in enumerate(topics)}
    print(f"🏷️ Topic mapping: {topic_to_idx}")
    
    # Features: [grammar_score, articles_score, synonyms_score, antonyms_score, sentences_score, time_spent]
    # Labels: topic index based on weakness
    
    data = []
    labels = []
    
    # Generate synthetic training data that reflects realistic student performance patterns
    for _ in range(2000):  # Increased dataset size for better training
        # Select a random topic as the weakness
        weak_topic_idx = random.randint(0, len(topics) - 1)
        
        # Base scores (50-90 range for more realistic distribution)
        scores = np.random.normal(70, 12, len(topics))
        scores = np.clip(scores, 30, 95)
        
        # Significantly weaken the selected skill (weakness area)
        scores[weak_topic_idx] = np.random.normal(40, 8)
        scores[weak_topic_idx] = np.clip(scores[weak_topic_idx], 20, 65)
        
        # Time spent varies based on difficulty and weakness
        base_time = np.random.normal(15, 4)
        if weak_topic_idx == 0:  # Grammar typically takes longer
            base_time += np.random.normal(5, 2)
        
        time_spent = max(5, base_time)  # Minimum 5 minutes
        
        # Create feature vector
        feature_row = list(scores) + [time_spent]
        data.append(feature_row)
        labels.append(weak_topic_idx)
    
    print(f"✅ Generated {len(data)} training samples")
    return np.array(data), np.array(labels), topics

def train_weakness_detector():
    """Train the ML model to detect student weaknesses using CSV dataset"""
    print("🤖 Training weakness detection model...")
    X, y, topics = create_training_data_from_csv()
    
    print("🔄 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("📊 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        class_weight='balanced'  # Handle class imbalance
    )
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"✅ Model accuracy: {accuracy:.2%}")
    
    # Feature importance analysis
    feature_names = list(topics) + ['time_spent']
    importance_dict = dict(zip(feature_names, model.feature_importances_))
    print("📈 Feature importance:")
    for feature, importance in sorted(importance_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {feature}: {importance:.3f}")
    
    # Save model and topic mapping
    model_data = {
        'model': model,
        'topics': topics,
        'topic_to_idx': {topic: idx for idx, topic in enumerate(topics)},
        'feature_names': feature_names
    }
    
    with open("models/weakness_detector.pkl", "wb") as f:
        pickle.dump(model_data, f)
    
    print("💾 Model saved to models/weakness_detector.pkl")
    return model, topics

def create_enhanced_questions_csv():
    """Create an enhanced questions CSV dataset with proper structure and DISTINCT options"""
    print("📚 Creating enhanced questions dataset with properly distinct options...")
    
    # Enhanced question set with CLEARLY DIFFERENT options
    questions = [
        # Grammar questions - FIXED to have distinct options
        ("grammar", "What is the correct negative form of 'I am happy'?", "I am not happy", "I not happy", "I don't happy", "I am no happy", "A", "easy"),
        ("grammar", "Choose the plural form of 'child':", "childs", "children", "childes", "child", "B", "medium"),
        ("grammar", "What is the past tense of 'run'?", "runned", "ran", "run", "running", "B", "easy"),
        ("grammar", "Which sentence is correct?", "She don't like pizza", "She doesn't like pizza", "She not like pizza", "She no like pizza", "B", "easy"),
        ("grammar", "Choose the correct form: 'There ___ many books'", "is", "are", "was", "be", "B", "easy"),
        ("grammar", "What is the correct question form?", "Do you like music?", "You like music?", "Like you music?", "You do like music?", "A", "medium"),
        ("grammar", "Which is the correct comparative?", "more good", "better", "gooder", "best", "B", "medium"),
        ("grammar", "Choose the correct possessive:", "The dog's tail", "The dogs tail", "The dog tail's", "The dogs' tail", "A", "easy"),
        ("grammar", "What is the correct present continuous?", "I am work", "I am working", "I working", "I work am", "B", "easy"),
        ("grammar", "Which modal verb fits: 'You ___ study hard'?", "should", "can", "will", "must", "A", "medium"),
        
        # Articles questions - IMPROVED with clearer distinctions
        ("articles", "Fill in the blank: '___ apple is red'", "A", "An", "The", "No article", "B", "easy"),
        ("articles", "Choose the correct article: '___ university'", "A", "An", "The", "No article", "A", "medium"),
        ("articles", "Which is correct for a specific book you both know?", "I need a book", "I need an book", "I need the book", "I need books", "C", "medium"),
        ("articles", "___ sun rises in the east", "A", "An", "The", "No article", "C", "easy"),
        ("articles", "She is ___ honest person", "a", "an", "the", "no article", "B", "medium"),
        ("articles", "I saw ___ elephant at the zoo", "a", "an", "the", "some", "B", "easy"),
        ("articles", "Can you pass me ___ salt on the table?", "a", "an", "the", "some", "C", "easy"),
        ("articles", "He wants to be ___ engineer", "a", "an", "the", "one", "B", "medium"),
        ("articles", "___ water is essential for life", "A", "An", "The", "No article", "D", "medium"),
        ("articles", "I'm going to ___ hospital to visit someone", "a", "an", "the", "no article", "C", "medium"),
        
        # Synonyms questions - IMPROVED with clearer distinctions
        ("synonyms", "What is a synonym for 'happy'?", "sad", "joyful", "angry", "worried", "B", "easy"),
        ("synonyms", "Which word means the same as 'big'?", "small", "large", "tiny", "thin", "B", "easy"),
        ("synonyms", "What is a synonym for 'quick'?", "slow", "fast", "heavy", "careful", "B", "easy"),
        ("synonyms", "Which word is similar to 'beautiful'?", "ugly", "lovely", "strange", "plain", "B", "easy"),
        ("synonyms", "What means the same as 'intelligent'?", "stupid", "smart", "confused", "ignorant", "B", "medium"),
        ("synonyms", "Choose a synonym for 'difficult':", "easy", "hard", "simple", "soft", "B", "medium"),
        ("synonyms", "What word is similar to 'ancient'?", "new", "old", "modern", "young", "B", "medium"),
        ("synonyms", "Pick a synonym for 'courageous':", "scared", "brave", "weak", "nervous", "B", "medium"),
        ("synonyms", "Which means the same as 'wealthy'?", "poor", "rich", "hungry", "sick", "B", "medium"),
        ("synonyms", "Choose a synonym for 'exhausted':", "energetic", "tired", "excited", "healthy", "B", "easy"),
        
        # Antonyms questions - IMPROVED with unambiguous opposites
        ("antonyms", "What is the opposite of 'hot'?", "warm", "cold", "cool", "mild", "B", "easy"),
        ("antonyms", "What is the opposite of 'tall'?", "high", "short", "long", "big", "B", "easy"),
        ("antonyms", "Choose the opposite of 'happy':", "glad", "sad", "excited", "cheerful", "B", "early"),
        ("antonyms", "What is the opposite of 'bright' (light)?", "dim", "dark", "shiny", "clear", "B", "easy"),
        ("antonyms", "Choose the opposite of 'new':", "fresh", "old", "clean", "modern", "B", "easy"),
        ("antonyms", "What's the opposite of 'loud'?", "noisy", "quiet", "sound", "voice", "B", "easy"),
        ("antonyms", "Choose the opposite of 'fast':", "quick", "slow", "rapid", "swift", "B", "easy"),
        ("antonyms", "What's the opposite of 'empty'?", "vacant", "full", "hollow", "bare", "B", "easy"),
        ("antonyms", "Pick the opposite of 'strong':", "powerful", "weak", "tough", "solid", "B", "easy"),
        ("antonyms", "Choose the opposite of 'up':", "down", "high", "top", "above", "A", "easy"),
        
        # Sentence Structure questions - FIXED
        ("sentences", "Which sentence is correct?", "The dog run fast", "The dog runs fast", "The dog running fast", "The dog ran fastly", "B", "medium"),
        ("sentences", "Choose the correct sentence:", "I have go to school", "I has go to school", "I have gone to school", "I have went to school", "C", "medium"),
        ("sentences", "Which is grammatically correct?", "Me and John went", "John and me went", "John and I went", "I and John went", "C", "medium"),
        ("sentences", "Select the proper sentence:", "She don't know", "She doesn't knows", "She doesn't know", "She not know", "C", "easy"),
        ("sentences", "Which sentence is right?", "I can sings well", "I can sing well", "I can sang well", "I can singing well", "B", "easy"),
        ("sentences", "Choose the correct word order:", "Always I am happy", "I always am happy", "I am always happy", "I am happy always", "C", "medium"),
        ("sentences", "Which sentence uses correct tense?", "I will went tomorrow", "I will go tomorrow", "I will going tomorrow", "I will be went tomorrow", "B", "medium"),
        ("sentences", "Pick the grammatically correct sentence:", "There is five cats", "There are five cats", "There be five cats", "There have five cats", "B", "easy"),
        ("sentences", "Which sentence is properly formed?", "What you doing?", "What are you doing?", "What you are doing?", "You what doing?", "B", "easy"),
        ("sentences", "Choose the correct conditional:", "If I was rich, I buy a car", "If I were rich, I would buy a car", "If I am rich, I will bought a car", "If I be rich, I buying a car", "B", "hard"),
    ]
    
    df = pd.DataFrame(questions, columns=[
        "topic", "question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "difficulty"
    ])
    
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/manabifun_questions.csv", index=False)
    print(f"📚 Enhanced questions dataset saved with {len(df)} questions")
    
    # Display statistics
    for topic in df['topic'].unique():
        count = len(df[df['topic'] == topic])
        print(f"  - {topic}: {count} questions")
    
    return df

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    print("🚀 Starting ManabiFun ML Training...")
    
    # Step 1: Always create a fresh, corrected dataset
    print("📚 Creating corrected questions dataset with distinct options...")
    create_enhanced_questions_csv()
    
    # Step 2: Train weakness detection model using the CSV data
    model, topics = train_weakness_detector()
    
    print("✅ Setup complete! Ready to run the Streamlit app.")
    print("🎯 Shuffling Algorithm: Fisher-Yates shuffle implemented in quiz selection")
    print("📊 Model trained on student performance patterns from question topics")
    print("\n🔧 FIXED: All questions now have clearly distinct options!")
    print("✅ No more 'I am not happy' vs 'I'm not happy' confusion!")
