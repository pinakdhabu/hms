from flask import Blueprint, request, jsonify
from backend.db.mysql_db import get_mysql_connection

bp = Blueprint('customers', __name__)

@bp.route('/', methods=['GET'])
def list_customers():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT customer_id, first_name, last_name, email, phone FROM Customer')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json() or {}
    first = data.get('first_name')
    last = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Customer (first_name, last_name, email, phone) VALUES (%s,%s,%s,%s)', (first, last, email, phone))
    conn.commit()
    cid = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'customer_id': cid}), 201
