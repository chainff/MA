import unittest
from back_run import get_stock_data, compute_signal, create_order

class TestBackRun(unittest.TestCase):

    def test_get_stock_data(self):
        df = get_stock_data(stock_code='AAPL', start='2020-01-01', end='2020-01-10')
        self.assertNotEqual(df.empty, True, "DataFrame should not be empty")
        self.assertIn('Close', df.columns, "DataFrame should contain the Close column")

    def test_compute_signal(self):
        """Test signal computation functionality"""
        df = get_stock_data(stock_code='AAPL', start='2020-01-01', end='2020-01-31')
        df = compute_signal(df, short_window=5, long_window=10)
        self.assertIn('signal', df.columns, "DataFrame should contain the signal column")
        # Check if buy/sell signals are generated
        self.assertTrue(any(df['signal'] != 0), "Buy/sell signals should be generated")

    def test_create_order(self):
        """Test order creation functionality"""
        order = create_order(stock_code='AAPL', amount=100, cur_price=150, run_date='2020-01-15', trade_type='buy')
        self.assertEqual(order['stock_code'], 'AAPL', "Stock code should be AAPL")
        self.assertEqual(order['amount'], 100, "Purchase amount should be 100")
        self.assertEqual(order['price'], 150, "Current price should be 150")
        self.assertEqual(order['type'], 'buy', "Trade type should be buy")

if __name__ == '__main__':
    unittest.main()
