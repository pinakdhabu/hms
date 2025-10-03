"""Simple in-memory mock DB used when MOCK_MODE=1 for demos/tests without running MySQL/MongoDB."""
from datetime import datetime
import threading

_lock = threading.Lock()

# seed data
_rooms = [
    {'room_id': 1, 'room_number': '101', 'room_type': 'Single', 'rate': 50.0, 'is_available': True},
    {'room_id': 2, 'room_number': '102', 'room_type': 'Double', 'rate': 80.0, 'is_available': True},
    {'room_id': 3, 'room_number': '201', 'room_type': 'Suite', 'rate': 150.0, 'is_available': True},
]

_reservations = {}
_payments = {}
_next_res_id = 1
_reviews = []

def list_rooms():
    # return copy
    with _lock:
        return [r.copy() for r in _rooms]

def create_reservation(customer_id, room_id, check_in, check_out):
    global _next_res_id
    with _lock:
        res_id = _next_res_id
        _next_res_id += 1
        rec = {
            'reservation_id': res_id,
            'customer_id': customer_id,
            'room_id': room_id,
            'check_in': check_in,
            'check_out': check_out,
            'status': 'BOOKED',
            'created_at': datetime.utcnow().isoformat()
        }
        _reservations[res_id] = rec
        # mark room unavailable in mock
        for r in _rooms:
            if r['room_id'] == room_id:
                r['is_available'] = False
        return res_id

def get_reservation(reservation_id):
    with _lock:
        return _reservations.get(reservation_id)

def cancel_reservation(reservation_id):
    with _lock:
        rec = _reservations.get(reservation_id)
        if not rec:
            return False
        rec['status'] = 'CANCELLED'
        # free the room
        for r in _rooms:
            if r['room_id'] == rec['room_id']:
                r['is_available'] = True
        return True

def add_payment(reservation_id, amount, method):
    with _lock:
        arr = _payments.setdefault(reservation_id, [])
        p = {'amount': amount, 'method': method, 'created_at': datetime.utcnow().isoformat()}
        arr.append(p)
        return p

def list_payments(reservation_id):
    with _lock:
        return _payments.get(reservation_id, [])

def insert_review(payload):
    # in mock just return inserted doc
    with _lock:
        doc = payload.copy()
        doc['_id'] = len(_reviews) + 1
        doc['createdAt'] = datetime.utcnow().isoformat()
        _reviews.append(doc)
        return doc

def add_room(room_number, room_type, rate):
    with _lock:
        rid = max([r['room_id'] for r in _rooms] + [0]) + 1
        rec = {'room_id': rid, 'room_number': room_number, 'room_type': room_type, 'rate': float(rate), 'is_available': True}
        _rooms.append(rec)
        return rid

def find_reviews(query=None):
    query = query or {}
    with _lock:
        def match(d):
            for k, v in query.items():
                if d.get(k) != v:
                    return False
            return True
        return [d.copy() for d in _reviews if match(d)]
