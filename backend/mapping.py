import folium
from folium import plugins
import polyline
import os

def generate_route_map(locations, truck_route, start_end_point, output_file="api_tsp_map.html"):
    coords = []
    for leg in truck_route['trip']['legs']:
        coords.extend(polyline.decode(leg['shape'], 6))
        
    m = folium.Map(location=[start_end_point["lat"], start_end_point["lon"]], zoom_start=14)
    optimized_locations = truck_route['trip']['locations']
    
    for idx, loc in enumerate(optimized_locations):
        is_depot = (idx == 0 or idx == len(optimized_locations) - 1)
        marker_color = 'black' if is_depot else 'blue'
        marker_icon = 'home' if is_depot else 'info-sign'
        label = "Start Depot" if idx == 0 else ("End Depot" if is_depot else f"Stop {idx}")
        
        folium.Marker(
            [loc["lat"], loc["lon"]], 
            tooltip=f"{label} (Original Input #{loc.get('original_index', '?')})", 
            icon=folium.Icon(color=marker_color, icon=marker_icon),
            popup=f"<b>{label}</b>"
        ).add_to(m)
        
        if not is_depot:
            folium.map.Marker(
                [loc["lat"], loc["lon"]],
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(0,0),
                    html=f'<div style="font-size: 14pt; font-weight: bold; color: red;">{idx}</div>'
                )
            ).add_to(m)
        
    plugins.AntPath(
        locations=coords,
        color="red",
        weight=5,
        opacity=0.8,
        delay=800,
        dash_array=[15, 30],
        tooltip="Optimized Garbage Truck TSP Route (Follow the arrows)"
    ).add_to(m)
    
    map_path = os.path.join(os.path.dirname(__file__), output_file)
    m.save(map_path)
    return map_path
