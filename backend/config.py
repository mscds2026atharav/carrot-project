import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# Find the root folder (one level above 'backend') and load .env
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(base_dir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.environ.get('DB_PORT', 3307))
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'Billing')
    DB_SOCKET = os.environ.get('DB_SOCKET', '')

def get_db_connection():
    """
    Establishes connection to MariaDB.
    Uses Unix socket if specified and exists on system, otherwise defaults to TCP connection.
    """
    if Config.DB_SOCKET and os.path.exists(Config.DB_SOCKET):
        return pymysql.connect(
            unix_socket=Config.DB_SOCKET,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )