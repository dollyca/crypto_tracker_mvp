import streamlit as st
import pandas as pd
import plotly.express as px

# 安全加載資料函數
def safe_load_data():
    try:
        df = pd.read_csv("data/crypto_prices.csv",
                         encoding='utf-8-sig',
                         parse_dates=['timestamp'])
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        column_mapping = {
            '24h_change': 'change_24h',
            'change_24hr': 'change_24h',
            'price_change': 'change_24h'
        }
        df.rename(columns=column_mapping, inplace=True)

        required_columns = ['timestamp', 'coin', 'price', 'change_24h']
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"⚠️ 缺少必要欄位: {', '.join(missing)}")
            st.stop()

        return df

    except FileNotFoundError:
        st.error("找不到資料檔案，請先執行資料抓取腳本。")
        return pd.DataFrame(columns=required_columns)

    except Exception as e:
        st.error(f"資料載入失敗：{str(e)}")
        return pd.DataFrame(columns=required_columns)

# 1️⃣ 頁面設定
st.set_page_config(page_title="加密貨幣追蹤儀表板", layout="wide")
st.title("📈 加密貨幣即時追蹤系統")

# 2️⃣ 載入資料
df = safe_load_data()

# 3️⃣ 側邊控制面板
with st.sidebar:
    st.header("控制面板")
    coins = df["coin"].unique().tolist() if not df.empty else []
    selected_coin = st.selectbox("選擇幣種", coins, index=0 if coins else None)
    time_range = st.radio("時間範圍", ["24小時", "7天", "1個月"], horizontal=True)

# 4️⃣ 主區域：顯示內容
if not df.empty:
    filtered_df = df[df["coin"] == selected_coin].sort_values("timestamp")

    latest = filtered_df.iloc[-1]
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("當前價格", f"${latest['price']:,.2f}")
        with col2:
            delta_color = "inverse" if latest['change_24h'] < 0 else "normal"
            st.metric("24小時漲跌", f"{latest['change_24h']:.2f}%", delta_color=delta_color)
        with col3:
            st.metric("最後更新時間", latest['timestamp'].strftime("%Y-%m-%d %H:%M"))

    if time_range == "7天":
        filtered_df = filtered_df[filtered_df['timestamp'] > pd.Timestamp.now() - pd.DateOffset(days=7)]
    elif time_range == "1個月":
        filtered_df = filtered_df[filtered_df['timestamp'] > pd.Timestamp.now() - pd.DateOffset(months=1)]

    fig = px.line(filtered_df,
                  x="timestamp",
                  y="price",
                  title=f"{selected_coin.upper()} 價格趨勢",
                  labels={'price': '價格 (USD)', 'timestamp': '時間'},
                  template="plotly_dark")

    fig.update_layout(
        hovermode="x unified",
        showlegend=False,
        xaxis=dict(rangeslider=dict(visible=True))
    )

    fig.add_annotation(
        x=latest['timestamp'],
        y=latest['price'],
        text=f"當前: ${latest['price']:,.2f}",
        showarrow=True,
        arrowhead=1
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 查看原始數據"):
        st.dataframe(filtered_df.style.format({
            'price': '${:,.2f}',
            'change_24h': '{:.2f}%'
        }))
else:
    st.warning("📭 尚無資料，等待初次更新或請確認資料檔案存在。")
