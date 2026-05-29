from location import Location
from tour import Tour

def main():
    picked_locations = [
        {'id': 0, 'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522, 'pos': 0, 'cn': 0, 'chi': 0}, 
        {'id': 3, 'name': 'Arras', 'lat': 50.292, 'lon': 2.78, 'pos': 1, 'cn': 1, 'chi': 3}, 
        {'id': 1, 'name': 'Lille', 'lat': 50.6292, 'lon': 3.0573, 'pos': 2, 'cn': 1, 'chi': 3}, 
        {'id': 2, 'name': 'Amiens', 'lat': 49.894, 'lon': 2.2957, 'pos': 3, 'cn': 1, 'chi': 3}, 
        {'id': 4, 'name': 'Lyon', 'lat': 45.764, 'lon': 4.8357, 'pos': 4, 'cn': 2, 'chi': 4}
    ]

    # 1. On recrée les objets Location avec leurs nouvelles propriétés d'ordre
    list_location = []
    for loc in picked_locations:
        location_obj = Location(loc["id"], loc["name"], loc["lat"], loc["lon"])
        location_obj.position = loc["pos"]
        location_obj.cluster_number = loc["cn"]
        location_obj.cluster_hotel_id = loc["chi"]
        list_location.append(location_obj)

    # On s'assure que la liste suit bien l'ordre des positions modifiées par l'utilisateur
    list_location.sort(key=lambda x: x.position)
    
    # Instance globale pour le calcul ou l'export futur
    global_tour = Tour(list_location)

    # 2. On extrait uniquement les hôtels uniques, dans l'ordre d'apparition choisi par l'utilisateur
    ordered_hotel_locations = []
    seen_hotel_ids = set()

    for location in list_location:
        # Si la ville actuelle est marquée comme un hôtel et qu'on ne l'a pas encore ajoutée
        if location.id == location.cluster_hotel_id and location.id not in seen_hotel_ids:
            ordered_hotel_locations.append(location)
            seen_hotel_ids.add(location.id)

    # 3. On crée le macro-tour composé uniquement de ces hôtels ordonnés
    macro_tour = Tour(ordered_hotel_locations)

    # 4. On crée la liste des indices pour calculer le score (avec retour au point de départ)
    hotel_indices = list(range(len(ordered_hotel_locations)))
    hotel_indices.append(hotel_indices[0])  # On boucle sur le premier hôtel du voyage

    # 5. Calcul de la nouvelle distance totale entre les hôtels
    new_total_distance = macro_tour.tour_score(hotel_indices)

    # 6. Affichage pour vérification avant envoi en BDD
    print("=== RECALCUL DU TRAJET PERSONNALISÉ ===")
    print("Ordre des hôtels choisi par l'utilisateur :")
    for order, hotel in enumerate(ordered_hotel_locations, start=1):
        print(f" Hôtel Étape {order} : {hotel.name} (Cluster N°: {hotel.cluster_number})")
    
    print(f"\nNouvelle distance totale entre les hôtels : {round(new_total_distance, 2)} km")

    # Ici, vous pouvez appeler votre fonction BDD pour mettre à jour les positions et la distance
    # update_trip_in_database(global_tour.export_itinerary(), new_total_distance)

if __name__ == "__main__":
    main()