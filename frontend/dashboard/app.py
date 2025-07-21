import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from streamlit_autorefresh import st_autorefresh
import sys
import os

# ✅ This must be the first Streamlit command
st.set_page_config(page_title="GeoSense Dashboard", layout="wide")

# Ensure root project dir is in the path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai.model import DisasterClassifier
from ai.nlp_explain import explain_prediction

# Auto-refresh every 15 seconds
st_autorefresh(interval=15000, key="refresh")

# Load and inject CSS
STYLE_PATH = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(STYLE_PATH):
    with open(STYLE_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🌍 GeoSense: Real-Time Disaster Intelligence")

# Load data
try:
    res = requests.get("http://localhost:8000/map")
    data = pd.DataFrame(res.json())
except:
    st.warning("API offline. Start FastAPI server.")
    data = pd.DataFrame(columns=["lat", "lon", "text", "severity", "source", "timestamp"])

# Add icons
def severity_icon(sev):
    return {"high": "🔥", "medium": "⚠️", "low": "🌀"}.get(sev, "❓")

if not data.empty:
    data["icon"] = data["severity"].apply(severity_icon)

# Sidebar filters
st.sidebar.title("🔍 Filter Events")
source_filter = st.sidebar.multiselect("Source", data["source"].unique(), default=list(data["source"].unique()))
severity_filter = st.sidebar.multiselect("Severity", data["severity"].unique(), default=list(data["severity"].unique()))

# Filtered dataset
filtered = data[data["source"].isin(source_filter) & data["severity"].isin(severity_filter)]

# Stats
col1, col2, col3 = st.columns(3)
col1.metric("🌐 Total Events", len(data))
col2.metric("🔥 High Severity", sum(data["severity"] == "high"))
col3.metric("⚡ Sources Active", len(data["source"].unique()))

# Alert banner
if not filtered.empty and "high" in filtered["severity"].values:
    st.markdown(
        '<div style="background-color:#ff4b4b;padding:10px;border-radius:10px;">'
        '<h3 style="color:white;text-align:center;">⚠️ High-Severity Disaster Detected!</h3>'
        '</div>', unsafe_allow_html=True
    )

# Map
st.subheader("🗺️ Live Event Map")
if not filtered.empty:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=filtered["lat"].mean(), longitude=filtered["lon"].mean(), zoom=2),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 160]',
                get_radius=60000,
                pickable=True,
                auto_highlight=True,
            )
        ],
        tooltip={"text": "{text}\nSeverity: {severity}"},
    ))
else:
    st.info("No matching events.")

# Heatmap toggle
if st.checkbox("📊 Show Timeline Heatmap"):
    filtered["timestamp"] = pd.to_datetime(filtered["timestamp"])
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(latitude=filtered["lat"].mean(), longitude=filtered["lon"].mean(), zoom=2),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=filtered,
                get_position='[lon, lat]',
                get_weight=1,
                radiusPixels=60,
            )
        ]
    ))

# Recent events
st.subheader("📜 Recent Events")
st.dataframe(filtered[["timestamp", "text", "severity", "icon", "source"]].sort_values(by="timestamp", ascending=False).head(10))

# LIME Explain
with st.expander("🧠 Explain AI Classification with LIME"):
    text_input = st.text_area("Paste disaster tweet/text")
    if st.button("Explain Prediction"):
        if text_input.strip():
            explanation, pred = explain_prediction(text_input)
            st.write("**Prediction:**", pred["label"], f"({round(pred['score'], 2)})")
            st.write("**Key Words Influencing Model:**")
            for word, weight in explanation:
                st.write(f"- `{word}` ({'+' if weight > 0 else ''}{round(weight, 3)})")
        else:
            st.warning("Enter some text first.")
