from flask import Blueprint
from services.price_service import get_current_price, get_price_history
from config import COIN_ID, CURRENCY

price_bp = Blueprint('price', __name__)

@price_bp.route('/price')
def price():
    try:
        current_price = get_current_price()
        return {'coin': COIN_ID, 'price': current_price, 'currency': CURRENCY}
    except Exception as e:
        return {'error': str(e)}, 500

@price_bp.route('/history')
def history():
    try:
        prices = get_price_history()
        if not prices:
            return {'data': [], 'message': 'MinIO not enabled or no data yet'}
        return {'data': prices}
    except Exception as e:
        return {'error': str(e)}, 500