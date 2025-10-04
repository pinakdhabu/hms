from flask import Blueprint, request, jsonify
from backend.db.mongo_db import get_mongo_client
from backend.db import mock_db

bp = Blueprint('reviews', __name__)


@bp.route('/', methods=['POST'])
def add_review():
    data = request.get_json() or {}
    try:
        mclient = get_mongo_client()
        db = mclient['hotel_ms']
        doc = {
            'customerId': data.get('customerId'),
            'reservationId': data.get('reservationId'),
            'roomType': data.get('roomType'),
            'score': data.get('score'),
            'comment': data.get('comment'),
            'createdAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc)
        }
        res = db.reviews.insert_one(doc)
        return jsonify({'insertedId': str(res.inserted_id)}), 201
    except Exception:
        # fallback to mock
        doc = mock_db.insert_review(data)
        return jsonify({'insertedId': str(doc.get('_id'))}), 201


@bp.route('/customer/<int:customer_id>', methods=['GET'])
def reviews_for_customer(customer_id):
    try:
        mclient = get_mongo_client()
        db = mclient['hotel_ms']
        rows = list(db.reviews.find({'customerId': customer_id}))
        for r in rows:
            r['_id'] = str(r['_id'])
        return jsonify(rows)
    except Exception:
        rows = mock_db.find_reviews({'customerId': customer_id})
        for r in rows:
            r['_id'] = str(r.get('_id'))
        return jsonify(rows)
