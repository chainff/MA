import unittest
import timeit
from back_run import computer_signal, get_stock_data

class PerformanceTest(unittest.TestCase):
    def test_computer_signal_performance(self):
        """Test the performance of the computer_signal function."""
        df = get_stock_data(stock_code='AAPL', start='2020-01-01', end='2020-12-31')
        elapsed_time = timeit.timeit(lambda: computer_signal(df, short_window=5, long_window=15), number=10)
        self.assertLess(elapsed_time, 1, "computer_signal function is too slow.")

if __name__ == '__main__':
    unittest.main()
