import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "WX-1"
org = "ArkanDB"
token = "1-wzx2DYoC_qDCuBGEgIq9Lyg9XMuGiHNUbfx_aFHZFXk6fH3PH8EiXv1knRyT13XZOxnfyfINJMfx8loT801g=="

url="http://192.168.0.6:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_test").tag("TEST", "Testing").field("testfield", 926)
write_api.write(bucket=bucket, org=org, record=p)
print("Done!")
