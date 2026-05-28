from abc import ABC, abstractmethod

class BasePathFindingAlgorithm(ABC):
    @abstractmethod
    def find_shortest_itinerary(self, distance_matrix):
        """
        This method solves the problem of the shortest path by taking a distance matric of the locations and returning the list of the id of the locations, making an itinerary.
        """
        pass 