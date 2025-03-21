import os
import json
import re

def parse_gps_info(gps_info_str):
    try:
        # Extrahera latitud och longitud med regex
        lat_match = re.search(r"2: \((\d+\.\d+), (\d+\.\d+), (\d+\.\d+)\)", gps_info_str)
        lon_match = re.search(r"4: \((\d+\.\d+), (\d+\.\d+), (\d+\.\d+)\)", gps_info_str)
        
        if lat_match and lon_match:
            lat_deg, lat_min, lat_sec = map(float, lat_match.groups())
            lon_deg, lon_min, lon_sec = map(float, lon_match.groups())
            
            # Konvertera till decimalgrader
            latitude = lat_deg + lat_min/60 + lat_sec/3600
            longitude = lon_deg + lon_min/60 + lon_sec/3600
            
            # Kontrollera N/S och E/W
            if 'S' in gps_info_str:
                latitude = -latitude
            if 'W' in gps_info_str:
                longitude = -longitude
                
            return latitude, longitude
    except Exception as e:
        print(f"Error parsing GPS info: {e}")
    return None

def main():
    # Läs EXIF-data från JSON-filen
    with open('exif_data.json', 'r', encoding='utf-8') as f:
        exif_data = json.load(f)
    
    # Skapa en ny dictionary för koordinater
    coordinates = {}
    
    for filename, data in exif_data.items():
        if 'GPSInfo' in data:
            coords = parse_gps_info(data['GPSInfo'])
            if coords:
                coordinates[filename] = {
                    'lat': coords[0],
                    'lng': coords[1]
                }
    
    # Spara koordinaterna till en ny JSON-fil
    with open('coordinates.json', 'w', encoding='utf-8') as f:
        json.dump(coordinates, f, indent=2)
    
    # Skriv ut koordinaterna i ett format som är lätt att kopiera till Google Maps
    print("\nKoordinater för varje dörr:")
    for filename, coords in coordinates.items():
        print(f"{filename}: {coords['lat']}, {coords['lng']}")
    
    print("\nAntal dörrar med koordinater:", len(coordinates))

if __name__ == "__main__":
    main() 