import requests
import json
import time
import os
import math
import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(filename='/home/arkan/Documents/testOutput/wxnow.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Define the absolute path for the output file
output_file_path = r"/home/arkan/Documents/testOutput/wxnow.txt"

# Define the ThingSpeak URL with average, round, and results parameters
url = "https://thingspeak.com/channels/2499370/feed.json?average=10&round=3&results=1"

# InfluxDB configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "KZoUIqUtrPOPu80hP0oIzhCjsPn7K7dLCrQ_OlHfcxrmwKr6exZq8l8H8FdsrSoFcMWV3ILile2sT7r8mtXp1A=="
INFLUXDB_ORG = "ArkanDB"
INFLUXDB_BUCKET = "WX-1"

def write_data_to_file(data):
    """
    Writes the extracted data from the ThingSpeak API to a specified file for APRS WX station use.

    Args:
    data (dict): The JSON data retrieved from the ThingSpeak API.
    """
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    strf = time.strftime("%b %d %Y %H:%M")
    try:
        with open(output_file_path, "w") as file:
            # Date and time
            file.write(f"{strf}\n")
            # Filler for wind data
            file.write(f".../...g...")
            # Extract desired information from the JSON data
            for feed in data["feeds"]:
                celsius = float(feed['field1'])
                f = (celsius * 9 / 5) + 32
                file.write(f"t0{math.trunc(f)}")
                rh = feed['field2']
                rh = clamp(float(rh), 0, 99)
                file.write(f"h{math.trunc(float(rh))}")
                baro = feed['field3']
                baro = clamp(float(baro), 1000, 1010)
                baro = f"{baro:.1f}"
                file.write(f"b{int(str(baro).replace('.', ''))}")
        logging.info("Data successfully written to wxnow.txt")
    except Exception as e:
        logging.error(f"Error writing data to file: {e}")

def write_to_influxdb(data):
    """
    Writes the data to InfluxDB.

    Args:
    data (dict): The JSON data retrieved from the ThingSpeak API.
    """
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        for feed in data["feeds"]:
            point = Point("weather_data") \
                .field("temperature", float(feed['field1'])) \
                .field("humidity", float(feed['field2'])) \
                .field("pressure", float(feed['field3'])) \
                .field("heat_index", float(feed['field4'])) \
                .field("dew_point", float(feed['field5'])) \
                .field("rain", float(feed['field7'])) \
                .time(feed['created_at'])

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        logging.info("Data successfully written to InfluxDB")
    except Exception as e:
        logging.error(f"Error writing data to InfluxDB: {e}")
    finally:
        client.close()

def main():
    """
    Main function that fetches data from ThingSpeak API every 5 minutes, 
    writes it to a file, and sends it to InfluxDB.
    """
    while True:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            # Check for successful response
            if response.status_code == 200:
                # Parse the JSON data
                data = json.loads(response.text)
                # Write the data to the file
                write_data_to_file(data)
                # Write the data to InfluxDB
                # write_to_influxdb(data)
            else:
                logging.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
        # Wait for 5 minutes before the next request
        time.sleep(60 * 5)  # (60 * 5 = 300s) 300s = 5m

if __name__ == "__main__":
    main()