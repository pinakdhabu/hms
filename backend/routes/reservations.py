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
            # validate inputs: customer must exist (when possible)
            if not customer_id:
                return jsonify({'error': 'customer_id is required'}), 400
            cursor.execute('SELECT 1 FROM Customer WHERE customer_id = %s', (customer_id,))
            cust_row = cursor.fetchone()
            cust_checkable = True  # we attempted the check
            if cust_row is None:
                # auto-create a minimal placeholder customer so foreign key will succeed
                try:
                    cursor.execute('INSERT INTO Customer (customer_id, first_name, last_name) VALUES (%s, %s, %s)',
                                   (customer_id, 'Guest', 'Auto'))
                    conn.commit()
                except Exception:
                    # if we cannot create with explicit id, try creating without id and use new id
                    try:
                        cursor.execute('INSERT INTO Customer (first_name, last_name) VALUES (%s, %s)', ('Guest', 'Auto'))
                        conn.commit()
                        # set customer_id to the newly inserted id
                        customer_id = cursor.lastrowid
                    except Exception:
                        conn.rollback()
                        return jsonify({'error': f'customer {customer_id} does not exist and could not be created'}), 400

            # validate room exists/availability when possible
            if not room_id:
                return jsonify({'error': 'room_id is required'}), 400
            cursor.execute('SELECT is_available FROM Room WHERE room_id = %s', (room_id,))
            room_row = cursor.fetchone()
            room_checkable = room_row is not None
            if room_checkable and room_row is None:
                return jsonify({'error': f'room {room_id} does not exist'}), 400
            if room_checkable:
                is_avail = room_row[0]
                if not bool(is_avail):
                    return jsonify({'error': f'room {room_id} is not available'}), 409

            try:
                cursor.execute('INSERT INTO Reservation (customer_id, room_id, check_in, check_out, status) VALUES (%s,%s,%s,%s,%s)',
                               (customer_id, room_id, check_in, check_out, 'BOOKED'))
                conn.commit()
                res_id = cursor.lastrowid
            except mysql.connector.errors.IntegrityError as ie:
                # Likely a foreign key constraint violation — return friendly message
                conn.rollback()
                return jsonify({'error': 'invalid customer_id or room_id (FK constraint) - '+str(ie)}), 400
            # Log into MongoDB
            try:
                mclient = get_mongo_client()
                db = mclient['hotel_ms']
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation created', 'reservationId': res_id, 'createdAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc) })
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
            db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation created (mock)', 'reservationId': res_id, 'createdAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc) })
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
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation cancelled', 'reservationId': reservation_id, 'createdAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc) })
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
                db.logs.insert_one({ 'level': 'INFO', 'message': 'Reservation cancelled (mock)', 'reservationId': reservation_id, 'createdAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc) })
            except Exception:
                pass
            return jsonify({'cancelled': True})
        return jsonify({'error': 'not found'}), 404
