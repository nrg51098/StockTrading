import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Force TensorFlow to use CPU only
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as data    
import streamlit as st
import sklearn.preprocessing
from keras.models import load_model
# Define the date range
start = '2010-01-01'
end = '2019-12-31'

st.title("Stock Trend Prediction App")
# Download the data using yfinance instead of data.DataReader
user_input = st.text_input('Enter stock ticker', 'AAPL')
df = yf.download(user_input, start=start, end=end)

st.subheader('Data from 2010 - 2019')
st.write(df.describe())

# Visualization
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close, 'b', label='Closing Price')
st.pyplot(fig)
st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r', label='100MA')
plt.plot(df.Close, 'b', label='Closing Price')
plt.legend()
st.pyplot(fig)
st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r', label='100MA')
plt.plot(ma200, 'g', label='200MA')
plt.plot(df.Close, 'b', label='Closing Price')
plt.legend()
st.pyplot(fig)

# Splitting the data into training and testing
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))]) 

print(data_training.shape)
print(data_testing.shape)
from sklearn.preprocessing import MinMaxScaler  
scaler = MinMaxScaler(feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)

x_test = []
y_test = []
x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor  

# Load the model with error handling
try:
    model = load_model('my_keras_model.h5')
    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data = scaler.fit_transform(final_df) 

    x_test = []
    y_test = []
    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100: i])
        y_test.append(input_data[i, 0])
    x_test, y_test = np.array(x_test), np.array(y_test)
    y_predicted = model.predict(x_test)
    scaler_arr = scaler.scale_
    scale_factor = 1/scaler_arr[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor  

    # Final graph
    st.subheader('Predictions vs Original')
    fig2 = plt.figure(figsize=(12, 6))
    plt.plot(y_test, 'b', label='Original Price')
    plt.plot(y_predicted, 'r', label='predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Model loading or prediction failed: {e}")
