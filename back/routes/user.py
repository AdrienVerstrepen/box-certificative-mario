from connexion import connect_to_database
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

userBlueprint = Blueprint('userBlueprint', __name__)

@userBlueprint.route("/login", methods=['POST'])
def login():
    """
    This function returns the information of a user if the provided credentials are correct.
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM AppUser WHERE email = %s;", (email,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Authentication failed."}), 401

        stored_password = result[3]
        password_matches = False

        try:
            password_matches = check_password_hash(stored_password, password)
        except ValueError:
            password_matches = False

        if not password_matches and stored_password == password:
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "UPDATE AppUser SET UserPassword = %s WHERE email = %s;",
                (hashed_password, email),
            )
            conn.commit()
            password_matches = True

        if not password_matches:
            return jsonify({"error": "Authentication failed."}), 401

        user = {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "role": result[4],
        }
        return jsonify({"user": user}), 200
    finally:
        cursor.close()
        conn.close()


@userBlueprint.route("/register", methods=['POST'])
def register():
    """
    This function registers a new user in the database.
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required."}), 400

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM AppUser WHERE email = %s;", (email,))
        if cursor.fetchone() is not None:
            return jsonify({"error": "A user with this email already exists."}), 409

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO AppUser (Username, email, UserPassword, UserRoles) VALUES (%s, %s, %s, 'USER');",
            (name, email, hashed_password),
        )
        conn.commit()
        return jsonify({"message": "User registered successfully."}), 201
    finally:
        cursor.close()
        conn.close()
