import yfinance as yf
print(yf.download("AAPL", period="1mo", interval="1d").head())
