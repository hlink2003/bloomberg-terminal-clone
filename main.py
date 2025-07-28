# main.py - Optimized Bloomberg Terminal Layout
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append('src')

from data.data_fetcher import MarketDataFetcher
from data.news_fetcher import NewsDataFetcher

# Page config
st.set_page_config(
    page_title="Luther Terminal",
    page_icon="👊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize data fetchers
@st.cache_resource
def init_data_fetchers():
    return MarketDataFetcher(), NewsDataFetcher()

market_fetcher, news_fetcher = init_data_fetchers()

# Professional Bloomberg CSS
st.markdown("""
<style>
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Override Streamlit defaults */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Bloomberg color scheme */
    :root {
        --bloomberg-orange: #FF6D00;
        --bloomberg-dark: #1C1C1C;
        --bloomberg-darker: #0F0F0F;
        --bloomberg-green: #4CAF50;
        --bloomberg-red: #F44336;
        --bloomberg-blue: #2196F3;
        --bloomberg-text: #FFFFFF;
        --bloomberg-border: #404040;
    }
    
    /* Main terminal styling */
    .stApp {
        background-color: var(--bloomberg-darker) !important;
    }
    
    /* Header bar */
    .terminal-header {
        background: linear-gradient(135deg, var(--bloomberg-orange), #FF8A50);
        color: white;
        padding: 15px 25px;
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        margin: 0;
        box-shadow: 0 4px 12px rgba(255, 109, 0, 0.3);
        border-bottom: 3px solid #CC5500;
    }
    
    /* Status bar */
    .status-bar {
        background: var(--bloomberg-dark);
        color: var(--bloomberg-green);
        padding: 8px 25px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        border-bottom: 1px solid var(--bloomberg-border);
        display: flex;
        justify-content: space-between;
    }
    
    /* Main grid container */
    .terminal-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 12px;
        padding: 12px;
        height: calc(100vh - 120px);
        background: var(--bloomberg-darker);
    }
    
    /* Panel styling */
    .terminal-panel {
        background: linear-gradient(145deg, var(--bloomberg-dark), #2A2A2A);
        border: 2px solid var(--bloomberg-border);
        border-radius: 8px;
        padding: 20px;
        overflow-y: auto;
        position: relative;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .panel-header {
        color: var(--bloomberg-orange);
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--bloomberg-border);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Market data styling */
    .market-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #333;
        font-family: 'Courier New', monospace;
    }
    
    .symbol {
        color: var(--bloomberg-blue);
        font-weight: bold;
        font-size: 14px;
    }
    
    .price {
        color: var(--bloomberg-text);
        font-size: 14px;
    }
    
    .change-positive {
        color: var(--bloomberg-green);
        font-weight: bold;
    }
    
    .change-negative {
        color: var(--bloomberg-red);
        font-weight: bold;
    }
    
    .change-neutral {
        color: #999;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        color: var(--bloomberg-orange);
        font-size: 18px;
    }
    
    .spinner {
        border: 4px solid #333;
        border-top: 4px solid var(--bloomberg-orange);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin-right: 15px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for caching
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.market_data = None
    st.session_state.trending_data = None

# Header
current_time = datetime.now()
market_status = "MARKET OPEN" if 9 <= current_time.hour < 16 and current_time.weekday() < 5 else "MARKET CLOSED"

st.markdown("""
<div class="terminal-header">
    👊 LUTHER TERMINAL - THAT BOY LUTH EDITION
</div>
<div class="status-bar">
    <span>""" + market_status + """ | """ + current_time.strftime("%Y-%m-%d %H:%M:%S") + """</span>
    <span>REAL-TIME DATA | AI POWERED</span>
</div>
""", unsafe_allow_html=True)

# Simple data loading with progress
def load_basic_data():
    """Load essential data only"""
    try:
        # Just get a few key symbols
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
        data = {}
        
        for symbol in symbols:
            info = market_fetcher.get_stock_info(symbol)
            if info:
                data[symbol] = {
                    'price': info.get('current_price', 0),
                    'change': info.get('current_price', 0) - info.get('52_week_low', 0)
                }
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

# Load data with caching
if not st.session_state.data_loaded:
    with st.spinner("Loading Luther Terminal..."):
        st.session_state.trending_data = load_basic_data()
        st.session_state.data_loaded = True

# Create the main grid layout
col1, col2 = st.columns(2)

with col1:
    # TOP LEFT: Market Overview
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-header">📊 Market Overview</div>
    """, unsafe_allow_html=True)
    
    # Sample market data (you can enhance this)
    sample_indices = {
        'S&P 500': {'current': 5500, 'change_pct': 0.5},
        'DOW': {'current': 40000, 'change_pct': -0.2},
        'NASDAQ': {'current': 17000, 'change_pct': 1.2},
        'VIX': {'current': 15, 'change_pct': -2.1}
    }
    
    for name, data in sample_indices.items():
        change_class = "change-positive" if data['change_pct'] > 0 else "change-negative" if data['change_pct'] < 0 else "change-neutral"
        st.markdown(f"""
        <div class="market-item">
            <span class="symbol">{name}</span>
            <span class="price">{data['current']:.0f}</span>
            <span class="{change_class}">{data['change_pct']:+.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin: 20px 0; border-top: 1px solid #444;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🔥 Luther\'s Watchlist</div>', unsafe_allow_html=True)
    
    # Display loaded stock data
    if st.session_state.trending_data:
        for symbol, data in st.session_state.trending_data.items():
            change_class = "change-positive" if data['change'] > 0 else "change-negative"
            st.markdown(f"""
            <div class="market-item">
                <span class="symbol">{symbol}</span>
                <span class="price">${data['price']:.2f}</span>
                <span class="{change_class}">+{data['change']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # TOP RIGHT: Simple Chart
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-header">📈 Live Charts</div>
    """, unsafe_allow_html=True)
    
    # Simple chart placeholder
    if st.session_state.trending_data:
        symbols = list(st.session_state.trending_data.keys())
        prices = [data['price'] for data in st.session_state.trending_data.values()]
        
        fig = go.Figure(data=go.Bar(x=symbols, y=prices, marker_color='#FF6D00'))
        fig.update_layout(
            title="Portfolio Snapshot",
            plot_bgcolor='#0F0F0F',
            paper_bgcolor='#0F0F0F',
            font_color='white',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Second row
col3, col4 = st.columns(2)

with col3:
    # BOTTOM LEFT: News
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-header">📰 Luther's News Feed</div>
    """, unsafe_allow_html=True)
    
    # Mock news for now (loads instantly)
    mock_news = [
        {"title": "Tech Stocks Rally on Strong Earnings", "source": "Reuters", "time": "2h ago"},
        {"title": "Fed Signals Rate Cut Consideration", "source": "Bloomberg", "time": "4h ago"},
        {"title": "AI Stocks Lead Market Gains", "source": "CNBC", "time": "6h ago"},
        {"title": "Energy Sector Shows Strength", "source": "WSJ", "time": "8h ago"}
    ]
    
    for article in mock_news:
        st.markdown(f"""
        <div style="background: rgba(255, 109, 0, 0.1); border-left: 3px solid #FF6D00; padding: 10px; margin: 8px 0; border-radius: 4px;">
            <div style="color: white; font-weight: 600; font-size: 13px; margin-bottom: 4px;">
                {article['title'][:60]}...
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #888;">
                <span>{article['source']}</span>
                <span>{article['time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # BOTTOM RIGHT: AI Analytics
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-header">🤖 Luther.AI Analytics</div>
    """, unsafe_allow_html=True)
    
    # Market sentiment
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #333;">
        <span>Market Sentiment:</span>
        <span style="color: #4CAF50; font-weight: bold;">Positive</span>
    </div>
    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #333;">
        <span>AI Confidence:</span>
        <span>78%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick AI Chat
    st.markdown('<div style="color: #ff6b00; font-weight: bold; margin: 15px 0 10px 0;">💬 Quick Query</div>', unsafe_allow_html=True)
    
    with st.form("ai_query", clear_on_submit=True):
        query = st.text_input("Ask Luther.AI", placeholder="e.g., AAPL price", label_visibility="collapsed")
        submitted = st.form_submit_button("Ask", use_container_width=True)
        
        if submitted and query:
            if "aapl" in query.lower():
                response = f"AAPL: ${st.session_state.trending_data.get('AAPL', {}).get('price', 150):.2f}"
            elif "market" in query.lower():
                response = "Market is showing mixed signals with tech leading gains."
            else:
                response = "Ask me about stock prices or market conditions!"
                
            st.markdown(f'<div style="background: rgba(33, 150, 243, 0.1); border: 1px solid #2196F3; color: white; padding: 10px; border-radius: 4px; margin: 8px 0; font-size: 12px;">{response}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh button
if st.button("Refresh Data"):
    st.session_state.data_loaded = False
    st.rerun()

# Footer
st.markdown(f"""
<div style="text-align: center; margin-top: 20px; color: #666; font-size: 0.8rem;">
    Built by That Boy Luther | Last update: {datetime.now().strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)