from connexion import connect_to_database
from flask import Blueprint, current_app, jsonify, request
from psycopg2 import sql

tourBlueprint = Blueprint('tourBlueprint', __name__)


def parse_bool(value):
    """
    Convert API visibility values to the database boolean representation.
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


def parse_float(value):
    """
    Convert a numeric API value to float.
    """
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_optional_int(value):
    """
    Convert an optional API value to int.
    """
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_place(place, index):
    """
    Validate and normalize a place payload for the Place table.
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
        return None, (
            f"Place at index {index} must contain PlaceName, Latitude, "
            "Longitude, and Country."
        )

    normalized_name = str(name).strip()
    normalized_country = str(country).strip()

    if not normalized_name or not normalized_country:
        return None, f"Place at index {index} contains empty text fields."

    return {
        "name": normalized_name,
        "latitude": latitude,
        "longitude": longitude,
        "country": normalized_country,
    }, None


def parse_stage(stage, index):
    """
    Validate and normalize a stage payload for the Stage table.
    """
    if not isinstance(stage, dict):
        return None, f"Stage at index {index} must be an object."

    place, error = parse_place(stage, index)
    if error is not None:
        return None, error

    step_number = parse_optional_int(stage.get("StepNumber", stage.get("step")))
    cluster_number = parse_optional_int(
        stage.get("ClusterNumber", stage.get("clusterNumber", stage.get("cluster")))
    )
    hotel_number = parse_optional_int(
        stage.get("HotelNumber", stage.get("hotelNumber", stage.get("hotel")))
    )

    if step_number is None:
        step_number = index + 1
    if cluster_number is None:
        cluster_number = 1

    return {
        **place,
        "step_number": step_number,
        "cluster_number": cluster_number,
        "hotel_number": hotel_number,
    }, None


def get_tour_length_column(cursor):
    """
    Return the tour length column if present in the database.
    """
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'tour'
            AND lower(column_name) IN ('tourlength', 'tourlenght');
        """
    )
    result = cursor.fetchone()
    return result[0] if result is not None else None


def find_or_create_place(cursor, stage):
    """
    Return the PlaceID for a stage place, creating the place when necessary.
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
        (stage["name"], stage["latitude"], stage["longitude"], stage["country"]),
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
        (stage["name"], stage["latitude"], stage["longitude"], stage["country"]),
    )
    return cursor.fetchone()[0], True


def save_tour(cursor, user_id, tour_name, visibility, tour_length):
    """
    Create or update a Tour row and return its TourID.
    """
    cursor.execute(
        """
        SELECT TourID
        FROM Tour
        WHERE UserID = %s AND TourName = %s;
        """,
        (user_id, tour_name),
    )
    result = cursor.fetchone()
    tour_length_column = get_tour_length_column(cursor)

    if result is None:
        columns = ["UserID", "TourName", "Visibility"]
        values = [user_id, tour_name, visibility]
        placeholders = [sql.Placeholder()] * len(values)

        if tour_length_column is not None and tour_length is not None:
            columns.append(tour_length_column)
            values.append(tour_length)
            placeholders.append(sql.Placeholder())

        query = sql.SQL("INSERT INTO Tour ({}) VALUES ({}) RETURNING TourID;").format(
            sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            sql.SQL(", ").join(placeholders),
        )
        cursor.execute(query, values)
        return cursor.fetchone()[0], True

    tour_id = result[0]
    if tour_length_column is not None and tour_length is not None:
        query = sql.SQL(
            "UPDATE Tour SET Visibility = %s, {} = %s WHERE TourID = %s;"
        ).format(sql.Identifier(tour_length_column))
        cursor.execute(query, (visibility, tour_length, tour_id))
    else:
        cursor.execute(
            "UPDATE Tour SET Visibility = %s WHERE TourID = %s;",
            (visibility, tour_id),
        )
    return tour_id, False


def serialize_stage(row):
    """
    Convert a joined Stage/Place row to an API response object.
    """
    return {
        "placeId": row[0],
        "tourId": row[1],
        "stepNumber": row[2],
        "clusterNumber": row[3],
        "hotelNumber": row[4],
        "placeName": row[5],
        "latitude": row[6],
        "longitude": row[7],
        "country": row[8],
    }


