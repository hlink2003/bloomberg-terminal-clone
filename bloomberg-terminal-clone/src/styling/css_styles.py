import streamlit as st

def apply_terminal_styles():
    """Apply Bloomberg terminal CSS styling with improved text visibility"""
    st.markdown("""
    <style>
        .main { background-color: #0F0F0F; color: #FFFFFF; }
        .stApp { background-color: #0F0F0F; }
        
        /* Force all text to be bright white */
        .stMarkdown, .stMarkdown p, .stMarkdown div {
            color: #FFFFFF !important;
        }
        
        .terminal-header {
            background: linear-gradient(90deg, #FF6600 0%, #FF8533 100%);
            color: white; padding: 15px; text-align: center; font-weight: bold;
            font-size: 28px; margin-bottom: 20px; border-radius: 5px;
        }
        .market-status {
            background-color: #1a1a1a; padding: 8px 15px; border-radius: 20px;
            color: #00ff00; font-size: 14px; display: inline-block; margin-left: 20px;
            border: 1px solid #00ff00;
        }
        .quadrant {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 2px solid #333; border-radius: 10px; padding: 20px;
            margin: 10px; height: 400px; overflow-y: auto;
            color: #FFFFFF !important;
        }
        .quadrant-title {
            color: #ff6600 !important; font-size: 20px; font-weight: bold;
            margin-bottom: 15px; border-bottom: 2px solid #ff6600;
            padding-bottom: 8px; text-transform: uppercase;
        }
        .metric-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%);
            padding: 15px; border-radius: 8px; margin: 8px 0;
            border-left: 4px solid #ff6600;
            color: #FFFFFF !important;
        }
        .metric-card strong {
            color: #00ff88 !important; /* Bright green for stock symbols */
            font-size: 16px;
        }
        .metric-card small {
            color: #CCCCCC !important; /* Light grey for volume/details */
        }
        .ticker-tape {
            background: linear-gradient(90deg, #000 0%, #1a1a1a 50%, #000 100%);
            color: #00ff00; padding: 10px; white-space: nowrap; overflow: hidden;
            animation: scroll 30s linear infinite; font-family: 'Courier New', monospace;
            border: 1px solid #333; margin-bottom: 20px;
        }
        @keyframes scroll {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* Fix Streamlit's default text colors */
        .element-container, .stMarkdown > div {
            color: #FFFFFF !important;
        }
        
        /* Style price changes more prominently */
        .price-positive {
            color: #00ff88 !important;
            font-weight: bold;
        }
        .price-negative {
            color: #ff4444 !important;
            font-weight: bold;
        }
        .price-neutral {
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)