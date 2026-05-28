from path_finding_algorithms.base_path_finding_algorithm import BasePathFindingAlgorithm

class NearestNeighboursTSP(BasePathFindingAlgorithm):
    """
    This method finds the exact shortest path using the Nearest Neighbours approach.
    For each location, we look at the closest neigbour and we travel to that location.
    We do that until we visited all the locations.
    """
    def find_shortest_itinerary(self, distance_matrix):
        number_locations = len(distance_matrix)
        if number_locations <= 1:
            return list(range(number_locations))

        path = [0]
        visited = {0}
        current_location = 0
        while len(path) < number_locations:
            minimum_distance = float('inf')
            next_location = -1
            # for each location, we find the closest one
            for location in range(number_locations):
                if location not in visited:
                    distance = distance_matrix[current_location][location]
                    if distance < minimum_distance:
                        minimum_distance = distance
                        next_location = location
            path.append(next_location)
            visited.add(next_location)
            current_location = next_location

        path.append(0)
        return path