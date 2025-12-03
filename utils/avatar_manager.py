import streamlit as st
from streamlit_lottie import st_lottie
import requests
from config import AVATAR_URLS, GENERIC_LOTTIE

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        # st.error(f"Error loading avatar: {str(e)}") # Suppress error for cleaner UI
        pass
    return None

def get_emotion_from_sentiment(sentiment_label, sentiment_score):
    """
    Determine emotion based on sentiment analysis
    
    Args:
        sentiment_label: 'positive', 'neutral', or 'negative'
        sentiment_score: float between 0-1
    
    Returns:
        emotion: 'happy', 'neutral', or 'sad'
    """
    if sentiment_label == 'positive':
        return 'happy'
    elif sentiment_label == 'negative':
        return 'sad'
    else:
        return 'neutral'

def display_3d_avatar(gender, sentiment_label, sentiment_score):
    """
    Display animated 3D avatar based on gender and sentiment
    
    Args:
        gender: 'Male' or 'Female' (case insensitive)
        sentiment_label: 'positive', 'neutral', or 'negative'
        sentiment_score: float sentiment score
    """
    emotion = get_emotion_from_sentiment(sentiment_label, sentiment_score)
    gender_key = gender.lower()
    
    # Container for avatar
    st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
    
    # Try specific avatar URL
    avatar_url = AVATAR_URLS.get(gender_key, {}).get(emotion)
    lottie_avatar = None
    
    if avatar_url:
        lottie_avatar = load_lottie_url(avatar_url)
    
    # Fallback to generic if specific fails
    if not lottie_avatar:
        lottie_avatar = load_lottie_url(GENERIC_LOTTIE.get(emotion))
        
    if lottie_avatar:
        st_lottie(
            lottie_avatar,
            height=350,
            width=350,
            key=f"avatar_{gender}_{emotion}",
            quality="high",
            speed=1
        )
    else:
        # Fallback to emoji if Lottie fails completely
        emotion_emoji = {'happy': '😊', 'neutral': '😐', 'sad': '😢'}
        st.markdown(
            f"<h1 style='font-size: 150px; text-align: center;'>{emotion_emoji.get(emotion, '😐')}</h1>",
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_sentiment_message(sentiment_label):
    """Get appropriate message for sentiment"""
    messages = {
        'positive': "Great! This review shows positive sentiment! 🎉",
        'neutral': "This review has neutral sentiment. 🤔",
        'negative': "This review shows negative sentiment. 😔"
    }
    return messages.get(sentiment_label, "Analysis complete.")
