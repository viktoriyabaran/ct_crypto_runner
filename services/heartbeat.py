import time
from datetime import datetime
from config import COIN_ID, HEARTBEAT_INTERVAL
from services.price_service import record_price
from prometheus_client import Counter, Gauge, Histogram

price_gauge = Gauge('vb_current_price', 'Current crypto price', ['coin'])
fetch_counter = Counter('vb_price_fetches_total', 'Total price fetches', ['status'])
fetch_duration = Histogram('vb_fetch_duration_seconds', 'Price fetch duration')

def run_heartbeat():
    while True:
        try:
            start = time.time()
            price, key = record_price()
            duration = time.time() - start

            price_gauge.labels(coin=COIN_ID).set(price)
            fetch_counter.labels(status='success').inc()
            fetch_duration.observe(duration)

            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - {COIN_ID.title()}: ${price} -> {key}", flush=True)
        except Exception as e:
            fetch_counter.labels(status='error').inc()
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}", flush=True)
        time.sleep(HEARTBEAT_INTERVAL)