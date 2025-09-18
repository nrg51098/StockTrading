import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
from datetime import date, timedelta

st.set_page_config(page_title="Stock SMAs", layout="wide")

st.title("Stock SMAs (5 & 9)")
ticker = st.text_input("Ticker", value="AAPL").strip().upper()
col_choice = st.selectbox("Price column", ["Close", "Adj Close"], index=0)
today = date.today()
start = st.date_input("Start", value=today - timedelta(days=365))
end = st.date_input("End", value=today)

if st.button("Fetch & Compute"):
    with st.spinner("Fetching data..."):
        df = yf.download(ticker, start=start.isoformat(), end=end.isoformat(), interval="1d", auto_adjust=False, progress=False)
    if df.empty:
        st.error("No data returned. Check ticker or date range.")
    else:
        df[f"SMA_5"] = df[col_choice].rolling(5, min_periods=5).mean()
        df[f"SMA_9"] = df[col_choice].rolling(9, min_periods=9).mean()

        st.subheader("Data (tail)")
        def highlight_row(row):
            try:
                price = float(row[col_choice])
                sma5 = float(row["SMA_5"])
                sma9 = float(row["SMA_9"])
            except (KeyError, ValueError, TypeError):
                return [""] * len(row)
            if pd.isna(sma5) or pd.isna(sma9) or pd.isna(price):
                return [""] * len(row)
            if sma5 > sma9 and price > sma5:
                return ["background-color: #c6efce"] * len(row)  # green
            elif sma5 < sma9 and price < sma5:
                return ["background-color: #ffc7ce"] * len(row)  # red
            else:
                return [""] * len(row)

        df_tail = df[[col_choice, "SMA_5", "SMA_9"]].tail(20)
        styled_df = df_tail.style.apply(highlight_row, axis=1)
        st.dataframe(styled_df)

        base = alt.Chart(df.reset_index()).encode(x="Date:T")
        line_price = base.mark_line(color="#1f77b4").encode(y=alt.Y(f"{col_choice}:Q", title="Price"))
        line_sma5 = base.mark_line(color="#ff7f0e").encode(y="SMA_5:Q")
        line_sma9 = base.mark_line(color="#2ca02c").encode(y="SMA_9:Q")
        st.altair_chart((line_price + line_sma5 + line_sma9).properties(height=420), use_container_width=True)

        csv = df.to_csv(index=True).encode("utf-8")
