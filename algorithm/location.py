import math
import haversine as hs   
from haversine import Unit

class Location:
    def __init__(self, city_id, name, latitude, longitude):
        self.id = city_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.coordonates = (latitude, longitude)

    def distance_locations(self, location_2):
        return hs.haversine(self.coordonates, location_2.coordonates, unit=Unit.KILOMETERS)

    def __repr__(self):
        return f"{self.name} (ID : {self.id})"