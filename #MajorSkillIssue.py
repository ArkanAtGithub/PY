import tkinter as tk
from tkinter import messagebox
import socket

def search_symbol(symbol):
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
        messagebox.showerror("Error", "Symbol not found")
        return None, None

    return table, sub

def decimal_to_nmea(lat, lon):
    try:
        lat_deg = int(abs(lat))
        lat_min = (abs(lat) - lat_deg) * 60
        lat_dir = 'N' if lat >= 0 else 'S'
    
        lon_deg = int(abs(lon))
        lon_min = (abs(lon) - lon_deg) * 60
        lon_dir = 'E' if lon >= 0 else 'W'
    
        lat_nmea = f"{lat_deg:02d}{lat_min:05.2f}{lat_dir}"
        lon_nmea = f"{lon_deg:03d}{lon_min:05.2f}{lon_dir}"
    
        return lat_nmea, lon_nmea
    except:
        messagebox.showerror("Error", "Invalid coordinates")
        return None, None

def send_aprs_message():
    callsign = callsign_entry.get()
    passcode = passcode_entry.get()
    server = server_entry.get()
    port = int(port_entry.get())
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())
    symbol = symbol_entry.get()
    message = message_entry.get()

    lat_nmea, lon_nmea = decimal_to_nmea(latitude, longitude)
    if not lat_nmea or not lon_nmea:
        return

    table, sub = search_symbol(symbol)
    if not table or not sub:
        return

    connection_string = f"user {callsign} pass {passcode} vers PythonAPRS 1.0"
    aprs_message = f"{callsign}>APRS,TCPIP*:!{lat_nmea}{table}{lon_nmea}{sub} {message}"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        sock.sendall(connection_string.encode('utf-8') + b'\r\n')
        sock.sendall(aprs_message.encode('utf-8') + b'\r\n')
        sock.close()

        messagebox.showinfo("Success", "Message sent successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Error sending message: {e}")

app = tk.Tk()
app.title("APRS Message Sender")

# Set a consistent font style
font_style = ("Helvetica", 12)

# Make the window fixed size
app.geometry("300x400")
app.resizable(False, False)

# Add a title label
title_label = tk.Label(app, text="APRS Message Sender", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

tk.Label(app, text="Callsign:", font=font_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
callsign_entry = tk.Entry(app, font=font_style)
callsign_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Passcode:", font=font_style).grid(row=2, column=0, padx=10, pady=5, sticky="e")
passcode_entry = tk.Entry(app, font=font_style)
passcode_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Server:", font=font_style).grid(row=3, column=0, padx=10, pady=5, sticky="e")
server_entry = tk.Entry(app, font=font_style)
server_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(app, text="Port:", font=font_style).grid(row=4, column=0, padx=10, pady=5, sticky="e")
port_entry = tk.Entry(app, font=font_style)
port_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(app, text="Latitude:", font=font_style).grid(row=5, column=0, padx=10, pady=5, sticky="e")
latitude_entry = tk.Entry(app, font=font_style)
latitude_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(app, text="Longitude:", font=font_style).grid(row=6, column=0, padx=10, pady=5, sticky="e")
longitude_entry = tk.Entry(app, font=font_style)
longitude_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(app, text="Symbol:", font=font_style).grid(row=7, column=0, padx=10, pady=5, sticky="e")
symbol_entry = tk.Entry(app, font=font_style)
symbol_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(app, text="Message:", font=font_style).grid(row=8, column=0, padx=10, pady=5, sticky="e")
message_entry = tk.Entry(app, font=font_style)
message_entry.grid(row=8, column=1, padx=10, pady=5)

send_button = tk.Button(app, text="Send APRS Message", font=font_style, command=send_aprs_message)
send_button.grid(row=9, column=0, columnspan=2, pady=(20, 10))

app.mainloop()
