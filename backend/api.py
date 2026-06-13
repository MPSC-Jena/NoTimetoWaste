from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from database import init_db, get_route_hash, get_cached_route, save_route_to_cache
from services import generate_random_locations, geocode_addresses, get_optimized_route
from mapping import generate_route_map

app = FastAPI(title="NoTimeToWaste Routing API")

# Run DB init on startup
init_db()

class TruckConfig(BaseModel):
    truck_id: str
    addresses: Optional[List[str]] = None
    coordinates: Optional[List[dict]] = None
    num_points: Optional[int] = None # for random mode per truck

class RoutingRequest(BaseModel):
    mode: str  # "random" or "custom"
    trucks: List[TruckConfig]

@app.post("/optimize_route")
def optimize_route(req: RoutingRequest):
    start_end_point = {"lat": 50.9270, "lon": 11.5830, "radius": 1000} # KSJ Depot
    
    all_truck_results = []
    
    # Process each truck
    for truck in req.trucks:
        locations = []
        if req.mode == "random":
            pts = truck.num_points if truck.num_points else 5
            locations = generate_random_locations(start_end_point, pts)
        elif req.mode == "custom":
            locations.append(start_end_point)
            if truck.addresses:
                locations.extend(geocode_addresses(truck.addresses))
            elif truck.coordinates:
                locations.extend(truck.coordinates)
            else:
                raise HTTPException(status_code=400, detail=f"Custom mode requires addresses for {truck.truck_id}")
        else:
            raise HTTPException(status_code=400, detail="Mode must be 'random' or 'custom'")
            
        # Append the start point to the end to force a round trip
        if req.mode == "custom" and len(locations) > 1:
            locations.append(start_end_point)
        elif req.mode == "random" and locations[-1] != start_end_point:
            locations.append(start_end_point)
            
        if len(locations) < 2:
            continue

        # Check Cache
        route_hash = get_route_hash(locations)
        truck_route = get_cached_route(route_hash)
        is_cached = True
        
        if truck_route:
            print(f"Returning route for {truck.truck_id} from SQLite Cache!")
        else:
            print(f"Route for {truck.truck_id} not found in cache. Querying Valhalla...")
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
                raise HTTPException(status_code=500, detail=f"Failed to connect to Valhalla for {truck.truck_id}")
                
            save_route_to_cache(route_hash, truck_route)
            
        all_truck_results.append({
            "truck_id": truck.truck_id,
            "locations_used": locations,
            "valhalla_response": truck_route,
            "cached": is_cached
        })

    if not all_truck_results:
        raise HTTPException(status_code=400, detail="No valid routes could be generated")

    # Generate Map with all trucks
    map_path = generate_route_map(all_truck_results, start_end_point)
        
    return {
        "status": "success",
        "num_trucks_routed": len(all_truck_results),
        "truck_routes": all_truck_results,
        "map_generated_at": map_path
    }
