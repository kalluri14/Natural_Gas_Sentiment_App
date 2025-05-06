import streamlit as st
from word_sentiment_price import predict_sentiment_and_price

# Set wide layout
st.set_page_config(page_title="Natural Gas Predictor", layout="wide")

# === CSS Styling ===
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTextArea textarea {
        font-size: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Page Title ===
st.markdown('<div class="center-title">📊 Natural Gas Sentiment & Price Predictor</div>', unsafe_allow_html=True)
st.markdown("#### Enter a news article and publish date to analyze sentiment and predict natural gas price.")

# === Inputs ===
article_text = st.text_area("📰 Paste the Article Text", height=150, placeholder="Paste article here...")
article_date = st.date_input("📅 Article Publish Date", format="YYYY/MM/DD")

# === Prediction Button ===
if st.button("🔍 Predict Sentiment & Price"):
    if article_text and article_date:
        result = predict_sentiment_and_price(article_text, article_date)

        # === Color Mapping Function ===
        def sentiment_box(sentiment):
            sentiment = sentiment.lower()
            styles = {
                "positive": "background-color:#d4edda; color:#155724; border:1px solid #c3e6cb;",
                "neutral": "background-color:#f8f9fa; color:#383d41; border:1px solid #d6d8db;",
                "negative": "background-color:#f8d7da; color:#721c24; border:1px solid #f5c6cb;"
            }
            style = styles.get(sentiment, "")
            return f"<span style='display:inline-block; padding:4px 10px; border-radius:5px; {style}'>{sentiment.capitalize()}</span>"


        st.markdown("---")
        st.subheader("🧠 Prediction Output")

        st.markdown(f"**Supply Sentiment :** {sentiment_box(result['supply_sentiment'])}", unsafe_allow_html=True)
        st.markdown(f"**Demand Sentiment :** {sentiment_box(result['demand_sentiment'])}", unsafe_allow_html=True)
        st.markdown(f"**Predicted Sentiment :** {sentiment_box(result['final_sentiment'])}", unsafe_allow_html=True)

        st.markdown(f"**Predicted Price:** <span style='font-weight:bold'>${result['predicted_price']:.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-weight:bold'>Advice:</span> {result['advice']}", unsafe_allow_html=True)



    else:
        st.warning("Please enter both article text and publish date.")
