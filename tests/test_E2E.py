import unittest
from CODE.demo_p import TradingApp
from tkinter import Tk

class TestTradingApp(unittest.TestCase):

    def setUp(self):
        # Create a Tkinter root window but don't display it
        self.root = Tk()
        self.root.withdraw()  # Make the root window invisible
        self.app = TradingApp(self.root)

    def tearDown(self):
        # Destroy the Tkinter window after the test
        self.root.destroy()

    def test_validate_integer(self):
        self.assertTrue(self.app.validate_integer("10"), "Should return True, because '10' is an integer")
        self.assertFalse(self.app.validate_integer("abc"), "Should return False, because 'abc' is not an integer")

    def test_validate_float(self):
        self.assertTrue(self.app.validate_float("10.5"), "Should return True, because '10.5' is a float")
        self.assertFalse(self.app.validate_float("abc"), "Should return False, because 'abc' is not a float")

    def test_encrypt_decrypt_positions(self):
        self.app.portfolio['positions'] = {'AAPL': 100}
        self.app.encrypt_positions()
        self.assertNotEqual(self.app.portfolio['positions'], {'AAPL': 100}, "The positions should change after encryption")
        self.app.decrypt_positions()
        self.assertEqual(self.app.portfolio['positions'], {'AAPL': 100}, "The positions should revert to original after decryption")

if __name__ == '__main__':
    unittest.main()
