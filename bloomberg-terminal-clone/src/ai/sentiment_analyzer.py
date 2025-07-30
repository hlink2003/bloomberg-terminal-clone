# src/ai/sentiment_analyzer.py
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import re

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

class SentimentAnalyzer:
    def __init__(self):
        self.financial_keywords = {
            'positive': ['bullish', 'surge', 'rally', 'growth', 'profit', 'gain', 'rise', 'strong', 'beat', 'upgrade'],
            'negative': ['bearish', 'crash', 'decline', 'loss', 'drop', 'fall', 'weak', 'miss', 'downgrade', 'recession']
        }
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        if not text:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
        
        # Clean text
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        if TEXTBLOB_AVAILABLE:
            # Use TextBlob for basic sentiment
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        else:
            # Fallback to keyword-based analysis
            polarity = self._keyword_sentiment(text)
            subjectivity = 0.5
        
        # Adjust for financial keywords
        polarity = self._adjust_for_financial_keywords(text, polarity)
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'confidence': abs(polarity)
        }
    
    def analyze_news_batch(self, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment for multiple news articles"""
        if not news_articles:
            return {'overall_sentiment': 'neutral', 'sentiment_score': 0, 'article_count': 0}
        
        sentiments = []
        detailed_results = []
        
        for article in news_articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            analysis = self.analyze_text(text)
            sentiments.append(analysis['polarity'])
            
            detailed_results.append({
                'title': article.get('title', ''),
                'sentiment': analysis['sentiment'],
                'polarity': analysis['polarity'],
                'confidence': analysis['confidence']
            })
        
        # Calculate overall metrics
        avg_sentiment = np.mean(sentiments)
        sentiment_std = np.std(sentiments)
        
        overall_label = 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral'
        
        return {
            'overall_sentiment': overall_label,
            'sentiment_score': avg_sentiment,
            'sentiment_std': sentiment_std,
            'article_count': len(news_articles),
            'positive_count': len([s for s in sentiments if s > 0.1]),
            'negative_count': len([s for s in sentiments if s < -0.1]),
            'neutral_count': len([s for s in sentiments if -0.1 <= s <= 0.1]),
            'detailed_results': detailed_results
        }
    
    def _keyword_sentiment(self, text: str) -> float:
        """Fallback sentiment analysis using keywords"""
        positive_score = sum(1 for word in self.financial_keywords['positive'] if word in text)
        negative_score = sum(1 for word in self.financial_keywords['negative'] if word in text)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0
        
        return (positive_score - negative_score) / max(total_words, 1)
    
    def _adjust_for_financial_keywords(self, text: str, base_polarity: float) -> float:
        """Adjust sentiment based on financial keywords"""
        adjustment = 0
        
        # Check for positive financial keywords
        for keyword in self.financial_keywords['positive']:
            if keyword in text:
                adjustment += 0.1
        
        # Check for negative financial keywords  
        for keyword in self.financial_keywords['negative']:
            if keyword in text:
                adjustment -= 0.1
        
        # Apply adjustment with dampening
        adjusted_polarity = base_polarity + (adjustment * 0.5)
        
        # Keep within bounds
        return max(-1, min(1, adjusted_polarity))