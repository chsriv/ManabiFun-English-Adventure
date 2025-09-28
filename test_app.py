#!/usr/bin/env python3
"""
Quick test of Alex Adventure navigation
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Navigation Test", layout="wide")

# Load data
@st.cache_data
def load_test_data():
    return pd.read_csv("data/manabifun_questions.csv")

# Initialize session state
if 'test_realm' not in st.session_state:
    st.session_state.test_realm = None
    st.session_state.test_chapter = None

st.title("🧪 Navigation Test")

df = load_test_data()
st.write(f"Loaded {len(df)} questions across {df['topic'].nunique()} realms")

# Show current state
st.write("**Current State:**")
st.write(f"- Realm: {st.session_state.test_realm}")
st.write(f"- Chapter: {st.session_state.test_chapter}")

st.divider()

# Test realm selection
st.subheader("1. Test Realm Selection")
realms = df['topic'].unique()
for realm in realms:
    realm_questions = df[df['topic'] == realm]
    if st.button(f"🔮 {realm} ({len(realm_questions)} questions)", key=f"realm_{realm}"):
        st.session_state.test_realm = realm
        st.session_state.test_chapter = None
        st.rerun()

st.divider()

# Test chapter selection  
if st.session_state.test_realm:
    st.subheader(f"2. Test Chapter Selection for {st.session_state.test_realm}")
    realm_df = df[df['topic'] == st.session_state.test_realm]
    
    for difficulty in ['easy', 'medium', 'hard']:
        chapter_questions = realm_df[realm_df['difficulty'] == difficulty]
        if len(chapter_questions) > 0:
            if st.button(f"📖 {difficulty.title()} ({len(chapter_questions)} questions)", 
                        key=f"chapter_{difficulty}"):
                st.session_state.test_chapter = difficulty
                st.rerun()
        else:
            st.write(f"❌ {difficulty.title()}: No questions available")

st.divider()

# Test question display
if st.session_state.test_realm and st.session_state.test_chapter:
    st.subheader(f"3. Test Questions - {st.session_state.test_realm} / {st.session_state.test_chapter}")
    
    questions = df[
        (df['topic'] == st.session_state.test_realm) & 
        (df['difficulty'] == st.session_state.test_chapter)
    ]
    
    if len(questions) > 0:
        st.success(f"✅ Found {len(questions)} questions!")
        
        # Show first question as example
        first_q = questions.iloc[0]
        st.write("**Sample Question:**")
        st.write(f"Q: {first_q['question']}")
        st.write(f"A) {first_q['option_a']}")
        st.write(f"B) {first_q['option_b']}")
        st.write(f"C) {first_q['option_c']}")
        st.write(f"D) {first_q['option_d']}")
        st.write(f"Correct: {first_q['correct_answer']}")
    else:
        st.error("❌ No questions found!")

# Reset button
if st.button("🔄 Reset Test"):
    st.session_state.test_realm = None
    st.session_state.test_chapter = None
    st.rerun()