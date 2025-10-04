import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# Serve frontend static files from the sibling `frontend` directory when present
STATIC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

from backend.db.mysql_db import get_mysql_connection
from backend.db.mongo_db import get_mongo_client

# Register blueprints
from backend.routes.customers import bp as customers_bp
from backend.routes.rooms import bp as rooms_bp
from backend.routes.reservations import bp as reservations_bp
from backend.routes.payments import bp as payments_bp
from backend.routes.reviews import bp as reviews_bp

app.register_blueprint(customers_bp, url_prefix='/customers')
app.register_blueprint(rooms_bp, url_prefix='/rooms')
app.register_blueprint(reservations_bp, url_prefix='/reservations')
app.register_blueprint(payments_bp, url_prefix='/payments')
app.register_blueprint(reviews_bp, url_prefix='/reviews')


@app.route('/')
def index():
    # Serve the frontend index.html when available, otherwise return a JSON status
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return {'service': 'Hotel Management API', 'status': 'ok'}


@app.route('/<path:filename>')
def static_files(filename):
    # Serve static assets (CSS/JS/images). If not found, fall back to index.html to support SPA routes.
    if app.static_folder:
        requested = os.path.join(app.static_folder, filename)
        if os.path.exists(requested):
            return send_from_directory(app.static_folder, filename)
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
    return {'error': 'Not found'}, 404


@app.route('/health')
def health():
    status = {'service': 'Hotel Management API', 'ok': True}
    # Check MySQL
    try:
        conn = None
        try:
            conn = get_mysql_connection()
            # Some dummy cursors may not implement .is_connected(); do a lightweight ping if available
            cur = conn.cursor()
            try:
                # try simple query
                cur.execute('SELECT 1')
                _ = cur.fetchone()
                status['mysql'] = 'ok'
            except Exception:
                status['mysql'] = 'unavailable'
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
        finally:
            try:
                if conn:
                    conn.close()
            except Exception:
                pass
    except Exception as e:
        status['mysql'] = 'error'
        status['ok'] = False

    # Check MongoDB
    try:
        mclient = get_mongo_client()
        try:
            # pymongo has list_database_names; dummy client may not, but accessing a collection is safe
            names = None
            try:
                names = mclient.list_database_names()
            except Exception:
                # try accessing a collection
                _ = mclient['hotel_ms']
            status['mongo'] = 'ok'
        except Exception:
            status['mongo'] = 'unavailable'
    except Exception:
        status['mongo'] = 'error'
        status['ok'] = False

    return status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
