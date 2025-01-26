import time
import logging
from influxdb_client import InfluxDBClient
import aprslib

# Configure logging
logging.basicConfig(
    filename='/home/arkan/Documents/testOutput/wxnow.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# InfluxDB configuration
INFLUXDB_URL = "http://192.168.0.10:8086"
INFLUXDB_TOKEN = "u-gZObLHMXTvFaCOeCE4bMx7y3sxQ0ZUOjZV5YU3ZMjP4uufxowI1b_GwN12BMZN9ReoiqqigX-pspIz8W51aQ=="
INFLUXDB_ORG = "ArkanDB"
INFLUXDB_BUCKET = "WX-1"

# APRS-IS configuration
callsign = "YG2BXP-1"
passcode = "16567"
server_host = "asia.aprs2.net"
server_port = 14580

def get_data_from_influxdb():
    """
    Retrieves the latest data from InfluxDB.
    Returns:
        dict: A dictionary containing the latest weather data.
    """
    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        query_api = client.query_api()
        query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -5m) |> last()'
        tables = query_api.query(query)
        # Extract data from the response and convert it into a dictionary
        data = {}
        for table in tables:
            for record in table.records:
                data[record.get_field()] = record.get_value()
        logging.info("Data successfully retrieved from InfluxDB")
        return data
    except Exception as e:
        logging.error(f"Error retrieving data from InfluxDB: {e}")
        raise
    finally:
        client.close()

def send_data_via_aprs(data, AIS):
    """
    Sends data via APRS.

    Args:
    data (dict): A dictionary containing weather data.
    """
    try:
        # Construct APRS message using data retrieved from InfluxDB
        temp = data.get('temperature', 0)
        temp = round((temp * 9/5) + 32)
        humid = min(int(data.get('humidity', 0)), 100)  # Ensure humidity doesn't exceed 100
        humid = 0 if humid == 100 else humid  # Convert 100 to 00
        pressure = int(data.get('pressure', 0) * 10) # Assuming pressure in hPa and multiplying for APRS format

        message = f"{callsign}>APRS,TCPIP*:!0726.45S/10916.45E_.../...g...t{temp:03d}h{humid:02d}b{pressure:05d} https://bit.ly/yg2bxp-wx"
        AIS.sendall(message)
        
        logging.info("Data successfully sent via APRS")
    except Exception as e:
        logging.error(f"Error sending data via APRS: {e}")
        login_to_aprs()
        raise

def login_to_aprs():
    global AIS
    # One time login (*hopefully)
    try:
        AIS = aprslib.IS(callsign, passwd=passcode, host=server_host, port=server_port)
        logging.info(f"Login as {callsign}")
        AIS.connect()
    except Exception as e:
        logging.error(f"Error on login: {e}")
        raise

def main():
    # Call login to APRS-IS
    login_to_aprs()

    """
    Main function that fetches data from InfluxDB every 5 minutes and sends it via APRS.
    """
    while True:
        try:
            # Fetch the latest data from InfluxDB
            data = get_data_from_influxdb()
            # Send the data via APRS
            send_data_via_aprs(data, AIS)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
        # Wait for 5 minutes before the next request
        time.sleep(60 * 5)  # 5 minutes

if __name__ == "__main__":
    main()
