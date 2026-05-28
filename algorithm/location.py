import math
import haversine as hs   
from haversine import Unit

class Location:
    def __init__(self, city_id, name, latitude, longitude):
        """
        The location is represented by a city id, a name and coordinates, that can be accessed directly or the two of them together.
        """
        self.id = city_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        #self.country = country
        self.coordonates = (latitude, longitude)

    def distance_locations(self, location_2):
        """
        The distance between two coordinates is calculated using the haversine library which calculates the distance bewteen two points on the planet using the surface of a sphere.
        """
        return hs.haversine(self.coordonates, location_2.coordonates, unit=Unit.KILOMETERS)

    def __repr__(self):
        """
        This method shows the information of the location.
        """
        return f"{self.name} (ID : {self.id})"