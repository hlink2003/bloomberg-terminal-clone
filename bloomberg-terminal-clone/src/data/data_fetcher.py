import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests

class DynamicStockFetcher:
    def __init__(self):
        # Fallback lists in case APIs fail
        self.fallback_indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC', 
            'DOW': '^DJI',
            'VTI (Total Market)': 'VTI',
            'VIX': '^VIX'
        }
        
        self.fallback_popular = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'UBER', 'BABA']

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_sp500_components(_self):
        """Fetch S&P 500 component stocks dynamically"""
        try:
            # Wikipedia has a regularly updated list of S&P 500 companies
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(url)
            sp500_table = tables[0]
            symbols = sp500_table['Symbol'].tolist()
            return symbols[:50]  # Return top 50 for performance
        except:
            return _self.fallback_popular

    @st.cache_data(ttl=3600)
    def get_nasdaq100_components(_self):
        """Fetch NASDAQ 100 component stocks"""
        try:
            url = "https://en.wikipedia.org/wiki/Nasdaq-100"
            tables = pd.read_html(url)
            nasdaq_table = tables[4]  # Usually the 5th table
            symbols = nasdaq_table['Ticker'].tolist()
            return symbols[:30]  # Return top 30
        except:
            return _self.fallback_popular

    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def get_trending_stocks(_self):
        """Get trending stocks from Yahoo Finance"""
        try:
            # Yahoo Finance trending tickers
            import yfinance as yf
            # Get some popular ETFs and indices to find trending stocks
            trending_symbols = []
            
            # Check volume leaders from major exchanges
            volume_leaders = ['AAPL', 'TSLA', 'NVDA', 'AMD', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX', 'SPY']
            
            # Get their info and sort by volume
            volume_data = []
            for symbol in volume_leaders:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    volume = info.get('volume', 0)
                    if volume > 0:
                        volume_data.append((symbol, volume))
                except:
                    continue
            
            # Sort by volume and return top performers
            volume_data.sort(key=lambda x: x[1], reverse=True)
            trending_symbols = [symbol for symbol, volume in volume_data[:10]]
            
            return trending_symbols if trending_symbols else _self.fallback_popular
            
        except:
            return _self.fallback_popular

    @st.cache_data(ttl=3600)
    def get_sector_leaders(_self):
        """Get leading stocks from each major sector"""
        sector_leaders = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META'],
            'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'MRK'],
            'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB'],
            'Consumer': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE'],
            'Industrial': ['BA', 'CAT', 'GE', 'LMT', 'UPS'],
            'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP'],
            'Materials': ['LIN', 'APD', 'SHW', 'FCX', 'NEM'],
            'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'SPG'],
            'Telecom': ['VZ', 'T', 'TMUS', 'CHTR', 'CMCSA']
        }
        
        # Flatten and return unique symbols
        all_leaders = []
        for sector_stocks in sector_leaders.values():
            all_leaders.extend(sector_stocks)
        
        return list(set(all_leaders))

    def get_dynamic_indices(self):
        """Get major market indices (these are fairly static)"""
        return self.fallback_indices

    def get_dynamic_watchlist(self, source='trending'):
        """Get dynamic watchlist based on different sources"""
        if source == 'trending':
            return self.get_trending_stocks()
        elif source == 'sp500':
            return self.get_sp500_components()[:10]  # Top 10
        elif source == 'nasdaq':
            return self.get_nasdaq100_components()[:10]
        elif source == 'sectors':
            leaders = self.get_sector_leaders()
            return leaders[:15]  # Top 15 sector leaders
        else:
            return self.fallback_popular

# Updated data fetcher functions
@st.cache_data(ttl=300)
def get_real_stock_data(symbol):
    """Fetch real stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d", interval="1m")
        
        if hist.empty:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
        
        return {
            'symbol': symbol,
            'price': current_price,
            'change': change,
            'change_pct': change_pct,
            'volume': hist['Volume'].sum(),
            'high': hist['High'].max(),
            'low': hist['Low'].min()
        }
    except:
        return None

@st.cache_data(ttl=300)
def get_market_indices():
    """Get major market indices dynamically"""
    fetcher = DynamicStockFetcher()
    indices = fetcher.get_dynamic_indices()
    
    data = {}
    for name, symbol in indices.items():
        result = get_real_stock_data(symbol)
        if result:
            data[name] = result
    return data

@st.cache_data(ttl=300)
def get_watchlist_data(source='trending'):
    """Get dynamic watchlist based on source"""
    fetcher = DynamicStockFetcher()
    watchlist = fetcher.get_dynamic_watchlist(source)
    
    data = {}
    for symbol in watchlist:
        result = get_real_stock_data(symbol)
        if result:
            data[symbol] = result
    return data

# Format functions remain the same
def format_price_change(change, change_pct):
    """Format price change with better, more visible colors"""
    if change >= 0:
        return f'<span style="color: #00ff88; font-weight: bold;">+${change:.2f} (+{change_pct:.2f}%)</span>'
    else:
        return f'<span style="color: #ff4444; font-weight: bold;">${change:.2f} ({change_pct:.2f}%)</span>'