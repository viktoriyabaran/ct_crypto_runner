import io
import csv
from datetime import datetime
from minio import Minio
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

CSV_KEY = "prices/stellar/prices.csv"
CSV_HEADER = ["timestamp", "coin", "currency", "price"]

def ensure_bucket():
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)

def _get_existing_csv():
    try:
        response = client.get_object(MINIO_BUCKET, CSV_KEY)
        return response.read().decode('utf-8')
    except:
        return ",".join(CSV_HEADER) + "\n"

def save_price(coin_id, currency, price):
    ensure_bucket()
    existing = _get_existing_csv()
    timestamp = datetime.now().isoformat()
    new_row = f"{timestamp},{coin_id},{currency},{price}\n"
    updated = existing + new_row

    data = updated.encode('utf-8')
    client.put_object(
        MINIO_BUCKET, CSV_KEY,
        io.BytesIO(data), len(data),
        content_type='text/csv',
    )
    return CSV_KEY

def get_prices(coin_id, limit=100):
    ensure_bucket()
    try:
        response = client.get_object(MINIO_BUCKET, CSV_KEY)
        content = response.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        rows = [row for row in reader if row['coin'] == coin_id]
        return rows[-limit:]
    except:
        return []