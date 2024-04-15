import unittest
import pandas as pd
from CODE.demo_p import get_realtime_data, get_last_price


class TestRealTimeData(unittest.TestCase):

    def test_realtime_data_access(self):
        ticker = 'AAPL'
        data = get_realtime_data(ticker)

        self.assertIn('Open', data.columns, "Real-time data does not contain opening price.")
        self.assertIn('Close', data.columns, "Real-time data does not contain closing price.")
        self.assertIn('Volume', data.columns, "Real-time data does not contain volume data.")

        self.assertFalse(data.empty, "Real-time data retrieval returned an empty dataset.")

    def test_realtime_last_price(self):
        # Test the ability to get the last trading price of a specific stock
        ticker = 'AAPL'
        # Attempt to get the last price
        last_price = get_last_price(ticker)

        # Check if the last price is a float since stock prices are floats
        self.assertIsInstance(last_price, float, "The last price of the stock is not a float.")


# Run the test cases
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
