import psycopg2
import os
import flask

api = flask.Flask(__name__)

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'db')

def Connection():
    """
    This function establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port='5432'
    )
    return conn