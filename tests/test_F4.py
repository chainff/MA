import unittest

import numpy as np
import pandas as pd
from unittest.mock import MagicMock
from CODE.demo_p import calculate_moving_averages, TradingApp


class TestCustomization(unittest.TestCase):

    def setUp(self):
        # Set up any necessary parameters for the tests
        self.default_short_window = 40
        self.default_long_window = 100
        self.custom_short_window = 15
        self.custom_long_window = 50
        self.mock_data = pd.DataFrame({
            'Close': np.random.rand(200) * 100 + 100  # Generate some mock closing prices
        })

    def test_window_customization(self):
        # Create a mock TradingApp object
        app = MagicMock(spec=TradingApp)
        # Mock the short_window and long_window attribute to mimic user customization
        app.short_window = self.custom_short_window
        app.long_window = self.custom_long_window

        # Test if the calculate_moving_averages function uses the custom parameters
        calculated_data = calculate_moving_averages(self.mock_data, app.short_window, app.long_window)

        # The first `custom_short_window - 1` values should be NaN because of the rolling window
        self.assertTrue(calculated_data['Short_MA'].isna().sum() == self.custom_short_window - 1,
                        "Short-term moving average not using custom window size.")

        # The first `custom_long_window - 1` values should be NaN because of the rolling window
        self.assertTrue(calculated_data['Long_MA'].isna().sum() == self.custom_long_window - 1,
                        "Long-term moving average not using custom window size.")


# Run all tests
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
