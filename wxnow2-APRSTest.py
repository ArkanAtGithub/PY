import unittest
from unittest.mock import patch, MagicMock
from wxnow2 import login_to_aprs, send_data_via_aprs

class TestAPRSFunctions(unittest.TestCase):

    @patch('tenacity.retry', lambda *args, **kwargs: lambda f: f)  # Disable retries globally
    @patch('wxnow2.aprslib.IS')
    def test_login_to_aprs_success(self, MockAPRSLib):
        mock_ais = MockAPRSLib.return_value
        mock_ais.connect.return_value = None

        login_to_aprs()

        mock_ais.connect.assert_called_once()
        MockAPRSLib.assert_called_once_with(
            'YG2BXP-1', passwd='16567', host='asia.aprs2.net', port=14580
        )

    @patch('tenacity.retry', lambda *args, **kwargs: lambda f: f)
    @patch('wxnow2.aprslib.IS')
    def test_login_to_aprs_failure(self, MockAPRSLib):
        mock_ais = MockAPRSLib.return_value
        mock_ais.connect.side_effect = Exception("APRS connection error")

        with self.assertRaises(Exception):
            login_to_aprs()

        # Adjust for retries if still triggered
        self.assertGreaterEqual(mock_ais.connect.call_count, 1)

    @patch('tenacity.retry', lambda *args, **kwargs: lambda f: f)
    @patch('wxnow2.login_to_aprs')
    @patch('wxnow2.AIS')
    def test_send_data_via_aprs_success(self, MockAIS, mock_login_to_aprs):
        mock_ais_connection = MagicMock()
        MockAIS.sendall = mock_ais_connection.sendall

        data = {
            'temperature': 25,
            'humidity': 70,
            'pressure': 1013
        }

        send_data_via_aprs(data, mock_ais_connection)

        expected_message = (
            "YG2BXP-1>APRS,TCPIP*:!0726.45S/10916.45E_.../...g...t077h70b10130 https://bit.ly/yg2bxp-wx"
        )
        mock_ais_connection.sendall.assert_called_once_with(expected_message)

    @patch('tenacity.retry', lambda *args, **kwargs: lambda f: f)
    @patch('wxnow2.AIS')
    def test_send_data_via_aprs_error(self, MockAIS):
        mock_ais_connection = MagicMock()
        mock_ais_connection.sendall.side_effect = Exception("Send error")

        data = {'temperature': 25, 'humidity': 70, 'pressure': 1013}

        with self.assertRaises(Exception):
            send_data_via_aprs(data, mock_ais_connection)

        self.assertGreaterEqual(mock_ais_connection.sendall.call_count, 1)

if __name__ == '__main__':
    unittest.main()
