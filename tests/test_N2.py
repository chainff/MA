import unittest
from unittest.mock import patch, MagicMock
from demo_p1 import TradingApp, get_realtime_data
import tkinter as tk  # Correct import statement for tkinter



class TestTradingAppUserEmpowerment(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.app = TradingApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_user_can_select_stock(self):
        # Verify the user can select a stock
        self.app.stock_code_combobox.set('AAPL')
        self.app.on_stock_selected(None)
        self.assertEqual(self.app.ticker, 'AAPL')

    def test_user_can_set_initial_capital(self):
        # Verify the user can set initial capital
        self.app.init_cash.set(100000)
        self.assertEqual(self.app.portfolio['init_capital'], 0)  # Initial value
        self.app.update_parameters()  # Update parameters
        self.assertEqual(self.app.portfolio['init_capital'], 100000)

    def test_user_can_set_trade_amount(self):
        # Verify the user can set trade amount
        self.app.trade_amount.set(100)
        self.assertEqual(self.app.trade_amount.get(), 100)

    @patch('demo_p1.yf.download')
    def test_user_can_set_moving_averages(self, mock_download):
        # Mock yfinance download to return example data
        mock_data = MagicMock()
        mock_download.return_value = mock_data

        # Verify the user can set moving average windows
        self.app.short_window.set(20)
        self.app.long_window.set(50)
        self.app.update_trading()  # This should initiate a trade based on moving averages
        self.assertEqual(self.app.short_window.get(), 20)
        self.assertEqual(self.app.long_window.get(), 50)



if __name__ == '__main__':
    unittest.main()
