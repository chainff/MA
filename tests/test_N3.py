import unittest
from unittest.mock import patch
import tkinter as tk
from demo_p1 import TradingApp, calculate_moving_averages, generate_signals
import pandas as pd

# Mock data to simulate stock prices
mock_stock_data = {
    'Close': [100 + i + (i % 3 - 1) * 5 for i in range(30)]  # This simulates some 'noise' in stock prices
}
mock_stock_data_frame = pd.DataFrame(mock_stock_data)

class TestTradingAppMarketNoiseMitigation(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = TradingApp(self.root)
        self.app.short_window.set(5)  # Shorter window for more sensitivity
        self.app.long_window.set(10)  # Longer window for trend identification

    def tearDown(self):
        self.root.destroy()

    @patch('demo_p1.get_realtime_data')
    def test_mitigate_market_noise(self, mock_get_realtime_data):
        # Return mock data when get_realtime_data is called
        mock_get_realtime_data.return_value = mock_stock_data_frame

        # Directly use the mock data, as update_trading does not return data
        calculated_data = calculate_moving_averages(mock_stock_data_frame, self.app.short_window.get(), self.app.long_window.get())

        # Generate signals based on the calculated moving averages
        signals = generate_signals(calculated_data)

        # Check if moving averages smooth out the noise
        self.assertTrue((calculated_data['Short_MA'].diff().abs().mean() < calculated_data['Close'].diff().abs().mean()),
                        "Short moving average did not smooth out the noise")
        self.assertTrue((calculated_data['Long_MA'].diff().abs().mean() < calculated_data['Close'].diff().abs().mean()),
                        "Long moving average did not smooth out the noise")

        # Check for the presence of signals indicating significant trends
        self.assertTrue(signals['Signal'].sum() != 0, "No signals generated to indicate significant trends")

        # Optionally, check if signals align with expected trends in mock data

if __name__ == '__main__':
    unittest.main()
