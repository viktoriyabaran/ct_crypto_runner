from dotenv import load_dotenv
load_dotenv()

import os

PORT = int(os.getenv('PORT', 2297))

COIN_ID = os.getenv('COIN_ID', 'stellar')
CURRENCY = os.getenv('CURRENCY', 'usd')
HEARTBEAT_INTERVAL = int(os.getenv('HEARTBEAT_INTERVAL', 60))
LOG_LINES = 100

USE_MINIO = os.getenv('USE_MINIO', 'false').lower() == 'true'
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'vb-prices')