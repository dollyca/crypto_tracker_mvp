import streamlit as st
import pandas as pd
import plotly.express as px

# 讀取 CSV 資料
df = pd.read_csv("data/crypto_prices.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 幣種選單
coins = df["coin"].unique().tolist()
selected_coin = st.selectbox("Select a coin", coins)

# 篩選資料
filtered_df = df[df["coin"] == selected_coin].sort_values("timestamp")

# 最新一筆
latest = filtered_df.iloc[-1]
price = latest["price"]
change = latest["change_24h"]

# 顯示區塊
st.title("Crypto Tracker MVP")
st.subheader(f"💰 {selected_coin.capitalize()} Latest Price: ${price:,.2f}")

change_color = "green" if change > 0 else "red"
arrow = "▲" if change > 0 else "▼"
st.markdown(f"**24H Change:** <span style='color:{change_color}'>{arrow} {change:.2f}%</span>", unsafe_allow_html=True)

# 畫 Plotly 線圖
fig = px.line(filtered_df, x="timestamp", y="price", title=f"{selected_coin.capitalize()} Price Trend")
fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)
