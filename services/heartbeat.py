import time
from datetime import datetime
from config import COIN_ID, HEARTBEAT_INTERVAL
from services import record_price

def run_heartbeat():
    while True:
        try:
            price, key = record_price()
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - {COIN_ID.title()}: ${price} -> {key}", flush=True)
        except Exception as e:
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}", flush=True)
        time.sleep(HEARTBEAT_INTERVAL)