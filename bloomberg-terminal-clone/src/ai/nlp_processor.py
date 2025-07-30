# src/ai/nlp_processor.py
import re
from typing import Dict, List, Tuple

class NLPProcessor:
    def __init__(self):
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BABA', 'UBER']
        self.query_patterns = {
            'price': r'(?:price|cost|value)\s+(?:of\s+)?(\w+)',
            'news': r'news\s+(?:for\s+|about\s+)?(\w+)',
            'prediction': r'(?:predict|forecast|future)\s+(?:price\s+)?(?:of\s+)?(\w+)',
            'analysis': r'(?:analyze|analysis)\s+(\w+)',
            'compare': r'compare\s+(\w+)\s+(?:and|with|to)\s+(\w+)'
        }
    
    def parse_query(self, query: str) -> Dict:
        """Parse natural language query and extract intent and entities"""
        query = query.lower().strip()
        
        result = {
            'intent': 'unknown',
            'entities': [],
            'symbols': [],
            'original_query': query
        }
        
        # Extract stock symbols
        symbols_found = []
        for symbol in self.stock_symbols:
            if symbol.lower() in query:
                symbols_found.append(symbol)
        
        result['symbols'] = symbols_found
        
        # Determine intent
        for intent, pattern in self.query_patterns.items():
            match = re.search(pattern, query)
            if match:
                result['intent'] = intent
                result['entities'] = list(match.groups())
                break
        
        # Additional intent detection
        if 'market' in query and ('overview' in query or 'summary' in query):
            result['intent'] = 'market_overview'
        elif 'trending' in query or 'popular' in query:
            result['intent'] = 'trending'
        elif 'portfolio' in query:
            result['intent'] = 'portfolio'
        
        return result
    
    def generate_response_template(self, intent: str, entities: List[str]) -> str:
        """Generate response template based on intent"""
        templates = {
            'price': "The current price of {symbol} is ${price:.2f}",
            'news': "Here are the latest news for {symbol}:",
            'prediction': "Based on analysis, {symbol} is predicted to {direction}",
            'market_overview': "Here's the current market overview:",
            'trending': "Here are the trending stocks:",
            'unknown': "I can help you with stock prices, news, predictions, and market analysis."
        }
        
        return templates.get(intent, templates['unknown'])