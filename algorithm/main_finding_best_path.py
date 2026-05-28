from location import Location
from tour import Tour
from path_finding_algorithms.dynamic_held_karp import DynamicHeldKarpTSP

def main():
    picked_locations = [
        {"id": 0, "name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"id": 1, "name": "Lille", "lat": 50.6292, "lon": 3.0573},
        {"id": 2, "name": "Lyon", "lat": 45.7640, "lon": 4.8357}
    ]

    list_location = []
    for location in picked_locations:
        list_location.append(Location(location["id"], location["name"], location["lat"], location["lon"]))
    tour = Tour(list_location)

    if len(list_location) <= 15:
        chosen_path_algorithm = DynamicHeldKarpTSP()
    else:
        chosen_path_algorithm = DynamicHeldKarpTSP()

    best_indices = chosen_path_algorithm.find_shortest_itinerary(tour.distance_matrix)
    total_distance = tour.tour_score(best_indices)
    itinerary = tour.format_itinerary(best_indices)

    for step in itinerary:
        order = step["visit_order"]
        city_name = step["location_object"].name
        print(f"Étape {order} : {city_name}")
        
    print(f"\nDistance totale du trajet : {round(total_distance, 2)} km")

if __name__ == "__main__":
    main()