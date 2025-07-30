import streamlit as st
from datetime import datetime
import yfinance as yf

def render_interactive_header():
    """Render the main terminal header with working Mag 7 quick access buttons"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    market_hour = datetime.now().hour
    market_status = "MARKET OPEN" if 9 <= market_hour <= 16 else "MARKET CLOSED"
    status_color = "#00ff00" if "OPEN" in market_status else "#ff6600"

    # Header
    st.markdown(f"""
    <div class="terminal-header">
        LUTHER TERMINAL - THAT BOY LUTH EDITION
        <span class="market-status" style="color: {status_color}; border-color: {status_color};">
            {market_status}
        </span>
        <div style="font-size: 14px; margin-top: 8px; opacity: 0.8;">
            Last Updated: {current_time}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock search section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
                border: 2px solid #ff6600; border-radius: 10px; padding: 15px;
                margin: 10px 0 20px 0; text-align: center;">
        <strong style="color: #ff6600; font-size: 18px;">🔍 STOCK LOOKUP</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Search input
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Check if a button was clicked (using separate session state keys)
        selected_symbol = None
        
        # Mag 7 Quick Access Buttons BEFORE the text input
        st.markdown('<div style="margin-bottom: 10px;"><small style="color: #ff6600;">📊 MAG 7 QUICK ACCESS:</small></div>', unsafe_allow_html=True)
        
        # Create 7 columns for Mag 7 stocks
        col_msft, col_aapl, col_googl, col_amzn, col_nvda, col_meta, col_tsla = st.columns(7)
        
        # Microsoft
        with col_msft:
            if st.button("MSFT", key="mag7_msft", help="Microsoft", use_container_width=True):
                st.session_state.selected_stock = "MSFT"
                st.session_state.chart_symbol = "MSFT"
                selected_symbol = "MSFT"
        
        # Apple
        with col_aapl:
            if st.button("AAPL", key="mag7_aapl", help="Apple", use_container_width=True):
                st.session_state.selected_stock = "AAPL"
                st.session_state.chart_symbol = "AAPL"
                selected_symbol = "AAPL"
        
        # Google/Alphabet
        with col_googl:
            if st.button("GOOGL", key="mag7_googl", help="Google/Alphabet", use_container_width=True):
                st.session_state.selected_stock = "GOOGL"
                st.session_state.chart_symbol = "GOOGL"
                selected_symbol = "GOOGL"
        
        # Amazon
        with col_amzn:
            if st.button("AMZN", key="mag7_amzn", help="Amazon", use_container_width=True):
                st.session_state.selected_stock = "AMZN"
                st.session_state.chart_symbol = "AMZN"
                selected_symbol = "AMZN"
        
        # NVIDIA
        with col_nvda:
            if st.button("NVDA", key="mag7_nvda", help="NVIDIA", use_container_width=True):
                st.session_state.selected_stock = "NVDA"
                st.session_state.chart_symbol = "NVDA"
                selected_symbol = "NVDA"
        
        # Meta
        with col_meta:
            if st.button("META", key="mag7_meta", help="Meta Platforms", use_container_width=True):
                st.session_state.selected_stock = "META"
                st.session_state.chart_symbol = "META"
                selected_symbol = "META"
        
        # Tesla
        with col_tsla:
            if st.button("TSLA", key="mag7_tsla", help="Tesla", use_container_width=True):
                st.session_state.selected_stock = "TSLA"
                st.session_state.chart_symbol = "TSLA"
                selected_symbol = "TSLA"
        
        # Get the default value for text input
        default_value = st.session_state.get("selected_stock", "")
        
        # Stock symbol input - use the selected stock as default
        symbol_input = st.text_input(
            "",
            value=default_value,
            placeholder="Enter stock symbol (e.g., AAPL, TSLA, GOOGL)",
            key="stock_search",
            help="Type any stock symbol to get real-time data"
        ).upper().strip()
        
        # If symbol was typed manually, update chart symbol
        if symbol_input and symbol_input != default_value:
            st.session_state.chart_symbol = symbol_input
            st.session_state.selected_stock = symbol_input
    
    # Use the symbol from input or button selection
    symbol_to_display = selected_symbol or symbol_input
    
    # Display stock info if symbol entered
    if symbol_to_display and len(symbol_to_display) > 0:
        try:
            ticker = yf.Ticker(symbol_to_display)
            info = ticker.info
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty and info:
                current_price = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current_price)
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                change_color = "#00ff88" if change >= 0 else "#ff4444"
                change_sign = "+" if change >= 0 else ""
                
                company_name = info.get('longName', symbol_to_display)
                market_cap = info.get('marketCap', 0)
                volume = hist['Volume'].sum() if not hist['Volume'].empty else 0
                
                # Format market cap
                if market_cap > 1e12:
                    market_cap_str = f"${market_cap/1e12:.2f}T"
                elif market_cap > 1e9:
                    market_cap_str = f"${market_cap/1e9:.2f}B"
                elif market_cap > 1e6:
                    market_cap_str = f"${market_cap/1e6:.2f}M"
                else:
                    market_cap_str = f"${market_cap:,.0f}"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
                            border: 2px solid {change_color}; border-radius: 10px; padding: 20px;
                            margin: 15px 0; text-align: center;">
                    <h2 style="color: #00ff88; margin: 0;">{symbol_to_display}</h2>
                    <h4 style="color: #FFFFFF; margin: 5px 0;">{company_name}</h4>
                    <h1 style="color: #FFFFFF; margin: 10px 0;">${current_price:.2f}</h1>
                    <h3 style="color: {change_color}; margin: 5px 0;">
                        {change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)
                    </h3>
                    <div style="color: #CCCCCC; margin-top: 15px;">
                        Market Cap: {market_cap_str} | Volume: {volume:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Store the symbol for charts
                st.session_state.chart_symbol = symbol_to_display
                
        except Exception as e:
            st.error(f"❌ Could not find data for '{symbol_to_display}'. Please check the symbol and try again.")
    
    return symbol_to_display

def render_ticker_tape(watchlist_data):
    """Render scrolling ticker tape with stock prices"""
    if not watchlist_data:
        return
        
    ticker_items = []
    for symbol, data in watchlist_data.items():
        change_sign = "+" if data['change'] >= 0 else ""
        ticker_items.append(f"{symbol}: ${data['price']:.2f} ({change_sign}{data['change_pct']:.2f}%)")

    ticker_text = " • ".join(ticker_items)
    st.markdown(f"""
    <div class="ticker-tape">
        LUTHER TERMINAL LIVE • {ticker_text} • THAT BOY LUTH TRADING • 
    </div>
    """, unsafe_allow_html=True)