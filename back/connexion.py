def connect_to_database():
    """
    This function establishes a connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db,
        port='5432'
    )
    return conn