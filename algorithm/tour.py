from location import Location

class Tour:
    def __init__(self, locations = None):
        """
        A tour is represented by a list of locations and a matrix of the distances between each location.
        The locations are ordered in the location list by their visit order.
        """
        if locations is not None :
            self.locations = locations
        else :
            self.locations = []
        self.distance_matrix = []
        if self.locations:
            self.generate_distance_matrix()

    def add_location(self, location):
        """
        This method adds a location to the tour and updates the distance matrix.
        """
        self.locations.append(location)
        self.generate_distance_matrix()

    def generate_distance_matrix(self):
        """
        This method generates a graph represented by an adjacency matrix, where each cell (the value at matrix[i][j]) contains the distance between location i and location j.
        """
        n = len(self.locations)
        distance_matrix = []
        for i in range(n):
            distance_matrix.append([0.0] * n)
        self.distance_matrix = distance_matrix
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.distance_matrix[i][j] = self.locations[i].distance_locations(self.locations[j])

    def tour_score(self, itinerary_indices):
        """
        This method calculates the total distance of a given sequence of location indices.
        The path returns to the starting location to complete the tour.
        """
        if not itinerary_indices or len(itinerary_indices) < 2:
            return 0.0
        total_distance = 0.0
        for i in range(len(itinerary_indices) - 1):
            index_start = itinerary_indices[i]
            index_end = itinerary_indices[i+1]
            total_distance += self.distance_matrix[index_start][index_end]
        return total_distance
    
    def format_itinerary(self, itinerary_indices):
        """
        This method takes an ordered list of indices and pairs each Location with its visit order.
        """
        tour_itinerary = []
        for order, index in enumerate(itinerary_indices):
            location = self.locations[index]
            if location.position == -1:
                location.position = order
            tour_itinerary.append({
                "visit_order": order + 1,
                "location_object": location
            })
        return tour_itinerary

    def export_itinerary(self):
        """
        This method exports the tour as a list of dictionaries ordered by their visit position.
        Each location contains its id, name, coordinates, and its final position index.
        """
        ordered_locations = sorted(self.locations, key=lambda loc: loc.position)
        exported_list = []
        for loc in ordered_locations:
            exported_list.append({
                "id": loc.id,
                "name": loc.name,
                "lat": loc.latitude,
                "lon": loc.longitude,
                "pos": loc.position
            })
        return exported_list

    def __repr__(self):
        """
        This method shows the information of the tour.
        """
        return f"Tour with {len(self.locations)} locations"