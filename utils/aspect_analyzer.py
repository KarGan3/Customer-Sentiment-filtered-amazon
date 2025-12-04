import re
from collections import defaultdict

class AspectAnalyzer:
    """Extract and analyze product aspects from reviews with proper sentiment scoring"""
    
    def __init__(self):
        # Define aspect keywords
        self.aspect_keywords = {
            'Battery Life': ['battery', 'charge', 'charging', 'power', 'lasting'],
            'Performance': ['fast', 'slow', 'speed', 'performance', 'lag', 'smooth', 'responsive'],
            'Shipping': ['shipping', 'delivery', 'arrived', 'package', 'delayed'],
            'Build Quality': ['quality', 'build', 'sturdy', 'durable', 'broken', 'solid', 'plasticky', 'flimsy'],
            'Value for Money': ['price', 'worth', 'value', 'expensive', 'cheap', 'affordable', 'paid'],
            'Customer Service': ['service', 'support', 'help', 'response', 'customer', 'helpful', 'unhelpful'],
            'Design': ['design', 'look', 'aesthetic', 'style', 'beautiful', 'ugly'],
            'Ease of Use': ['easy', 'simple', 'intuitive', 'complicated', 'user-friendly']
        }
        
        # Sentiment words with intensity levels
        self.strong_positive = ['great', 'excellent', 'amazing', 'incredible', 'fantastic', 
                                'love', 'perfect', 'outstanding', 'best', 'superb']
        
        self.positive = ['good', 'nice', 'solid', 'reliable', 'pleased', 
                        'satisfied', 'works', 'clear', 'bright', 'recommend']
        
        self.neutral = ['okay', 'fine', 'decent', 'average', 'acceptable', 'standard']
        
        self.critical = ['unhelpful', 'questionable', 'mediocre', 'subpar', 'struggles', 
                        'issues', 'weak', 'below average', 'poor']
        
        self.negative = ['terrible', 'awful', 'horrible', 'worst', 'pathetic', 'useless', 
                        'nightmare', 'garbage', 'disappointed', 'broken', 'failed', 'cheap', 'junk',
                        'disaster', 'joke', 'zero']
        
        # Negation words (TRUE negations only - words that flip meaning)
        self.negation_words = ['not', 'no', 'never', 'neither', 'nor', 'none', "n't"]
        
        # Qualifying/contrasting words
        self.qualifiers = ['but', 'though', 'however', 'although', 'yet', 'still', 'just']
    
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
                score = self._calculate_aspect_sentiment(review_lower, keywords, review_text)
                aspect_scores[aspect] = score
            else:
                # Default neutral score if not mentioned
                aspect_scores[aspect] = 0.5
        
        return aspect_scores
    
    def _calculate_aspect_sentiment(self, review_text, aspect_keywords, original_text):
        """Calculate sentiment score for specific aspect (0.0 = negative, 1.0 = positive)"""
        # Find sentences containing aspect keywords
        sentences = re.split(r'[.!?]+', review_text)
        relevant_sentences = [
            s.strip() for s in sentences 
            if any(keyword in s for keyword in aspect_keywords) and s.strip()
        ]
        
        if not relevant_sentences:
            return 0.5  # Neutral if no relevant context
        
        total_score = 0.0
        sentence_count = 0
        
        for sentence in relevant_sentences:
            words = sentence.split()
            sentence_score = 0.5  # Start neutral
            sentiment_found = False
            
            # Check for negative words (Strongest signal first)
            if any(word in sentence for word in self.negative):
                sentence_score = 0.1
                sentiment_found = True
            # Check for critical/qualifying words
            elif any(word in sentence for word in self.critical):
                sentence_score = 0.2  # Mid-low score
                sentiment_found = True
            # Check for neutral words
            elif any(word in sentence for word in self.neutral):
                sentence_score = 0.55
                sentiment_found = True
            # Check for strong positive words
            elif any(word in sentence for word in self.strong_positive):
                sentence_score = 0.9
                sentiment_found = True
            # Check for positive words
            elif any(word in sentence for word in self.positive):
                sentence_score = 0.75
                sentiment_found = True
            
            # Handle negation - flip the score
            has_negation = any(neg in sentence for neg in self.negation_words)
            if has_negation and sentiment_found:
                # Flip around 0.5
                sentence_score = 1.0 - sentence_score
            
            # Handle qualifiers - reduce score slightly
            has_qualifier = any(qual in sentence for qual in self.qualifiers)
            if has_qualifier and sentence_score > 0.5:
                sentence_score -= 0.15  # Reduce positive scores
            elif has_qualifier and sentence_score < 0.5:
                sentence_score += 0.05  # Slightly increase negative scores
            
            total_score += sentence_score
            sentence_count += 1
        
        # Average the scores
        final_score = total_score / sentence_count if sentence_count > 0 else 0.5
        
        # DEBUG
        aspect_name = aspect_keywords[0] if aspect_keywords else "unknown"
        print(f"DEBUG [{aspect_name}]: final_score={final_score:.2f}, sentences={len(relevant_sentences)}")
        for i, sent in enumerate(relevant_sentences[:2]):
            print(f"  Sentence {i+1}: {sent[:80]}")
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, final_score))
    
    def extract_key_phrases(self, review_text, aspect):
        """Extract key phrases related to specific aspect"""
        keywords = self.aspect_keywords.get(aspect, [])
        
        sentences = re.split(r'[.!?]+', review_text)
        relevant_phrases = [
            s.strip() for s in sentences 
            if any(keyword in s.lower() for keyword in keywords) and s.strip()
        ]
        
        return relevant_phrases[:3]  # Return top 3 relevant phrases

    def analyze_overall_sentiment(self, review_text):
        """
        Calculate overall sentiment score based on rules (0.0 = negative, 1.0 = positive).
        Useful for validating/overriding ML model predictions.
        """
        # Treat the whole text as one "aspect" context
        # We pass a dummy keyword list that matches everything to reuse the logic, 
        # or better, just reuse the internal logic.
        
        # Let's reuse _calculate_aspect_sentiment but pass the whole text and a dummy keyword that is guaranteed to be found if we want to use that method,
        # BUT _calculate_aspect_sentiment filters sentences based on keywords.
        # So we should duplicate the core logic or refactor. 
        # For safety and minimal refactoring risk, I'll adapt the core logic here for the whole text.
        
        sentences = re.split(r'[.!?]+', review_text)
        # Filter empty
        relevant_sentences = [s.strip() for s in sentences if s.strip()]
        
        if not relevant_sentences:
            return 0.5
            
        total_score = 0.0
        sentence_count = 0
        
        for sentence in relevant_sentences:
            sentence = sentence.lower()
            words = sentence.split()
            sentence_score = 0.55  # Start neutral (updated baseline)
            sentiment_found = False
            
            # Check for negative words (Strongest signal first)
            if any(word in sentence for word in self.negative):
                sentence_score = 0.1
                sentiment_found = True
            # Check for critical/qualifying words
            elif any(word in sentence for word in self.critical):
                sentence_score = 0.2
                sentiment_found = True
            # Check for neutral words
            elif any(word in sentence for word in self.neutral):
                sentence_score = 0.55
                sentiment_found = True
            # Check for strong positive words
            elif any(word in sentence for word in self.strong_positive):
                sentence_score = 0.9
                sentiment_found = True
            # Check for positive words
            elif any(word in sentence for word in self.positive):
                sentence_score = 0.75
                sentiment_found = True
            
            # Handle negation
            has_negation = any(neg in sentence for neg in self.negation_words)
            if has_negation and sentiment_found:
                sentence_score = 1.0 - sentence_score
            
            # Handle qualifiers
            has_qualifier = any(qual in sentence for qual in self.qualifiers)
            if has_qualifier and sentence_score > 0.5:
                sentence_score -= 0.15
            elif has_qualifier and sentence_score < 0.5:
                sentence_score += 0.05
            
            total_score += sentence_score
            sentence_count += 1
            
        final_score = total_score / sentence_count if sentence_count > 0 else 0.5
        return max(0.0, min(1.0, final_score))
