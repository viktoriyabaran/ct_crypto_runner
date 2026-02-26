from flask import Blueprint
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def home():
    from config import COIN_ID
    return f"[VB_SERVICE]: Running since startup, tracking {COIN_ID}"

@health_bp.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}