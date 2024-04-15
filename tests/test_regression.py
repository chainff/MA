import unittest
from unittest.mock import patch
import pandas as pd
from CODE.demo_p import calculate_moving_averages, generate_signals, get_realtime_data

class TestTradingAppRegression(unittest.TestCase):

    @patch('demo_p.yf.download')
    def test_get_realtime_data(self, mock_download):
        mock_data = pd.DataFrame({'Close': [100, 105, 110]})
        mock_download.return_value = mock_data

        ticker = 'AAPL'
        data = get_realtime_data(ticker)
        self.assertFalse(data.empty, "获取实时数据失败")
        self.assertIn('Close', data.columns, "数据中应包含Close列")

    def test_calculate_moving_averages(self):
        # 创建测试数据
        data = pd.DataFrame({'Close': [100, 105, 110, 115, 120]})
        short_window = 3
        long_window = 5

        # 测试计算移动平均线
        result = calculate_moving_averages(data, short_window, long_window)
        self.assertIn('Short_MA', result.columns, "结果中应包含短期移动平均线")
        self.assertIn('Long_MA', result.columns, "结果中应包含长期移动平均线")

    def test_generate_signals(self):
        # 创建测试数据，包括短期和长期移动平均线
        data = pd.DataFrame({
            'Close': [100, 105, 110, 115, 120],
            'Short_MA': [None, None, 105, 110, 115],
            'Long_MA': [None, None, None, None, 110]
        })

        # 测试生成交易信号
        signals = generate_signals(data)
        self.assertIn('Signal', signals.columns, "结果中应包含Signal列")
        self.assertIn('Position', signals.columns, "结果中应包含Position列")

if __name__ == '__main__':
    unittest.main()
