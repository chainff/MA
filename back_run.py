
import os
import time

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
from datetime import datetime, timedelta


def date_list(start_date, end_date):
    date_list = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_list


def create_outpath(sg_name):
    # Get current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    # 创建时间戳目录Creating a timestamp catalog
    timestamp = str(int(time.time()))
    timestamp_dir = os.path.join(current_path, 'output', sg_name, timestamp)
    os.makedirs(timestamp_dir)
    print("Create Timestamp Catalog Successfully：", timestamp_dir)
    return timestamp_dir


def get_stock_data(stock_code='AAPL', start='2010-01-01', end='2023-12-31'):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_path, 'output', f'{stock_code}.csv')
    if not os.path.exists(file_name):
        df = yf.download(stock_code, start=start, end=end)
        df.rename(columns={'Adj Close': 'adj_close'}, inplace=True)
        df.to_csv(file_name)
    return pd.read_csv(file_name)


def computer_signal(df, short_window, long_window):
    df['ma_short'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    df['ma_long'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
    df['signal'] = 0.0
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1.0
    df.loc[df['ma_short'] < df['ma_long'], 'signal'] = -1.0
    df['trade_signal'] = df['signal'].diff()
    return df


def get_cur_trade_signal(df, cur_date):
    first_value = 0
    try:
        first_value = df.loc[df['Date'] == cur_date, 'trade_signal'].values[0]
    except Exception as e:
        pass
    return first_value


def get_buy_price(df, cur_date):
    try:
        first_value = df.loc[df['Date'] == cur_date, 'Close'].values[0]
    except Exception as e:
        print(e)
        return 0
    return first_value


def create_order(stock_code, amount, cur_price, run_date, trade_type):
    order = {
        'stock_code': stock_code,
        'date': run_date,
        'amount': amount,
        'price': cur_price,
        'type': trade_type,
    }
    return order


def get_hold_num(asset):
    hold_num = 0
    for stock_code in asset['positions']:
        if asset['positions'][stock_code] > 0:
            hold_num += 1
    return hold_num


def back_run(config):
    outpath = create_outpath(config['name'])
    config['outpath'] = outpath
    hq_date_list = []
    dd = {}
    for stock_code in config['stock_codes']:
        df = get_stock_data(stock_code, start=config['start_date'], end=config['end_date'])
        df = computer_signal(df, short_window=config['short_window'], long_window=config['long_window'])
        # date_list = df['Date'].tolist()
        # df.set_index('Date', inplace=True)
        dd[stock_code] = df

    hq_date_list = dd[config['stock_codes'][0]]['Date'].tolist()

    asset = {
        "init_capital": config['capital'],
        "cash": config['capital'],
        "market_value": 0,
        'positions': {},
        'total_value': config['capital'],
        "return": 0.0
    }
    position_history = []
    singla_trades = []

    run_date_list = date_list(config['start_date'], config['end_date'])
    for run_date in run_date_list:
        if run_date not in hq_date_list:
            continue
        print(f"begin date：{run_date}")
        for stock_code in config['stock_codes']:
            df = dd[stock_code]
            singla = get_cur_trade_signal(df, run_date)
            if singla > 0:
                if get_hold_num(asset) < config['max_holding_num'] and asset['positions'].get(stock_code, 0) < 100:
                    cur_price = get_buy_price(df, run_date)
                    amount = int(asset['cash'] / cur_price / 100 / (1 + config['fee'])) * 100
                    if amount >= 100:
                        order = create_order(stock_code, amount, cur_price, run_date, 'buy')
                        order['buy_price'] = cur_price
                        singla_trades.append(order)
                        print(f"buy{stock_code}，price{cur_price}")
                        asset['cash'] -= amount * cur_price * (1 + config['fee'])
                        if stock_code not in asset['positions']:
                            asset['positions'][stock_code] = 0
                        asset['positions'][stock_code] += amount
            elif singla < 0:
                if stock_code in asset['positions'] and asset['positions'].get(stock_code, 0) > 0:
                    cur_price = get_buy_price(df, run_date)
                    amount = asset['positions'][stock_code]
                    order = create_order(stock_code, amount, cur_price, run_date, 'sell')
                    order['sell_price'] = cur_price
                    singla_trades.append(order)
                    print(f"sell{stock_code}，price{cur_price}")
                    asset['cash'] += amount * cur_price * (1 - config['fee'])
                    asset['positions'][stock_code] = 0
            else:
                pass

        market_value = 0
        for stock_code in asset['positions']:
            market_value += asset['positions'][stock_code] * get_buy_price(dd[stock_code], run_date)
        asset['market_value'] = market_value
        last_total_value = asset['total_value']
        asset['total_value'] = asset['cash'] + market_value
        asset['return'] = (asset['total_value'] - asset['init_capital']) / asset['init_capital']
        asset['last_return'] = asset['total_value'] / last_total_value - 1

        print(f"date{run_date}end，fund{asset}")
        position_history.append(asset.copy())

    df_position = pd.DataFrame(position_history)
    df_position.to_csv(os.path.join(outpath, 'position.csv'), index=False)
    df_trade = pd.DataFrame(singla_trades)
    df_trade.to_csv(os.path.join(outpath, 'trade.csv'), index=False)

    print('------------------------------------------')

    daily_returns = df_position['last_return']

    # Calculation of cumulative rate of return
    portfolio_value = np.cumprod(1 + np.array(daily_returns))
    cum_return = (portfolio_value[-1] / portfolio_value[0]) - 1

    # Calculation of annual rate of return
    annual_return = ((portfolio_value[-1] / portfolio_value[0]) ** (252 / len(portfolio_value))) - 1

    # Calculate the Sharpe ratio assuming a risk-free rate of 0.02
    risk_free_rate = 0.02
    volatility = np.std(daily_returns) * np.sqrt(252)  # Assuming 252 trading days per year
    sharpe_ratio = (annual_return - risk_free_rate) / volatility

    # Calculate maximum retracement
    drawdown = (portfolio_value / np.maximum.accumulate(portfolio_value)) - 1
    max_drawdown = np.min(drawdown)

    # Print results
    print("Cumulative Rate of Return：", cum_return)
    print("Annualized Rate of Return：", annual_return)
    print("Sharpe Ratio：", sharpe_ratio)
    print("Maximum Retracement：", max_drawdown)

    # Plotting Strategy Return Curves
    plt.plot(portfolio_value)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.title("Strategy Return Curve")
    # plt.show()
    plt.savefig(os.path.join(outpath, 'portfolio_value.png'))
    plt.close()


if __name__ == '__main__':
    sg_config = {
        'name': 'short_long_strategy',
        'start_date': '2020-01-17',
        'end_date': '2023-12-31',
        'capital': 1000000,
        'commission': 0.0001,
        'stock_codes': ['AAPL', 'MSFT', 'GOOGL'],
        'max_holding_num': 3,
        'short_window': 5,
        'long_window': 15,
        'fee': 0.0002,
    }
    back_run(sg_config)
