import streamlit as st
import pandas as pd
from utils.styles import apply_custom_css, add_keyboard_shortcuts
from utils.avatar_manager import display_3d_avatar, get_sentiment_message
from utils.visualizations import (
    create_sentiment_gauge,
    create_aspect_analysis_chart,
    create_sentiment_distribution
)
from utils.aspect_analyzer import AspectAnalyzer
from utils.animations import show_analysis_animation
from config import COLORS, PRODUCT_ASPECTS
import sys
import os
import sentiment # Import our refactored module

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Sentiment Analyzer",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_custom_css()
add_keyboard_shortcuts()

# Initialize session state
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""
if 'aspect_analyzer' not in st.session_state:
    st.session_state.aspect_analyzer = AspectAnalyzer()
if 'review_history' not in st.session_state:
    st.session_state.review_history = []

# Load Model - Ensure it's trained every time to avoid cache issues
@st.cache_resource(show_spinner="Training sentiment analysis model...")
def load_and_train_model():
    """Loads data and trains/loads the model. Cached for performance."""
    try:
        df = sentiment.load_data()
        # Train the model - this sets the global variables in sentiment.py
        model, vectorizer, scaler, label_encoder, accuracy = sentiment.train_model(df)
        # Return the artifacts so they're cached
        return df, model, vectorizer, scaler, label_encoder, accuracy, True
    except FileNotFoundError:
        st.error("Error: 'Customer_Sentiment_filtered_amazon.csv' not found. Please ensure the file is in the directory.")
        return None, None, None, None, None, None, False

# Load the model and artifacts
df, model, vectorizer, scaler, label_encoder, accuracy, model_loaded = load_and_train_model()

# Ensure model is loaded before proceeding
if not model_loaded or df is None:
    st.stop()

# Set the global variables in sentiment module (in case cache cleared them)
sentiment._model = model
sentiment._vectorizer = vectorizer
sentiment._scaler = scaler
sentiment._label_encoder = label_encoder

