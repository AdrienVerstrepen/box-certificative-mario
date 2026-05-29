from location import Location
from tour import Tour
from path_finding_algorithms.dynamic_held_karp import DynamicHeldKarpTSP
from path_finding_algorithms.nearest_neighbours import NearestNeighboursTSP
from cluster_manager import ClusterManager

def main(picked_locations):
    """
    This is the pipeline to get the the optimized tour for a user with the locations they picked.
    It returns a list with the dictionary for each location and the total distance.
    """
    list_location = []
    for location in picked_locations:
        list_location.append(Location(location["id"], location["name"], location["lat"], location["lon"]))
    tour = Tour(list_location)

    manager = ClusterManager(list_location, max_radius_km=100.0)
    clusters = manager.create_clusters()
    hotel_locations = []
    for cluster in clusters:
        hotel_locations.append(cluster["hotel"])
    macro_tour = Tour(hotel_locations)

    if len(hotel_locations) <= 15:
        chosen_path_algorithm = DynamicHeldKarpTSP()
    else:
        chosen_path_algorithm = NearestNeighboursTSP()

    best_hotel_indices = chosen_path_algorithm.find_shortest_itinerary(macro_tour.distance_matrix)
    global_indices = []
    for hotel_index_in_macro in best_hotel_indices[:-1]:
        current_hotel = macro_tour.locations[hotel_index_in_macro]
        global_hotel_index = tour.locations.index(current_hotel)
        global_indices.append(global_hotel_index)

        current_cluster = None
        for cluster in clusters:
            if cluster["hotel"].id == current_hotel.id:
                current_cluster = cluster
                break
        
        for location in current_cluster["locations"]:
            if location.id != current_hotel.id:
                global_villes_index = tour.locations.index(location)
                global_indices.append(global_villes_index)

    global_indices.append(global_indices[0])
    itinerary = tour.format_itinerary(global_indices)
    total_distance = tour.tour_score(global_indices)

    for step in itinerary:
        location = step["location_object"]

    json_export = tour.export_itinerary()
    json_export.append(total_distance)
    return json_export

if __name__ == "__main__":
    main()