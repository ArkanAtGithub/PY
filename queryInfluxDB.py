import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import time
import math
import logging
from logging.handlers import TimedRotatingFileHandler
from collections import deque
from statistics import mean

# InfluxDB connection parameters
bucket = "WX-1"
org = "ArkanDB"
token = "KZoUIqUtrPOPu80hP0oIzhCjsPn7K7dLCrQ_OlHfcxrmwKr6exZq8l8H8FdsrSoFcMWV3ILile2sT7r8mtXp1A=="
url = "http://192.168.0.6:8086"

# ThingSpeak parameters
ts_channel_id = "2499370"
ts_write_api_key = "R6ECLOX1FEOLV0MG"
ts_api_url = f"https://api.thingspeak.com/update?api_key={ts_write_api_key}"

# APRS WX file output path
output_file_path = "/home/arkan/Documents/testOutput/wxnow.txt"

# Initialize InfluxDB client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Query API
query_api = client.query_api()

# Set up logging
log_file_path = '/home/arkan/Documents/testOutput/wxnow.log'
backup_count = 7  # Number of backup files to keep (e.g., 7 days of logs)

# Custom namer function for log rotation
def namer(default_name):
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}{ext}"

# Set up logging with TimedRotatingFileHandler
handler = TimedRotatingFileHandler(
    log_file_path, 
    when="midnight", 
    interval=1, 
    backupCount=backup_count
)
handler.namer = namer
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Data storage for 10-minute averages
data_storage = {
    'temperature': deque(maxlen=40),  # 40 * 15 seconds = 10 minutes
    'humidity': deque(maxlen=40),
    'pressure': deque(maxlen=40)
}

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def query_influxdb():
    query = f'''
    from(bucket:"{bucket}")
    |> range(start: -1m)
    |> filter(fn: (r) => r._measurement == "weather_station")
    |> last()
    '''

    result = query_api.query(query)

    data = {}
    for table in result:
        for record in table.records:
            data[record.get_field()] = record.get_value()

    return data

def send_to_thingspeak(data):
    params = {
        'field1': data.get('temperature', ''),
        'field2': data.get('humidity', ''),
        'field3': data.get('pressure', ''),
        'field4': data.get('heat_index', ''),
        'field5': data.get('dew_point', ''),
        'field6': data.get('rssi', ''),
        'field7': data.get('rain', ''),
        # Add more fields as needed
    }

    response = requests.get(ts_api_url, params=params)

    if response.status_code == 200:
        logging.info("Data successfully sent to ThingSpeak")
    else:
        logging.error(f"Failed to send data to ThingSpeak. Status code: {response.status_code}")

def write_data_to_file(data):
    strf = time.strftime("%b %d %Y %H:%M")
    try:
        with open(output_file_path, "w") as file:
            file.write(f"{strf}\n")
            file.write(f".../...g...")
            celsius = float(data.get('temperature', 0))
            f = (celsius * 9 / 5) + 32
            file.write(f"t{math.trunc(f):03d}")
            rh = clamp(float(data.get('humidity', 0)), 0, 99)
            file.write(f"h{math.trunc(rh)}")
            baro = clamp(float(data.get('pressure', 1000)), 1000, 1010)
            baro = f"{baro:.1f}"
            file.write(f"b{int(str(baro).replace('.', ''))}")
        logging.info("Data successfully written to wxnow.txt")
    except Exception as e:
        logging.error(f"Error writing data to file: {e}")

def update_data_storage(data):
    for key in data_storage.keys():
        if key in data:
            data_storage[key].append(float(data[key]))

def get_averaged_data():
    return {
        'temperature': mean(data_storage['temperature']) if data_storage['temperature'] else None,
        'humidity': mean(data_storage['humidity']) if data_storage['humidity'] else None,
        'pressure': mean(data_storage['pressure']) if data_storage['pressure'] else None
    }

def main():
    last_file_write = 0
    while True:
        try:
            current_time = time.time()
            data = query_influxdb()

            if data:
                update_data_storage(data)
                send_to_thingspeak(data)

                # Write to file every 5 minutes with 10-minute averaged data
                if current_time - last_file_write >= 300:  # 300 seconds = 5 minutes
                    averaged_data = get_averaged_data()
                    write_data_to_file(averaged_data)
                    last_file_write = current_time
            else:
                logger.warning("No data retrieved from InfluxDB")

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

        time.sleep(15)  # Sleep for 15 seconds

if __name__ == "__main__":
    main()