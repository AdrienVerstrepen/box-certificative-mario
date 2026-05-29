from .location import Location
from .tour import Tour

def main(picked_locations):
    """
    This is the pipeline to get the recalculated length of a path that was modified by the user.
    It returns a list with the dictionary for each location and the total distance.
    """
    list_location = []
    for location in picked_locations:
        location_object = Location(location["id"], location["country"], location["name"], location["lat"], location["lon"])
        location_object.position = location["pos"]
        location_object.cluster_number = location["clustnumber"]
        location_object.cluster_hotel_id = location["clusthotel"]
        list_location.append(location_object)

    list_location.sort(key=lambda x: x.position)
    tour = Tour(list_location)
    ordered_hotel_locations = []
    seen_hotel_ids = set()
    for location in list_location:
        if location.id == location.cluster_hotel_id and location.id not in seen_hotel_ids:
            ordered_hotel_locations.append(location)
            seen_hotel_ids.add(location.id)

    macro_tour = Tour(ordered_hotel_locations)
    hotel_indices = list(range(len(ordered_hotel_locations)))
    hotel_indices.append(hotel_indices[0])
    new_total_distance = macro_tour.tour_score(hotel_indices)

    json_export = tour.export_itinerary()
    json_export.append(new_total_distance)
    print(json_export)
    return json_export

if __name__ == "__main__":
    main()