import sqlite3
import hashlib
import json

DB_FILE = "routes_cache.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cached_routes (
            route_hash TEXT PRIMARY KEY,
            valhalla_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_route_hash(locations):
    loc_strings = [f"{loc['lat']:.5f},{loc['lon']:.5f}" for loc in locations]
    stable_string = "|".join(loc_strings)
    return hashlib.sha256(stable_string.encode('utf-8')).hexdigest()

def get_cached_route(route_hash):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT valhalla_response FROM cached_routes WHERE route_hash = ?", (route_hash,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def save_route_to_cache(route_hash, response):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cached_routes (route_hash, valhalla_response) VALUES (?, ?)", 
                   (route_hash, json.dumps(response)))
    conn.commit()
    conn.close()
