# test_main.py - Simple Test Version
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Luther Terminal Test",
    page_icon="👊",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #0F0F0F; color: white; }
    .header { background: #FF6D00; color: white; padding: 20px; text-align: center; font-size: 24px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">👊 LUTHER TERMINAL - TEST VERSION</div>', unsafe_allow_html=True)

# Simple test
st.write("Testing basic functionality...")

try:
    # Test data fetching
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    st.success(f"✅ Data fetch working! AAPL price: ${info.get('currentPrice', 'N/A')}")
    
    # Test chart
    data = ticker.history(period="1d")
    if not data.empty:
        st.line_chart(data['Close'])
        st.success("✅ Charts working!")
    else:
        st.error("❌ Chart data empty")
        
except Exception as e:
    st.error(f"❌ Error: {e}")

st.write("If you see this message, Streamlit is working!")
st.write(f"Current time: {datetime.now()}")