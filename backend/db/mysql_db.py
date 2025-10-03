import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = os.getenv('MYSQL_DB', 'hotel_ms')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

# Simple connection wrapper using pooling
_pool = None

# Use mock mode if requested
MOCK_MODE = os.getenv('MOCK_MODE', '0') == '1'

def _init_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(pool_name='mypool', pool_size=5,
                                           host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                           database=MYSQL_DB, port=MYSQL_PORT)

def get_mysql_connection():
    """Return a connection from the pool. Initializes the pool lazily so importing the module doesn't attempt to open connections."""
    if MOCK_MODE:
        class DummyConn:
            def cursor(self, *args, **kwargs):
                raise RuntimeError('Mock mode: do not use real MySQL connection')
            def close(self):
                return
        return DummyConn()
    if _pool is None:
        _init_pool()
    return _pool.get_connection()
