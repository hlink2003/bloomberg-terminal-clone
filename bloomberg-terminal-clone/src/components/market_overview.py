import streamlit as st
import sys
import yfinance as yf
sys.path.append('src')

def render_market_overview(market_data, watchlist_data):
    """Render market overview quadrant with real data"""
    st.markdown('<div class="quadrant"><div class="quadrant-title">Market Overview</div>', unsafe_allow_html=True)
    
    # VTI Total Market section
    try:
        vti_ticker = yf.Ticker('VTI')
        vti_info = vti_ticker.info
        vti_hist = vti_ticker.history(period="1d", interval="1m")
        
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
        st.error(f"VTI Error: {e}")
    
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
                        key=f"index_{symbol}_{name.replace(' ', '_')}", 
                        help=f"Click to view {name} chart",
                        use_container_width=True):
                st.session_state.chart_symbol = symbol
                st.session_state.selected_stock = symbol
                st.rerun()
    else:
        st.warning("⚠️ Market indices not loaded")
    
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
    else:
        st.warning("⚠️ Watchlist not loaded")
    
    st.markdown('</div>', unsafe_allow_html=True)