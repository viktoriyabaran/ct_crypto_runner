import threading
from flask import Flask
from config import PORT
from routes.health import health_bp
from routes.price import price_bp
from services.heartbeat import run_heartbeat

app = Flask(__name__)
app.register_blueprint(health_bp)
app.register_blueprint(price_bp)

if __name__ == '__main__':
    thread = threading.Thread(target=run_heartbeat, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=PORT)