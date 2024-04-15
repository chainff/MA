import unittest
from unittest.mock import patch
from CODE.demo_p import TradingApp, calculate_moving_averages, generate_signals
import pandas as pd
from tkinter import Tk

class TestTradingAppIntegration(unittest.TestCase):
    def setUp(self):
        # Create a hidden root window for testing
        self.root = Tk()
        self.root.withdraw()  # Hide the window
        self.app = TradingApp(self.root)

    def tearDown(self):
        # Destroy the hidden root window after the test
        self.root.destroy()

    def test_data_encryption_and_decryption(self):
        # Test encryption and decryption functionality
        original_positions = {'AAPL': 100}
        self.app.portfolio['positions'] = original_positions
        self.app.encrypt_positions()  # Encrypt
        self.assertNotEqual(self.app.portfolio['positions'], original_positions, "Positions should be encrypted")
        self.app.decrypt_positions()  # Decrypt
        self.assertEqual(self.app.portfolio['positions'], original_positions, "Positions should be decrypted back to original")

    def test_validate_integer_input(self):
        # Test integer input validation
        valid_input = "10"
        invalid_input = "ten"
        self.assertTrue(self.app.validate_integer(valid_input), "Valid integer input should return True")
        self.assertFalse(self.app.validate_integer(invalid_input), "Invalid integer input should return False")

    def test_validate_float_input(self):
        # Test float input validation
        valid_input = "10.5"
        invalid_input = "ten.point.five"
        self.assertTrue(self.app.validate_float(valid_input), "Valid float input should return True")
        self.assertFalse(self.app.validate_float(invalid_input), "Invalid float input should return False")

    def test_moving_averages_and_signals(self):
        # Test moving averages and signal generation
        data = pd.DataFrame({
            'Close': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
        })
        short_window = 3
        long_window = 5
        data_with_ma = calculate_moving_averages(data, short_window, long_window)
        signals = generate_signals(data_with_ma)
        self.assertIn('Short_MA', data_with_ma.columns, "Data should have short moving averages")
        self.assertIn('Long_MA', data_with_ma.columns, "Data should have long moving averages")
        self.assertIn('Signal', signals.columns, "Signals should be generated")

if __name__ == '__main__':
    unittest.main()
