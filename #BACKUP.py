import socket

def search_symbol(symbol):
    # http://www.aprs.org/symbols/symbolsX.txt
    symbol_table = {
        "house": "/ -",
        "car": "/ >",
        "human": "/ [",
        "phone": "/ $"
    }

    symbol = symbol.lower()
    if symbol in symbol_table:
        table, sub = symbol_table[symbol].split()
    else:
        table, sub = None, None
        print("Not found")
        exit()

    return table, sub

def decimal_to_nmea(lat, lon):
    # Convert latitude
    try:
        lat_deg = int(abs(lat))
    except:
        print("Use float")
        exit()
    lat_min = (abs(lat) - lat_deg) * 60
    lat_dir = 'N' if lat >= 0 else 'S'
    
    # Convert longitude
    try:
        lon_deg = int(abs(lon))
    except:
        print("Use float")
        exit()
    lon_min = (abs(lon) - lon_deg) * 60
    lon_dir = 'E' if lon >= 0 else 'W'
    
    # Format the results
    lat_nmea = f"{lat_deg:02d}{lat_min:05.2f}{lat_dir}"
    lon_nmea = f"{lon_deg:03d}{lon_min:05.2f}{lon_dir}"
    
    return lat_nmea, lon_nmea

def send_aprs_message(callsign, passcode, server, port, message):
    # Construct the connection string
    connection_string = f"user {callsign} pass {passcode} vers PythonAPRS 1.0"

    # Construct the APRS message
    aprs_message = f"{callsign}>APRS,TCPIP*:!{lat_nmea}{table}{lon_nmea}{sub}{message}"

    try:
        # Establish connection to APRS-IS server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))

        # Send login string
        sock.sendall(connection_string.encode('utf-8') + b'\r\n')
        
        # Send APRS message
        sock.sendall(aprs_message.encode('utf-8') + b'\r\n')

        # Close the socket
        sock.close()

        print("==========================================")
        print(aprs_message)
        print("==========================================")
        print("Message sent successfully.")

    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # APRS-IS server
    server = "asia.aprs2.net"
    port = 14580

    # MYCALL
    callsign = "YG2BXP-1"
    passcode = "16567"

    # Decimal degrees coordinates
    latitude = -7.440777864357334
    longitude = 109.27445427202109

    # Symbol, see line 5 for list
    symbol = "HOUSE"

    # Your message
    message = "TEST"

    lat_nmea, lon_nmea = decimal_to_nmea(latitude, longitude)
    table, sub = search_symbol(symbol)
    send_aprs_message(callsign, passcode, server, port, message)