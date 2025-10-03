from flask import Blueprint, request, jsonify
from backend.db.mysql_db import get_mysql_connection
from backend.db import mock_db
import mysql.connector

bp = Blueprint('rooms', __name__)

@bp.route('/', methods=['GET'])
def list_rooms():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT room_id, room_number, room_type, rate, is_available FROM Room')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        # fallback to mock
        return jsonify(mock_db.list_rooms())

@bp.route('/', methods=['POST'])
def add_room():
    data = request.get_json() or {}
    room_number = data.get('room_number')
    room_type = data.get('room_type')
    rate = data.get('rate')
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Room (room_number, room_type, rate) VALUES (%s,%s,%s)', (room_number, room_type, rate))
        conn.commit()
        rid = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'room_id': rid}), 201
    except (mysql.connector.errors.InterfaceError, ConnectionRefusedError, OSError):
        rid = mock_db.add_room(room_number, room_type, rate)
        return jsonify({'room_id': rid}), 201

@bp.route('/<int:room_id>', methods=['PATCH'])
def update_room(room_id):
    data = request.get_json() or {}
    is_available = data.get('is_available')
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Room SET is_available = %s WHERE room_id = %s', (is_available, room_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'updated': True})
