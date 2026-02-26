from app import app
from config import COIN_ID

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert COIN_ID in response.text

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_price_endpoint():
    client = app.test_client()
    response = client.get('/price')
    assert response.status_code in [200, 500]

def test_history_without_minio():
    client = app.test_client()
    response = client.get('/history')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data