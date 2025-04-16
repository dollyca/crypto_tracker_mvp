import requests
import pandas as pd
from datetime import datetime
import os

def fetch_crypto_price(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url).json()
    price = response[coin_id]['usd']
    return price

def save_to_csv(price, coin_id="bitcoin"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_path = "data/crypto_prices.csv"
    df = pd.DataFrame([[now, coin_id, price]], columns=["timestamp", "coin", "price"])
    if os.path.exists(data_path):
        df.to_csv(data_path, mode='a', header=False, index=False)
    else:
        df.to_csv(data_path, index=False)

if __name__ == "__main__":
    price = fetch_crypto_price("bitcoin")
    save_to_csv(price, "bitcoin")
