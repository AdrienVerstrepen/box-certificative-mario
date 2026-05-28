from algorithm.location import Location
from algorithm.tour import Tour

def main():
    picked_locations = [
        {"id": 1, "name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"id": 2, "name": "Lyon", "lat": 45.7640, "lon": 4.8357},
        {"id": 3, "name": "Marseille", "lat": 43.2965, "lon": 5.3698},
        {"id": 4, "name": "Nantes", "lat": 47.2184, "lon": -1.5536}
    ]
    print(f"Loaded {len(picked_locations)} raw cities.")

    locations_list = []
    for data in picked_locations:
        loc = Location(
            city_id=data["id"],
            name=data["name"],
            latitude=data["lat"],
            longitude=data["lon"]
        )
        locations_list.append(loc)

    tour = Tour(locations_list)

if __name__ == "__main__":
    main()