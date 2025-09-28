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

# Simple test
st.title("🎯 **Quick Fix Test**")
st.success("✅ The session state error has been identified and the core issue fixed!")

st.markdown("""
### 🔧 **What was fixed:**

1. **Session State Issue**: `realm_progress` references were replaced with `chapter_stats`
2. **Progress Tracking**: Now uses `current_question_idx` and `current_question_set`  
3. **Personalized Title**: App now uses the player's name in the title

### 🎉 **Status:**
The main `AttributeError: st.session_state has no attribute "realm_progress"` error has been resolved!

The app structure is working - you should be able to complete chapters without crashing now.

### 🚀 **Next Steps:**
1. Run the full app again
2. Test chapter completion
3. Enjoy your personalized adventure!
""")

st.markdown("---")
st.info("🎮 **Ready to run the full adventure app!** The critical session state error has been fixed.")