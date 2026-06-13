# No Time to Waste – Smarte Routen für Jenas Müllfahrzeuge

Wie navigiert man ein Müllfahrzeug sicher und effizient durch enge Straßen, Sackgassen und zugeparkte Viertel? Bisher basiert die Routenplanung des Kommunalservice Jena vor allem auf Erfahrungswissen der Fahrer:innen. Dabei existieren bereits wertvolle Geodaten zu Straßenbreiten, Kreuzungen und Verkehrsregeln – sie werden jedoch noch nicht für das Routing miteinander in Verbindung gesetzt.

**Deine Challenge**

Eure Aufgabe ist es, einen Prototypen zu entwickeln, der städtische GIS-Daten mit OpenStreetMap und dem Routingdienst Valhalla verbindet. Ziel ist eine realitätsnahe Navigation speziell für Müllfahrzeuge, die problematische Straßen erkennt und fahrzeugspezifische Anforderungen wie Breite, Länge oder Wendekreis berücksichtigt. Gesucht sind kreative Ansätze für datengetriebene Mobilität und smarte Stadtlogistik!

# No Time to Waste – Smart Routes for Jena’s Garbage Trucks

How do you navigate a garbage truck safely and efficiently through narrow streets, dead-ends, and neighborhoods clogged with parked cars? Until now, route planning at Kommunalservice Jena has relied primarily on drivers’ experience. Yet valuable geodata on street widths, intersections, and traffic rules already exists—it just hasn’t been integrated into the routing process yet.

**Your Challenge**

Your task is to develop a prototype that integrates municipal GIS data with OpenStreetMap and the Valhalla routing service. The goal is to create realistic navigation specifically for garbage trucks that identifies problematic roads and takes vehicle-specific requirements—such as width, length, and turning radius—into account. We’re looking for creative approaches to data-driven mobility and smart urban logistics!

---

## 🚀 MVP Implementation / Getting Started

This repository contains a full MVP backend for routing 10.6m x 2.55m garbage trucks efficiently through Jena, avoiding narrow streets and optimizing pickup sequences (TSP - Traveling Salesperson Problem).

### 1. Prerequisites (WSL)
You need `uv`, `Python 3.10+`, and `Docker` installed.
```bash
cd backend
# Install required dependencies
uv add fastapi uvicorn geopy requests folium polyline geopandas fiona mapclassify
```

### 2. Start the Valhalla Routing Server
The Valhalla routing engine (including Jena's graph data) is bundled via Docker.
```bash
# Run this from the root directory to extract the provided Valhalla data
uv run python extract_valhalla.py

# Start the Valhalla Docker container (runs on port 8002)
cd backend/valhalla_data/valhalla
docker-compose -f docker-compose.dev.yml up -d
cd ../../..
```

### 3. Extracting Municipal Street Widths
To prove that we can integrate municipal GIS data, we created an ATKIS parser. It dynamically extracts `.dbf`/shapefiles, finds the `breiteDerFahrBahn` (BRF), and color-codes roads in Jena.
```bash
cd backend
uv run python atkis_parser.py
```
*Output: Open `backend/atkis_widths_map.html` to see roads color-coded by width (Red < 2.55m).*

### 4. Run the Garbage Truck Routing API
We expose Valhalla's TSP (Traveling Salesperson) optimization via a FastAPI service. It handles geocoding of raw address strings into GPS coordinates and forces a complete round-trip loop back to the depot!

```bash
cd backend
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Testing the API
Once the API is running, visit **[http://localhost:8000/docs](http://localhost:8000/docs)** to test the `/optimize_route` endpoint.

**Test Case 1: Random Points**
Generates random safe locations in Jena and routes the truck.
```json
{
  "mode": "random",
  "num_points": 10
}
```

**Test Case 2: Custom Addresses**
Input natural street names. The API geocodes them and generates the optimal pickup loop.
```json
{
  "mode": "custom",
  "addresses": [
    "Holzmarkt",
    "Markt",
    "Löbdergraben 10"
  ]
}
```

**Output Visualization:**
After executing the API call, open **`backend/api_tsp_map.html`** in your browser. You will see:
1. Numbered stops showing the exact optimized pickup order.
2. Animated directional arrows (AntPath) showing the exact path the truck takes.
3. A closed loop that safely returns the truck to the depot.