@tourBlueprint.route("/tour", methods=["POST"])
@tourBlueprint.route("/tours", methods=["POST"])
def create_tour():
    """
    Save a tour with its places and stages.
    """
    data = request.get_json(silent=True) or {}
    user_id = parse_optional_int(data.get("UserID", data.get("userID", data.get("userId"))))
    tour_name = data.get("TourName") or data.get("tourName") or data.get("name")
    visibility = parse_bool(data.get("Visibility", data.get("visibility", True)))
    tour_length = parse_float(
        data.get("tourLength", data.get("TourLength", data.get("TourLenght")))
    )
    stages = data.get("stages") or data.get("places") or data.get("tourDatas")

    if user_id is None:
        return jsonify({"error": "UserID is required."}), 400
    if not tour_name or not str(tour_name).strip():
        return jsonify({"error": "TourName is required."}), 400
    if visibility is None:
        return jsonify({"error": "Visibility must be a boolean value."}), 400
    if not isinstance(stages, list) or not stages:
        return jsonify({"error": "A non-empty list of stages is required."}), 400

    parsed_stages = []
    for index, stage in enumerate(stages):
        parsed_stage, error = parse_stage(stage, index)
        if error is not None:
            return jsonify({"error": error}), 400
        parsed_stages.append(parsed_stage)

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        tour_id, created = save_tour(
            cursor,
            user_id,
            str(tour_name).strip(),
            visibility,
            tour_length,
        )
        cursor.execute("DELETE FROM Stage WHERE TourID = %s;", (tour_id,))

        saved_stages = []
        created_places = 0
        for stage in parsed_stages:
            place_id, place_created = find_or_create_place(cursor, stage)
            created_places += 1 if place_created else 0
            cursor.execute(
                """
                INSERT INTO Stage (
                    PlaceID,
                    TourID,
                    StepNumber,
                    ClusterNumber,
                    HotelNumber
                )
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    place_id,
                    tour_id,
                    stage["step_number"],
                    stage["cluster_number"],
                    stage["hotel_number"],
                ),
            )
            saved_stages.append({
                **stage,
                "placeId": place_id,
                "tourId": tour_id,
                "createdPlace": place_created,
            })

        conn.commit()
        return jsonify({
            "message": "Tour saved successfully.",
            "tourId": tour_id,
            "created": created,
            "createdPlaces": created_places,
            "stages": saved_stages,
        }), 201 if created else 200
    except Exception:
        if conn is not None:
            conn.rollback()
        current_app.logger.exception("Unable to save tour")
        return jsonify({"error": "Unable to save tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tours", methods=["GET"])
def list_tours():
    """
    List tours for a user, or public tours when no user is provided.
    """
    user_id = parse_optional_int(request.args.get("userID", request.args.get("userId")))
    include_public = parse_bool(request.args.get("includePublic", "true"))

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        tour_length_column = get_tour_length_column(cursor)
        length_select = (
            sql.SQL(", {}").format(sql.Identifier(tour_length_column))
            if tour_length_column is not None
            else sql.SQL("")
        )

        if user_id is None:
            query = sql.SQL(
                "SELECT TourID, TourName, Visibility, UserID{} "
                "FROM Tour WHERE Visibility = true ORDER BY TourID;"
            ).format(length_select)
            cursor.execute(query)
        elif include_public:
            query = sql.SQL(
                "SELECT TourID, TourName, Visibility, UserID{} "
                "FROM Tour WHERE UserID = %s OR Visibility = true ORDER BY TourID;"
            ).format(length_select)
            cursor.execute(query, (user_id,))
        else:
            query = sql.SQL(
                "SELECT TourID, TourName, Visibility, UserID{} "
                "FROM Tour WHERE UserID = %s ORDER BY TourID;"
            ).format(length_select)
            cursor.execute(query, (user_id,))

        tours = []
        for row in cursor.fetchall():
            tour = {
                "tourId": row[0],
                "tourName": row[1],
                "visibility": row[2],
                "userId": row[3],
            }
            if tour_length_column is not None:
                tour["tourLength"] = row[4]
            tours.append(tour)

        return jsonify({"tours": tours}), 200
    except Exception:
        current_app.logger.exception("Unable to list tours")
        return jsonify({"error": "Unable to list tours."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


@tourBlueprint.route("/tours/<int:tour_id>", methods=["GET"])
def get_tour(tour_id):
    """
    Return one tour and its ordered stages.
    """
    user_id = parse_optional_int(request.args.get("userID", request.args.get("userId")))

    conn = None
    cursor = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        tour_length_column = get_tour_length_column(cursor)
        length_select = (
            sql.SQL(", {}").format(sql.Identifier(tour_length_column))
            if tour_length_column is not None
            else sql.SQL("")
        )
        query = sql.SQL(
            "SELECT TourID, TourName, Visibility, UserID{} "
            "FROM Tour WHERE TourID = %s;"
        ).format(length_select)
        cursor.execute(query, (tour_id,))
        tour_row = cursor.fetchone()

        if tour_row is None:
            return jsonify({"error": "Tour not found."}), 404
        if not tour_row[2] and user_id != tour_row[3]:
            return jsonify({"error": "Forbidden."}), 403

        cursor.execute(
            """
            SELECT
                Stage.PlaceID,
                Stage.TourID,
                Stage.StepNumber,
                Stage.ClusterNumber,
                Stage.HotelNumber,
                Place.PlaceName,
                Place.Latitude,
                Place.Longitude,
                Place.Country
            FROM Stage
            JOIN Place ON Place.PlaceID = Stage.PlaceID
            WHERE Stage.TourID = %s
            ORDER BY Stage.StepNumber;
            """,
            (tour_id,),
        )

        tour = {
            "tourId": tour_row[0],
            "tourName": tour_row[1],
            "visibility": tour_row[2],
            "userId": tour_row[3],
            "stages": [serialize_stage(row) for row in cursor.fetchall()],
        }
        if tour_length_column is not None:
            tour["tourLength"] = tour_row[4]

        return jsonify({"tour": tour}), 200
    except Exception:
        current_app.logger.exception("Unable to get tour")
        return jsonify({"error": "Unable to get tour."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
