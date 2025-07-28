# src/data/data_fetcher.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import os
from typing import Dict, List, Optional
import time

class MarketDataFetcher:
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.cache = {}
        
    def get_stock_data(self, symbol: str, period: str = "1d", interval: str = "1m") -> pd.DataFrame:
        """
        Fetch real-time stock data
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            # Add technical indicators
            data['MA_20'] = data['Close'].rolling(window=20).mean()
            data['MA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self._calculate_rsi(data['Close'])
            
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple stocks"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_stock_data(symbol)
            time.sleep(0.1)  # Rate limiting
        return results
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get company information and key metrics"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract key metrics
            key_metrics = {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'current_price': info.get('currentPrice', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0)
            }
            
            return key_metrics
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {}
    
    def get_trending_stocks(self) -> List[str]:
        """Get trending stocks (using predefined list for now)"""
        # In a real implementation, you'd fetch this from a financial API
        trending = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
        return trending
    
    def get_market_overview(self) -> Dict:
        """Get market indices overview"""
        indices = {
            'S&P 500': '^GSPC',
            'DOW': '^DJI',
            'NASDAQ': '^IXIC',
            'VIX': '^VIX'
        }
        
        overview = {}
        for name, symbol in indices.items():
            data = self.get_stock_data(symbol, period="2d", interval="1d")
            if not data.empty:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-2] if len(data) > 1 else current
                change = current - previous
                change_pct = (change / previous) * 100
                
                overview[name] = {
                    'symbol': symbol,
                    'current': current,
                    'change': change,
                    'change_pct': change_pct
                }
        
        return overview
    
    def search_stocks(self, query: str) -> List[Dict]:
        """Search for stocks by name or symbol"""
        # Simple implementation - in production, use a proper search API
        common_stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
            {'symbol': 'NFLX', 'name': 'Netflix Inc.'}
        ]
        
        query = query.upper()
        results = []
        for stock in common_stocks:
            if query in stock['symbol'] or query in stock['name'].upper():
                results.append(stock)
        
        return results
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def get_crypto_data(self, symbol: str) -> pd.DataFrame:
        """Get cryptocurrency data"""
        try:
            crypto_symbol = f"{symbol}-USD"
            return self.get_stock_data(crypto_symbol)
        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    
    # Test the fetcher
    print("Market Overview:")
    overview = fetcher.get_market_overview()
    for name, data in overview.items():
        print(f"{name}: {data['current']:.2f} ({data['change_pct']:+.2f}%)")
    
    print("\nStock Info for AAPL:")
    info = fetcher.get_stock_info('AAPL')
    print(f"Company: {info['company_name']}")
    print(f"Price: ${info['current_price']:.2f}")
    print(f"Market Cap: ${info['market_cap']:,}")