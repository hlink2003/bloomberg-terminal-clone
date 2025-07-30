import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append('src')

# Import components
from styling.css_styles import apply_terminal_styles
from components.header import render_interactive_header, render_ticker_tape
from components.charts import render_interactive_charts
from components.news_feed import render_news_feed
from components.ai_analytics import render_ai_analytics

# Import dynamic data fetcher
from data.data_fetcher import get_real_stock_data, get_market_indices, get_watchlist_data

# Configure page
st.set_page_config(
    page_title="Luther Terminal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply styling
apply_terminal_styles()

# Render interactive header and get searched symbol
searched_symbol = render_interactive_header()

# Load market data
with st.spinner("Loading market data..."):
    try:
        market_data = get_market_indices()
        watchlist_data = get_watchlist_data('trending')
        
        st.success(f"✅ Loaded {len(market_data)} indices and {len(watchlist_data)} trending stocks")
        
    except Exception as e:
        st.error(f"❌ Data loading error: {e}")
        # Create fallback data
        market_data = {
            'S&P 500': {'symbol': '^GSPC', 'price': 5200.0, 'change': 15.0, 'change_pct': 0.29},
            'NASDAQ': {'symbol': '^IXIC', 'price': 16500.0, 'change': -25.0, 'change_pct': -0.15},
            'DOW': {'symbol': '^DJI', 'price': 38000.0, 'change': 80.0, 'change_pct': 0.21}
        }
        watchlist_data = {}

# Render ticker tape only if we have data
if watchlist_data:
    render_ticker_tape(watchlist_data)

# Create four quadrants
col1, col2 = st.columns(2)

with col1:
    # Market Overview - inline component since import might be an issue
    st.markdown('<div class="quadrant"><div class="quadrant-title">Market Overview</div>', unsafe_allow_html=True)
    
    # VTI Total Market section
    try:
        import yfinance as yf
        vti_ticker = yf.Ticker('VTI')
        vti_info = vti_ticker.info
        vti_hist = vti_ticker.history(period="1d", interval="5m")
        
        if not vti_hist.empty:
            current_price = vti_hist['Close'].iloc[-1]
            prev_close = vti_info.get('previousClose', current_price)
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            change_color = "#00ff88" if change >= 0 else "#ff4444"
            change_sign = "+" if change >= 0 else ""
            
            # Make VTI clickable
            if st.button(f"🏛️ VTI (Total Market) - ${current_price:.2f} {change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)", 
                        key="vti_button", 
                        help="Click to view VTI chart",
                        use_container_width=True):
                st.session_state.chart_symbol = 'VTI'
                st.session_state.selected_stock = 'VTI'
                st.rerun()
                
    except Exception as e:
        st.warning(f"VTI data unavailable: {e}")
    
    # Major indices
    if market_data:
        st.markdown('<div style="margin-top: 15px;"><strong style="color: #ff6600; font-size: 14px;">MAJOR INDICES:</strong></div>', unsafe_allow_html=True)
        
        for name, data in market_data.items():
            if 'VTI' in name:
                continue
                
            change_color = "#00ff88" if data['change'] >= 0 else "#ff4444"
            change_sign = "+" if data['change'] >= 0 else ""
            symbol = data['symbol']
            
            # Make each index clickable
            if st.button(f"{name}: ${data['price']:.2f} {change_sign}{data['change']:.2f} ({change_sign}{data['change_pct']:.2f}%)", 
                        key=f"index_{symbol}_{name.replace(' ', '_').replace('&', 'and')}", 
                        help=f"Click to view {name} chart",
                        use_container_width=True):
                st.session_state.chart_symbol = symbol
                st.session_state.selected_stock = symbol
                st.rerun()
    
    # Dynamic watchlist
    if watchlist_data:
        st.markdown('<div class="quadrant-title" style="margin-top: 20px; color: #ff6600;">🔥 TRENDING STOCKS</div>', unsafe_allow_html=True)
        
        # Show as clickable buttons in 2 columns
        cols = st.columns(2)
        for i, (symbol, data) in enumerate(list(watchlist_data.items())[:8]):  # Limit to 8 for space
            with cols[i % 2]:
                change_color = "#00ff88" if data['change'] >= 0 else "#ff4444"
                change_sign = "+" if data['change'] >= 0 else ""
                
                if st.button(f"{symbol}: ${data['price']:.2f} {change_sign}{data['change_pct']:.2f}%", 
                            key=f"watch_{symbol}_{i}", 
                            help=f"Click to view {symbol} chart",
                            use_container_width=True):
                    st.session_state.chart_symbol = symbol
                    st.session_state.selected_stock = symbol
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # News Feed
    render_news_feed()

with col2:
    # Interactive Charts
    render_interactive_charts()
    
    # AI Analytics
    render_ai_analytics()

# Add refresh button
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Refresh All Data", key="refresh_main"):
        st.cache_data.clear()
        st.rerun()

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; 
     background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); 
     color: #ff6600; padding: 8px; text-align: center; font-size: 12px; 
     border-top: 1px solid #333; z-index: 999;">
    Luther Terminal v2.0 | Interactive | Live Data | That Boy Luth © 2024
</div>
""", unsafe_allow_html=True)