# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.special import softmax

# Global variables to store the trained artifacts
_model = None
_vectorizer = None
_scaler = None
_label_encoder = None

def load_data(filepath='Customer_Sentiment_filtered_amazon.csv'):
    return pd.read_csv(filepath)

def train_model(df):
    global _model, _vectorizer, _scaler, _label_encoder
    
    print("Preparing data...")
    X = df['review_text']
    y = df['sentiment']

    # Encode labels
    _label_encoder = LabelEncoder()
    y_encoded = _label_encoder.fit_transform(y)

    # Vectorize text
    _vectorizer = TfidfVectorizer()
    X_vectorized = _vectorizer.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y_encoded, test_size=0.2, random_state=42)

    # Handle sparse matrices
    if hasattr(X_train, 'toarray'):
        X_train_dense = X_train.toarray()
        X_test_dense = X_test.toarray()
    else:
        X_train_dense = X_train
        X_test_dense = X_test

    # Scale features
    _scaler = StandardScaler(with_mean=False)
    X_train_scaled = _scaler.fit_transform(X_train_dense)
    X_test_scaled = _scaler.transform(X_test_dense)

    # Train Model (using the best params found previously: C=0.1, kernel='linear')
    print("Training SVM model...")
    _model = SVC(kernel='linear', C=0.1, random_state=42)
    _model.fit(X_train_scaled, y_train)
    
    print("Model training complete.")
    
    # Evaluate
    y_pred = _model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    
    return _model, _vectorizer, _scaler, _label_encoder, accuracy

def predict_sentiment(text_input):
    """Predicts sentiment for a single text input."""
    if _model is None:
        raise ValueError("Model not trained. Call train_model() first.")
        
    text_vectorized = _vectorizer.transform([text_input])
    
    if hasattr(text_vectorized, 'toarray'):
        text_dense = text_vectorized.toarray()
    else:
        text_dense = text_vectorized

    text_scaled = _scaler.transform(text_dense)
    prediction = _model.predict(text_scaled)
    predicted_sentiment = _label_encoder.inverse_transform(prediction)
    
    return predicted_sentiment[0]

def predict_sentiment_with_probabilities(text_input):
    """
    Enhanced prediction function that returns probabilities
    
    Returns:
        tuple: (predicted_label, probabilities_dict)
    """
    if _model is None:
        raise ValueError("Model not trained. Call train_model() first.")

    text_vectorized = _vectorizer.transform([text_input])
    
    if hasattr(text_vectorized, 'toarray'):
        text_dense = text_vectorized.toarray()
    else:
        text_dense = text_vectorized
    
    text_scaled = _scaler.transform(text_dense)
    
    # Get prediction
    prediction = _model.predict(text_scaled)
    predicted_sentiment = _label_encoder.inverse_transform(prediction)[0]
    
    # Get decision function scores (for SVM)
    if hasattr(_model, 'decision_function'):
        decision_scores = _model.decision_function(text_scaled)
        
        # Simple softmax approximation for decision scores
        if decision_scores.ndim == 1:
             # This shouldn't happen with 3 classes, but if it does:
             probabilities = softmax(np.array([-decision_scores[0], decision_scores[0]]))
        else:
             probabilities = softmax(decision_scores[0])
        
        # Map to sentiment labels
        prob_dict = {
            label: float(prob) 
            for label, prob in zip(_label_encoder.classes_, probabilities)
        }
    else:
        # Fallback if decision_function not available
        prob_dict = {
            'positive': 0.33,
            'neutral': 0.33,
            'negative': 0.34
        }
    
    return predicted_sentiment, prob_dict

def get_artifacts():
    """Returns the trained model and transformers."""
    return _model, _vectorizer, _scaler, _label_encoder

if __name__ == "__main__":
    # This block only runs when executing the script directly
    try:
        df = load_data()
        train_model(df)
        
        # Example usage
        test_review = "This product is amazing!"
        print(f"Test Review: '{test_review}' -> Sentiment: {predict_sentiment(test_review)}")
        
    except FileNotFoundError:
        print("Error: 'Customer_Sentiment_filtered_amazon.csv' not found.")