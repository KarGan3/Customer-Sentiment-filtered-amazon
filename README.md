# E-Commerce Sentiment Analysis Dashboard 🛍️

A modern, interactive sentiment analysis web application built with Streamlit that analyzes e-commerce product reviews using machine learning and displays results through expressive 3D avatar animations.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red)

---

## 🎯 Features

### Core Functionality
- **AI-Powered Sentiment Analysis**: Uses a trained SVM (Support Vector Machine) model to classify reviews as Positive, Neutral, or Negative
- **3D Avatar Feedback System**: Dynamic Lottie animations that respond to sentiment with expressive emotions (Happy 😊, Neutral 😐, Sad 😢)
- **Aspect-Based Analysis**: Identifies sentiment for specific product aspects:
  - Battery Life
  - Performance
  - Shipping
  - Build Quality
  - Value for Money
  - Customer Service
  - Design
  - Ease of Use

### Interactive Visualizations
- **Sentiment Gauge**: Animated gauge chart showing sentiment score (0-100)
- **Sentiment Distribution**: Donut chart displaying probability breakdown
- **Aspect Analysis Chart**: Horizontal bar chart with color-coded aspect scores
- **Strengths & Weaknesses**: Automatic extraction of product highlights and issues

### User Experience
- **Gender-Specific Avatars**: Choose between Male or Female avatar preferences
- **Analysis History**: Sidebar tracking of recent analyses
- **Export Functionality**: Download analysis history as CSV
- **Dark Theme**: Professional UI with custom color palette
- **Responsive Design**: Works seamlessly on desktop and tablet

---

## 🎨 Design Specifications

### Color Palette
```
Primary Background:   #222831 (Dark Charcoal)
Secondary Background: #393E46 (Slate Gray)
Accent Color:         #948979 (Warm Taupe)
Text/Highlight:       #DFD0B8 (Cream Beige)

Sentiment Colors:
- Positive: #4CAF50 (Green)
- Neutral:  #FFC107 (Amber)
- Negative: #F44336 (Red)
```

### Typography
- **Headings**: Poppins (700 weight)
- **Body**: Inter (400 weight)
- **Metrics**: Roboto Mono (500 weight)

---

## 📁 Project Structure

```
Customer-Sentiment-filtered-amazon/
│
├── app.py                          # Main Streamlit application
├── sentiment.py                    # ML model (SVM) and prediction logic
├── config.py                       # Configuration (colors, avatars, aspects)
│
├── utils/
│   ├── styles.py                   # Custom CSS styling
│   ├── avatar_manager.py           # Avatar display logic
│   ├── visualizations.py           # Plotly chart generators
│   ├── aspect_analyzer.py          # Aspect extraction and scoring
│   └── animations.py               # Loading animations
│
├── assets/
│   └── avatars/                    # 3D avatar files (Lottie JSON)
│
├── Customer_Sentiment_filtered_amazon.csv  # Training dataset
└── README.md                       # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Customer-Sentiment-filtered-amazon
```

### Step 2: Install Dependencies
```bash
pip install streamlit plotly pandas scikit-learn scipy numpy matplotlib seaborn streamlit-lottie requests
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Verify Dataset
Ensure `Customer_Sentiment_filtered_amazon.csv` is in the project root directory.

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will automatically:
- Load the dataset
- Train the SVM model (cached for performance)
- Open in your default browser at `http://localhost:8501`

---

## 📊 Usage Guide

### 1. Landing Page
- Choose your avatar preference (Male or Female)
- Click the corresponding button to proceed to the dashboard

### 2. Enter Review
- Type or paste a product review in the text area
- Click **"🔍 Analyze Review"** to start analysis

### 3. View Results
The dashboard displays:
- **3D Avatar**: Animated character showing emotion based on sentiment
- **Sentiment Badge**: Color-coded label (Positive/Neutral/Negative)
- **Sentiment Gauge**: Visual score representation (0-100)
- **Sentiment Distribution**: Probability breakdown chart
- **Original Review**: Your input text displayed
- **Aspect Analysis**: Bar chart showing scores for product aspects
- **Strengths & Weaknesses**: Lists of positive and negative aspects with relevant phrases

### 4. Navigation
- **🔄 Analyze Another Review**: Return to input screen
- **🏠 Start Over**: Return to avatar selection
- **🔄 Change Avatar**: Switch between Male/Female avatars

### 5. History & Export
- View recent analyses in the sidebar
- Export analysis history as CSV
- Clear history when needed

---

## 🧠 Machine Learning Model

### Model Details
- **Algorithm**: Support Vector Machine (SVM)
- **Kernel**: Linear
- **Regularization**: C=0.1
- **Features**: TF-IDF Vectorization
- **Preprocessing**: StandardScaler (with_mean=False)
- **Accuracy**: ~98% on test set

