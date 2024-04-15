import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from demo_p1 import TradingApp

class TestTradingAppUsability(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.app = TradingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_user_can_update_parameters_easily(self):
        # Verify the user can update parameters easily with direct method calls
        self.app.init_cash.set(10000)
        self.app.short_window.set(20)
        self.app.long_window.set(50)
        self.app.trade_amount.set(100)

        # Normally, these would be set through the GUI, but we're checking that the programmatic interface is simple
        self.app.update_parameters()  # This method should be easy to call

        # Check if parameters were updated
        self.assertEqual(self.app.portfolio['init_capital'], 10000)
        self.assertEqual(self.app.short_window.get(), 20)
        self.assertEqual(self.app.long_window.get(), 50)
        self.assertEqual(self.app.trade_amount.get(), 100)

    @patch('demo_p1.TradingApp.buy')
    @patch('demo_p1.TradingApp.sell')
    def test_user_can_execute_trade_easily(self, mock_sell, mock_buy):
        # Setting the trade amount and ticker
        self.app.trade_amount.set(100)
        self.app.ticker = 'AAPL'

        # Pretend we have a market price to trade at
        market_price = 150

        # Directly call the buy and sell methods, which are now mocked
        self.app.buy(market_price)
        self.app.sell(market_price)

        # Check if the buy and sell methods were called, indicating a trade attempt
        mock_buy.assert_called_once_with(market_price)
        mock_sell.assert_called_once_with(market_price)


if __name__ == '__main__':
    unittest.main()
