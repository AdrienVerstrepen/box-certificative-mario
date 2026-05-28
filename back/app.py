from config import api, Connection
from routes import *




if __name__ == "__main__":
    get_tour(1, "Tour de France", True, [
    {
        "name": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "country": "France",
        "step": 1
    },
    {
        "name": "Lyon",
        "latitude": 45.7640,
        "longitude": 4.8357,
        "country": "France",
        "step": 2
    },
    {
        "name": "Marseille",
        "latitude": 43.2965,
        "longitude": 5.3698,
        "country": "France",
        "step": 3
    }
    ])