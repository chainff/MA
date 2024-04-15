import unittest
from CODE.demo_p import TradingApp
from random import uniform
import tkinter as tk

class TestTradingAppScalability(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = TradingApp(self.root)
        self.load_test_data()

    def load_test_data(self):
        for i in range(1000):  #  test 1000 transactions
            stock_symbol = f"TEST{i}"
            amount = round(uniform(1, 10), 2)
            price = round(uniform(10, 500), 2)
            self.app.portfolio['positions'][stock_symbol] = {'amount': amount, 'price': price}

    def test_scalability(self):
        stock_symbols = list(self.app.portfolio['positions'].keys())
        for stock_symbol in stock_symbols:
            price = self.app.portfolio['positions'][stock_symbol]['price']
            self.app.buy(price)
            self.app.sell(price)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
