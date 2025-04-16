import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Crypto Tracker MVP")

df = pd.read_csv("data/crypto_prices.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.write("Latest Data")
st.write(df.tail())

fig, ax = plt.subplots()
for coin in df["coin"].unique():
    subset = df[df["coin"] == coin]
    ax.plot(subset["timestamp"], subset["price"], label=coin)
ax.set_title("Price Trend")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)
