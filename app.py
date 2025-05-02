import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Page setup
st.set_page_config(page_title="Equity Tracker", layout="wide")
st.title("📈 Equity Tracker")
st.markdown("Track stock price performance, moving averages, and volatility trends.")

# Sidebar input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, COST):", value="AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Load data
@st.cache_data
def load_data(ticker, start, end):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start, end=end)
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['Volatility'] = data['Close'].rolling(window=20).std()
    return data

data = load_data(ticker, start_date, end_date)

# Check if data is returned
if data.empty:
    st.warning("No data found for the selected ticker and date range.")
else:
    # Price chart with moving averages
    st.subheader(f"{ticker} Price Chart with Moving Averages")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(data.index, data['Close'], label="Close Price", linewidth=1.5)
    ax1.plot(data.index, data['MA20'], label="20-day MA", linestyle='--')
    ax1.plot(data.index, data['MA50'], label="50-day MA", linestyle='--')
    ax1.set_ylabel("Price (USD)")
    ax1.set_xlabel("Date")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Volatility chart
    st.subheader(f"{ticker} 20-Day Rolling Volatility")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(data.index, data['Volatility'], color="orange", label="20-Day Std Dev")
    ax2.set_ylabel("Volatility")
    ax2.set_xlabel("Date")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    # Show raw data
    st.subheader("Raw Data Preview")
    st.dataframe(data.tail(20))

