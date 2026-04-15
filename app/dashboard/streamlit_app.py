# dashboard/app.py
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import streamlit as st
import pandas as pd
import datetime

# Import your services
from app.services.prediction_service import PredictionService
from app.services.insight_service import InsightService
from app.services.chatbot_service import ChatbotService

# Initialize services
prediction_service = PredictionService()
insight_service = InsightService()
chatbot_service = ChatbotService()

# In-memory storage (simple demo)
if "data" not in st.session_state:
    st.session_state.data = []

# -----------------------------
# UI HEADER
# -----------------------------
st.set_page_config(page_title="AI Feedback Analyzer", layout="wide")

st.title("🤖 AI Customer Feedback Analyzer")
st.markdown("Analyze feedback and get insights instantly")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("📝 Enter Feedback")

col1, col2, col3 = st.columns(3)

with col1:
    domain = st.selectbox("Select Domain", ["E-commerce", "App", "Service"])

with col2:
    category = st.selectbox("Select Category", ["Electronics", "Food", "Software", "Delivery"])

with col3:
    product = st.text_input("Product / Service Name")

text_input = st.text_area("Enter Feedback")

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🔍 Analyze Feedback"):

    if text_input.strip() == "":
        st.warning("Please enter some feedback")
    else:
        # -------- Prediction --------
        result = prediction_service.predict(text_input)

        sentiment = result["sentiment"]
        confidence = result["confidence"]
        keywords = result["keywords"]

        # -------- Insight --------
        insight = insight_service.generate_insight(
            sentiment=sentiment,
            keywords=keywords,
            domain=domain,
            category=category,
            product=product
        )

        # -------- Chatbot --------
        response = chatbot_service.generate_response(
            sentiment=sentiment,
            keywords=keywords,
            product=product
        )

        # -------- Store data --------
        st.session_state.data.append({
            "text": text_input,
            "sentiment": sentiment,
            "domain": domain,
            "category": category,
            "product": product,
            "time": datetime.datetime.now()
        })

        # -----------------------------
        # OUTPUT SECTION
        # -----------------------------
        st.subheader("📊 Result")

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"Sentiment: {sentiment}")
            if confidence:
                st.info(f"Confidence: {round(confidence, 2)}")

        with col2:
            st.write("**Keywords:**", keywords)

        st.write("**Insight:**", insight)
        st.write("**Chatbot Response:**", response)

# -----------------------------
# ANALYTICS SECTION
# -----------------------------
st.subheader("📈 Analytics Dashboard")

if len(st.session_state.data) > 0:

    df = pd.DataFrame(st.session_state.data)

    col1, col2 = st.columns(2)

    # Sentiment Distribution
    with col1:
        st.write("### Sentiment Distribution")
        st.bar_chart(df["sentiment"].value_counts())

    # Category Distribution
    with col2:
        st.write("### Category Distribution")
        st.bar_chart(df["category"].value_counts())

    # Product Insights
    st.write("### Product-wise Sentiment")
    st.dataframe(df.groupby("product")["sentiment"].value_counts())

else:
    st.info("No data yet. Start by analyzing feedback!")