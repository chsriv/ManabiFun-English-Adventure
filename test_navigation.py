import streamlit as st
import pandas as pd

# Test the navigation logic
def test_navigation():
    print("Testing navigation states...")
    
    # Initialize test session state
    test_states = {
        'player_name': 'TestExplorer',
        'current_realm': None,
        'current_chapter': None,
        'show_question': False,
        'question_answered': False,
        'realm_progress': {
            'grammar': {'easy': 0, 'medium': 0, 'hard': 0},
            'articles': {'easy': 0, 'medium': 0, 'hard': 0},
            'synonyms': {'easy': 0, 'medium': 0, 'hard': 0},
            'antonyms': {'easy': 0, 'medium': 0, 'hard': 0},
            'sentences': {'easy': 0, 'medium': 0, 'hard': 0}
        }
    }
    
    # Load questions
    df = pd.read_csv('data/manabifun_questions.csv')
    print(f"Loaded {len(df)} questions")
    
    # Test navigation flow
    print("\n1. Player name set, current_realm = None -> Should show realm selection")
    
    print("\n2. Test each realm navigation:")
    for realm in ['grammar', 'articles', 'synonyms', 'antonyms', 'sentences']:
        test_states['current_realm'] = realm
        test_states['current_chapter'] = None
        
        realm_questions = df[df['topic'] == realm]
        print(f"   {realm}: {len(realm_questions)} questions available")
        
        for difficulty in ['easy', 'medium', 'hard']:
            chapter_questions = realm_questions[realm_questions['difficulty'] == difficulty]
            print(f"     {difficulty}: {len(chapter_questions)} questions")
            
            if len(chapter_questions) > 0:
                test_states['current_chapter'] = difficulty
                test_states['show_question'] = True
                current_progress = test_states['realm_progress'][realm][difficulty]
                
                if current_progress < len(chapter_questions):
                    current_question = chapter_questions.iloc[current_progress]
                    print(f"       Current question: {current_question['question'][:50]}...")
                else:
                    print(f"       Chapter completed!")

if __name__ == "__main__":
    test_navigation()