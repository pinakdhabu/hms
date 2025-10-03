import os
import json
import werkzeug
from backend.app import app

# Some environments install Werkzeug 3.x which removed __version__ attribute used
# by older Flask testing code. Provide a safe fallback for tests.
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.0.0'


def test_index():
    client = app.test_client()
    rv = client.get('/')
    assert rv.status_code == 200
    # Accept either the API JSON status or the frontend HTML index
    if rv.is_json:
        j = rv.get_json()
        assert j.get('service') == 'Hotel Management API'
    else:
        text = rv.get_data(as_text=True)
        # Basic smoke checks for the demo frontend
        assert ('Hotel Management - Demo' in text) or ('<!doctype html' in text) or ('Hotel Management API' in text)

# Note: More tests should be added to mock DB connections or use a test database
