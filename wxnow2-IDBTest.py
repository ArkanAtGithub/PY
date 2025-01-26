import unittest
from unittest.mock import patch, MagicMock
from wxnow2 import get_data_from_influxdb  # Replace 'your_module' with the file name

class TestGetDataFromInfluxDB(unittest.TestCase):

    @patch('wxnow2.InfluxDBClient')
    def test_get_data_from_influxdb_success(self, MockInfluxDBClient):
        # Mock the client and query API response
        mock_client = MockInfluxDBClient.return_value
        mock_query_api = mock_client.query_api.return_value

        # Mock response from InfluxDB query
        mock_record = MagicMock()
        mock_record.get_field.return_value = 'temperature'
        mock_record.get_value.return_value = 25

        mock_table = MagicMock()
        mock_table.records = [mock_record]

        mock_query_api.query.return_value = [mock_table]

        # Call the function
        result = get_data_from_influxdb()

        # Assertions
        self.assertEqual(result, {'temperature': 25})
        mock_client.close.assert_called_once()

    @patch('wxnow2.InfluxDBClient')
    def test_get_data_from_influxdb_exception(self, MockInfluxDBClient):
        # Mock an exception when querying InfluxDB
        mock_client = MockInfluxDBClient.return_value
        mock_client.query_api.side_effect = Exception("InfluxDB error")

        with self.assertRaises(Exception):
            get_data_from_influxdb()

        mock_client.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
