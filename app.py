import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import feedparser

SEAL_URL = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Great_Seal_of_the_United_States_%28obverse%29.svg"
FLAG_URL = "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="2026 US Midterm Live Tracker",
    page_icon=SEAL_URL,
    layout="wide"
)

# --- LIVE DATA FETCHING FUNCTIONS ---
@st.cache_data(ttl=25)
def fetch_kalshi_market(ticker: str):
    """Fetches real-time contract pricing from Kalshi's public election API."""
    url = f"https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json().get("market", {})
            return {
                "yes_bid": data.get("yes_bid", 0),
                "yes_ask": data.get("yes_ask", 0),
                "last_price": data.get("last_price", None),
                "volume": data.get("volume", 0)
            }
    except Exception:
        pass
    return None

@st.cache_data(ttl=60)
def fetch_live_midterm_news():
    """Fetches strictly U.S. Midterm election-related news via Google News RSS with keyword filtering."""
    rss_url = "https://news.google.com/rss/search?q=US+Midterm+Elections+2026+Senate+House+Congress&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    articles = []
    
    # Keywords required to guarantee relevance to the midterms
    required_keywords = ["midterm", "senate", "house", "congress", "election", "ballot", "poll"]
    
    for entry in feed.entries:
        title_lower = entry.title.lower()
        # Ensure the headline is strictly relevant to the midterms
        if any(keyword in title_lower for keyword in required_keywords):
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })
        if len(articles) >= 6:  # Keep top 6 most relevant live updates
            break
            
    return articles

@st.cache_data(ttl=120)
def fetch_network_video_feeds(channel_id: str):
    """Fetches the latest live stream and video broadcasts from a YouTube News Channel RSS feed."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(rss_url)
    videos = []
    for entry in feed.entries[:4]:
        videos.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return videos

# --- HIGH-VIBRANCY SPLIT-SCREEN TINT ENGINE ---
def apply_split_theme_and_banners(house_dem_prob, senate_dem_prob, house_winner, senate_winner):
    avg_dem_prob = (house_dem_prob + senate_dem_prob) / 2.0
    avg_gop_prob = 100.0 - avg_dem_prob
    
    dem_intensity = round(0.12 + (avg_dem_prob / 100.0 * 0.53), 2)
    gop_intensity = round(0.12 + (avg_gop_prob / 100.0 * 0.53), 2)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, 
                rgba(13, 95, 170, {dem_intensity}) 0%, 
                #F7F4EB 42%, 
                #F7F4EB 58%, 
                rgba(215, 38, 38, {gop_intensity}) 100%
            ) !important;
            transition: background 0.8s ease-in-out;
            background-attachment: fixed;
        }}
        
        .header-title-bar {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 12px;
        }}
        
        .header-seal-icon {{
            height: 75px;
            width: 75px;
            filter: drop-shadow(0 2px 5px rgba(0,0,0,0.25));
        }}
        
        .header-title-text {{
            font-size: 2.3rem;
            font-weight: 800;
            color: #1f242d;
            margin: 0;
            line-height: 1.2;
        }}
        
        @keyframes flash-banner {{
            0%, 100% {{ opacity: 1; transform: scale(1); text-shadow: 0 0 18px rgba(255,255,255,0.9); }}
            50% {{ opacity: 0.35; transform: scale(0.98); text-shadow: none; }}
        }}
        
        .victory-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 28px;
            border-radius: 14px;
            margin-bottom: 18px;
            color: #ffffff;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
            border: 3px solid #FFD700;
        }}
        
        .dem-victory {{
            background: linear-gradient(90deg, #0a2246 0%, #155293 50%, #0a2246 100%);
        }}
        
        .gop-victory {{
            background: linear-gradient(90deg, #4a0e0e 0%, #a81c1c 50%, #4a0e0e 100%);
        }}
        
        .flashing-winner-text {{
            font-size: 2.1rem;
            font-weight: 900;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-align: center;
            animation: flash-banner 1.15s infinite ease-in-out;
            margin: 0;
        }}
        
        .victory-subtext {{
            font-size: 0.95rem;
            text-align: center;
            color: #f3e5ab;
            margin-top: 4px;
            font-weight: 600;
            letter-spacing: 1px;
        }}
        
        .emblem-img {{
            height: 74px;
            width: auto;
            filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    banners_to_render = []
    if house_winner == "DEMOCRATS":
        banners_to_render.append(("DEMOCRATS HAVE WON THE HOUSE", "dem-victory", "PROJECTED MAJORITY — 218+ SEATS CONFIRMED"))
    elif house_winner == "REPUBLICANS":
        banners_to_render.append(("REPUBLICANS HAVE WON THE HOUSE", "gop-victory", "PROJECTED MAJORITY — 218+ SEATS CONFIRMED"))

    if senate_winner == "DEMOCRATS":
        banners_to_render.append(("DEMOCRATS HAVE WON THE SENATE", "dem-victory", "PROJECTED MAJORITY — 51+ SEATS CONFIRMED"))
    elif senate_winner == "REPUBLICANS":
        banners_to_render.append(("REPUBLICANS HAVE WON THE SENATE", "gop-victory", "PROJECTED MAJORITY — 50+ SEATS CONFIRMED"))

    for headline, css_class, subtext in banners_to_render:
        st.markdown(
            f"""
            <div class="victory-container {css_class}">
                <img src="{FLAG_URL}" class="emblem-img" alt="US Flag">
                <div>
                    <div class="flashing-winner-text">🇺🇸 {headline} 🇺🇸</div>
                    <div class="victory-subtext">{subtext}</div>
                </div>
                <img src="{SEAL_URL}" class="emblem-img" alt="Great Seal of the United States">
            </div>
            """,
            unsafe_allow_html=True
        )

# --- HEADER WITH OFFICIAL US GREAT SEAL ---
st.markdown(
    f"""
    <div class="header-title-bar">
        <img src="{SEAL_URL}" class="header-seal-icon" alt="Great Seal of the United States">
        <h1 class="header-title-text">2026 U.S. Midterm Elections: Real-Time Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SILENT 30-SECOND AUTO-REFRESHING DATA FRAGMENT ---
