import folium
from folium import plugins
import polyline
import os

def generate_route_map(all_truck_results, start_end_point, output_file="api_tsp_map.html"):
    m = folium.Map(location=[start_end_point["lat"], start_end_point["lon"]], zoom_start=14)
    
    # Pre-defined colors for different trucks
    colors = ["red", "blue", "green", "purple", "orange", "darkred", "cadetblue"]
    
    # Add Start Depot Marker
    folium.Marker(
        [start_end_point["lat"], start_end_point["lon"]], 
        tooltip="Start / End Depot", 
        icon=folium.Icon(color='black', icon='home'),
        popup="<b>KSJ Depot</b>"
    ).add_to(m)

    for truck_idx, truck_data in enumerate(all_truck_results):
        truck_id = truck_data["truck_id"]
        truck_route = truck_data["valhalla_response"]
        truck_color = colors[truck_idx % len(colors)]
        
        coords = []
        for leg in truck_route['trip']['legs']:
            coords.extend(polyline.decode(leg['shape'], 6))
            
        optimized_locations = truck_route['trip']['locations']
        
        for idx, loc in enumerate(optimized_locations):
            is_depot = (idx == 0 or idx == len(optimized_locations) - 1)
            if is_depot:
                continue # Already drew depot
                
            label = f"{truck_id} - Stop {idx}"
            
            folium.Marker(
                [loc["lat"], loc["lon"]], 
                tooltip=f"{label} (Original Input #{loc.get('original_index', '?')})", 
                icon=folium.Icon(color=truck_color, icon='info-sign'),
                popup=f"<b>{label}</b>"
            ).add_to(m)
            
            # Add a text label showing the stop number
            folium.map.Marker(
                [loc["lat"], loc["lon"]],
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(0,0),
                    html=f'<div style="font-size: 14pt; font-weight: bold; color: {truck_color};">{idx}</div>'
                )
            ).add_to(m)
            
        # Add route polyline (AntPath)
        plugins.AntPath(
            locations=coords,
            color=truck_color,
            weight=5,
            opacity=0.8,
            delay=800,
            dash_array=[15, 30],
            tooltip=f"{truck_id} Optimized Route"
        ).add_to(m)
    
    map_path = os.path.join(os.path.dirname(__file__), output_file)
    m.save(map_path)
    return map_path
