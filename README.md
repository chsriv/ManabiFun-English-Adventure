# 🌸 ManabiFun - English Learning Adventure

> **Your AI-Powered English Learning Companion with Duolingo-Style Experience**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 **What is ManabiFun?**

ManabiFun is an **AI-powered English learning platform** that combines the engaging experience of Duolingo with advanced machine learning to create personalized learning paths. The app features:

- 🏝️ **Island-based progression system** (like Duolingo)
- 🤖 **AI weakness detection** using Random Forest ML
- 🔀 **Fisher-Yates shuffle algorithm** for fair question randomization
- 📊 **Real-time progress tracking** with XP, streaks, and levels
- 🎯 **Adaptive difficulty** based on performance
- 📚 **TOEFL preparation support** for advanced learners

---

## 🚀 **Quick Start**

### **1. Installation**
```bash
# Clone the repository
git clone https://github.com/your-username/ManabiFun.git
cd ManabiFun

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### **2. Train the AI Model**
```bash
python train_model.py
```

### **3. Launch the App**
```bash
streamlit run app.py
```

### **4. Open in Browser**
Navigate to `http://localhost:8501` and start learning!

---

## 🎮 **User Interface & Experience (UI/UX)**

### **🏠 Home Screen & Student Login**

```
┌─────────────────────────────────────────────────────────┐
│  🌸 ManabiFun - English Learning Adventure 🌸           │
│  Master English like a Pro - From Basics to TOEFL!     │
│                                                         │
│  🎭 Enter your name: [________________] [Start]         │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Simple name-based login (no complex authentication)
- Immediate access to learning content
- Persistent progress tracking per student

---

### **📊 Student Dashboard**

```
┌─────────────────────────────────────────────────────────┐
│  Welcome back, Alex! 👋                                │
│                                                         │
│  💎 1,250 XP    🔥 7 Day Streak    🏆 3 Islands    ⭐ Lvl 13 │
│                                                         │
│  📈 Progress Overview:                                  │
│  ████████░░ 80% Grammar Complete                       │
│  ██████░░░░ 60% Articles Complete                      │
│  ████░░░░░░ 40% Synonyms Complete                      │
└─────────────────────────────────────────────────────────┘
```

**Dashboard Elements:**
- **XP (Experience Points)**: 10 XP per correct answer + bonus for streaks
- **Streak Counter**: Daily learning streak motivation
- **Islands Completed**: Visual progress indicator
- **Level System**: Automatic level-up every 100 XP
- **Progress Bars**: Topic-specific completion tracking

---

### **🗺️ Island Selection Screen**

```
┌─────────────────────────────────────────────────────────┐
│  🗺️ Choose Your Learning Island                         │
│                                                         │
│  [🏝️ Grammar Island]     [🏖️ Articles Beach]           │
│   ✅ Completed             🎯 Available                 │
│                                                         │
│  [🌴 Synonyms Jungle]    [🗻 Antonyms Mountain]         │
│   🎯 Available             🔒 Locked                    │
│                                                         │
│  [🏰 Sentence Castle]    [📚 TOEFL Reading]            │
│   🔒 Locked               🔒 Locked                     │
└─────────────────────────────────────────────────────────┘
```

**Island System:**
- **Progressive Unlocking**: Complete previous island with 70%+ score
- **Visual Status Indicators**: ✅ Completed, 🎯 Available, 🔒 Locked
- **Theme-based Learning**: Each island focuses on specific English skills
- **Motivation**: "🎊 New Island Unlocked!" celebrations

---

### **📚 Topic Rules & Basics Screen**

```
┌─────────────────────────────────────────────────────────┐
│  🏝️ Grammar Island                                      │
│                                                         │
│  📝 Grammar Basics                                      │
│  🔹 Subject-Verb Agreement: The subject and verb must   │
│     agree in number                                     │
│  🔹 Tenses: Past, Present, Future - choose the right    │
│     time frame                                          │
│  🔹 Pronouns: I, me, my, mine - use the correct form    │
│  🔹 Plurals: Add -s or -es for most nouns, some are     │
│     irregular                                           │
│                                                         │
│  Choose difficulty: [Easy ▼] [Medium] [Hard]           │
│                                                         │
│  🎯 Quiz Rules                                          │
│  - Answer 10 questions                                  │
│  - Score 70%+ to unlock next island                    │
│  - Earn 10 XP per correct answer                       │
│                                                         │
│  [🚀 Start Grammar Island Quiz!]                       │
└─────────────────────────────────────────────────────────┘
```

**Pre-Quiz Features:**
- **Learning Rules**: Key concepts explained before testing
- **Difficulty Selection**: Easy, Medium, Hard progression
- **Clear Expectations**: Quiz format and success criteria
- **Motivational Design**: Island-themed presentation

---

### **❓ Quiz Interface**

```
┌─────────────────────────────────────────────────────────┐
│  🏝️ Grammar Island Quiz                                 │
│                                                         │
│  Question 3 of 10                                       │
│  ████████░░ 80% Complete                               │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Q3: What is the correct negative form of            │ │
│  │     'I am happy'?                                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  Select your answer:                                    │
│  ○ I am not happy                                      │
│  ○ I not happy                                         │
│  ○ I don't happy                                       │
│  ○ I am no happy                                       │
│                                                         │
│  [⬅️ Previous]                [Next ➡️]                  │
│                                                         │
│  Score: 2/2                                            │
└─────────────────────────────────────────────────────────┘
```

**Quiz Features:**
- **Progress Bar**: Visual completion tracking
- **Question Counter**: Current position in quiz
- **Clear Options**: Each answer tests different concepts
- **Navigation**: Back/forward through questions
- **Live Scoring**: Real-time correct answer tracking

---

### **🎉 Quiz Results Screen**

```
┌─────────────────────────────────────────────────────────┐
│  🎉 Congratulations! Island Completed!                  │
│                                                         │
│  🎊 🌴 Synonyms Jungle UNLOCKED! 🎊                     │
│                                                         │
│  📊 Final Score: 8/10  │  📈 Percentage: 80.0%          │
│  💎 XP Earned: +80 XP  │  🔥 Streak: 8 days            │
│                                                         │
│  📝 Review Your Mistakes                                │
│  ▶ Mistake #1                                          │
│    Question: Choose the correct article: '___ honest'   │
│    Your Answer: ❌ a honest                            │
│    Correct Answer: ✅ an honest                        │
│                                                         │
│  ▶ Mistake #2                                          │
│    Question: What is a synonym for 'difficult'?        │
│    Your Answer: ❌ easy                                │
│    Correct Answer: ✅ hard                             │
│                                                         │
│  [🔄 Try Again]  [🏠 Back to Islands]                   │
└─────────────────────────────────────────────────────────┘
```

**Results Features:**
- **Celebration Animations**: Balloons, confetti for success
- **Detailed Scoring**: Multiple metrics displayed
- **Mistake Review**: Learn from incorrect answers
- **Next Steps**: Retry or continue to island selection

---

### **🤖 AI Weakness Detection**

```
┌─────────────────────────────────────────────────────────┐
│  📊 Your Progress Analytics                             │
│                                                         │
│  🤖 AI Suggests: Focus more on **Articles**             │
│  📊 Prediction confidence: 87.3%                       │
│                                                         │
│  📈 Performance by Topic:                              │
│   Grammar:   ██████████ 85%                           │
│   Articles:  ████░░░░░░ 45% ← Needs Work              │
│   Synonyms:  ████████░░ 78%                           │
│   Antonyms:  ███████░░░ 72%                           │
│   Sentences: ████████░░ 80%                           │
│                                                         │
│  📅 Weekly Progress:                                    │
│   [Line Chart showing score trends over time]          │
└─────────────────────────────────────────────────────────┘
```

**AI Features:**
- **Smart Recommendations**: ML-powered weakness identification
- **Confidence Scores**: Transparency in AI predictions
- **Visual Analytics**: Charts and graphs for progress tracking
- **Personalized Learning**: Adaptive content suggestions

---

## 🔧 **Technical Architecture**

### **🧠 Machine Learning Pipeline**

```
┌─────────────────────────────────────────────────────────┐
│  📊 Data Flow                                           │
│                                                         │
│  [Student Answers] → [Feature Engineering] → [ML Model] │
│         ↓                      ↓                    ↓    │
│   Raw Quiz Data        Score Patterns        Weakness    │
│                       Time Analysis         Prediction   │
│                                                         │
│  🤖 Random Forest Classifier                            │
│  - 150 estimators (decision trees)                     │
│  - 92.25% accuracy on test data                        │
│  - Features: [topic_scores, time_spent]                │
│  - Output: Predicted weakness area                     │
└─────────────────────────────────────────────────────────┘
```

### **🔀 Fisher-Yates Shuffle Algorithm**

```python
def fisher_yates_shuffle(questions_list):
    """
    Time Complexity: O(n)
    Space Complexity: O(1) - in-place shuffling
    
    Algorithm:
    1. Start from the last element
    2. Generate random index from 0 to current position
    3. Swap current element with randomly selected element
    4. Move to previous element and repeat
    """
    n = len(questions_list)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        questions_list[i], questions_list[j] = questions_list[j], questions_list[i]
    return questions_list
