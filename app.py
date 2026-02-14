import os
import signal
import subprocess
import threading
import time
from datetime import datetime

import requests
from flask import Flask

app = Flask(__name__)
PORT = 2297

CONFIG = {
    'coin_id': 'stellar',
    'currency': 'usd',
    'interval_seconds': 60,
    'log_lines': 100,
}


def get_price():
    """Get the prixe of the cryptocurrency."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={CONFIG['coin_id']}&vs_currencies={CONFIG['currency']}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()[CONFIG['coin_id']][CONFIG['currency']]


@app.route('/')
def home():
    return f"[VB_SERVICE]: Running since startup, tracking {CONFIG['coin_id']}"


@app.route('/price')
def price():
    """Current price from request."""
    try:
        current_price = get_price()
        return {'coin': CONFIG['coin_id'], 'price': current_price, 'currency': CONFIG['currency']}
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/health')
def health():
    """For monitoring/load balancer."""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}


@app.route('/kill')
def kill():
    print("[VB_SERVICE]: Shutting down...")
    os.kill(os.getpid(), signal.SIGTERM)
    return "Shutting down..."


@app.route('/logs')
def logs():
    result = subprocess.run(
        ['sudo', 'journalctl', '-u', 'vb_service', '-n', str(CONFIG['log_lines']), '--no-pager'],
        capture_output=True,
        text=True
    )
    return f"<html><body><pre>{result.stdout or result.stderr}</pre></body></html>"


def heartbeat():
    while True:
        try:
            current_price = get_price()
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - {CONFIG['coin_id'].title()}: ${current_price}", flush=True)
        except requests.RequestException as e:
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - Network error: {e}", flush=True)
        except Exception as e:
            print(f"[VB_SERVICE] {datetime.now():%Y-%m-%d %H:%M:%S} - Error: {e}", flush=True)
        
        time.sleep(CONFIG['interval_seconds'])


if __name__ == '__main__':
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=PORT)
