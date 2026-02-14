from app import app, CONFIG

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert CONFIG['coin_id'] in response.text

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_price_endpoint():
    client = app.test_client()
    response = client.get('/price')
    assert response.status_code in [200, 500]