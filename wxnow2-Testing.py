import unittest
from unittest.mock import patch, MagicMock
import logging
import time
import aprslib
import influxdb_client

# Import the functions to test
from wxnow2 import get_data_from_influxdb, send_data_via_aprs, login_to_aprs

class TestWeatherDataScript(unittest.TestCase):
    def setUp(self):
        # Override logging to write to a specific file during tests
        logging.disable(logging.CRITICAL)  # Disable logging temporarily

    def tearDown(self):
        # Re-enable logging after tests
        logging.disable(logging.NOTSET)

    @patch('influxdb_client.InfluxDBClient')
    def test_get_data_from_influxdb_success(self, MockInfluxDBClient):
        # Create mock objects to simulate InfluxDB response
        mock_client = MockInfluxDBClient.return_value
        mock_query_api = MagicMock()
        mock_client.query_api.return_value = mock_query_api

        # Create a mock table with records
        mock_table = MagicMock()
        mock_record1 = MagicMock()
        mock_record1.get_field.return_value = 'temperature'
        mock_record1.get_value.return_value = 25.5
        mock_record2 = MagicMock()
        mock_record2.get_field.return_value = 'humidity'
        mock_record2.get_value.return_value = 60

        mock_table.records = [mock_record1, mock_record2]
        mock_query_api.query.return_value = [mock_table]

        # Temporarily modify the function to use the mocked client
        with patch('wxnow2.InfluxDBClient', MockInfluxDBClient):
            # Call the function
            result = get_data_from_influxdb()

        # Assertions
        self.assertEqual(result, {'temperature': 25.5, 'humidity': 60})
        mock_client.close.assert_called_once()

    def test_send_data_via_aprs_success_with_output(self):
        # Prepare test data
        test_data = {
            'temperature': 25.5,
            'humidity': 60,
            'pressure': 1013.25
        }

        # Create a mock APRS connection
        mock_ais = MagicMock()

        # Call the function
        send_data_via_aprs(test_data, mock_ais)

        # Verify sendall was called with a properly formatted message
        mock_ais.sendall.assert_called_once()
        
        # Get the sent message
        sent_message = mock_ais.sendall.call_args[0][0]
        
        # Print the output string for visual inspection
        print("\nUse case output APRS Message:")
        print("-" * 40)
        print(sent_message)
        print("-" * 40)
        
        # Check the message format (basic checks)
        self.assertIn('YG2BXP-13>APRS', sent_message)
        self.assertIn('t078h60b10132', sent_message)  # Converted temp, humidity, pressure

    def test_send_data_via_aprs_edge_cases_with_output(self):
        # Test with missing or extreme values
        edge_cases = [
            # All values missing
            {},
            # Extreme temperature
            {'temperature': 100, 'humidity': 100, 'pressure': 1200},
            # Negative temperature
            {'temperature': -10, 'humidity': 0, 'pressure': 900},
            # All in
            {'temperature': -30, 'humidity': 110, 'pressure': 300}
        ]

        # Create a mock APRS connection
        mock_ais = MagicMock()

        print("\nEdge Cases APRS Messages:")
        print("-" * 40)
        for test_data in edge_cases:
            # Call the function
            send_data_via_aprs(test_data, mock_ais)

            # Get the sent message
            sent_message = mock_ais.sendall.call_args[0][0]
            
            # Print the output string for each edge case
            print(f"Input: {test_data}")
            print(f"Output: {sent_message}")
            print("-" * 40)

            # Verify sendall was called
            mock_ais.sendall.assert_called_once()
            
            # Reset the mock for next iteration
            mock_ais.sendall.reset_mock()

if __name__ == '__main__':
    unittest.main()
