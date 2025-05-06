# word_sentiment_price.py (deployment-ready version using saved models)

import pandas as pd
import numpy as np
import warnings
import joblib

# === Load pre-trained models and data ===
logreg_pipeline = joblib.load("models/logreg_pipeline.pkl")
rf_pipeline = joblib.load("models/rf_pipeline.pkl")
close_series = joblib.load("models/close_series.pkl")

# === Define sentiment keywords ===
positive_supply_keywords = [
    "surplus", "oversupply", "ample supply", "increased production", 
    "higher output", "excess inventory", "ramped up supply", "expanded capacity", 
    "strong supply", "stable production", "resumed production", "supply recovery", 
    "improved supply", "supply boost", "supply up", "production ramp-up"
]

negative_supply_keywords = [
    "shortage", "supply cut", "supply disruption", "supply chain issues", 
    "output drop", "low inventory", "underproduction", "restricted supply", 
    "export ban", "declining production", "tight supply", "supply crunch", 
    "halted production", "damaged supply", "cutbacks", "supply down", 
    "production halt", "supply bottleneck"
]

positive_demand_keywords = [
    "soaring demand", "strong demand", "rising consumption", "robust appetite", 
    "high usage", "increased purchases", "booming demand", "growing interest", 
    "higher buying activity", "demand spike", "demand surge", "increased buying", 
    "demand rebound", "consumer optimism", "market appetite", "demand up"
]

negative_demand_keywords = [
    "weak demand", "falling demand", "sluggish consumption", "demand slump", 
    "reduced purchases", "demand decline", "low usage", "fading interest", 
    "poor buyer sentiment", "demand crash", "demand down", "consumer pessimism", 
    "shrinking demand", "demand drop", "market weakness", "lack of demand"
]

# === Sentiment classifier ===
def classify_sentiment(text):
    text = text.lower()
    supply_sentiment = "neutral"
    demand_sentiment = "neutral"

    if any(kw in text for kw in positive_supply_keywords):
        supply_sentiment = "positive"
    elif any(kw in text for kw in negative_supply_keywords):
        supply_sentiment = "negative"

    if any(kw in text for kw in positive_demand_keywords):
        demand_sentiment = "positive"
    elif any(kw in text for kw in negative_demand_keywords):
        demand_sentiment = "negative"

    return pd.Series([supply_sentiment, demand_sentiment])

# === Final sentiment calculator ===
def compute_simple_final_sentiment(row):
    supply_score = {"positive": 1, "negative": -1, "neutral": 0}.get(row['supply_sentiment'], 0)
    demand_score = {"positive": 1, "negative": -1, "neutral": 0}.get(row['demand_sentiment'], 0)
    net_score = supply_score + demand_score
    if net_score > 0:
        return "positive"
    elif net_score < 0:
        return "negative"
    else:
        return "neutral"

# === Main Prediction Function ===
def predict_sentiment_and_price(article_text: str, article_date: str):
    article_date = pd.to_datetime(article_date).date()
    input_df = pd.DataFrame([{
        'publishedAt': article_date,
        'combined_text': article_text,
    }])

    # Sentiment tagging
    input_df[['supply_sentiment', 'demand_sentiment']] = input_df['combined_text'].apply(classify_sentiment)
    input_df['final_sentiment'] = input_df.apply(compute_simple_final_sentiment, axis=1)

    # Map price from date
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        input_df['price_on_day'] = input_df['publishedAt'].map(close_series)
        input_df['price_on_day'] = input_df['price_on_day'].bfill().ffill()

    # Prepare features
    X_class = input_df[['combined_text', 'supply_sentiment', 'demand_sentiment']]
    X_reg = input_df[['combined_text', 'supply_sentiment', 'demand_sentiment', 'final_sentiment']]

    # Predict
    predicted_sentiment = logreg_pipeline.predict(X_class)[0]
    predicted_price = rf_pipeline.predict(X_reg)[0]

    # Advice logic
    if predicted_sentiment.lower() == "negative":
        price_range = "2.60USD - 3.90USD"
        advice = "🚨 Price is likely on the higher side (range: 2.60USD - 3.90USD). Consider waiting before making large purchases."
    else:
        price_range = "1.50USD - 2.60USD"
        advice = "✅ Price is likely in favorable range (1.50USD - 2.60USD). It could be a good time to invest or stock up."

    return {
        "supply_sentiment": input_df['supply_sentiment'].iloc[0],
        "demand_sentiment": input_df['demand_sentiment'].iloc[0],
        "final_sentiment": predicted_sentiment,
        "predicted_price": round(predicted_price, 2),
        "advice": advice,
        "price_range": price_range
    }
