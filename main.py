import requests
import time
from datetime import datetime

API_KEY = 'SB8FM45ADPZZ0ZVY'
BASE_URL = 'https://www.alphavantage.co/query?'

#Stocks and Moving Averages Parameters
SYMBOL = 'AAPL'
SHORT_WINDOW = 40
LONG_WINDOW = 100

#Alpha Vantage
def get_stock_data(symbol, interval='5min', outputsize='compact'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'outputsize': outputsize,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    time_series_key = list(data.keys())[1]
    return data[time_series_key]

#Calculate moving average
def calculate_moving_average(data, window):

    prices = [float(value['4. close']) for key, value in data.items()]
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window

#Look at short and long term moving averages to check for trading signals
def check_for_signal(short_ma, long_ma):
    if short_ma is None or long_ma is None:
        return 'No Signal'
    if short_ma > long_ma:
        return 'Buy'
    elif short_ma < long_ma:
        return 'Sell'
    else:
        return 'Hold'

def main(trading_interval=300):
    while True:
        print(f"Checking for trade signal at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        data = get_stock_data(SYMBOL)
        short_ma = calculate_moving_average(data, SHORT_WINDOW)
        long_ma = calculate_moving_average(data, LONG_WINDOW)
        signal = check_for_signal(short_ma, long_ma)
        print(f"Trade Signal: {signal}")
        time.sleep(trading_interval)

if __name__ == "__main__":
    main()
