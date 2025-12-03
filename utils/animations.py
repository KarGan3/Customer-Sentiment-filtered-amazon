import streamlit as st
import time

def show_analysis_animation():
    """Display animated loading screen during analysis"""
    
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    steps = [
        "🔍 Reading your review...",
        "🤖 Analyzing sentiment...",
        "📊 Extracting aspects...",
        "💡 Identifying insights...",
        "✨ Preparing results..."
    ]
    
    for i, step in enumerate(steps):
        progress_text.markdown(f"<h4 style='text-align: center; color: #DFD0B8;'>{step}</h4>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.3)
    
    progress_text.empty()
    progress_bar.empty()
