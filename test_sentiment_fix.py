
import sys
import os

# Add the current directory to sys.path to make sure we can import the modules
sys.path.append(os.getcwd())

from utils.aspect_analyzer import AspectAnalyzer

def test_sentiment_scoring():
    analyzer = AspectAnalyzer()
    
    test_cases = [
        ("The battery life is terrible - it barely lasts 3 hours", "Battery Life", 0.1),
        ("Customer service was completely unhelpful", "Customer Service", 0.1),
        ("Performance has been a nightmare", "Performance", 0.1)
    ]
    
    print(f"{'Review':<60} | {'Aspect':<20} | {'Score':<10} | {'Expected':<10} | {'Status'}")
    print("-" * 120)
    
    for review, aspect, expected_score in test_cases:
        scores = analyzer.analyze_aspects(review)
        actual_score = scores.get(aspect, 0.5)
        
        # We'll consider it a pass if it's within 0.15 of the expected score for now, 
        # but the goal is to get it very close to the expected low score.
        # The user wants < 0.45 for weaknesses.
        
        status = "PASS" if abs(actual_score - expected_score) < 0.2 else "FAIL"
        if actual_score > 0.65 and expected_score < 0.4:
             status = "CRITICAL FAIL (Inverted)"
             
        print(f"{review[:57]:<60} | {aspect:<20} | {actual_score:<10.2f} | {expected_score:<10.2f} | {status}")

if __name__ == "__main__":
    test_sentiment_scoring()