# ============================================
# LANDING PAGE - GENDER SELECTION
# ============================================
if st.session_state.gender is None:
    # Header Section
    st.markdown('<h1 class="landing-title">🛍️ E-Commerce Review Analyzer</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="landing-subtitle">AI-Powered Sentiment Analysis with 3D Avatar Feedback</p>',
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
  
    
    # Gender Selection
    st.markdown('<h2 style="text-align: center; color: #DFD0B8;">Choose Your Avatar</h2>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        gender_col1, gender_col2 = st.columns(2)
        
        with gender_col1:
            st.markdown('<h2 style="font-size: 80px;">👨</h2>', unsafe_allow_html=True)
            if st.button("Male Avatar", key="male_btn", use_container_width=True):
                st.session_state.gender = "male"
                st.rerun()
        
        with gender_col2:
            st.markdown('<h2 style="font-size: 80px;">👩</h2>', unsafe_allow_html=True)
            if st.button("Female Avatar", key="female_btn", use_container_width=True):
                st.session_state.gender = "female"
                st.rerun()

# ============================================
# MAIN DASHBOARD - REVIEW INPUT & ANALYSIS
# ============================================
else:
    # Header with reset option
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<h1 class="landing-title">🛍️ Review Sentiment Analyzer</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Change Avatar", key="reset"):
            st.session_state.gender = None
            st.session_state.analysis_done = False
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # ============================================
    # INPUT SECTION
    # ============================================
    if not st.session_state.analysis_done:
        st.markdown('<h2 style="color: #DFD0B8;">Enter Product Review</h2>', unsafe_allow_html=True)
        
        review_text = st.text_area(
            label="Review Text",
            placeholder="Type or paste your product review here... (e.g., 'The battery life is amazing! Fast shipping and great quality.')",
            height=200,
            key="review_input",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            analyze_button = st.button("🔍 Analyze Review", use_container_width=True)
        
        if analyze_button:
            if review_text.strip():
                st.session_state.review_text = review_text
                st.session_state.analysis_done = True
                st.rerun()
            else:
                st.error("⚠️ Please enter a review to analyze!")
        


    # ============================================
    # RESULTS SECTION
    # ============================================
    else:
        review_text = st.session_state.review_text
        
        # Perform sentiment analysis
        show_analysis_animation()
        sentiment_label, probabilities = sentiment.predict_sentiment_with_probabilities(review_text)
        sentiment_score = probabilities.get(sentiment_label, 0.5)
        
        # --- HYBRID SAFETY NET ---
        # Calculate rule-based score to validate ML prediction
        rule_based_score = st.session_state.aspect_analyzer.analyze_overall_sentiment(review_text)
        
        # Override if ML is Positive but Rules say Negative (Safety Net)
        if rule_based_score < 0.4 and sentiment_label == 'positive':
            sentiment_label = 'negative'
            sentiment_score = rule_based_score # Use the low score
            # Adjust probabilities for display
            probabilities = {'positive': 0.1, 'neutral': 0.1, 'negative': 0.8}
            
        # Override if ML is Negative but Rules say Strong Positive (Rare case)
        elif rule_based_score > 0.8 and sentiment_label == 'negative':
            sentiment_label = 'positive'
            sentiment_score = rule_based_score
            probabilities = {'positive': 0.9, 'neutral': 0.05, 'negative': 0.05}
        # -------------------------
        
        # Analyze aspects
        aspect_analyzer = st.session_state.aspect_analyzer
        aspects_data = aspect_analyzer.analyze_aspects(review_text)
        
        # Save to history
        current_review = {
            'text': review_text[:100] + '...' if len(review_text) > 100 else review_text,
            'sentiment': sentiment_label,
            'score': sentiment_score,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
        }
        if not any(r['text'] == current_review['text'] for r in st.session_state.review_history):
            st.session_state.review_history.insert(0, current_review)
            st.session_state.review_history = st.session_state.review_history[:10]

        # Display Results Header
        st.markdown('<h2 class="result-header">Analysis Results</h2>', unsafe_allow_html=True)
        
        # ============================================
        # ROW 1: Avatar + Sentiment Metrics
        # ============================================
        row1_col1, row1_col2 = st.columns([1, 1])
        
        with row1_col1:
            st.markdown('<h3 style="text-align: center; color: #DFD0B8;">Your Review Assistant</h3>', unsafe_allow_html=True)
            display_3d_avatar(st.session_state.gender, sentiment_label, sentiment_score)
            
            # Sentiment Message
            message = get_sentiment_message(sentiment_label)
            sentiment_class = f"sentiment-{sentiment_label}"
            st.markdown(
                f'<div style="text-align: center; margin-top: 20px;"><span class="{sentiment_class}">{sentiment_label.upper()}</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<p style="text-align: center; color: {COLORS["text"]}; font-size: 18px; margin-top: 10px;">{message}</p>', unsafe_allow_html=True)
        
        with row1_col2:
            st.markdown('<h3 style="text-align: center; color: #DFD0B8;">Sentiment Metrics</h3>', unsafe_allow_html=True)
            
            # Sentiment Gauge
            gauge_chart = create_sentiment_gauge(sentiment_score)
            st.plotly_chart(gauge_chart, use_container_width=True)
            
            # Sentiment Distribution
            dist_chart = create_sentiment_distribution(
                probabilities.get('positive', 0),
                probabilities.get('neutral', 0),
                probabilities.get('negative', 0)
            )
            st.plotly_chart(dist_chart, use_container_width=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============================================
        # ROW 2: Review Text Display
        # ============================================
        st.markdown('<h3 style="color: #DFD0B8;">📝 Original Review</h3>', unsafe_allow_html=True)
        st.markdown(
            f"""<div style='background-color: {COLORS['secondary_bg']}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['accent']};'>
            <p style='color: {COLORS['text']}; font-size: 16px; line-height: 1.6;'>{review_text}</p>
            </div>""",
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================
        # ROW 3: Aspect-Based Analysis
        # ============================================
        st.markdown('<h3 style="color: #DFD0B8;">🔍 Product Aspects Analysis</h3>', unsafe_allow_html=True)
        
        aspect_chart = create_aspect_analysis_chart(aspects_data)
        st.plotly_chart(aspect_chart, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================
        # ROW 4: Strengths & Weaknesses
        # ============================================
        strength_col, weakness_col = st.columns(2)
        
        # Identify strengths (aspects with high scores)
        strengths = {aspect: score for aspect, score in aspects_data.items() if score > 0.65}
        weaknesses = {aspect: score for aspect, score in aspects_data.items() if score < 0.45}
        
        with strength_col:
            st.markdown(f'<h3 style="color: {COLORS["positive"]};">✅ Product Strengths</h3>', unsafe_allow_html=True)
            if strengths:
                for aspect, score in sorted(strengths.items(), key=lambda x: x[1], reverse=True):
                    st.markdown(f"**{aspect}** - Score: {score:.2f}")
                    # Show relevant phrases
                    phrases = aspect_analyzer.extract_key_phrases(review_text, aspect)
                    if phrases:
                        with st.expander(f"See mentions of {aspect}"):
                            for phrase in phrases:
                                st.markdown(f"- *{phrase}*")
            else:
                st.markdown("*No significant strengths detected*")
        
        with weakness_col:
            st.markdown(f'<h3 style="color: {COLORS["negative"]};">⚠️ Product Weaknesses</h3>', unsafe_allow_html=True)
            if weaknesses:
                for aspect, score in sorted(weaknesses.items(), key=lambda x: x[1]):
                    st.markdown(f"**{aspect}** - Score: {score:.2f}")
                    # Show relevant phrases
                    phrases = aspect_analyzer.extract_key_phrases(review_text, aspect)
                    if phrases:
                        with st.expander(f"See mentions of {aspect}"):
                            for phrase in phrases:
                                st.markdown(f"- *{phrase}*")
            else:
                st.markdown("*No significant weaknesses detected*")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Action Buttons
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🔄 Analyze Another Review", use_container_width=True):
                st.session_state.analysis_done = False
                st.session_state.review_text = ""
                st.rerun()
        

        
        with action_col3:
            if st.button("🏠 Start Over", use_container_width=True):
                st.session_state.gender = None
                st.session_state.analysis_done = False
                st.session_state.review_text = ""
                st.rerun()

# ============================================
# SIDEBAR - Multi-Review Analysis
# ============================================
with st.sidebar:
    st.markdown(f'<h2 style="color: {COLORS["text"]};">📊 Analysis History</h2>', unsafe_allow_html=True)
    
    # Display history
    if st.session_state.review_history:
        st.markdown(f'<p style="color: {COLORS["accent"]};">Recent analyses:</p>', unsafe_allow_html=True)
        
        for i, review in enumerate(st.session_state.review_history):
            with st.expander(f"Review {i+1} - {review['sentiment'].title()}"):
                st.markdown(f"**Text:** {review['text']}")
                st.markdown(f"**Sentiment:** {review['sentiment'].title()}")
                st.markdown(f"**Score:** {review['score']:.2f}")
                st.markdown(f"**Time:** {review['timestamp']}")
        
        if st.button("🗑️ Clear History"):
            st.session_state.review_history = []
            st.rerun()

    else:
        st.info("No analysis history yet. Start analyzing reviews!")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    f"""<div style='text-align: center; color: {COLORS['accent']}; padding: 20px;'>
    <p>Powered by AI Sentiment Analysis | Built by Team Clusters</p>
    </div>""",
    unsafe_allow_html=True
)
