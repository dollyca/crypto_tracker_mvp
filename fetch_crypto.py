import requests
import pandas as pd
from datetime import datetime
import os

# 建立資料夾
os.makedirs("data", exist_ok=True)

# 幣種列表
coins = ["bitcoin", "ethereum", "tether"]

# 擷取資料
rows = []
for coin in coins:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    res = requests.get(url).json()
    price = res["market_data"]["current_price"]["usd"]
    change = res["market_data"]["price_change_percentage_24h"]
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    rows.append([now, coin, price, change])

# 存成 DataFrame
df = pd.DataFrame(rows, columns=["timestamp", "coin", "price", "change_24h"])

# 儲存到 CSV（append 模式）
csv_path = "data/crypto_prices.csv"
if os.path.exists(csv_path):
    df.to_csv(csv_path, mode="a", index=False, header=False)
else:
    df.to_csv(csv_path, index=False)
