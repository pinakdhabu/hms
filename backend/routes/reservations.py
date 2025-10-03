from flask import Blueprint, request, jsonify
from backend.db.mysql_db import get_mysql_connection
from backend.db.mongo_db import get_mongo_client
from backend.db import mock_db
import mysql.connector

bp = Blueprint('reservations', __name__)

@bp.route('/', methods=['POST'])
def create_reservation():
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Reservation (customer_id, room_id, check_in, check_out, status) VALUES (%s,%s,%s,%s,%s)',
                           (customer_id, room_id, check_in, check_out, 'BOOKED'))
            conn.commit()
            res_id = cursor.lastrowid
            # Log into MongoDB
            try:
                mclient = get_mongo_client()
                db = mclient['hotel_ms']
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation created', 'reservationId': res_id, 'createdAt': __import__('datetime').datetime.utcnow() })
            except Exception:
                # ignore mongo logging failures
                pass
            return jsonify({'reservation_id': res_id}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        # fallback to mock DB
        res_id = mock_db.create_reservation(customer_id, room_id, check_in, check_out)
        try:
            mclient = get_mongo_client()
            db = mclient['hotel_ms']
            db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation created (mock)', 'reservationId': res_id, 'createdAt': __import__('datetime').datetime.utcnow() })
        except Exception:
            pass
        return jsonify({'reservation_id': res_id}), 201

@bp.route('/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Reservation WHERE reservation_id = %s', (reservation_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return jsonify({'error': 'not found'}), 404
        return jsonify(row)
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        rec = mock_db.get_reservation(int(reservation_id))
        if not rec:
            return jsonify({'error': 'not found'}), 404
        return jsonify(rec)

@bp.route('/<int:reservation_id>/cancel', methods=['POST'])
def cancel_reservation(reservation_id):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE Reservation SET status = %s WHERE reservation_id = %s', ('CANCELLED', reservation_id))
            conn.commit()
            try:
                mclient = get_mongo_client()
                db = mclient['hotel_ms']
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation cancelled', 'reservationId': reservation_id, 'createdAt': __import__('datetime').datetime.utcnow() })
            except Exception:
                pass
            return jsonify({'cancelled': True})
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        ok = mock_db.cancel_reservation(int(reservation_id))
        if ok:
            try:
                mclient = get_mongo_client()
                db = mclient['hotel_ms']
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation cancelled (mock)', 'reservationId': reservation_id, 'createdAt': __import__('datetime').datetime.utcnow() })
            except Exception:
                pass
            return jsonify({'cancelled': True})
        return jsonify({'error': 'not found'}), 404
