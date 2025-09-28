# 📚 Explorer's English Adventure

> **A Magical Journey Through the Five Realms of Language Learning**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 **What is Explorer's English Adventure?**

Explorer's English Adventure is a **personalized English learning application** that transforms education into an enchanting journey through mystical realms. Inspired by Enid Blyton's storytelling magic, it combines advanced AI with beautiful adventure theming to create an engaging learning experience.

### 🏰 **Five Mystical Realms:**
- 🌳 **Grammar Grove** - Ancient trees whisper sentence structure secrets
- 📜 **Article Academy** - Mystical library where "a", "an", and "the" guard treasures  
- 🦋 **Synonym Sanctuary** - Sacred halls of word meanings and alternatives
- 🪞 **Antonym Archipelago** - Mirror islands where opposite words clash
- 🏰 **Sentence Citadel** - Majestic fortress where words unite powerfully

### ✨ **Key Features:**
- 🤖 **AI-Powered Weakness Analysis** using Random Forest ML (93-94% accuracy)
- 🔀 **Fisher-Yates Shuffle Algorithm** for fair question randomization  
- 🎨 **Beautiful Adventure UI** with Enid Blyton book styling
- 👤 **Personalized Experience** with custom player names
- 📊 **Progress Tracking** across difficulty levels (Novice → Advanced)
- 🎯 **250+ Curated Questions** across 5 core English topics

---

## 🚀 **Quick Start**

### **1. Installation**
```bash
# Clone the repository
git clone https://github.com/chsriv/Explorer-English-Adventure.git
cd Explorer-English-Adventure

# Install dependencies
pip install -r requirements.txt
```

### **2. Launch Your Adventure**
```bash
# Main adventure app
streamlit run alex_adventure.py

# Alternative simple version  
streamlit run app.py
```

### **3. Start Learning**
- Open `http://localhost:8501` in your browser
- Enter your adventurer name
- Choose your first mystical realm
- Begin your English mastery journey!

---

## 🛠️ **Technology Stack**

### **🧠 Machine Learning Core**
- **Random Forest Classifier**: 93-94% accuracy for weakness detection
- **Fisher-Yates Shuffle**: Mathematically fair question randomization
- **Scikit-learn**: ML model training and prediction pipeline
- **Pandas**: Data processing and CSV management

### **🎨 Frontend & UI**
- **Streamlit**: Reactive web app framework
- **Custom CSS**: Beautiful Enid Blyton book-style theming
- **Session State**: Persistent user progress and navigation
- **Responsive Design**: Works on desktop and mobile devices

### **📊 Data & Analytics**
- **CSV Database**: 250+ curated English questions
- **Topic Mapping**: Grammar, Articles, Synonyms, Antonyms, Sentences
- **Difficulty Levels**: Easy, Medium, Hard progression system
- **Progress Tracking**: Score history and performance analytics


## 📁 **Project Structure**

```
Explorer-English-Adventure/
├── 📱 alex_adventure.py           # Main Streamlit application
├── 📱 app.py                      # Alternative simple version
├── 🤖 train_model.py              # ML model training script
├── 📄 requirements.txt            # Python dependencies
├── 📖 README.md                   # Project documentation
├── 📊 data/
│   ├── manabifun_questions.csv    # Question database (250+ items)
│   └── student_scores.csv         # User progress tracking
├── 🧠 models/
│   ├── weakness_detector.py       # ML model utilities
│   └── weakness_detector.pkl      # Trained Random Forest model
└── 🧪 test_*.py                   # Test files
```

---

## 🤝 **Contributing**

We welcome contributions! Please feel free to:
- 🐛 Report bugs through GitHub issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Enid Blyton**: Inspiration for adventure storytelling
- **Streamlit**: Amazing web app framework
- **Scikit-learn**: Machine learning foundation
- **Open Source Community**: Continuous support and feedback

---

<div align="center">

**🌸 Made with ❤️ for English Learners Worldwide 🌸**

[🌟 Star this repo](https://github.com/chsriv/Explorer-English-Adventure) | [🐛 Report Bug](https://github.com/chsriv/Explorer-English-Adventure/issues) | [💡 Request Feature](https://github.com/chsriv/Explorer-English-Adventure/issues)

</div>
