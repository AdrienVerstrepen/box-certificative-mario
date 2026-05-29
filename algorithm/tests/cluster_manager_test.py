import unittest
from algorithm.cluster_manager import ClusterManager

class MockLocation:
    """
    We mock the location class to test the cluster manager.
    """
    def __init__(self, city_id, name):
        self.id = city_id
        self.name = name
        self.cluster_number = -1
        self.cluster_hotel_id = -1
        self.distances = {}

    def set_distance(self, other_location, distance_km):
        self.distances[other_location.id] = distance_km

    def distance_locations(self, other_location):
        if other_location.id == self.id:
            return 0.0
        return self.distances.get(other_location.id, 999.0)


class TestClusterManager(unittest.TestCase):
    def test_init_empty_locations(self):
        """
        This method tests the case of an empty list of locations.
        """
        manager = ClusterManager([])
        self.assertEqual(manager.locations, [])
        self.assertEqual(manager.max_radius_km, 100.0)
        self.assertEqual(manager.clusters, [])

    def test_create_clusters_single_location(self):
        """
        This method tests if the algorithm creates the cluster correctly when there is only one location.
        """
        paris = MockLocation(0, "Paris")
        manager = ClusterManager([paris], max_radius_km=100.0)
        clusters = manager.create_clusters()

        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["hotel"], paris)
        self.assertEqual(clusters[0]["locations"], [paris])
        self.assertEqual(paris.cluster_number, 0)
        self.assertEqual(paris.cluster_hotel_id, 0)

    def test_create_clusters_cities_within_radius(self):
        """
        This method tests the creation of a cluster when there is two cities that are close.
        """
        paris = MockLocation(0, "Paris")
        lille = MockLocation(1, "Lille")
        
        paris.set_distance(lille, 50.0)
        lille.set_distance(paris, 50.0)

        manager = ClusterManager([paris, lille], max_radius_km=100.0)
        clusters = manager.create_clusters()

        self.assertEqual(len(clusters), 1)
        self.assertIn(paris, clusters[0]["locations"])
        self.assertIn(lille, clusters[0]["locations"])
        self.assertEqual(paris.cluster_number, 0)
        self.assertEqual(lille.cluster_number, 0)

    def test_create_clusters_cities_too_far(self):
        """
        This method tests the creation of the clusters when the cities are far away.
        """
        paris = MockLocation(0, "Paris")
        marseille = MockLocation(2, "Marseille")
        
        paris.set_distance(marseille, 800.0)
        marseille.set_distance(paris, 800.0)

        manager = ClusterManager([paris, marseille], max_radius_km=100.0)
        clusters = manager.create_clusters()

        self.assertEqual(len(clusters), 2)
        self.assertEqual(paris.cluster_number, 0)
        self.assertEqual(marseille.cluster_number, 1)
        self.assertEqual(paris.cluster_hotel_id, 0)
        self.assertEqual(marseille.cluster_hotel_id, 2)

    def test_find_best_hotel_central_election(self):
        """
        This method tests to find the best hotel between three candidates.
        """
        location_a = MockLocation(0, "A")
        location_b = MockLocation(1, "B")
        location_c = MockLocation(2, "C")

        location_a.set_distance(location_b, 10.0)
        location_a.set_distance(location_c, 20.0)

        location_b.set_distance(location_a, 10.0)
        location_b.set_distance(location_c, 10.0)

        location_c.set_distance(location_a, 20.0)
        location_c.set_distance(location_b, 10.0)

        manager = ClusterManager([])
        best_hotel = manager.find_best_hotel([location_a, location_b, location_c])

        self.assertEqual(best_hotel, location_b)


if __name__ == "__main__":
    unittest.main()