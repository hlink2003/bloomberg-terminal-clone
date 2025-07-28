# src/data/news_fetcher.py
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List, Dict
import time

class NewsDataFetcher:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        
    def get_financial_news(self, query: str = "finance", limit: int = 20) -> List[Dict]:
        """Get general financial news"""
        if not self.news_api_key:
            return self._get_mock_news()
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'sortBy': 'publishedAt',
                'apiKey': self.news_api_key,
                'pageSize': limit,
                'language': 'en'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._format_news_data(data.get('articles', []))
        
        except Exception as e:
            print(f"Error fetching news: {e}")
            return self._get_mock_news()
    
    def get_stock_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Get news specific to a stock symbol"""
        if not self.news_api_key:
            return self._get_mock_stock_news(symbol)
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': f"{symbol} stock",
                'sortBy': 'publishedAt',
                'apiKey': self.news_api_key,
                'pageSize': limit,
                'language': 'en'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._format_news_data(data.get('articles', []))
        
        except Exception as e:
            print(f"Error fetching stock news for {symbol}: {e}")
            return self._get_mock_stock_news(symbol)
    
    def get_market_news(self, limit: int = 15) -> List[Dict]:
        """Get general market news"""
        queries = ["stock market", "NYSE", "NASDAQ", "S&P 500", "DOW"]
        all_news = []
        
        for query in queries:
            news = self.get_financial_news(query, limit=5)
            all_news.extend(news)
            time.sleep(0.2)  # Rate limiting
        
        # Remove duplicates and sort by date
        seen_urls = set()
        unique_news = []
        for article in all_news:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_news.append(article)
        
        return sorted(unique_news, key=lambda x: x['published_at'], reverse=True)[:limit]
    
    def get_sector_news(self, sector: str, limit: int = 10) -> List[Dict]:
        """Get news for a specific sector"""
        sector_queries = {
            'tech': 'technology stocks',
            'healthcare': 'healthcare stocks',
            'finance': 'financial stocks banking',
            'energy': 'energy stocks oil',
            'real_estate': 'real estate stocks REIT'
        }
        
        query = sector_queries.get(sector.lower(), f"{sector} stocks")
        return self.get_financial_news(query, limit)
    
    def _format_news_data(self, articles: List[Dict]) -> List[Dict]:
        """Format news data for consistent structure"""
        formatted_news = []
        
        for article in articles:
            formatted_article = {
                'title': article.get('title', 'No Title'),
                'description': article.get('description', 'No Description'),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published_at': article.get('publishedAt', ''),
                'author': article.get('author', 'Unknown'),
                'url_to_image': article.get('urlToImage', ''),
                'content': article.get('content', '')
            }
            formatted_news.append(formatted_article)
        
        return formatted_news
    
    def _get_mock_news(self) -> List[Dict]:
        """Mock news data for when API is not available"""
        return [
            {
                'title': 'Markets Rally as Tech Stocks Surge',
                'description': 'Technology stocks led market gains today with strong earnings reports.',
                'url': 'https://example.com/news1',
                'source': 'Financial Times',
                'published_at': datetime.now().isoformat(),
                'author': 'Financial Reporter',
                'url_to_image': '',
                'content': 'Technology stocks surged today following strong quarterly earnings...'
            },
            {
                'title': 'Federal Reserve Signals Interest Rate Decision',
                'description': 'The Fed hints at potential rate changes in upcoming meeting.',
                'url': 'https://example.com/news2',
                'source': 'Bloomberg',
                'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'author': 'Market Analyst',
                'url_to_image': '',
                'content': 'Federal Reserve officials indicated potential policy changes...'
            },
            {
                'title': 'Oil Prices Fluctuate on Global Supply Concerns',
                'description': 'Energy markets show volatility amid geopolitical tensions.',
                'url': 'https://example.com/news3',
                'source': 'Reuters',
                'published_at': (datetime.now() - timedelta(hours=4)).isoformat(),
                'author': 'Energy Correspondent',
                'url_to_image': '',
                'content': 'Oil prices experienced significant movements today...'
            }
        ]
    
    def _get_mock_stock_news(self, symbol: str) -> List[Dict]:
        """Mock stock-specific news"""
        return [
            {
                'title': f'{symbol} Reports Strong Quarterly Results',
                'description': f'{symbol} exceeded analyst expectations in latest earnings report.',
                'url': f'https://example.com/{symbol}-earnings',
                'source': 'MarketWatch',
                'published_at': datetime.now().isoformat(),
                'author': 'Stock Analyst',
                'url_to_image': '',
                'content': f'{symbol} announced quarterly results that surpassed expectations...'
            },
            {
                'title': f'Analyst Upgrades {symbol} Rating',
                'description': f'Major investment firm raises target price for {symbol}.',
                'url': f'https://example.com/{symbol}-upgrade',
                'source': 'CNBC',
                'published_at': (datetime.now() - timedelta(hours=6)).isoformat(),
                'author': 'Market Reporter',
                'url_to_image': '',
                'content': f'Investment analysts have upgraded their outlook for {symbol}...'
            }
        ]
    
    def analyze_news_sentiment(self, news_articles: List[Dict]) -> Dict:
        """Basic sentiment analysis of news articles"""
        try:
            from textblob import TextBlob
        except ImportError:
            return {'average_sentiment': 0, 'sentiment_label': 'Neutral', 'total_articles': 0}
        
        sentiments = []
        for article in news_articles:
            text = f"{article['title']} {article['description']}"
            blob = TextBlob(text)
            sentiments.append(blob.sentiment.polarity)
        
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
            
            return {
                'average_sentiment': avg_sentiment,
                'sentiment_label': sentiment_label,
                'total_articles': len(news_articles),
                'positive_articles': len([s for s in sentiments if s > 0.1]),
                'negative_articles': len([s for s in sentiments if s < -0.1]),
                'neutral_articles': len([s for s in sentiments if -0.1 <= s <= 0.1])
            }
        
        return {'average_sentiment': 0, 'sentiment_label': 'Neutral', 'total_articles': 0}

# Example usage
if __name__ == "__main__":
    news_fetcher = NewsDataFetcher()
    
    print("Market News:")
    market_news = news_fetcher.get_market_news(limit=5)
    for article in market_news:
        print(f"- {article['title']}")
        print(f"  Source: {article['source']}")
        print(f"  Published: {article['published_at']}")
        print()
    
    print("AAPL News:")
    aapl_news = news_fetcher.get_stock_news('AAPL', limit=3)
    for article in aapl_news:
        print(f"- {article['title']}")
    
    print("\nNews Sentiment Analysis:")
    sentiment = news_fetcher.analyze_news_sentiment(market_news)
    print(f"Overall sentiment: {sentiment['sentiment_label']}")
    print(f"Average score: {sentiment['average_sentiment']:.2f}")