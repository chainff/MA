import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from CODE.demo_p import TradingApp, calculate_moving_averages, generate_signals

class TestDualMovingAverageStrategy(unittest.TestCase):

    def setUp(self):
        self.ticker = 'AAPL'
        self.short_window = 40
        self.long_window = 100
        self.mock_data = pd.DataFrame({
            'Close': np.random.rand(200) * 100 + 100
        })

    def test_moving_average_calculation(self):
        calculated_data = calculate_moving_averages(self.mock_data, self.short_window, self.long_window)
        self.assertIn('Short_MA', calculated_data, 'wrong SMA')
        self.assertIn('Long_MA', calculated_data, 'wrong lMA')

    def test_signal_generation(self):
        calculated_data = calculate_moving_averages(self.mock_data, self.short_window, self.long_window)
        signal_data = generate_signals(calculated_data)
        self.assertTrue((signal_data['Signal'].dropna().isin([1, 0, -1])).all(), 'wrong signal')

    def test_execute_trades(self):
        # Create a mock for the TradingApp instance
        with patch('demo_p.TradingApp') as MockTradingApp:
            # Create an instance of the mock TradingApp
            app = MockTradingApp()
            app.short_window.get.return_value = self.short_window
            app.long_window.get.return_value = self.long_window
            app.mock_data = self.mock_data

            # Patch the `execute_trade` method of the TradingApp instance
            with patch.object(app, 'execute_trade') as mock_execute_trade:
                # Assume execute_trade method decides to buy or sell
                mock_execute_trade.side_effect = lambda signal, price: app.buy(price) if signal == 1 else app.sell(
                    price)

                # Proceed with testing execute_trade logic
                calculated_data = calculate_moving_averages(app.mock_data, self.short_window, self.long_window)
                signal_data = generate_signals(calculated_data)

                # We need to set up the buy and sell methods on the app mock
                app.buy = MagicMock()
                app.sell = MagicMock()

                # Execute the mocked execute_trade method for each row
                for _, row in signal_data.iterrows():
                    price = row['Close']
                    signal = row['Position']
                    app.execute_trade(signal, price)

                if any(signal_data['Position'] == 1):
                    app.buy.assert_called()
                if any(signal_data['Position'] == -1):
                    app.sell.assert_called()

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
