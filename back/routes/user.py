from connexion import connect_to_database

from flask import Blueprint

userBlueprint = Blueprint('userBlueprint', __name__)

@userBlueprint.route("/login", methods=['GET'])
def login(email, password):
    """
    This function returns the information of a user if the provided credentials are correct.
    """

    conn = connect_to_database()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AppUser WHERE email like %s;", (email,))
    result = cursor.fetchone()
    if result is not None:
        stored_password = result[3]
        if stored_password == password:
            print("Authentication successful.")
            print("User details:", result)
            return result
        else:
            return "Authentication failed: Incorrect password."

    cursor.close()
    conn.close()


@userBlueprint.route("/register", methods=['GET'])
def register(name, email, password):
    """
    This function registers a new user in the database.
    """

    conn = connect_to_database()

    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM AppUser")
    count = cursor.fetchone()
    id = count[0] + 1
    cursor.execute("INSERT INTO AppUser VALUES (%s, %s, %s, %s, 'USER');", (id, name, email, password,))
    conn.commit()
    print("User registered successfully.")

    cursor.close()
    conn.close()
