import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from demo_p1 import TradingApp, get_realtime_data

class TestTradingApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.app = TradingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('demo_p1.yf.download')
    def test_get_realtime_data(self, mock_download):
        # Setup mock
        mock_data = MagicMock()
        mock_download.return_value = mock_data

        # Execute
        ticker = 'AAPL'
        data = get_realtime_data(ticker)

        # Assert
        mock_download.assert_called_once_with(tickers=ticker, period='1mo', interval='5m')
        self.assertEqual(data, mock_data)

if __name__ == '__main__':
    unittest.main()