```

### **📊 Question Quality Assurance**

**Before Fix:**
```
❌ Question: "What is the negative form of 'I am happy'?"
   Options: ["I am not happy", "I'm not happy", ...]
   Problem: Both options are essentially the same!
```

**After Fix:**
```
✅ Question: "What is the negative form of 'I am happy'?"
   Options: ["I am not happy", "I not happy", "I don't happy", "I am no happy"]
   Solution: Each option tests different grammar concepts!
```

---

## 📂 **Project Structure**

```
ManabiFun/
├── 📱 app.py                          # Main Streamlit application
├── 🎨 app_enhanced.py                 # Enhanced Duolingo-style UI
├── 🤖 train_model.py                  # ML model training script
├── 📊 create_comprehensive_dataset.py # Dataset expansion tool
├── 📋 requirements.txt                # Python dependencies
├── 📖 README.md                       # This documentation
├── 📊 data/
│   ├── manabifun_questions.csv        # Main question database
│   ├── student_scores.csv             # Quiz results history
│   └── student_progress.csv           # Learning progress tracking
├── 🤖 models/
│   ├── weakness_detector.pkl          # Trained ML model
│   └── weakness_detector.py           # Model utilities
└── 📚 docs/
    └── TOEFL_Dataset_Guide.md         # TOEFL preparation guide
