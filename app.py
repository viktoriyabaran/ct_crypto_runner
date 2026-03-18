import threading

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from config import PORT
from routes import dashboard_bp, health_bp, price_bp
from services import run_heartbeat

app = Flask(__name__)
app.register_blueprint(health_bp)
app.register_blueprint(price_bp)
app.register_blueprint(dashboard_bp)

metrics = PrometheusMetrics(app)

if __name__ == '__main__':
    thread = threading.Thread(target=run_heartbeat, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=PORT)