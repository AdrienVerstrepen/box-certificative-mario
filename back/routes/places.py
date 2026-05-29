from connexion import connect_to_database
from flask import Blueprint, current_app, jsonify, request

from algorithm.main_finding_best_path import main

placesBlueprint = Blueprint('placesBlueprint', __name__)

def optimizeTravel(places):
    """
    Run the path-finding algorithm on the persisted places.
    """
    try:
        optimized_tour = main(places)
        current_app.logger.info("Optimized tour generated for %s place(s).", len(places))
        return optimized_tour
    except Exception:
        current_app.logger.exception("Unable to optimize travel")
        return None

def parse_place(place):
    """
    This function validates and normalizes a place payload.
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

    if not name or latitude is None or longitude is None or not country:
        return None

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None

    normalized_name = str(name).strip()
    normalized_country = str(country).strip()

    if not normalized_name or not normalized_country:
        return None

    return {
        "name": normalized_name,
        "latitude": latitude,
        "longitude": longitude,
        "country": normalized_country,
    }

@placesBlueprint.route("/places", methods=["POST"])
def create_places():
    """
    This function receives a list of places and stores new places in the database.
    """
    payload = request.get_json(silent=True)
    places = payload.get("places") if isinstance(payload, dict) else payload

    if not isinstance(places, list):
        return jsonify({"error": "A list of places is required."}), 400

    parsed_places = []
    for index, place in enumerate(places):
        if not isinstance(place, dict):
            return jsonify({"error": f"Place at index {index} must be an object."}), 400

        parsed_place = parse_place(place)
        if parsed_place is None:
            return jsonify({
                "error": (
                    f"Place at index {index} must contain PlaceName, Latitude, "
                    "Longitude, and Country."
                )
            }), 400

        parsed_places.append(parsed_place)

    conn = None
    cursor = None
    created_count = 0
    saved_places = []

    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        for place in parsed_places:
            cursor.execute(
                """
                SELECT PlaceID
                FROM Place
                WHERE PlaceName = %s
                    AND Latitude = %s
                    AND Longitude = %s
                    AND Country = %s;
                """,
                (
                    place["name"],
                    place["latitude"],
                    place["longitude"],
                    place["country"],
                ),
            )

            existing_place = cursor.fetchone()
            if existing_place is not None:
                saved_places.append({**place, "id": existing_place[0], "created": False})
                continue

            cursor.execute(
                """
                INSERT INTO Place (PlaceName, Latitude, Longitude, Country)
                VALUES (%s, %s, %s, %s)
                RETURNING PlaceID;
                """,
                (
                    place["name"],
                    place["latitude"],
                    place["longitude"],
                    place["country"],
                ),
            )
            place_id = cursor.fetchone()[0]
            saved_places.append({**place, "id": place_id, "created": True})
            created_count += 1

        conn.commit()

        saved_places_for_algorithm = [
            {
                "id": place["id"],
                "name": place["name"],
                "country": place["country"],
                "lat": place["latitude"],
                "lon": place["longitude"],
            }
            for place in saved_places
        ]

        # Places have been saved to DB, now compute the optimized itinerary.
        optimizeTravel(saved_places_for_algorithm)

        return jsonify({
            "message": "Places received successfully.",
            "received": len(parsed_places),
            "created": created_count,
            "places": saved_places,
        }), 201
    except Exception as error:
        if conn is not None:
            conn.rollback()
        current_app.logger.exception("Unable to save places")
        return jsonify({"error": "Unable to save places."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
