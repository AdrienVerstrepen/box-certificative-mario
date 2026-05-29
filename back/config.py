import psycopg2
import os
import flask

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('DB_PASSWORD')

api = flask.Flask(__name__)

def Connection():
    """
    This function establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host='localhost',
    )
    return conn