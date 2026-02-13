import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Phishing Dashboard")
st.title("🛡️ Multimodal Phishing Detection System")

import os
api_url = st.sidebar.text_input(
    "API URL", 
    value=os.getenv("API_URL", "http://localhost:8000")
)

st.subheader("🔍 Check URL / Email")
col1, col2 = st.columns(2)

with col1:
    url_count = st.number_input("URL Count", min_value=0, value=0)
    url_length_max = st.number_input("URL Length Max", min_value=0, value=0)
    url_subdom_max = st.number_input("URL Subdomains Max", min_value=0, value=0)
    attachment_count = st.number_input("Attachment Count", min_value=0, value=0)

with col2:
    email_text = st.text_area("Email Text (optional)", height=200)

if st.button("Analyze"):
    try:
        features = [url_count, url_length_max, url_subdom_max, attachment_count]
        payload = {"url_features": features, "email_text": email_text}
        resp = requests.post(f"{api_url}/predict", json=payload, timeout=60)
        result = resp.json()
        prob = result["phishing_probability"]
        label = result["label"]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            domain={"x": [0,1], "y": [0,1]},
            title={"text": "Phishing Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkred" if prob > 0.5 else "green"},
                "steps": [
                    {"range": [0, 50], "color": "lightgreen"},
                    {"range": [50, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "salmon"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 75
                }
            }
        ))
        st.plotly_chart(fig)
        st.success(f"**Classification:** {label.upper()}  \n**Confidence:** {result['confidence']:.2%}")
    except Exception as e:
        st.error(f"Error: {e}")
