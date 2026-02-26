from clients.coingecko import fetch_price
from config import COIN_ID, CURRENCY, USE_MINIO

def get_current_price():
    return fetch_price()

def record_price():
    price = fetch_price()
    key = None
    if USE_MINIO:
        from clients.minio_client import save_price
        key = save_price(COIN_ID, CURRENCY, price)
    return price, key

def get_price_history(limit=100):
    if USE_MINIO:
        from clients.minio_client import get_prices
        return get_prices(COIN_ID, limit)
    return []