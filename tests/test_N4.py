import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import pandas as pd
from demo_p1 import TradingApp, generate_signals

class TestTradingAppEnhancedComprehension(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = TradingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('demo_p1.get_realtime_data')
    @patch('demo_p1.calculate_moving_averages')
    def test_enhanced_comprehension(self, mock_calculate_moving_averages, mock_get_realtime_data):
        # Set up mock data
        mock_data_frame = pd.DataFrame({
            'Close': [100 + i for i in range(30)],  # Simplified mock data
        })
        mock_calculate_moving_averages.return_value = mock_data_frame.assign(
            Short_MA=lambda x: x['Close'].rolling(5).mean(),
            Long_MA=lambda x: x['Close'].rolling(10).mean()
        )
        mock_get_realtime_data.return_value = mock_data_frame

        # Invoke the trading logic
        self.app.update_trading()

        # Check if moving averages were calculated
        mock_calculate_moving_averages.assert_called_once()

        # Generate signals
        signals = generate_signals(mock_calculate_moving_averages.return_value)

        # Check if signals were generated, indicating potential comprehension
        self.assertIn('Signal', signals.columns, "Signal column is not present in the data")

        # Assert that there are buy/sell signals in the generated data
        self.assertTrue(signals['Signal'].abs().sum() > 0, "No buy/sell signals were generated")


if __name__ == '__main__':
    unittest.main()
