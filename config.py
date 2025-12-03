# Configuration file for the application

# Color Palette
COLORS = {
    'primary_bg': '#222831',
    'secondary_bg': '#393E46',
    'accent': '#948979',
    'text': '#DFD0B8',
    'positive': '#4CAF50',
    'neutral': '#FFC107',
    'negative': '#F44336'
}

# Avatar URLs (Using LottieFiles URLs as placeholders)
AVATAR_URLS = {
    "male": {
        "happy": "https://lottie.host/4d6e8c9e-happy-male.json", # Placeholder
        "neutral": "https://lottie.host/5f7g9h0i-neutral-male.json", # Placeholder
        "sad": "https://lottie.host/6g8h1j2k-sad-male.json" # Placeholder
    },
    "female": {
        "happy": "https://lottie.host/7h9i2k3l-happy-female.json", # Placeholder
        "neutral": "https://lottie.host/8i0j3k4m-neutral-female.json", # Placeholder
        "sad": "https://lottie.host/9j1k4l5n-sad-female.json" # Placeholder
    }
}

# Fallback Generic Lottie URLs (People/Emotions) - ensuring these work for demo
GENERIC_LOTTIE = {
    "happy": "https://assets5.lottiefiles.com/packages/lf20_happy.json",
    "neutral": "https://assets10.lottiefiles.com/packages/lf20_p7ki6kjb.json", 
    "sad": "https://assets5.lottiefiles.com/packages/lf20_sad.json"
}

# Sentiment Thresholds
SENTIMENT_THRESHOLDS = {
    'positive': 0.6,
    'negative': 0.4
}

# Product Aspects to Analyze
PRODUCT_ASPECTS = [
    'Battery Life',
    'Performance',
    'Shipping',
    'Build Quality',
    'Value for Money',
    'Customer Service',
    'Design',
    'Ease of Use'
]
