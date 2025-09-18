import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# App title and description
st.title("Simple Stock Price App")
st.markdown("""
This app retrieves historical stock data for any ticker using the `yfinance` library and displays the price chart.
""")

# Sidebar for user input
st.sidebar.header('User Input')

# Function to get ticker data with caching
@st.cache_data
def get_stock_data(ticker_symbol, start_date, end_date):
    """Fetches historical stock data from Yahoo Finance."""
    ticker_data = yf.Ticker(ticker_symbol)
    df = ticker_data.history(start=start_date, end=end_date)
    return df

# User inputs
ticker_symbol = st.sidebar.text_input('Enter a stock ticker', 'AAPL')
start_date = st.sidebar.date_input('Start date', date.today() - timedelta(days=365))
end_date = st.sidebar.date_input('End date', date.today())

print(start_date)
print(end_date)

# Fetch and display stock data
if st.sidebar.button('Get Stock Data'):
    if ticker_symbol:
        st.subheader(f"Data for {ticker_symbol.upper()}")
        
        # Get data
        stock_df = get_stock_data(ticker_symbol.upper(), start_date, end_date)

        if not stock_df.empty:
            # Display basic data table
            st.write("### Historical Data")
            st.dataframe(stock_df)

            # Create interactive plot
            st.write("### Stock Price Chart")
            fig = go.Figure(data=[go.Candlestick(
                x=stock_df.index,
                open=stock_df['Open'],
                high=stock_df['High'],
                low=stock_df['Low'],
                close=stock_df['Close']
            )])
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Could not retrieve data for ticker '{ticker_symbol}'. Please check the ticker symbol.")
    else:
        st.warning("Please enter a stock ticker symbol.")

