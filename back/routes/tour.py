from connexion import connect_to_database
from flask import Blueprint, current_app, jsonify, request
from psycopg2 import sql

tourBlueprint = Blueprint('tourBlueprint', __name__)


def parse_optional_int(value):
    """
    Parse an optional integer value.
    """
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value):
    """
    Parse an optional floating-point value.
    """
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_visibility(value):
    """
    Parse visibility values as booleans.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "public", "1", "yes"}:
            return True
        if normalized in {"false", "private", "0", "no"}:
            return False
    return None


def request_payload():
    """
    Return the JSON payload as a dict when possible.
    """
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else {}


def extract_optional_stages(data):
    """
    Return the stages payload only when it is explicitly provided.
    """
    if not isinstance(data, dict):
        return None
    if "stages" in data:
        return data.get("stages")
    if "places" in data:
        return data.get("places")
    if "tourDatas" in data:
        return data.get("tourDatas")
    return None


def get_tour_length_column(cursor):
    """
    Return the tour-length column name when it exists in the database.
    """
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE lower(table_name) = 'tour'
            AND lower(column_name) IN ('tourlength', 'tourlenght');
        """
    )
    result = cursor.fetchone()
    return result[0] if result is not None else None


def get_stage_hotel_column(cursor):
    """
    Return the stage hotel reference column name when it exists.
    """
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE lower(table_name) = 'stage'
            AND lower(column_name) IN ('clusterhotelid', 'hotelnumber');
        """
    )
    result = cursor.fetchone()
    return result[0] if result is not None else None


def parse_place_payload(place, index=None):
    """
    Validate and normalize a place payload.
    """
    name = place.get("PlaceName") or place.get("Name") or place.get("name")
    latitude = (
        place.get("Latitude")
        if "Latitude" in place
        else place.get("latitude", place.get("lat"))
    )
    longitude = (
        place.get("Longitude")
        if "Longitude" in place
        else place.get("longitude", place.get("lon"))
    )
    country = place.get("Country") or place.get("country")

    latitude = parse_float(latitude)
    longitude = parse_float(longitude)

    if not name or latitude is None or longitude is None or not country:
        location = f" at index {index}" if index is not None else ""
        return None, (
            f"Place{location} must contain PlaceName, Latitude, Longitude, and Country."
        )

    normalized_name = str(name).strip()
    normalized_country = str(country).strip()

    if not normalized_name or not normalized_country:
        location = f" at index {index}" if index is not None else ""
        return None, f"Place{location} contains empty text fields."

    return {
        "name": normalized_name,
        "latitude": latitude,
        "longitude": longitude,
        "country": normalized_country,
    }, None


def parse_stage_payload(stage, index):
    """
    Validate and normalize a stage payload.
    """
    if not isinstance(stage, dict):
        return None, f"Stage at index {index} must be an object."

    place, error = parse_place_payload(stage, index)
    if error is not None:
        return None, error

    step_number = parse_optional_int(
        stage.get("StepNumber", stage.get("step", stage.get("position")))
    )
    cluster_number = parse_optional_int(
        stage.get("ClusterNumber", stage.get("clusterNumber", stage.get("cluster")))
    )
    hotel_id = parse_optional_int(
        stage.get("clusterHotelID", stage.get("HotelNumber", stage.get("hotel")))
    )

    if step_number is None:
        step_number = index + 1
    if cluster_number is None:
        cluster_number = 1

    return {
        **place,
        "step_number": step_number,
        "cluster_number": cluster_number,
        "hotel_id": hotel_id,
    }, None


def extract_user_id(data=None):
    """
    Read a user id from the payload or query string.
    """
    payload = data if isinstance(data, dict) else request_payload()
    return parse_optional_int(
        payload.get("UserID")
        or payload.get("userID")
        or payload.get("userId")
        or request.args.get("userID")
        or request.args.get("userId")
    )


def insert_or_get_place(cursor, place):
    """
    Return the PlaceID for a place, creating it when needed.
    """
    cursor.execute(
        """
        SELECT PlaceID
        FROM Place
        WHERE PlaceName = %s
            AND Latitude = %s
            AND Longitude = %s
            AND Country = %s;
        """,
        (place["name"], place["latitude"], place["longitude"], place["country"]),
    )
    result = cursor.fetchone()
    if result is not None:
        return result[0], False

    cursor.execute(
        """
        INSERT INTO Place (PlaceName, Latitude, Longitude, Country)
        VALUES (%s, %s, %s, %s)
        RETURNING PlaceID;
        """,
        (place["name"], place["latitude"], place["longitude"], place["country"]),
    )
    return cursor.fetchone()[0], True


def insert_stages(cursor, tour_id, stages):
    """
    Insert Stage rows for a tour.
    """
    hotel_column = get_stage_hotel_column(cursor)
    saved_stages = []

    for index, stage in enumerate(stages):
        parsed_stage, error = parse_stage_payload(stage, index)
        if error is not None:
            raise ValueError(error)

        place_id, place_created = insert_or_get_place(cursor, parsed_stage)
        hotel_id = parsed_stage["hotel_id"] if parsed_stage["hotel_id"] is not None else place_id

        columns = ["PlaceID", "TourID", "StepNumber", "ClusterNumber"]
        values = [
            place_id,
            tour_id,
            parsed_stage["step_number"],
            parsed_stage["cluster_number"],
        ]

        if hotel_column is not None:
            columns.append(hotel_column)
            values.append(hotel_id)

        query = sql.SQL("INSERT INTO Stage ({}) VALUES ({})").format(
            sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            sql.SQL(", ").join(sql.Placeholder() for _ in values),
        )
        cursor.execute(query, values)
        saved_stages.append({
            "placeId": place_id,
            "tourId": tour_id,
            "stepNumber": parsed_stage["step_number"],
            "clusterNumber": parsed_stage["cluster_number"],
            "hotelNumber": hotel_id,
            "createdPlace": place_created,
            **parsed_stage,
        })

    return saved_stages


def build_tour_query(cursor, where_clause="", params=()):
    """
    Build a SELECT query for tours with the optional tour length column.
    """
    tour_length_column = get_tour_length_column(cursor)
    columns = ["TourID", "TourName", "Visibility", "UserID"]
    if tour_length_column is not None:
        columns.append(tour_length_column)

    query = sql.SQL("SELECT {} FROM Tour {} ORDER BY TourID;").format(
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
        sql.SQL(where_clause),
    )
    return query, params, tour_length_column


def serialize_tour_row(row, tour_length_column):
    """
    Convert a tour row to an API object.
    """
    tour = {
        "tourId": row[0],
        "tourName": row[1],
        "visibility": row[2],
        "userId": row[3],
    }
    if tour_length_column is not None:
        tour["tourLength"] = row[4]
    return tour


def load_tour_with_stages(cursor, tour_id):
    """
    Load a single tour and its ordered stages.
    """
    tour_length_column = get_tour_length_column(cursor)
    tour_columns = ["TourID", "TourName", "Visibility", "UserID"]
    if tour_length_column is not None:
        tour_columns.append(tour_length_column)

    query = sql.SQL("SELECT {} FROM Tour WHERE TourID = %s;").format(
        sql.SQL(", ").join(sql.Identifier(column) for column in tour_columns)
    )
    cursor.execute(query, (tour_id,))
    tour_row = cursor.fetchone()
    if tour_row is None:
        return None

    hotel_column = get_stage_hotel_column(cursor)
    stage_select = [
        sql.SQL("Stage.PlaceID"),
        sql.SQL("Stage.TourID"),
        sql.SQL("Stage.StepNumber"),
        sql.SQL("Stage.ClusterNumber"),
    ]
    if hotel_column is not None:
        stage_select.append(sql.SQL(f"Stage.{hotel_column}"))
    stage_select.extend(
        [
            sql.SQL("Place.PlaceName"),
            sql.SQL("Place.Latitude"),
            sql.SQL("Place.Longitude"),
            sql.SQL("Place.Country"),
        ]
    )

    cursor.execute(
        sql.SQL(
            """
            SELECT {}
            FROM Stage
            JOIN Place ON Place.PlaceID = Stage.PlaceID
            WHERE Stage.TourID = %s
            ORDER BY Stage.StepNumber, Stage.PlaceID;
            """
        ).format(sql.SQL(", ").join(stage_select)),
        (tour_id,),
    )

    stages = []
    for row in cursor.fetchall():
        stage = {
            "placeId": row[0],
            "tourId": row[1],
            "stepNumber": row[2],
            "clusterNumber": row[3],
            "placeName": row[5 if hotel_column is not None else 4],
            "latitude": row[6 if hotel_column is not None else 5],
            "longitude": row[7 if hotel_column is not None else 6],
            "country": row[8 if hotel_column is not None else 7],
        }
        if hotel_column is not None:
            stage["hotelNumber"] = row[4]
        stages.append(stage)

    tour = serialize_tour_row(tour_row, tour_length_column)
    tour["stages"] = stages
    return tour


def require_owner(cursor, tour_id, user_id):
    """
    Verify ownership of a tour.
    """
    cursor.execute("SELECT UserID FROM Tour WHERE TourID = %s;", (tour_id,))
    row = cursor.fetchone()
    if row is None:
        return None, jsonify({"error": "Tour not found."}), 404
    if user_id is None:
        return row[0], None, None
    if row[0] != user_id:
        return row[0], jsonify({"error": "Forbidden."}), 403
    return row[0], None, None


@tourBlueprint.route("/tour", methods=["POST"])
@tourBlueprint.route("/tours", methods=["POST"])
def create_tour():
    """
    Create a new tour and optionally attach its stages.
    """
    data = request_payload()
    user_id = extract_user_id(data)
    tour_name = data.get("TourName") or data.get("tourName") or data.get("name")
    visibility = parse_visibility(data.get("Visibility", data.get("visibility", True)))
    tour_length = parse_float(
        data.get("tourLength", data.get("TourLength", data.get("TourLenght")))
    )
    stages = extract_optional_stages(data)

    if user_id is None:
        return jsonify({"error": "UserID is required."}), 400
    if not tour_name or not str(tour_name).strip():
        return jsonify({"error": "TourName is required."}), 400
    if visibility is None:
        return jsonify({"error": "Visibility must be a boolean value."}), 400
    if stages is not None and not isinstance(stages, list):
        return jsonify({"error": "Stages must be a list when provided."}), 400

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        tour_length_column = get_tour_length_column(cursor)

        columns = ["UserID", "TourName", "Visibility"]
        values = [user_id, str(tour_name).strip(), visibility]
        if tour_length_column is not None and tour_length is not None:
            columns.append(tour_length_column)
            values.append(tour_length)

        query = sql.SQL("INSERT INTO Tour ({}) VALUES ({}) RETURNING TourID;").format(
            sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            sql.SQL(", ").join(sql.Placeholder() for _ in values),
        )
        cursor.execute(query, values)
        tour_id = cursor.fetchone()[0]

        saved_stages = []
        if isinstance(stages, list) and stages:
            saved_stages = insert_stages(cursor, tour_id, stages)

        conn.commit()
        tour = load_tour_with_stages(cursor, tour_id)
        if tour is None:
            return jsonify({"error": "Unable to load created tour."}), 500

        return jsonify({
            "success": True,
            "message": "Tour created successfully.",
            "tour": tour,
            "stagesCreated": len(saved_stages),
        }), 201
    except ValueError as error:
        if conn is not None:
            conn.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        if conn is not None:
            conn.rollback()
        current_app.logger.exception("Unable to create tour")
        return jsonify({"error": "Unable to create tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tours", methods=["GET"])
def list_tours():
    """
    List tours, optionally including public tours for a specific user.
    """
    user_id = extract_user_id()
    include_public = parse_visibility(request.args.get("includePublic", "true"))

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        tour_length_column = get_tour_length_column(cursor)

        columns = ["TourID", "TourName", "Visibility", "UserID"]
        if tour_length_column is not None:
            columns.append(tour_length_column)

        if user_id is None:
            query = sql.SQL("SELECT {} FROM Tour WHERE Visibility = true ORDER BY TourID;").format(
                sql.SQL(", ").join(sql.Identifier(column) for column in columns)
            )
            cursor.execute(query)
        elif include_public is False:
            query = sql.SQL("SELECT {} FROM Tour WHERE UserID = %s ORDER BY TourID;").format(
                sql.SQL(", ").join(sql.Identifier(column) for column in columns)
            )
            cursor.execute(query, (user_id,))
        else:
            query = sql.SQL(
                "SELECT {} FROM Tour WHERE UserID = %s OR Visibility = true ORDER BY TourID;"
            ).format(sql.SQL(", ").join(sql.Identifier(column) for column in columns))
            cursor.execute(query, (user_id,))

        tours = [serialize_tour_row(row, tour_length_column) for row in cursor.fetchall()]
        return jsonify({"tours": tours}), 200
    except Exception:
        current_app.logger.exception("Unable to list tours")
        return jsonify({"error": "Unable to list tours."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tour/<int:tour_id>", methods=["GET"])
@tourBlueprint.route("/tours/<int:tour_id>", methods=["GET"])
def get_tour(tour_id):
    """
    Fetch a single tour with its stages.
    """
    user_id = extract_user_id()

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        tour_owner, error_response, status_code = require_owner(cursor, tour_id, user_id)
        if error_response is not None:
            cursor.execute("SELECT Visibility FROM Tour WHERE TourID = %s;", (tour_id,))
            visibility_row = cursor.fetchone()
            if visibility_row is None:
                return jsonify({"error": "Tour not found."}), 404
            if visibility_row[0] is False:
                return jsonify({"error": "Forbidden."}), 403

        tour = load_tour_with_stages(cursor, tour_id)
        if tour is None:
            return jsonify({"error": "Tour not found."}), 404

        if tour["visibility"] is False and user_id is not None and tour["userId"] != user_id:
            return jsonify({"error": "Forbidden."}), 403
        if tour["visibility"] is False and user_id is None:
            return jsonify({"error": "Forbidden."}), 403

        return jsonify({"tour": tour}), 200
    except Exception:
        current_app.logger.exception("Unable to get tour")
        return jsonify({"error": "Unable to get tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tour/<int:tour_id>", methods=["PUT", "PATCH"])
@tourBlueprint.route("/tours/<int:tour_id>", methods=["PUT", "PATCH"])
def update_tour(tour_id):
    """
    Update a tour's fields and optionally replace its stages.
    """
    data = request_payload()
    user_id = extract_user_id(data)
    tour_name = data.get("TourName") or data.get("tourName") or data.get("name")
    visibility = parse_visibility(data.get("Visibility", data.get("visibility")))
    tour_length = parse_float(
        data.get("tourLength", data.get("TourLength", data.get("TourLenght")))
    )
    stages = extract_optional_stages(data)

    if user_id is None:
        return jsonify({"error": "UserID is required."}), 400

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        owner_id, error_response, status_code = require_owner(cursor, tour_id, user_id)
        if error_response is not None:
            return error_response, status_code

        updates = []
        values = []
        tour_length_column = get_tour_length_column(cursor)

        if tour_name is not None and str(tour_name).strip():
            updates.append(sql.SQL("TourName = %s"))
            values.append(str(tour_name).strip())
        if visibility is not None:
            updates.append(sql.SQL("Visibility = %s"))
            values.append(visibility)
        if tour_length_column is not None and tour_length is not None:
            updates.append(sql.SQL("{} = %s").format(sql.Identifier(tour_length_column)))
            values.append(tour_length)

        if updates:
            values.append(tour_id)
            query = sql.SQL("UPDATE Tour SET {} WHERE TourID = %s;").format(
                sql.SQL(", ").join(updates)
            )
            cursor.execute(query, values)

        saved_stages = None
        if stages is not None:
            if not isinstance(stages, list):
                return jsonify({"error": "Stages must be a list when provided."}), 400
            cursor.execute("DELETE FROM Stage WHERE TourID = %s;", (tour_id,))
            saved_stages = insert_stages(cursor, tour_id, stages)

        conn.commit()
        tour = load_tour_with_stages(cursor, tour_id)
        if tour is None:
            return jsonify({"error": "Tour not found."}), 404

        return jsonify({
            "success": True,
            "message": "Tour updated successfully.",
            "tour": tour,
            "stagesReplaced": 0 if saved_stages is None else len(saved_stages),
        }), 200
    except ValueError as error:
        if conn is not None:
            conn.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        if conn is not None:
            conn.rollback()
        current_app.logger.exception("Unable to update tour")
        return jsonify({"error": "Unable to update tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tour/<int:tour_id>", methods=["DELETE"])
@tourBlueprint.route("/tours/<int:tour_id>", methods=["DELETE"])
def delete_tour(tour_id):
    """
    Delete a tour and its stages.
    """
    data = request_payload()
    user_id = extract_user_id(data)

    if user_id is None:
        return jsonify({"error": "UserID is required."}), 400

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        owner_id, error_response, status_code = require_owner(cursor, tour_id, user_id)
        if error_response is not None:
            return error_response, status_code

        cursor.execute("DELETE FROM Stage WHERE TourID = %s;", (tour_id,))
        cursor.execute("DELETE FROM Tour WHERE TourID = %s;", (tour_id,))
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Tour deleted successfully.",
            "tourId": tour_id,
        }), 200
    except Exception:
        if conn is not None:
            conn.rollback()
        current_app.logger.exception("Unable to delete tour")
        return jsonify({"error": "Unable to delete tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
