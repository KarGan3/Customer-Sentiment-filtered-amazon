import re
from collections import defaultdict

class AspectAnalyzer:
    """Extract and analyze product aspects from reviews"""
    
    def __init__(self):
        # Define aspect keywords
        self.aspect_keywords = {
            'Battery Life': ['battery', 'charge', 'charging', 'power', 'lasting'],
            'Performance': ['fast', 'slow', 'speed', 'performance', 'lag', 'smooth'],
            'Shipping': ['shipping', 'delivery', 'arrived', 'package', 'delayed'],
            'Build Quality': ['quality', 'build', 'sturdy', 'durable', 'broken', 'solid'],
            'Value for Money': ['price', 'worth', 'value', 'expensive', 'cheap', 'affordable'],
            'Customer Service': ['service', 'support', 'help', 'response', 'customer'],
            'Design': ['design', 'look', 'aesthetic', 'style', 'beautiful', 'ugly'],
            'Ease of Use': ['easy', 'simple', 'intuitive', 'complicated', 'user-friendly']
        }
        
        # Positive and negative indicators
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'love', 'perfect', 
            'best', 'awesome', 'fantastic', 'wonderful', 'outstanding'
        ]
        
        self.negative_words = [
            'bad', 'terrible', 'awful', 'hate', 'worst', 'poor', 
            'horrible', 'disappointing', 'useless', 'broken', 'issues'
        ]
    
    def analyze_aspects(self, review_text):
        """
        Analyze review for specific product aspects
        
        Returns:
            dict: Aspect names with sentiment scores (0-1)
        """
        review_lower = review_text.lower()
        aspect_scores = {}
        
        for aspect, keywords in self.aspect_keywords.items():
            # Check if aspect is mentioned
            aspect_mentioned = any(keyword in review_lower for keyword in keywords)
            
            if aspect_mentioned:
                # Calculate sentiment for this aspect
                score = self._calculate_aspect_sentiment(review_lower, keywords)
                aspect_scores[aspect] = score
            else:
                # Default neutral score if not mentioned
                aspect_scores[aspect] = 0.5
        
        return aspect_scores
    
    def _calculate_aspect_sentiment(self, review_text, aspect_keywords):
        """Calculate sentiment score for specific aspect"""
        # Find sentences containing aspect keywords
        sentences = re.split(r'[.!?]+', review_text)
        relevant_sentences = [
            s for s in sentences 
            if any(keyword in s for keyword in aspect_keywords)
        ]
        
        if not relevant_sentences:
            return 0.5  # Neutral if no relevant context
        
        # Count positive and negative words in relevant sentences
        positive_count = 0
        negative_count = 0
        
        for sentence in relevant_sentences:
            positive_count += sum(1 for word in self.positive_words if word in sentence)
            negative_count += sum(1 for word in self.negative_words if word in sentence)
        
        # Calculate score (0 = negative, 0.5 = neutral, 1 = positive)
        total = positive_count + negative_count
        if total == 0:
            return 0.5
        
        score = positive_count / total
        return score
    
    def extract_key_phrases(self, review_text, aspect):
        """Extract key phrases related to specific aspect"""
        review_lower = review_text.lower()
        keywords = self.aspect_keywords.get(aspect, [])
        
        sentences = re.split(r'[.!?]+', review_text)
        relevant_phrases = [
            s.strip() for s in sentences 
            if any(keyword in s.lower() for keyword in keywords)
        ]
        
        return relevant_phrases[:3]  # Return top 3 relevant phrases
