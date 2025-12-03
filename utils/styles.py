import streamlit as st
from config import COLORS

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Inter:wght@400&family=Roboto+Mono:wght@500&display=swap');
        
        /* Main Background */
        .stApp {{
            background-color: {COLORS['primary_bg']};
            color: {COLORS['text']};
            font-family: 'Inter', sans-serif;
        }}
        
        /* Headers */
        h1, h2, h3 {{
            font-family: 'Poppins', sans-serif;
            color: {COLORS['text']} !important;
        }}
        
        /* Metric Cards */
        div[data-testid="metric-container"] {{
            background-color: {COLORS['secondary_bg']};
            border-radius: 15px;
            padding: 25px;
            border-left: 5px solid {COLORS['accent']};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }}
        
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-5px);
        }}
        
        /* Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['secondary_bg']} 100%);
            color: {COLORS['text']};
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(148, 137, 121, 0.3);
        }}
        
        .stButton>button:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(148, 137, 121, 0.5);
            color: #fff;
        }}
        
        /* Text Input */
        .stTextArea>div>div>textarea {{
            background-color: {COLORS['secondary_bg']};
            color: {COLORS['text']};
            border: 2px solid {COLORS['accent']};
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            padding: 15px;
        }}
        
        /* Sentiment Badges */
        .sentiment-positive {{
            background-color: {COLORS['positive']};
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .sentiment-neutral {{
            background-color: {COLORS['neutral']};
            color: #222831;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .sentiment-negative {{
            background-color: {COLORS['negative']};
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        /* Avatar Container */
        .avatar-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-color: {COLORS['secondary_bg']};
            border-radius: 20px;
            margin: 20px 0;
        }}
        
        /* Landing Page */
        .landing-title {{
            text-align: center;
            font-size: 48px;
            font-weight: 700;
            color: {COLORS['text']};
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .landing-subtitle {{
            text-align: center;
            font-size: 20px;
            color: {COLORS['accent']};
            margin-bottom: 40px;
        }}
        
        /* Gender Selection Cards */
        .gender-card {{
            background-color: {COLORS['secondary_bg']};
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid transparent;
        }}
        
        .gender-card:hover {{
            border-color: {COLORS['accent']};
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(148, 137, 121, 0.4);
        }}
        
        /* Analysis Results */
        .result-header {{
            font-size: 32px;
            font-weight: 700;
            color: {COLORS['text']};
            margin-bottom: 20px;
            text-align: center;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['secondary_bg']};
        }}
        
    </style>
    """, unsafe_allow_html=True)

def add_keyboard_shortcuts():
    """Add keyboard shortcuts for better UX"""
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const analyzeBtn = document.querySelector('button[kind="primary"]');
            if (analyzeBtn) analyzeBtn.click();
        }
        
        // Esc to reset
        if (e.key === 'Escape') {
            const resetBtn = document.querySelector('button:contains("Start Over")');
            if (resetBtn) resetBtn.click();
        }
    });
    </script>
    """, unsafe_allow_html=True)
