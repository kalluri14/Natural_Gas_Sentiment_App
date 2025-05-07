# 🧠📊 Natural Gas Sentiment & Price Predictor

This Streamlit app predicts **natural gas prices** based on **news article sentiment** using a combination of rule-based sentiment detection and machine learning models. It is designed for use by analysts, traders, and researchers to better understand market sentiment around supply and demand factors.

---

## 🚀 Live Demo

👉 [Launch the app](https://pqmhukze64nscptlnzpcyz.streamlit.app/)  
*(Accessible on any browser. No installation needed.)*

---

## ✨ Features

- 📰 Accepts any natural gas–related news article text and publication date
- 📊 Extracts **supply** and **demand** sentiment using keyword patterns
- 🧠 Predicts overall sentiment using a Logistic Regression classifier
- 💰 Predicts natural gas price using a Random Forest model
- 📈 Retrieves historical prices using `yfinance`
- ✅ Gives actionable investment **advice** (buy/wait) based on sentiment

---

## 🛠️ Tech Stack

| Layer         | Technology       |
|---------------|------------------|
| Frontend      | Streamlit        |
| ML Models     | scikit-learn     |
| Data Handling | pandas, numpy    |
| Price Data    | yfinance         |
| Model Storage | joblib (`.pkl`)  |

---

## 📁 Project Structure
├── app.py # Streamlit app UI
├── word_sentiment_price.py # Model inference logic
├── requirements.txt # Python dependencies
├── models/ # Pretrained models
│ ├── logreg_pipeline.pkl
│ ├── rf_pipeline.pkl
│ └── close_series.pkl
└── .streamlit/config.toml # Streamlit layout config

---




## 🧠 Model Overview

- **Datset Used for Training**
    - Created our own Dataset by webscraping NewsAPI and Google News for Natural Gas related Articles and stored them in a csv file.
- **Sentiment Classification**
  - Inputs: TF-IDF from article + one-hot supply/demand sentiment
  - Model: Logistic Regression
- **Price Prediction**
  - Inputs: TF-IDF + one-hot final sentiment
  - Model: Random Forest Regressor
- **Keyword Sentiment**: Predefined keyword lists determine `supply_sentiment` and `demand_sentiment`

---

## 🧪 Run Locally

```bash
# Clone the repo
git clone https://github.com/kalluri14/Natural_Gas_Sentiment_App.git
cd Natural_Gas_Sentiment_App

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py

```
## 📚 Future Enhancements
- 🔄 Add real-time news scraping from sources like Google News or NewsAPI
- 📈 Enhance model with sentiment embeddings (BERT/FinBERT)
- 🌍 Support for global market analysis across regions and also expand to different domains