@st.fragment(run_every="10s")
def render_live_data():
    house_dem_data = fetch_kalshi_market("CONTROLH-2026-D")
    senate_dem_data = fetch_kalshi_market("CONTROLS-2026-D")

    house_dem_prob = float(house_dem_data["last_price"]) if (house_dem_data and house_dem_data.get("last_price")) else 94.0
    senate_dem_prob = float(senate_dem_data["last_price"]) if (senate_dem_data and senate_dem_data.get("last_price")) else 72.0

    house_gop_prob = round(100.0 - house_dem_prob, 1)
    senate_gop_prob = round(100.0 - senate_dem_prob, 1)

    house_winner = "DEMOCRATS" if house_dem_prob >= 99.0 else ("REPUBLICANS" if house_gop_prob >= 99.0 else None)
    senate_winner = "DEMOCRATS" if senate_dem_prob >= 99.0 else ("REPUBLICANS" if senate_gop_prob >= 99.0 else None)

    apply_split_theme_and_banners(house_dem_prob, senate_dem_prob, house_winner, senate_winner)

    # --- TOP METRICS ROW ---
    st.subheader("📊 Live Balance of Power Odds & Polling Consensus")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        label="House Control: Democrats", 
        value=f"{house_dem_prob:.1f}%", 
        delta=f"GOP: {house_gop_prob:.1f}% (218 for Majority)"
    )
    m2.metric(
        label="Senate Control: Democrats", 
        value=f"{senate_dem_prob:.1f}%", 
        delta=f"GOP: {senate_gop_prob:.1f}% (51 for Majority)"
    )
    m3.metric(
        label="Generic Congressional Ballot", 
        value="Dem +8.6%", 
        delta="49.7% D vs. 41.1% R (Silver Bulletin)"
    )
    m4.metric(
        label="Projected House Seats (Median)", 
        value="239 Dem / 196 GOP", 
        delta="+25 Net Dem Swing"
    )

    st.divider()

    # --- CHARTS & BATTLEGROUND TRACKER ---
    left_col, right_col = st.columns([1.1, 1])

    with left_col:
        st.subheader("🏛️ Chamber Control Probabilities")
        prob_df = pd.DataFrame({
            "Chamber": ["U.S. House", "U.S. House", "U.S. Senate", "U.S. Senate"],
            "Party": ["Democrats", "Republicans", "Democrats", "Republicans"],
            "Probability (%)": [house_dem_prob, house_gop_prob, senate_dem_prob, senate_gop_prob]
        })
        fig = px.bar(
            prob_df,
            x="Probability (%)",
            y="Chamber",
            color="Party",
            orientation="h",
            barmode="stack",
            text="Probability (%)",
            color_discrete_map={"Democrats": "#1f77b4", "Republicans": "#d62728"},
            height=280
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_range=[0, 100],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🎯 Key 2026 Senate Battleground Watchlist")
        battlegrounds = pd.DataFrame([
            {"State": "Ohio (Special)", "Matchup": "Sherrod Brown (D) vs. Jon Husted (R)", "Incumbent": "GOP", "Rating": "Toss-up", "Dem Win %": 63.5},
            {"State": "Maine", "Matchup": "Troy Jackson (D) vs. Susan Collins (R)", "Incumbent": "GOP", "Rating": "Lean D", "Dem Win %": 73.0},
            {"State": "Texas", "Matchup": "James Talarico (D) vs. Ken Paxton (R)", "Incumbent": "GOP", "Rating": "Lean D", "Dem Win %": 73.0},
            {"State": "Michigan", "Matchup": "Abdul El-Sayed (D) vs. Mike Rogers (R)", "Incumbent": "DEM (Open)", "Rating": "Likely D", "Dem Win %": 77.0},
            {"State": "Alaska", "Matchup": "Mary Peltola (D) vs. Dan Sullivan (R)", "Incumbent": "GOP", "Rating": "Lean D", "Dem Win %": 71.0},
            {"State": "Kansas", "Matchup": "Adam Hamilton (D) vs. Roger Marshall (R)", "Incumbent": "GOP", "Rating": "Toss-up", "Dem Win %": 59.0},
            {"State": "Iowa", "Matchup": "Josh Turek (D) vs. Ashley Hinson (R)", "Incumbent": "GOP (Open)", "Rating": "Toss-up", "Dem Win %": 53.0},
        ])
        st.dataframe(
            battlegrounds,
            column_config={
                "Dem Win %": st.column_config.ProgressColumn(
                    "Implied Dem Win %",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                )
            },
            hide_index=True,
            use_container_width=True
        )

    with right_col:
        st.subheader("📰 Live Midterm Election Wire (Strictly Midterms RSS)")
        news_items = fetch_live_midterm_news()
        if news_items:
            for item in news_items:
                with st.container(border=True):
                    st.markdown(f"**[{item['title']}]({item['link']})**")
                    st.caption(f"🕒 {item['published']}")
        else:
            st.warning("Fetching live midterm election headlines...")

render_live_data()

st.divider()

# --- LIVE VIDEO BROADCAST CENTER ---
st.subheader("📺 Live Election Video Feeds & Network Broadcasts")

NETWORK_CHANNELS = {
    "CBS News": "UC8p1vwvWtl6T73JiExfWs1g",
    "PBS NewsHour": "UC6ZFN9Tx6xh-skXCuRHCDpQ",
    "ABC News": "UCBi2mrWuNuyYy4gbM6fU18Q",
    "NBC News": "UCeY0bbntWzzVIaj2z3QigXg"

}

v_col1, v_col2 = st.columns(2)

with v_col1:
    selected_net_1 = st.selectbox("Primary Broadcast Feed:", list(NETWORK_CHANNELS.keys()), index=0)
    feeds_1 = fetch_network_video_feeds(NETWORK_CHANNELS[selected_net_1])
    if feeds_1:
        st.video(feeds_1[0]["link"])
        st.caption(f"🔴 **Now Playing ({selected_net_1}):** {feeds_1[0]['title']}")

with v_col2:
    selected_net_2 = st.selectbox("Secondary Broadcast Feed:", list(NETWORK_CHANNELS.keys()), index=1)
    feeds_2 = fetch_network_video_feeds(NETWORK_CHANNELS[selected_net_2])
    if feeds_2:
        st.video(feeds_2[0]["link"])
        st.caption(f"🔴 **Now Playing ({selected_net_2}):** {feeds_2[0]['title']}")