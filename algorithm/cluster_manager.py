from location import Location

class ClusterManager:
    def __init__(self, locations, max_radius_km=100.0):
        """
        A cluster is represented by a list of locations, a maximum radius in kilometers between the hotel and the locations of each cluster and the list of the clusters.
        """
        self.locations = locations
        self.max_radius_km = max_radius_km
        self.clusters = []

    def create_clusters(self):
        """
        This method creates the clusters by looking at the distance between the different locations.
        We go location to location to create clusters based on distance using a temporary hotel for the cluster.
        When all of the clusters are made, we look at each cluster and find the best hotel for that cluster.
        We then add the information of the number of the cluster and the id of the hotel to each location.
        """
        unassigned_locations = list(self.locations)
        raw_clusters = []
        while unassigned_locations:
            temporary_hotel = unassigned_locations.pop(0)
            current_cluster_villes = [temporary_hotel]
            cities_to_keep = []
            for location in unassigned_locations:
                if temporary_hotel.distance_locations(location) <= self.max_radius_km:
                    current_cluster_villes.append(location)
                else:
                    cities_to_keep.append(location)
            unassigned_locations = cities_to_keep
            raw_clusters.append(current_cluster_villes)

        for cluster_index, cluster_villes in enumerate(raw_clusters):
            best_hotel = self.find_best_hotel(cluster_villes)
            for location in cluster_villes:
                location.cluster_number = cluster_index
                location.cluster_hotel_id = best_hotel.id
            self.clusters.append({
                "hotel": best_hotel,
                "locations": cluster_villes
            })
        return self.clusters

    def find_best_hotel(self, cluster_villes):
        """
        This method finds the best hotel for a cluster by finding the location that has the smallest distance with each location of the cluster.
        """
        if len(cluster_villes) <= 2:
            return cluster_villes[0]
        best_hotel = None
        minimum_total_distance = float('inf')
        for potential_hotel in cluster_villes:
            total_distance = 0.0
            for location in cluster_villes:
                total_distance += potential_hotel.distance_locations(location)
            if total_distance < minimum_total_distance:
                minimum_total_distance = total_distance
                best_hotel = potential_hotel
        return best_hotel