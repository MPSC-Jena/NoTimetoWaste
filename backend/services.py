import requests
import random
from typing import List
from geopy.geocoders import Nominatim

VALHALLA_URL = "http://localhost:8002/optimized_route"
geolocator = Nominatim(user_agent="notimetowaste_hackathon")

def get_optimized_route(locations, costing="auto", costing_options=None):
    payload = {
        "locations": locations,
        "costing": costing,
        "units": "kilometers"
    }
    if costing_options:
        payload["costing_options"] = costing_options
        
    try:
        response = requests.post(VALHALLA_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Valhalla: {e}")
        return None

def generate_random_locations(start_end_point, num_points=10):
    start_end_point["radius"] = 1000
    locations = [start_end_point]
    min_lat, max_lat = 50.9231, 50.9324
    min_lon, max_lon = 11.5746, 11.5945
    
    random.seed(42) 
    for _ in range(num_points):
        locations.append({
            "lat": random.uniform(min_lat, max_lat),
            "lon": random.uniform(min_lon, max_lon),
            "radius": 1000
        })
    return locations

def geocode_addresses(addresses: List[str]):
    locations = []
    for address in addresses:
        search_query = f"{address}, Jena, Germany"
        location = geolocator.geocode(search_query)
        if location:
            locations.append({
                "lat": location.latitude, 
                "lon": location.longitude,
                "radius": 1000
            })
        else:
            print(f"Warning: Could not geocode address: {address}")
    return locations
