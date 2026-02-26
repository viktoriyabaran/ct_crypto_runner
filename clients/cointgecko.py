import requests
from config import COIN_ID, CURRENCY

def fetch_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={COIN_ID}&vs_currencies={CURRENCY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()[COIN_ID][CURRENCY]