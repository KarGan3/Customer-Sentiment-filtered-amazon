# Project Architecture & Workflow

## 📁 File Structure & Purpose

```
Customer-Sentiment-filtered-amazon/
│
├── app.py                                    # 🎯 MAIN APPLICATION
├── sentiment.py                              # 🤖 ML MODEL ENGINE
├── config.py                                 # ⚙️ CONFIGURATION
│
├── utils/
│   ├── styles.py                            # 🎨 CSS STYLING
│   ├── avatar_manager.py                    # 👤 AVATAR LOGIC
│   ├── visualizations.py                    # 📊 CHARTS
│   ├── aspect_analyzer.py                   # 🔍 ASPECT EXTRACTION
│   └── animations.py                        # ⏳ LOADING EFFECTS
│
├── assets/
│   └── avatars/                             # 🎭 AVATAR FILES
│
├── Customer_Sentiment_filtered_amazon.csv   # 📚 TRAINING DATA
├── README.md                                # 📖 DOCUMENTATION
└── ARCHITECTURE.md                          # 📐 THIS FILE
```

---

## 🔄 Application Workflow

### **Step 1: User Opens Application**
```
Browser → http://localhost:8507
         ↓
    app.py loads
         ↓
    Imports all modules
```

### **Step 2: Model Training (First Time Only)**
```
app.py
  ↓
sentiment.py
  ↓ load_data()
Customer_Sentiment_filtered_amazon.csv
  ↓ train_model()
SVM Model Trained ✅
  ↓
Cached in Streamlit
```

### **Step 3: Landing Page Display**
```
app.py
  ↓ apply_custom_css()
utils/styles.py → Injects dark theme CSS
  ↓
User sees: Gender Selection (Male/Female)
```

### **Step 4: User Selects Avatar**
```
User clicks "Male Avatar" or "Female Avatar"
  ↓
st.session_state.gender = "male" / "female"
  ↓
config.py → Loads avatar URLs
  ↓
Navigates to Dashboard
```

### **Step 5: User Enters Review**
```
User types review in text area
  ↓
Clicks "🔍 Analyze Review"
  ↓
utils/animations.py → show_analysis_animation()
  ↓
Processing begins...
```

### **Step 6: Sentiment Analysis**
```
app.py
  ↓ predict_sentiment_with_probabilities(review_text)
sentiment.py
  ↓ TF-IDF Vectorization
  ↓ StandardScaler
  ↓ SVM Prediction
  ↓
Returns: (sentiment_label, probabilities)
Example: ("negative", {"positive": 0.1, "neutral": 0.2, "negative": 0.7})
```

### **Step 7: Aspect Analysis**
```
app.py
  ↓ aspect_analyzer.analyze_aspects(review_text)
utils/aspect_analyzer.py
  ↓ Extract keywords (battery, performance, etc.)
  ↓ Find relevant sentences
  ↓ Detect sentiment words (good, terrible, etc.)
  ↓ Handle negation (not good → negative)
  ↓ Apply intensity modifiers (very good → 1.5x)
  ↓
Returns: {"Battery Life": 0.2, "Performance": 0.1, ...}
```

### **Step 8: Visualization**
```
app.py
  ↓ create_sentiment_gauge(score)
  ↓ create_sentiment_distribution(probabilities)
  ↓ create_aspect_analysis_chart(aspects_data)
utils/visualizations.py
  ↓ Plotly charts generated
  ↓
Displayed on dashboard
```

### **Step 9: Avatar Display**
```
app.py
  ↓ display_3d_avatar(gender, sentiment_label, score)
utils/avatar_manager.py
  ↓ get_emotion_from_sentiment()
  ↓ Determines: happy / neutral / sad
  ↓ load_lottie_url()
config.py → AVATAR_URLS[gender][emotion]
  ↓
Lottie animation displayed
```

### **Step 10: Results Display**
```
Dashboard shows:
  ✅ 3D Avatar with emotion
  ✅ Sentiment badge (Positive/Neutral/Negative)
  ✅ Sentiment gauge (0-100)
  ✅ Distribution donut chart
  ✅ Aspect analysis bar chart
  ✅ Strengths (score > 0.6)
  ✅ Weaknesses (score < 0.4)
  ✅ Key phrases from review
```

---

## 📄 Detailed File Descriptions

### **1. app.py** - Main Application Controller
**Purpose**: Orchestrates the entire application flow

**Key Functions**:
- `load_and_train_model()` - Loads ML model with caching
- Page configuration and layout
- Session state management
- User input handling
- Results display coordination

**Dependencies**:
- `sentiment.py` - For predictions
- `utils/styles.py` - For CSS
- `utils/avatar_manager.py` - For avatars
- `utils/visualizations.py` - For charts
- `utils/aspect_analyzer.py` - For aspect extraction
- `utils/animations.py` - For loading effects
- `config.py` - For settings

**Flow**:
```python
1. Import all modules
2. Configure Streamlit page
3. Apply custom CSS
4. Initialize session state
5. Load & train ML model (cached)
6. Display landing page OR dashboard
7. Handle user interactions
8. Display results
```

