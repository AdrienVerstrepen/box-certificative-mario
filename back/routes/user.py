from connexion import connect_to_database
from flask import Blueprint, jsonify, request
from psycopg2 import sql
from werkzeug.security import check_password_hash, generate_password_hash

userBlueprint = Blueprint('userBlueprint', __name__)

def get_user_role_column(cursor):
    """
    Return the user role column if present in the database.
    """
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'appuser'
            AND lower(column_name) IN ('userrole', 'userroles');
        """
    )
    result = cursor.fetchone()
    return result[0] if result is not None else "UserRoles"

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
        role_column = get_user_role_column(cursor)
        query = sql.SQL(
            "SELECT UserID, Username, Email, UserPassword, {} "
            "FROM AppUser WHERE Email = %s;"
        ).format(sql.Identifier(role_column))
        cursor.execute(query, (email,))
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
        return jsonify({"success": True, "user": user}), 200
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
        role_column = get_user_role_column(cursor)
        cursor.execute("SELECT 1 FROM AppUser WHERE Email = %s;", (email,))
        if cursor.fetchone() is not None:
            return jsonify({"error": "A user with this email already exists."}), 409

        hashed_password = generate_password_hash(password)
        query = sql.SQL(
            "INSERT INTO AppUser (Username, Email, UserPassword, {}) "
            "VALUES (%s, %s, %s, %s) "
            "RETURNING UserID, Username, Email, {};"
        ).format(sql.Identifier(role_column), sql.Identifier(role_column))
        cursor.execute(
            query,
            (name, email, hashed_password, "USER"),
        )
        result = cursor.fetchone()
        conn.commit()
        user = {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "role": result[3],
        }
        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "user": user,
        }), 201
    finally:
        cursor.close()
        conn.close()
