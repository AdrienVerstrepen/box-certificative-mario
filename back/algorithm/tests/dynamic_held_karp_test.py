import os
import sys
algorithm_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if algorithm_folder not in sys.path:
    sys.path.insert(0, algorithm_folder)
import unittest
from path_finding_algorithms.dynamic_held_karp import DynamicHeldKarpTSP

class TestDynamicHeldKarpTSP(unittest.TestCase):
    def setUp(self):
        """
        This method initialises the algorithm before each test.
        """
        self.solver = DynamicHeldKarpTSP()

    def test_empty_or_single_location(self):
        """
        This method verifies the behaviour when there is no location or one location.
        """
        self.assertEqual(self.solver.find_shortest_itinerary([]), [])
        
        matrix_one_location = [[0.0]]
        self.assertEqual(self.solver.find_shortest_itinerary(matrix_one_location), [0])

    def test_two_locations(self):
        """
        This method verifies the length of a round-trip between two cities.
        """
        matrix_two_locations = [
            [0.0, 150.0],
            [150.0, 0.0]
        ]
        expected_path = [0, 1, 0]
        self.assertEqual(self.solver.find_shortest_itinerary(matrix_two_locations), expected_path)

    def test_four_locations_optimal_path(self):
        """
        This method verifies the algorithm found the shortest path between four options.
        """
        matrix_four = [
            [0.0, 10.0, 50.0, 45.0],
            [10.0, 0.0, 15.0, 60.0],
            [50.0, 15.0, 0.0, 20.0],
            [30.0, 60.0, 20.0, 0.0]
        ]
        expected_path = [0, 1, 2, 3, 0]
        result_path = self.solver.find_shortest_itinerary(matrix_four)
        self.assertEqual(result_path, expected_path)

if __name__ == "__main__":
    unittest.main()