---

### **2. sentiment.py** - Machine Learning Engine
**Purpose**: Trains and runs the SVM sentiment classification model

**Key Functions**:
- `load_data(filepath)` - Loads CSV dataset
- `train_model(df)` - Trains SVM model with TF-IDF
- `predict_sentiment(text)` - Returns sentiment label
- `predict_sentiment_with_probabilities(text)` - Returns label + probabilities
- `get_artifacts()` - Returns trained model components

**ML Pipeline**:
```
Input Text
  ↓
TF-IDF Vectorization (converts text to numbers)
  ↓
StandardScaler (normalizes features)
  ↓
SVM Classifier (C=0.1, kernel='linear')
  ↓
Output: Positive / Neutral / Negative + Probabilities
```

**Global Variables**:
- `_model` - Trained SVM model
- `_vectorizer` - TF-IDF vectorizer
- `_scaler` - StandardScaler
- `_label_encoder` - Label encoder

---

### **3. config.py** - Configuration Settings
**Purpose**: Centralized configuration for colors, avatars, and aspects

**Contains**:
```python
COLORS = {
    'primary_bg': '#222831',
    'secondary_bg': '#393E46',
    'accent': '#948979',
    'text': '#DFD0B8',
    'positive': '#4CAF50',
    'neutral': '#FFC107',
    'negative': '#F44336'
}

AVATAR_URLS = {
    "male": {"happy": "...", "neutral": "...", "sad": "..."},
    "female": {"happy": "...", "neutral": "...", "sad": "..."}
}

PRODUCT_ASPECTS = [
    'Battery Life', 'Performance', 'Shipping', 
    'Build Quality', 'Value for Money', ...
]
```

---

### **4. utils/styles.py** - CSS Styling
**Purpose**: Applies custom dark theme styling

**Key Functions**:
- `apply_custom_css()` - Injects CSS into Streamlit
- `add_keyboard_shortcuts()` - Adds keyboard shortcuts

**Styles**:
- Dark theme colors
- Custom buttons with gradients
- Sentiment badges (colored pills)
- Avatar containers
- Metric cards with hover effects
- Hides Streamlit default UI (Deploy button, menu)

---

### **5. utils/avatar_manager.py** - Avatar Logic
**Purpose**: Manages 3D avatar loading and display

**Key Functions**:
- `load_lottie_url(url)` - Fetches Lottie JSON from URL
- `get_emotion_from_sentiment(label, score)` - Maps sentiment to emotion
- `display_3d_avatar(gender, label, score)` - Renders avatar
- `get_sentiment_message(label)` - Returns appropriate message

**Emotion Mapping**:
```
Positive (score > 0.6) → happy
Neutral (0.4 ≤ score ≤ 0.6) → neutral
Negative (score < 0.4) → sad
```

**Fallback**: If Lottie fails, displays emoji (😊 😐 😢)

---

### **6. utils/visualizations.py** - Chart Generation
**Purpose**: Creates interactive Plotly charts

**Key Functions**:
- `create_sentiment_gauge(score)` - Animated gauge (0-100)
- `create_sentiment_distribution(pos, neu, neg)` - Donut chart
- `create_aspect_analysis_chart(aspects_data)` - Horizontal bar chart

**Chart Features**:
- Dark theme colors
- Interactive tooltips
- Color-coded by sentiment
- Responsive sizing

---

### **7. utils/aspect_analyzer.py** - Aspect Extraction
**Purpose**: Analyzes specific product aspects from reviews

**Key Components**:

**Aspect Keywords**:
```python
{
    'Battery Life': ['battery', 'charge', 'power'],
    'Performance': ['fast', 'slow', 'speed', 'lag'],
    'Shipping': ['shipping', 'delivery', 'arrived'],
    ...
}
```

**Sentiment Words**:
- **Positive**: good, great, excellent, amazing, love, perfect, ...
- **Negative**: bad, terrible, awful, nightmare, broken, ...

**Intensity Modifiers**:
- **Amplifiers** (1.5x): very, extremely, incredibly, absolutely, ...
- **Diminishers** (0.5x): somewhat, slightly, a bit, fairly, ...

**Negation Handling**:
- **True Negations**: not, no, never, neither, nor, ...
- "not good" → flips to negative
- "not terrible" → flips to positive

**Key Functions**:
- `analyze_aspects(review_text)` - Returns aspect scores
- `_calculate_aspect_sentiment(text, keywords)` - Calculates score for one aspect
- `extract_key_phrases(text, aspect)` - Extracts relevant sentences

**Scoring Algorithm**:
```
1. Find sentences mentioning the aspect
2. Count positive/negative words
3. Apply intensity weights (amplifiers/diminishers)
4. Handle negation (flip sentiment if present)
5. Calculate: positive_score / (positive_score + negative_score)
6. Return: 0.0 (negative) to 1.0 (positive)
```

---

### **8. utils/animations.py** - Loading Effects
**Purpose**: Displays animated loading screen during analysis

**Key Functions**:
- `show_analysis_animation()` - Shows progress bar with steps

