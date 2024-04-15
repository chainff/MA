import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from demo_p1 import TradingApp


class TestTradingAppPerformanceAndReliability(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.app = TradingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('demo_p1.get_realtime_data')
    def test_timely_data_fetching(self, mock_get_realtime_data):
        # Mock the data fetching function to return data immediately
        mock_get_realtime_data.return_value = MagicMock()

        # Call the method that updates trading data
        self.app.update_trading()

        # Check if get_realtime_data was called, indicating that data fetching is being attempted
        mock_get_realtime_data.assert_called_once()

    @patch('demo_p1.TradingApp.execute_trade')
    def test_timely_trade_execution(self, mock_execute_trade):
        # Set up the conditions for a trade to occur
        self.app.portfolio['cash'] = 10000
        self.app.trade_amount.set(100)
        self.app.ticker = 'AAPL'

        # Simulate a market signal that should trigger a trade
        with patch('demo_p1.generate_signals') as mock_generate_signals:
            mock_generate_signals.return_value = MagicMock()
            mock_generate_signals.return_value['Position'].iloc[-1] = 1  # Signal to buy
            self.app.update_trading()

            # Check if execute_trade was called, indicating a trade attempt
            mock_execute_trade.assert_called_once()


if __name__ == '__main__':
    unittest.main()
