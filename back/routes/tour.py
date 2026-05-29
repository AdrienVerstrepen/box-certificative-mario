from connexion import connect_to_database
from flask import Blueprint, jsonify, request

@api.route("/tour", methods=['GET'])
def get_tour(userID, tourName, visibility, tourDatas):
    """
    This function adds a tour to the database.
    """

    conn = Connection()

    cursor = conn.cursor()

    cursor.execute("SELECT tourID FROM tour WHERE userID = %s AND tourName = %s;", (userID, tourName,))

    if cursor.fetchone() is None:
        cursor.execute("insert into tour (userID, tourName, visibility) values (%s, %s, %s);", (userID, tourName, visibility,))    


    cursor.execute("SELECT tourID FROM tour WHERE userID = %s AND tourName = %s;", (userID, tourName,))
    tourID = cursor.fetchone()[0]

    for tourData in tourDatas:
        cursor.execute("SELECT PlaceID FROM place WHERE placename = %s and latitude = %s and longitude = %s and country = %s;", (tourData['name'], tourData['latitude'], tourData['longitude'], tourData['country'],))

        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO place (PlaceName, Latitude, Longitude, Country) VALUES (%s, %s, %s, %s);", (tourData['name'], tourData['latitude'], tourData['longitude'], tourData['country'],))


        cursor.execute("SELECT PlaceID FROM place WHERE placename = %s and latitude = %s and longitude = %s and country = %s;", (tourData['name'], tourData['latitude'], tourData['longitude'], tourData['country'],))

        placeID = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM stage WHERE placeID = %s and tourID = %s;", (placeID, tourID,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO Stage VALUES (%s, %s, %s);", (placeID, tourID, tourData['step'],))

    conn.commit()

    cursor.close()
    conn.close()

    return tourDatas

