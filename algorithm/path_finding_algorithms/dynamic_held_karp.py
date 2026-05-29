from path_finding_algorithms.base_path_finding_algorithm import BasePathFindingAlgorithm

class DynamicHeldKarpTSP(BasePathFindingAlgorithm):
    def find_shortest_itinerary(self, distance_matrix):
        """
        This method finds the exact shortest path using the Held-Karp approach.
        """
        number_locations = len(distance_matrix)
        if number_locations <= 1:
            return list(range(number_locations))
            
        dict_distance = {}
        dict_decisions = {}

        def analysis_new_location(mask, index_location):
            # this is the end case where every location has been visited
            if mask == (1 << number_locations) - 1:
                return distance_matrix[index_location][0]

            key_current_state = (mask, index_location)
            # we check if we haven't previously done the research of the best next step
            if key_current_state in dict_distance:
                return dict_distance[key_current_state]

            minimum_distance = float('inf')
            best_next_node = -1
            for location in range(number_locations):
                # we add the location only if we didn't use it previously
                if not (mask & (1 << location)):
                    # we simulate a new mask and calculate the total cost of that possibility
                    new_mask = mask | (1 << location)
                    distance = distance_matrix[index_location][location] + analysis_new_location(new_mask, location)
                    if distance < minimum_distance:
                        # we add the new best option if the distance is lower than what we have previously found
                        minimum_distance = distance
                        best_next_node = location
            # we update the dictionnaries
            dict_distance[key_current_state] = minimum_distance
            dict_decisions[key_current_state] = best_next_node
            return minimum_distance

        # we set the starting point as the first location chosen and begin the analysis of the best steps
        analysis_new_location(1, 0)
        path = [0]
        mask = 1
        current_location = 0
        # we create the itinerary location by location
        while len(path) < number_locations:
            next_location = dict_decisions.get((mask, current_location))
            if next_location is None or next_location == -1:
                break
            path.append(next_location)
            # we do the fusion bewteen the previous mask and the new one
            mask |= (1 << next_location)
            current_location = next_location

        path.append(0)
        return path