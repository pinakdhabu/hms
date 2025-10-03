import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
MOCK_MODE = os.getenv('MOCK_MODE', '0') == '1'

_client = None


class _DummyCollection:
    def __init__(self):
        self._data = []

    def insert_one(self, doc):
        # mimic pymongo InsertOneResult with inserted_id
        _id = len(self._data) + 1
        doc_copy = dict(doc)
        doc_copy['_id'] = _id
        self._data.append(doc_copy)
        class Res:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return Res(_id)

    def find(self, q=None):
        # very small filter support: if q is None return all
        q = q or {}
        def match(doc):
            for k, v in q.items():
                if doc.get(k) != v:
                    return False
            return True
        return [d.copy() for d in self._data if match(d)]


class _DummyDB:
    def __init__(self):
        self.logs = _DummyCollection()
        self.reviews = _DummyCollection()

    def __getitem__(self, name):
        # allow mclient['hotel_ms'] style
        return self


class _DummyMongoClient:
    def __init__(self):
        self._db = _DummyDB()

    def __getitem__(self, name):
        return self._db


def get_mongo_client():
    """Return a pymongo.MongoClient or a dummy in-memory client when MOCK_MODE=1.

    The dummy client implements only the minimal API used by the routes:
    - client['hotel_ms'].logs.insert_one(...)
    - client['hotel_ms'].reviews.insert_one(...)
    - client['hotel_ms'].reviews.find({...})
    """
    global _client
    if MOCK_MODE:
        if _client is None:
            _client = _DummyMongoClient()
        return _client

    # lazy import to avoid requiring pymongo at import-time when mocking
    from pymongo import MongoClient
    if _client is None:
        _client = MongoClient(MONGO_URL)
    return _client
