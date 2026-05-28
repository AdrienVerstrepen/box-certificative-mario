import unittest
from algorithm.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.paris = Location(0, "Paris", 48.8566, 2.3522)
        self.lyon = Location(1, "Lyon", 45.7640, 4.8357)

    def test_initialization(self):
        self.assertEqual(self.paris.id, 0)
        self.assertEqual(self.paris.name, "Paris")
        self.assertEqual(self.paris.latitude, 48.8566)
        self.assertEqual(self.paris.longitude, 2.3522)
        self.assertEqual(self.paris.coordonates, (48.8566, 2.3522))

    def test_distance_between_different_locations(self):
        distance = self.paris.distance_locations(self.lyon)
        expected_distance = 392.2
        self.assertAlmostEqual(distance, expected_distance, delta=1.0)

    def test_distance_to_self_is_zero(self):
        distance = self.paris.distance_locations(self.paris)
        self.assertEqual(distance, 0.0)

    def test_repr(self):
        self.assertEqual(repr(self.paris), "Paris (ID : 0)")

if __name__ == "__main__":
    unittest.main()