```

---

## 🎯 **Learning Workflow**

### **👤 Student Journey**

```
1. 🎭 Student Login
   ↓
2. 📊 View Dashboard (XP, Streaks, Progress)
   ↓
3. 🗺️ Select Available Island
   ↓
4. 📚 Review Topic Rules & Basics  
   ↓
5. ⚙️ Choose Difficulty Level
   ↓
6. ❓ Take 10-Question Quiz (Fisher-Yates Shuffled)
   ↓
7. 📝 Receive Instant Feedback
   ↓
8. 🎉 View Results & Mistake Review
   ↓
9. 🤖 Get AI-Powered Weakness Analysis
   ↓
10. 🔓 Unlock Next Island (if 70%+ score)
    ↓
11. 🔄 Repeat Process for Continuous Learning
```

### **🎓 Educator Workflow**

```
1. 📊 Monitor Student Progress
   ↓
2. 🤖 Review AI Weakness Reports
   ↓
3. 📚 Identify Common Learning Gaps
   ↓
4. 🎯 Customize Difficulty Levels
   ↓
5. 📈 Track Class Performance Trends
   ↓
6. 🔄 Adjust Teaching Strategies
```

---

## 🚀 **Advanced Features**

### **🎯 Adaptive Difficulty**
- **Dynamic Adjustment**: Questions adapt based on performance
- **Personalized Pacing**: Slower progression for struggling areas
- **Challenge Mode**: Advanced questions for high performers

### **📊 Progress Analytics**
- **Performance Trends**: Weekly/monthly score analysis
- **Time-to-Completion**: Learning efficiency metrics
- **Streak Maintenance**: Motivation through consistency

### **🤖 AI Insights**
- **Learning Pattern Recognition**: Identify optimal study times
- **Weakness Prediction**: Proactive intervention suggestions
- **Content Recommendations**: Personalized learning paths

---

## 🌟 **Gamification Elements**

### **🏆 Achievement System**
- **Island Master**: Complete all questions in a topic
- **Streak Warrior**: Maintain 30-day learning streak
- **Speed Learner**: Complete quizzes under time limit
- **Perfectionist**: Score 100% on 5 consecutive quizzes

### **💎 XP & Leveling**
- **Base XP**: 10 points per correct answer
- **Streak Bonus**: +5 XP for daily consistency
- **Perfect Score**: +20 bonus XP for 100% quiz
- **Level Benefits**: Unlock special themes and features

### **🎨 Visual Rewards**
- **Island Themes**: Unlock new visual styles
- **Avatar Customization**: Personalize your learning character
- **Progress Celebrations**: Animations for milestones

---

## 🔧 **Customization Options**

### **⚙️ For Educators**
```python
# Customize difficulty thresholds
MIN_SCORE_TO_UNLOCK = 70  # Percentage required to advance
QUESTIONS_PER_QUIZ = 10   # Quiz length
XP_PER_CORRECT = 10       # Reward system