### Training Process
1. Load dataset from CSV
2. Encode sentiment labels (Positive, Neutral, Negative)
3. Vectorize review text using TF-IDF
4. Split data (80% train, 20% test)
5. Scale features
6. Train SVM model
7. Evaluate performance

### Prediction Pipeline
```python
Input Review → TF-IDF Vectorization → Scaling → SVM Prediction → Sentiment Label + Probabilities
```

---

## 🎭 Avatar System

### Implementation
The application uses **Lottie animations** for 3D avatar feedback:
- **Happy Avatar**: Displayed for positive sentiment (score > 0.6)
- **Neutral Avatar**: Displayed for neutral sentiment (0.4 ≤ score ≤ 0.6)
- **Sad Avatar**: Displayed for negative sentiment (score < 0.4)

### Customization
To use your own avatars:
1. Download Lottie JSON files from [LottieFiles](https://lottiefiles.com/)
2. Place them in `assets/avatars/` directory
3. Update `config.py` with the file paths:
```python
AVATAR_URLS = {
    "male": {
        "happy": "assets/avatars/male_happy.json",
        "neutral": "assets/avatars/male_neutral.json",
        "sad": "assets/avatars/male_sad.json"
    },
    "female": {
        "happy": "assets/avatars/female_happy.json",
        "neutral": "assets/avatars/female_neutral.json",
        "sad": "assets/avatars/female_sad.json"
    }
}
```

---

## 🔍 Aspect Analysis

The aspect analyzer uses **keyword-based extraction** with sentiment scoring:

### How It Works
1. **Keyword Matching**: Searches for aspect-related keywords in the review
2. **Context Analysis**: Identifies sentences containing aspect keywords
3. **Sentiment Scoring**: Counts positive/negative words in relevant sentences
4. **Score Calculation**: Computes a 0-1 score (0=negative, 0.5=neutral, 1=positive)

### Example
For the review: *"Great battery life but slow performance"*
- **Battery Life**: Score 0.8 (Strength)
- **Performance**: Score 0.2 (Weakness)

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Landing page loads with dark theme
- [ ] Avatar selection works (Male/Female)
- [ ] Review input accepts text
- [ ] Positive sentiment detected correctly
- [ ] Negative sentiment detected correctly
- [ ] Neutral sentiment detected correctly
- [ ] 3D avatars display appropriate emotions
- [ ] Charts render properly (gauge, donut, bar)
- [ ] Aspect analysis shows relevant scores
- [ ] Strengths/Weaknesses sections populate
- [ ] Navigation buttons work
- [ ] History tracking functions
- [ ] CSV export works

### Test Reviews
**Positive:**
```
Amazing product! Excellent battery life, fast performance, and quick shipping. Highly recommend!
```

**Negative:**
```
Terrible experience. Battery dies quickly, slow performance, delayed shipping. Very disappointed.
```

**Neutral:**
```
It's okay. Average battery, decent performance, normal shipping. Nothing special.
```

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Run `pip install streamlit`

**Issue**: `FileNotFoundError: Customer_Sentiment_filtered_amazon.csv not found`
- **Solution**: Ensure the CSV file is in the project root directory

**Issue**: `ValueError: Model not trained`
- **Solution**: Clear Streamlit cache with `Ctrl+C` and restart the app

**Issue**: Avatars not loading
- **Solution**: Check internet connection (for URL-based Lottie files) or verify local file paths in `config.py`

**Issue**: Charts not displaying
- **Solution**: Ensure `plotly` is installed: `pip install plotly`

---

## 📈 Performance

- **Model Training**: ~2-3 seconds (cached after first run)
- **Prediction Time**: <1 second per review
- **Page Load**: <2 seconds
- **Analysis Animation**: 1.5 seconds

---

## 🔒 Data Privacy

- All analysis is performed **locally** on your machine
- No data is sent to external servers
- Review history is stored only in the browser session
- Clearing history removes all stored data

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Credits

**Built by Team Clusters**

### Technologies Used
- [Streamlit](https://streamlit.io/) - Web framework
- [Scikit-learn](https://scikit-learn.org/) - Machine learning
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Lottie](https://lottiefiles.com/) - 3D animations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your Contact Information]

---

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Real-time review analysis from e-commerce APIs
- [ ] Advanced NLP models (BERT, GPT)
- [ ] Comparison mode for multiple products
- [ ] Sentiment trend analysis over time
- [ ] Mobile app version
- [ ] User authentication and saved profiles

---

**⭐ If you find this project useful, please give it a star!**
