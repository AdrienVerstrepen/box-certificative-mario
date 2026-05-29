import os
import psycopg2

def connect_to_database():
    """
    This function establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DATABASE') or os.getenv('DB_NAME'),
        user=os.getenv('POSTGRES_USER') or os.getenv('DB_USER'),
        password=os.getenv('POSTGRES_USER_PASSWORD') or os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn
