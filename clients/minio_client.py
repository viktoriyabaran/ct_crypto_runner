from minio import Minio
import json
from datetime import datetime
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
import io

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

def ensure_bucket():
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)

def save_price(coin_id, currency, price):
    ensure_bucket()
    timestamp = datetime.now().isoformat()
    data = json.dumps({
        'coin': coin_id,
        'currency': currency,
        'price': price,
        'timestamp': timestamp,
    })
    key = f"prices/{coin_id}/{timestamp}.json"
    client.put_object(
        MINIO_BUCKET, key,
        io.BytesIO(data.encode()), len(data),
        content_type='application/json',
    )
    return key

def get_prices(coin_id, limit=100):
    ensure_bucket()
    objects = client.list_objects(MINIO_BUCKET, prefix=f"prices/{coin_id}/")
    prices = []
    for obj in sorted(objects, key=lambda o: o.object_name, reverse=True)[:limit]:
        data = client.get_object(MINIO_BUCKET, obj.object_name)
        prices.append(json.loads(data.read()))
    return prices