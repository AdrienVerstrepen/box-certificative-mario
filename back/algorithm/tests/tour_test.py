import unittest
from back.algorithm.location import Location
from back.algorithm.tour import Tour

class TestTour(unittest.TestCase):
    def setUp(self):
        """"
        This method initializes three locations that will be used to test the rest.
        """
        self.paris = Location(0, "France", "Paris", 48.8566, 2.3522)
        self.lyon = Location(1, "France", "Lyon", 45.7640, 4.8357)
        self.marseille = Location(2, "France", "Marseille", 43.2965, 5.3698)

    def test_initialization_empty(self):
        """
        This method tests that an empty tour can be created.
        """
        tour = Tour()
        self.assertEqual(tour.locations, [])
        self.assertEqual(tour.distance_matrix, [])

    def test_initialization_with_locations(self):
        """
        This method tests that a tour with locations can be created.
        It also tests elements like the distance between a location and itself is 0 in the matrix, or the size of the matrix.
        """
        locations = [self.paris, self.lyon]
        tour = Tour(locations)
    
        self.assertEqual(len(tour.locations), 2)
        self.assertEqual(len(tour.distance_matrix), 2)
        self.assertEqual(len(tour.distance_matrix[0]), 2)
        self.assertEqual(tour.distance_matrix[0][0], 0.0)
        self.assertAlmostEqual(tour.distance_matrix[0][1], 392.2, delta=1.0)

    def test_add_location_updates_matrix(self):
        """
        This method tests the addition of a location to the tour, and the impacts it has on the matrix.
        """
        tour = Tour([self.paris])
        self.assertEqual(len(tour.distance_matrix), 1)
        
        tour.add_location(self.lyon)
        self.assertEqual(len(tour.distance_matrix), 2)
        self.assertAlmostEqual(tour.distance_matrix[1][0], 392.2, delta=1.0)

    def test_calculate_itinerary_distance(self):
        """
        This method calculates the total distance of an intinerary.
        """
        tour = Tour([self.paris, self.lyon, self.marseille])
        visit_order = [0, 1, 2, 0]
        
        distance_totale = tour.tour_score(visit_order)
        self.assertAlmostEqual(distance_totale, 1329.0, delta=5.0)

    def test_calculate_itinerary_distance_invalid_itinerary(self):
        """
        This method verifies that an incorrect path gives back "0.0".
        """
        tour = Tour([self.paris, self.lyon])

        self.assertEqual(tour.tour_score([]), 0.0)
        self.assertEqual(tour.tour_score([0]), 0.0)

    def test_format_itinerary(self):
        """
        This method tests if the format for the itinerary is correctly created.
        """
        tour = Tour([self.paris, self.lyon, self.marseille])
        visit_order = [0, 2, 1]
        itinerary = tour.format_itinerary(visit_order)
        
        self.assertEqual(len(itinerary), 3)
        
        self.assertEqual(itinerary[0]["visit_order"], 1)
        self.assertEqual(itinerary[0]["location_object"], self.paris)
        
        self.assertEqual(itinerary[1]["visit_order"], 2)
        self.assertEqual(itinerary[1]["location_object"], self.marseille)

    def test_repr(self):
        """
        This method verifies the information of a location are correctly showed.
        """
        tour = Tour([self.paris, self.lyon])
        self.assertEqual(repr(tour), "Tour with 2 locations")

if __name__ == "__main__":
    unittest.main()