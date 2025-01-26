def decimal_to_nmea(lat, lon):
    # Convert latitude
    try:
        lat_deg = int(abs(lat))
    except:
        print("Don't use string")
        exit()
    lat_min = (abs(lat) - lat_deg) * 60
    lat_dir = 'N' if lat >= 0 else 'S'
    
    # Convert longitude
    try:
        lon_deg = int(abs(lon))
    except:
        print("Din't use string")
        exit()
    lon_min = (abs(lon) - lon_deg) * 60
    lon_dir = 'E' if lon >= 0 else 'W'
    
    # Format the results
    lat_nmea = f"{lat_deg:02d}{lat_min:05.2f}{lat_dir}"
    lon_nmea = f"{lon_deg:03d}{lon_min:05.2f}{lon_dir}"
    
    return lat_nmea, lon_nmea

# Example usage
latitude = -7.445833
longitude = 109.279167

lat_nmea, lon_nmea = decimal_to_nmea(latitude, longitude)
print(f"NMEA Latitude: {lat_nmea}")
print(f"NMEA Longitude: {lon_nmea}")