**Steps**:
```
🔍 Reading your review...
🤖 Analyzing sentiment...
📊 Extracting aspects...
💡 Identifying insights...
✨ Preparing results...
```

---

### **9. Customer_Sentiment_filtered_amazon.csv** - Training Data
**Purpose**: Dataset for training the SVM model

**Columns**:
- `review_text` - The review content
- `sentiment` - Label (positive/neutral/negative)

**Usage**: Loaded by `sentiment.py` during model training

---

## 🔗 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│                  "Battery life is terrible"                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├──────────────────┬─────────────────┐
                         ↓                  ↓                 ↓
                  ┌──────────────┐   ┌─────────────┐  ┌──────────────┐
                  │ sentiment.py │   │aspect_      │  │ animations.py│
                  │              │   │analyzer.py  │  │              │
                  │ SVM Model    │   │             │  │ Loading...   │
                  │ TF-IDF       │   │ Keywords    │  └──────────────┘
                  │ Scaler       │   │ Sentiment   │
                  └──────┬───────┘   │ Negation    │
                         │           │ Intensity   │
                         ↓           └──────┬──────┘
                  ┌──────────────┐         │
                  │ "negative"   │         ↓
                  │ prob: 0.85   │  ┌──────────────┐
                  └──────┬───────┘  │Battery: 0.15 │
                         │          │Perform: 0.10 │
                         │          └──────┬───────┘
                         │                 │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │ avatar_manager  │
                         │ → sad avatar    │
                         └────────┬────────┘
                                  │
                         ┌────────┴────────┐
                         │ visualizations  │
                         │ → Gauge: 15     │
                         │ → Donut chart   │
                         │ → Bar chart     │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │   DASHBOARD     │
                         │   DISPLAY       │
                         └─────────────────┘
```

---

## 🎯 Key Interactions

### **app.py ↔ sentiment.py**
```python
# app.py calls:
sentiment_label, probabilities = sentiment.predict_sentiment_with_probabilities(review_text)

# sentiment.py returns:
("negative", {"positive": 0.05, "neutral": 0.10, "negative": 0.85})
```

### **app.py ↔ aspect_analyzer.py**
```python
# app.py calls:
aspects_data = aspect_analyzer.analyze_aspects(review_text)

# aspect_analyzer.py returns:
{
    "Battery Life": 0.15,
    "Performance": 0.10,
    "Shipping": 0.50,
    ...
}
```

### **app.py ↔ avatar_manager.py**
```python
# app.py calls:
display_3d_avatar(gender="male", sentiment_label="negative", sentiment_score=0.15)

# avatar_manager.py:
# 1. Maps "negative" + 0.15 → "sad"
# 2. Loads AVATAR_URLS["male"]["sad"]
# 3. Displays Lottie animation
```

### **app.py ↔ visualizations.py**
```python
# app.py calls:
gauge_chart = create_sentiment_gauge(0.85)
dist_chart = create_sentiment_distribution(0.05, 0.10, 0.85)
aspect_chart = create_aspect_analysis_chart(aspects_data)

# visualizations.py returns Plotly figure objects
```

---

## 🚀 Execution Order

1. **Startup** (app.py)
   - Import modules
   - Configure page
   - Apply CSS
   - Train model (cached)

2. **Landing Page** (app.py)
   - Display gender selection
   - Wait for user input

3. **Dashboard** (app.py)
   - Display review input
   - Wait for "Analyze" click

4. **Analysis** (when user clicks Analyze)
   - Show loading animation (animations.py)
   - Predict sentiment (sentiment.py)
   - Analyze aspects (aspect_analyzer.py)
   - Generate charts (visualizations.py)
   - Load avatar (avatar_manager.py)

5. **Display Results** (app.py)
   - Show avatar
   - Show sentiment badge
   - Show charts
   - Show strengths/weaknesses
   - Show key phrases

6. **User Actions**
   - "Analyze Another Review" → Back to step 3
   - "Start Over" → Back to step 2
   - "Change Avatar" → Back to step 2

---

## 📊 Performance Optimization

### **Caching Strategy**
```python
@st.cache_resource  # Model training cached
def load_and_train_model():
    # Only runs once per session
    # Subsequent calls use cached result
```

### **Session State**
```python
st.session_state.gender  # Persists across reruns
st.session_state.review_history  # Stores analysis history
st.session_state.aspect_analyzer  # Reuses analyzer instance
```

---

## 🎨 UI/UX Flow

```
Landing Page
    ↓ (Select Avatar)
Dashboard - Input
    ↓ (Enter Review + Click Analyze)
Loading Animation
    ↓ (1.5 seconds)
Results Display
    ├─ Avatar (left)
    ├─ Metrics (right)
    ├─ Original Review
    ├─ Aspect Chart
    └─ Strengths/Weaknesses
    ↓ (User Actions)
    ├─ Analyze Another → Back to Input
    ├─ Start Over → Back to Landing
    └─ Change Avatar → Back to Landing
```

---

**Built by Team Clusters** | Powered by AI Sentiment Analysis
