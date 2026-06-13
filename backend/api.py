from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from database import init_db, get_route_hash, get_cached_route, save_route_to_cache
from services import generate_random_locations, geocode_addresses, get_optimized_route
from mapping import generate_route_map

app = FastAPI(title="NoTimeToWaste Routing API")

# Run DB init on startup
init_db()

class RoutingRequest(BaseModel):
    mode: str  # "random" or "custom"
    num_points: Optional[int] = 10
    addresses: Optional[List[str]] = None
    coordinates: Optional[List[dict]] = None

@app.post("/optimize_route")
def optimize_route(req: RoutingRequest):
    start_end_point = {"lat": 50.9270, "lon": 11.5830, "radius": 1000} # KSJ Depot
    locations = []
    
    if req.mode == "random":
        locations = generate_random_locations(start_end_point, req.num_points)
    elif req.mode == "custom":
        locations.append(start_end_point)
        if req.addresses:
            locations.extend(geocode_addresses(req.addresses))
        elif req.coordinates:
            locations.extend(req.coordinates)
        else:
            raise HTTPException(status_code=400, detail="Custom mode requires addresses or coordinates")
    else:
        raise HTTPException(status_code=400, detail="Mode must be 'random' or 'custom'")
        
    # Append the start point to the end to force a round trip
    if req.mode == "custom" and len(locations) > 1:
        locations.append(start_end_point)
    elif req.mode == "random" and locations[-1] != start_end_point:
        locations.append(start_end_point)
        
    if len(locations) < 2:
        raise HTTPException(status_code=400, detail="Not enough valid locations to route")

    # Check Cache
    route_hash = get_route_hash(locations)
    truck_route = get_cached_route(route_hash)
    is_cached = True
    
    if truck_route:
        print("Returning route from SQLite Cache!")
    else:
        print("Route not found in cache. Querying Valhalla...")
        is_cached = False
        truck_options = {
            "truck": {
                "length": 10.6,
                "width": 2.55,
                "height": 3.55,
                "weight": 26.0
            }
        }
        truck_route = get_optimized_route(locations, costing="truck", costing_options=truck_options)
        
        if not truck_route:
            raise HTTPException(status_code=500, detail="Failed to connect to Valhalla")
            
        save_route_to_cache(route_hash, truck_route)

    # Generate Map
    map_path = generate_route_map(locations, truck_route, start_end_point)
        
    return {
        "status": "success",
        "cached": is_cached,
        "num_locations_routed": len(locations),
        "locations_used": locations,
        "map_generated_at": map_path,
        "valhalla_response": truck_route
    }
