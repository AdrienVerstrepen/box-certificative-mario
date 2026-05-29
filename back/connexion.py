import os
import psycopg2

db_name = os.getenv('POSTGRES_DATABASE')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_USER_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

def connect_to_database():
    """
    This function establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    return conn
