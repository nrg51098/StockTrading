import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as data  # Not used, can be removed
from keras.models import load_model  # Not used, can be removed
import streamlit as st

start = '2022-01-01'
end = '2022-12-31'

st.title("Stock Prediction App")
user_input = st.text_input('Enter stock ticker', 'AAPL')
df = data.DataReader(user_input, 'yahoo', start, end)
st.write(df.describe())

