import json
import sqlite3
import pytest
import types
import werkzeug
# Provide __version__ fallback when running with Werkzeug 3.x where __version__ may be missing
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.0.0'
from backend.app import app

# Helper: create an in-memory sqlite DB to emulate basic SELECT/INSERT behavior for tests
class DummyCursor:
    def __init__(self):
        self._rows = []
        self.lastrowid = 1
    def execute(self, query, params=None):
        # naive parser for simple queries used in routes
        if query.strip().lower().startswith('select'):
            self._rows = []
        elif query.strip().lower().startswith('insert'):
            self.lastrowid += 1
    def fetchall(self):
        return self._rows
    def fetchone(self):
        return None
    def close(self):
        pass

class DummyConn:
    def __init__(self):
        self.cursor_obj = DummyCursor()
    def cursor(self, dictionary=False):
        return self.cursor_obj
    def commit(self):
        pass
    def rollback(self):
        pass
    def close(self):
        pass

class DummyMongoColl:
    def __init__(self):
        self.docs = []
    def insert_one(self, doc):
        self.docs.append(doc)
        return types.SimpleNamespace(inserted_id='dummyid')
    def insert_many(self, docs):
        self.docs.extend(docs)
        return types.SimpleNamespace(inserted_ids=[1]*len(docs))
    def find(self, query):
        return self.docs

class DummyMongoClient:
    def __init__(self):
        # create a simple namespace-like DB object with collection attributes
        self._db_obj = types.SimpleNamespace(reviews=DummyMongoColl(), feedback=DummyMongoColl(), logs=DummyMongoColl())
    def __getitem__(self, name):
        # return the same namespace regardless of name (tests target single DB)
        return self._db_obj
    def __getattr__(self, name):
        return getattr(self._db_obj, name)
    def close(self):
        pass

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    # Patch MySQL connector to return DummyConn
    def fake_get_mysql_connection():
        return DummyConn()
    monkeypatch.setattr('backend.db.mysql_db.get_mysql_connection', fake_get_mysql_connection)
    # Also patch references imported into route modules (they did `from backend.db.mysql_db import get_mysql_connection`)
    try:
        monkeypatch.setattr('backend.routes.customers.get_mysql_connection', fake_get_mysql_connection)
    except Exception:
        pass
    try:
        monkeypatch.setattr('backend.routes.rooms.get_mysql_connection', fake_get_mysql_connection)
    except Exception:
        pass
    try:
        monkeypatch.setattr('backend.routes.reservations.get_mysql_connection', fake_get_mysql_connection)
    except Exception:
        pass
    try:
        monkeypatch.setattr('backend.routes.payments.get_mysql_connection', fake_get_mysql_connection)
    except Exception:
        pass

    # Patch Mongo client
    def fake_get_mongo_client():
        return DummyMongoClient()
    monkeypatch.setattr('backend.db.mongo_db.get_mongo_client', fake_get_mongo_client)
    # Patch route-level mongo references
    try:
        monkeypatch.setattr('backend.routes.reservations.get_mongo_client', fake_get_mongo_client)
    except Exception:
        pass
    try:
        monkeypatch.setattr('backend.routes.reviews.get_mongo_client', fake_get_mongo_client)
    except Exception:
        pass

    yield


def test_customers_add_and_list():
    client = app.test_client()
    # Add customer
    rv = client.post('/customers/', json={'first_name': 'Test', 'last_name': 'User', 'email': 't@example.com'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert 'customer_id' in data

    # List customers
    rv = client.get('/customers/')
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)


def test_rooms_add_and_list_and_update():
    client = app.test_client()
    rv = client.post('/rooms/', json={'room_number': '999', 'room_type': 'Single', 'rate': 99})
    assert rv.status_code == 201
    rv = client.get('/rooms/')
    assert rv.status_code == 200
    # Update availability (patch)
    rv = client.patch('/rooms/1', json={'is_available': False})
    assert rv.status_code == 200


def test_create_reservation_and_cancel_and_get():
    client = app.test_client()
    # create
    payload = {'customer_id': 1, 'room_id': 1, 'check_in': '2025-10-10', 'check_out': '2025-10-12'}
    rv = client.post('/reservations/', json=payload)
    assert rv.status_code == 201
    j = rv.get_json()
    assert 'reservation_id' in j
    res_id = j['reservation_id']

    # get
    rv = client.get(f'/reservations/{res_id}')
    # our DummyCursor returns None for fetchone so expect 404
    assert rv.status_code in (200, 404)

    # cancel
    rv = client.post(f'/reservations/{res_id}/cancel')
    assert rv.status_code == 200


def test_payments_and_reviews():
    client = app.test_client()
    rv = client.post('/payments/', json={'reservation_id': 1, 'amount': 100, 'method': 'card'})
    assert rv.status_code == 201
    rv = client.post('/reviews/', json={'customerId': 1, 'reservationId':1, 'roomType':'Single','score':5,'comment':'ok'})
    assert rv.status_code == 201
    rv = client.get('/reviews/customer/1')
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)
