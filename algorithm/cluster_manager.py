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
        """
        unassigned_locations = list(self.locations)
        raw_clusters = []
        while unassigned_locations:
            temp_hotel = unassigned_locations.pop(0)
            current_cluster_villes = [temp_hotel]

            villes_a_garder = []
            for loc in unassigned_locations:
                if temp_hotel.distance_locations(loc) <= self.max_radius_km:
                    current_cluster_villes.append(loc)
                else:
                    villes_a_garder.append(loc)
            
            unassigned_locations = villes_a_garder
            raw_clusters.append(current_cluster_villes)

        for cluster_index, cluster_villes in enumerate(raw_clusters):
            best_hotel = self._elect_central_hotel(cluster_villes)
            
            for loc in cluster_villes:
                loc.cluster_number = cluster_index
                loc.cluster_hotel_id = best_hotel.id

            self.clusters.append({
                "hotel": best_hotel,
                "locations": cluster_villes
            })

        return self.clusters

    def _elect_central_hotel(self, cluster_villes):
        if len(cluster_villes) <= 2:
            return cluster_villes[0]

        best_hotel = None
        minimum_total_distance = float('inf')

        for potential_hotel in cluster_villes:
            total_distance = 0.0
            for loc in cluster_villes:
                total_distance += potential_hotel.distance_locations(loc)
            
            if total_distance < minimum_total_distance:
                minimum_total_distance = total_distance
                best_hotel = potential_hotel

        return best_hotel