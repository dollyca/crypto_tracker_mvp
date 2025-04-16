import requests
import pandas as pd
from datetime import datetime
import os

# 幣種列表
coins = ["bitcoin", "ethereum", "tether"]

def fetch_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true"
    res = requests.get(url).json()
    price = res[coin]["usd"]
    change_24h = res[coin]["usd_24h_change"]
    return price, change_24h

def save_to_csv(data):
    df = pd.DataFrame(data, columns=["timestamp", "coin", "price", "change_24h"])
    file_path = "data/crypto_prices.csv"
    os.makedirs("data", exist_ok=True)
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", index=False, header=False)
    else:
        df.to_csv(file_path, index=False)

if __name__ == "__main__":
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for coin in coins:
        price, change = fetch_price(coin)
        rows.append([now, coin, price, change])
    save_to_csv(rows)
