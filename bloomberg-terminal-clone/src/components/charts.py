import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_interactive_charts():
    """Render interactive charts that respond to stock search"""
    # Get the symbol from search or default to AAPL
    chart_symbol = st.session_state.get('chart_symbol', 'AAPL')
    
    st.markdown(f'<div class="quadrant"><div class="quadrant-title">Live Charts - {chart_symbol}</div>', unsafe_allow_html=True)
    
    # Chart period selector - make buttons smaller and in one row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("1D", key="chart_1d", use_container_width=True):
            st.session_state.chart_period = "1d"
    with col2:
        if st.button("5D", key="chart_5d", use_container_width=True):
            st.session_state.chart_period = "5d"
    with col3:
        if st.button("1M", key="chart_1m", use_container_width=True):
            st.session_state.chart_period = "1mo"
    with col4:
        if st.button("3M", key="chart_3m", use_container_width=True):
            st.session_state.chart_period = "3mo"
    
    chart_period = st.session_state.get('chart_period', '5d')
    
    try:
        ticker = yf.Ticker(chart_symbol)
        
        # Get interval based on period
        if chart_period == "1d":
            interval = "5m"  # 5-minute intervals for 1 day
        elif chart_period == "5d":
            interval = "15m"  # 15-minute intervals for 5 days
        elif chart_period == "1mo":
            interval = "1h"   # 1-hour intervals for 1 month
        else:
            interval = "1d"   # Daily intervals for longer periods
            
        chart_data = ticker.history(period=chart_period, interval=interval)
        
        if not chart_data.empty:
            # Create single chart (just price) for better fit
            fig = go.Figure()
            
            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=chart_data.index,
                    open=chart_data['Open'],
                    high=chart_data['High'],
                    low=chart_data['Low'],
                    close=chart_data['Close'],
                    increasing_line_color='#00ff88',
                    decreasing_line_color='#ff4444',
                    name='Price'
                )
            )
            
            fig.update_layout(
                plot_bgcolor='#0F0F0F',
                paper_bgcolor='#1a1a1a',
                font_color='white',
                height=280,  # Reduced height to fit better
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False,
                xaxis_rangeslider_visible=False,
                xaxis=dict(
                    gridcolor='#333', 
                    showgrid=True,
                    title=""
                ),
                yaxis=dict(
                    gridcolor='#333', 
                    showgrid=True, 
                    title='Price ($)',
                    side='right'  # Move y-axis to right side
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Technical indicators in a compact format
            if len(chart_data) >= 20:
                try:
                    sma_20 = chart_data['Close'].rolling(window=20).mean().iloc[-1]
                    rsi = calculate_rsi(chart_data['Close']).iloc[-1]
                    
                    # Get current price and change
                    current_price = chart_data['Close'].iloc[-1]
                    prev_price = chart_data['Close'].iloc[-2] if len(chart_data) > 1 else current_price
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                    change_color = "#00ff88" if change >= 0 else "#ff4444"
                    change_sign = "+" if change >= 0 else ""
                    
                    st.markdown(f"""
                    <div style="background: #2a2a2a; padding: 8px; border-radius: 5px; margin-top: 10px;">
                        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                            <div>
                                <strong style="color: #ff6600;">Current:</strong> 
                                <span style="color: #FFFFFF;">${current_price:.2f}</span>
                            </div>
                            <div>
                                <strong style="color: #ff6600;">Change:</strong> 
                                <span style="color: {change_color};">{change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)</span>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <div>
                                <strong style="color: #ff6600;">SMA20:</strong> 
                                <span style="color: #FFFFFF;">${sma_20:.2f}</span>
                            </div>
                            <div>
                                <strong style="color: #ff6600;">RSI:</strong> 
                                <span style="color: #FFFFFF;">{rsi:.1f}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    pass
                
        else:
            st.error("Unable to load chart data")
            
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_rsi(prices, window=14):
    """Calculate RSI technical indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi