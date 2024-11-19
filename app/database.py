import mysql.connector
from .config import DATABASE_CONFIG

def get_db_connection():
    connection = mysql.connector.connect(**DATABASE_CONFIG)
    return connection
