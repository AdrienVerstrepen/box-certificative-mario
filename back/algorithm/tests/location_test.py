import unittest
from back.algorithm.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        """"
        This method initializes two locations that will be used to test the rest.
        """
        self.paris = Location(0, "France", "Paris", 48.8566, 2.3522)
        self.lyon = Location(1, "France", "Lyon", 45.7640, 4.8357)

    def test_initialization(self):
        """
        This method tests the initialization of the locations.
        """
        self.assertEqual(self.paris.id, 0)
        self.assertEqual(self.paris.name, "Paris")
        self.assertEqual(self.paris.latitude, 48.8566)
        self.assertEqual(self.paris.longitude, 2.3522)
        self.assertEqual(self.paris.coordonates, (48.8566, 2.3522))

    def test_distance_between_different_locations(self):
        """"
        This method tests the method calculating the distance between two locations.
        """
        distance = self.paris.distance_locations(self.lyon)
        expected_distance = 392.2
        self.assertAlmostEqual(distance, expected_distance, delta=1.0)

    def test_distance_to_self_is_zero(self):
        """"
        This method verifies the method calculating the distance between two locations returns a null distance when the starting point and end point are the same location.
        """
        distance = self.paris.distance_locations(self.paris)
        self.assertEqual(distance, 0.0)

    def test_repr(self):
        """
        This method verifies the information of a location are correctly showed.
        """
        self.assertEqual(repr(self.paris), "Paris, France (ID : 0)")

if __name__ == "__main__":
    unittest.main()