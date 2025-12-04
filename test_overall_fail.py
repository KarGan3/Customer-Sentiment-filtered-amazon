
import sys
import os
import pandas as pd

# Add the current directory to sys.path
sys.path.append(os.getcwd())

import sentiment
from utils.aspect_analyzer import AspectAnalyzer

def test_overall_sentiment():
    # Load and train model first (as app.py does)
    print("Loading and training model...")
    try:
        df = sentiment.load_data()
        sentiment.train_model(df)
    except Exception as e:
        print(f"Failed to train model: {e}")
        return

    test_phrases = [
        "worst purchase I've ever made",
        "absolute garbage",
        "completely useless",
        "pathetic",
        "a joke",
        "nightmare",
        "disaster",
        "zero stars if I could",
        "worst purchase I've ever made. absolute garbage. completely useless. pathetic. a joke. nightmare. disaster. zero stars if I could"
    ]
    
    print(f"{'Phrase':<40} | {'ML Label':<10} | {'Rule Score':<10} | {'Final Label':<10} | {'Status'}")
    print("-" * 100)
    
    analyzer = AspectAnalyzer()
    
    for phrase in test_phrases:
        # ML Prediction
        ml_label, probabilities = sentiment.predict_sentiment_with_probabilities(phrase)
        
        # Rule-based Score
        rule_score = analyzer.analyze_overall_sentiment(phrase)
        
        # Hybrid Logic (Simulation of app.py)
        final_label = ml_label
        if rule_score < 0.4 and ml_label == 'positive':
            final_label = 'negative (OVERRIDE)'
        elif rule_score > 0.8 and ml_label == 'negative':
            final_label = 'positive (OVERRIDE)'
            
        status = "PASS" if "negative" in final_label else "FAIL"
        if "garbage" in phrase and "positive" in final_label:
             status = "CRITICAL FAIL"
             
        print(f"{phrase[:37]:<40} | {ml_label:<10} | {rule_score:<10.2f} | {final_label:<10} | {status}")

if __name__ == "__main__":
    test_overall_sentiment()
