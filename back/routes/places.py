from connexion import connect_to_database
from flask import Blueprint, jsonify, request

placesBlueprint = Blueprint('placesBlueprint', __name__)

def parse_place(place):
    """
    This function validates and normalizes a place payload.
    """
    name = place.get("Name")
    latitude = place.get("latitude")
    longitude = place.get("longitude")
    country = place.get("Country")

    if not name or latitude is None or longitude is None or not country:
        return None

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None

    return {
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "country": country,
    }

@placesBlueprint.route("/places", methods=["POST"])
def create_places():
    """
    This function receives a list of places and stores new places in the database.
    """
    places = request.get_json(silent=True)

    if not isinstance(places, list):
        return jsonify({"error": "A list of places is required."}), 400

    parsed_places = []
    for place in places:
        if not isinstance(place, dict):
            return jsonify({"error": "Each place must be an object."}), 400

        parsed_place = parse_place(place)
        if parsed_place is None:
            return jsonify({
                "error": "Each place must contain Name, latitude, longitude, and Country."
            }), 400

        parsed_places.append(parsed_place)

    conn = connect_to_database()
    cursor = conn.cursor()
    created_count = 0

    try:
        for place in parsed_places:
            cursor.execute(
                """
                SELECT PlaceID
                FROM Place
                WHERE PlaceName = %s
                    AND latitude = %s
                    AND longitude = %s
                    AND country = %s;
                """,
                (
                    place["name"],
                    place["latitude"],
                    place["longitude"],
                    place["country"],
                ),
            )

            if cursor.fetchone() is not None:
                continue

            cursor.execute(
                """
                INSERT INTO Place (PlaceName, latitude, longitude, country)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    place["name"],
                    place["latitude"],
                    place["longitude"],
                    place["country"],
                ),
            )
            created_count += 1

        conn.commit()
        return jsonify({
            "message": "Places received successfully.",
            "received": len(parsed_places),
            "created": created_count,
        }), 201
    finally:
        cursor.close()
        conn.close()
