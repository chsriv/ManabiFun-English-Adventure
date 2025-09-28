#!/usr/bin/env python3
"""
🌟 English Adventure Explorer 
A simple working version to test core functionality
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import pickle
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="English Adventure Explorer",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("🌟 English Adventure Explorer")
    st.write("Welcome to your personalized English learning adventure!")
    
    # Simple test to verify the app works
    if st.button("Start Adventure"):
        st.success("🎉 App is working! The main app will be fixed shortly.")
        st.balloons()

if __name__ == "__main__":
    main()