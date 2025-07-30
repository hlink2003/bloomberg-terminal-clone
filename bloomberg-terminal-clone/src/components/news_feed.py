import streamlit as st

def render_news_feed():
    """Render news feed quadrant"""
    st.markdown("""
    <div class="quadrant">
        <div class="quadrant-title">Luther's News Feed</div>
        <div class="metric-card">
            <strong>Market Rally Continues</strong><br>
            <small>Tech stocks surge on AI optimism • 2 hours ago</small><br>
            <span style="color: #00ff00;">Sentiment: BULLISH</span>
        </div>
        <div class="metric-card">
            <strong>Fed Meeting Minutes</strong><br>
            <small>Central bank signals measured approach • 4 hours ago</small><br>
            <span style="color: #ffff00;">Sentiment: NEUTRAL</span>
        </div>
        <div class="metric-card">
            <strong>Earnings Season Preview</strong><br>
            <small>Tech earnings expected to beat estimates • 6 hours ago</small><br>
            <span style="color: #00ff00;">Sentiment: OPTIMISTIC</span>
        </div>
        <div class="metric-card">
            <strong>Energy Sector Update</strong><br>
            <small>Oil prices stabilize amid global tensions • 8 hours ago</small><br>
            <span style="color: #ffff00;">Sentiment: NEUTRAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)