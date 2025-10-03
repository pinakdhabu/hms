from flask import Blueprint, request, jsonify
from backend.db.mysql_db import get_mysql_connection
from backend.db import mock_db
import mysql.connector

bp = Blueprint('payments', __name__)

@bp.route('/', methods=['POST'])
def record_payment():
    data = request.get_json() or {}
    reservation_id = data.get('reservation_id')
    amount = data.get('amount')
    method = data.get('method')
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Payment (reservation_id, amount, method) VALUES (%s,%s,%s)', (reservation_id, amount, method))
            conn.commit()
            pid = cursor.lastrowid
            return jsonify({'payment_id': pid}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        p = mock_db.add_payment(reservation_id, amount, method)
        return jsonify({'payment': p}), 201

@bp.route('/reservation/<int:reservation_id>', methods=['GET'])
def payments_for_reservation(reservation_id):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Payment WHERE reservation_id = %s', (reservation_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        return jsonify(mock_db.list_payments(reservation_id))
