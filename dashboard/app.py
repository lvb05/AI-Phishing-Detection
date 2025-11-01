import streamlit as st
import pandas as pd
import joblib
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from io import StringIO
import plotly.express as px

st.set_page_config(
    page_title="AI-Powered Phishing Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Powered Phishing Detection and Mitigation System")
st.markdown("""
Real-time phishing detection engine built with **BERT/XGBoost** models.  
Monitors email content and URLs, fetching live threat intelligence via the **OpenPhish API**.
""")

@st.cache_resource
def load_models():
    try:
        email_model = joblib.load("../models/email_model.pkl")
        url_model = joblib.load("../models/url_model.pkl")
        vectorizer = joblib.load("../models/tfidf_vectorizer.pkl")
    except Exception as e:
        st.error(f"⚠️ Could not load models: {e}")
        email_model, url_model, vectorizer = None, None, None
    return email_model, url_model, vectorizer


email_model, url_model, vectorizer = load_models()
tab1, tab2, tab3 = st.tabs(["📧 Email Detection", "🔗 URL Detection", "🌐 OpenPhish Feed"])

with tab1:
    st.header("📩 Email Phishing Detector")
    email_input = st.text_area("Paste the email content here:")
    if st.button("Analyze Email"):
        if email_model and vectorizer:
            vec = vectorizer.transform([email_input])
            pred = email_model.predict(vec)[0]
            prob = email_model.predict_proba(vec)[0][1]
            st.success(f"Prediction: **{pred.upper()}** (Confidence: {prob:.2%})")
        else:
            st.error("Model not found. Please train and save your models first.")

with tab2:
    st.header("🌐 URL Phishing Detector")
    url_input = st.text_input("Enter a URL:")
    if st.button("Check URL"):
        if url_model:
            df = pd.DataFrame([[url_input]], columns=["url"])
            df["len"] = df["url"].apply(len)
            df["num_dots"] = df["url"].apply(lambda x: x.count('.'))
            df["has_https"] = df["url"].apply(lambda x: int("https" in x))
            pred = url_model.predict(df[["len", "num_dots", "has_https"]])[0]
            st.success(f"Prediction: **{pred.upper()}**")
        else:
            st.error("Model not found. Please train and save your models first.")

with tab3:
    st.header("🚨 Live Threat Feed (OpenPhish)")
    try:
        response = requests.get("https://openphish.com/feed.txt")
        if response.status_code == 200:
            urls = response.text.strip().split("\n")[:50]
            df_feed = pd.DataFrame(urls, columns=["Phishing URL"])
            st.dataframe(df_feed)
            st.info(f"Fetched {len(df_feed)} phishing URLs from OpenPhish.")
        else:
            st.warning("Could not fetch live feed. Using cached data instead.")
    except Exception:
        st.warning("Offline mode: Unable to reach OpenPhish API.")

st.sidebar.header("📊 Threat Analytics")
if "detections" not in st.session_state:
    st.session_state["detections"] = {"phishing": 0, "legitimate": 0}

if email_model or url_model:
    chart_data = pd.DataFrame.from_dict(st.session_state["detections"], orient='index', columns=["Count"])
    fig = px.pie(chart_data, values="Count", names=chart_data.index, title="Detection Distribution")
    st.sidebar.plotly_chart(fig)

st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **Developed by Lavanya Bhargava**\n\nAI-driven phishing detection system (BERT, XGBoost, AES, Docker, Streamlit).")
