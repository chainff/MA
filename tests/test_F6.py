import unittest
import tkinter as tk
from CODE.demo_p import TradingApp


class TestRiskManagement(unittest.TestCase):
    def setUp(self):
        # Setup code to create a root window and instantiate the TradingApp.
        self.root = tk.Tk()
        self.app = TradingApp(self.root)

        # Assume the start_trading method will not be invoked for testing.
        self.app.trading_thread = None

        # Set up default values for testing without starting the trading thread.
        self.app.stop_loss_var.set(-0.05)  # Default stop loss value.
        self.app.take_profit_var.set(0.10)  # Default take profit value.


    def test_update_risk_management(self):
        # Test updating stop-loss and take-profit values.
        test_stop_loss = -0.10
        test_take_profit = 0.15

        # Simulate user input for stop-loss and take-profit.
        self.app.stop_loss_entry.delete(0, tk.END)
        self.app.stop_loss_entry.insert(0, str(test_stop_loss))
        self.app.take_profit_entry.delete(0, tk.END)
        self.app.take_profit_entry.insert(0, str(test_take_profit))

        # Call the update_risk_management method to update the values.
        self.app.update_risk_management()

        # Assert the portfolio dictionary is updated with new values.
        self.assertEqual(self.app.portfolio['stop_loss'], test_stop_loss)
        self.assertEqual(self.app.portfolio['take_profit'], test_take_profit)


    def tearDown(self):
        # Destroy the root window after each test.
        self.app.root.destroy()


if __name__ == '__main__':
    unittest.main()