# Add custom topics
CUSTOM_TOPICS = {
    "business_english": "Professional Communication",
    "academic_writing": "Essay Composition",
    "pronunciation": "Speaking Practice"
}
```

### **🎨 For UI/UX**
```css
/* Custom color themes */
.island-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Streak badge styling */
.streak-badge {
    background: #FF6B35;
    animation: pulse 2s infinite;
}
```

---

## 📚 **TOEFL Preparation Path**

### **📈 Scaling to TOEFL Level**

**Current Foundation:**
- ✅ Basic English skills (Grammar, Articles, Vocabulary)
- ✅ AI-powered weakness detection
- ✅ Progressive difficulty system

**TOEFL Enhancement Plan:**
1. **Reading Comprehension** (30+ academic passages)
2. **Listening Practice** (Audio-based questions)
3. **Speaking Assessment** (Voice recognition)
4. **Writing Evaluation** (Essay scoring)

**Dataset Sources for TOEFL:**
- ETS Official Practice Tests
- Academic journal articles
- University lecture transcripts
- Standardized test prep materials

---

## 🛠️ **Development & Contribution**

### **🔧 Setup for Development**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black . && flake8 .

# Type checking
mypy app.py
```

### **📊 Add New Questions**
```python
# In train_model.py, add to questions list:
("topic", "question_text", "option_a", "option_b", "option_c", "option_d", "correct_answer", "difficulty")

# Ensure each option tests different concepts!
```

### **🤖 Model Improvements**
```python
# Experiment with different algorithms
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

# Hyperparameter tuning
from sklearn.model_selection import GridSearchCV
```

---

## 📊 **Performance Metrics**

### **🎯 Model Performance**
- **Accuracy**: 92.25% on test data
- **Training Time**: ~30 seconds
- **Prediction Speed**: <0.1 seconds per student
- **Memory Usage**: ~50MB model size

### **📱 App Performance**
- **Load Time**: <3 seconds initial startup
- **Response Time**: <0.5 seconds per interaction
- **Concurrent Users**: Supports 100+ simultaneous learners
- **Data Storage**: Efficient CSV-based progress tracking

---

## 🔐 **Privacy & Security**

### **📊 Data Handling**
- **Student Privacy**: Names only, no sensitive information
- **Local Storage**: All data stored locally by default
- **Progress Tracking**: Anonymized performance metrics
- **GDPR Compliant**: Easy data export/deletion

### **🔒 Security Features**
- **No Authentication Required**: Simplified access
- **Input Validation**: Prevents code injection
- **Secure File Handling**: Protected file operations

---

## 📞 **Support & Community**

### **🆘 Getting Help**
- **Documentation**: Comprehensive guides included
- **Issue Tracker**: GitHub Issues for bug reports
- **Community Forum**: Discord/Slack for discussions
- **Email Support**: Direct developer contact

### **🤝 Contributing**
- **Bug Reports**: Submit detailed issue descriptions
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Follow pull request guidelines
- **Translation**: Help localize for different languages

---

## 🚀 **Future Roadmap**

### **🔮 Version 2.0 Features**
- [ ] **Voice Recognition**: Speaking practice integration
- [ ] **Multi-language Support**: Spanish, French, German options
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Teacher Dashboard**: Classroom management tools
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Social Features**: Student collaboration tools

### **🎯 Long-term Vision**
- **AI Tutoring**: Personalized one-on-one instruction
- **Virtual Reality**: Immersive learning environments
- **Blockchain Certificates**: Verified skill credentials
- **Global Leaderboards**: Worldwide competition system

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Duolingo**: Inspiration for gamified learning
- **ETS**: TOEFL preparation guidance
- **Streamlit**: Amazing web app framework
- **Scikit-learn**: Machine learning foundation
- **Open Source Community**: Continuous support and feedback

---

<div align="center">

**🌸 Made with ❤️ for English Learners Worldwide 🌸**

[🌟 Star this repo](https://github.com/your-username/ManabiFun) | [🐛 Report Bug](https://github.com/your-username/ManabiFun/issues) | [💡 Request Feature](https://github.com/your-username/ManabiFun/issues)

</div>
