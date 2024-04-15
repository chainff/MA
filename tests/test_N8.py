import unittest
from CODE.demo_p import TradingApp
from cryptography.fernet import Fernet
import tkinter as tk


class TestTradingAppSecurity(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.app = TradingApp(self.root)
        self.app.encryption_key = Fernet.generate_key()

        self.sample_positions = {
            'AAPL': {'amount': 10, 'price': 150},
            'MSFT': {'amount': 5, 'price': 200}
        }
        self.app.portfolio['positions'] = self.sample_positions

    def test_encryption_decryption(self):

        self.app.encrypt_positions()
        encrypted_positions = self.app.portfolio['positions']
        self.assertNotEqual(encrypted_positions, self.sample_positions)


        self.app.decrypt_positions()
        decrypted_positions = self.app.portfolio['positions']
        self.assertEqual(decrypted_positions, self.sample_positions)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
