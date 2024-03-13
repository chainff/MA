import yfinance as yf
import numpy as np
import pandas as pd
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ticker = 'APLE'
interval = '5m'
refresh_rate = 5

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")

        self.default_short_window = 40
        self.default_long_window = 100

        self.short_window = tk.IntVar(value=self.default_short_window)
        self.long_window = tk.IntVar(value=self.default_long_window)

        self.trading_thread = threading.Thread(target=self.start_trading)
        self.trading_thread.daemon = True
        self.trading_thread.start()

        self.apply_styles()
        self.setup_widgets()

    def setup_widgets(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.buy_button = ttk.Button(self.root, text="Buy", command=self.buy)
        self.buy_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.sell_button = ttk.Button(self.root, text="Sell", command=self.sell)
        self.sell_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Short MA Window
        self.short_window_label = ttk.Label(self.root, text="Short MA Window:")
        self.short_window_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.short_window_entry = ttk.Entry(self.root, textvariable=self.short_window)
        self.short_window_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        # Long MA Window
        self.long_window_label = ttk.Label(self.root, text="Long MA Window:")
        self.long_window_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.long_window_entry = ttk.Entry(self.root, textvariable=self.long_window)
        self.long_window_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        # Update Parameters button
        self.update_button = ttk.Button(self.root, text="Update Parameters", command=self.update_parameters)
        self.update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Log Text Area
        self.log_text = ScrolledText(self.root, state='disabled', height=8)
        self.log_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        self.log_message(f"{datetime.now()}: default_short_window = 40, default_long_window = 100")
        self.log_message(f"{datetime.now()}: Start TradingApp.")

    def log_message(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.configure(state='disabled')
        self.log_text.yview(tk.END)

    def buy(self):
        self.log_message(f"{datetime.now()}: Executing BUY trade.")

    def sell(self):
        self.log_message(f"{datetime.now()}: Executing SELL trade.")

    def update_parameters(self):
        try:
            short_window = int(self.short_window_entry.get())
            long_window = int(self.long_window_entry.get())

            if short_window <= 0 or long_window <= 0:
                raise ValueError("The MA windows must be positive integers.")

            if short_window >= long_window:
                raise ValueError("Short MA window must be less than Long MA window.")

            self.short_window.set(short_window)
            self.long_window.set(long_window)

            self.log_message(f"Parameters updated: Short MA Window = {short_window}, Long MA Window = {long_window}")
        except ValueError as ve:
            self.log_message(f"Parameter Error: {ve}")

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('TLabel', font=('Helvetica', 10), padding=6)
        style.configure('TEntry', font=('Helvetica', 10), padding=6)

    def start_trading(self):
        self.update_trading()

    def update_trading(self):
        try:
            data = get_realtime_data(ticker)
            data = calculate_moving_averages(data, self.short_window.get(), self.long_window.get())
            signals = generate_signals(data)

            latest_signal = signals['Position'].iloc[-1]
            if latest_signal != 0:
                self.execute_trade(latest_signal)
            self.plot_data(data)
            self.log_message(f"{datetime.now()}: NO signal detected.")

        except Exception as e:
            self.log_message(f"An error occurred: {e}")

        # Schedule the next update
        self.root.after(refresh_rate * 1000, self.update_trading)

    def execute_trade(self, signal):
        if signal == 1:
            self.log_message(f"{datetime.now()}: BUY signal detected.")
            self.buy()

        elif signal == -1:
            self.log_message(f"{datetime.now()}: SELL signal detected.")
            self.sell()

    def plot_data(self, data):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_facecolor('#e1e1e1')
        self.ax.set_title('Stock Price and Moving Averages', fontsize=4)
        self.ax.set_xlabel('Date', fontsize=4)
        self.ax.set_ylabel('Price', fontsize=4)
        data['Close'].plot(ax=self.ax, label='Close', color='blue', linewidth=1)
        data['Short_MA'].plot(ax=self.ax, label=f'Short MA ({self.short_window.get()})', color='orange', linewidth=1)
        data['Long_MA'].plot(ax=self.ax, label=f'Long MA ({self.long_window.get()})', color='green', linewidth=1)
        self.ax.legend(fontsize=4)
        self.ax.tick_params(axis='both', which='major', labelsize=4)
        self.canvas.draw()

def get_realtime_data(ticker):
    data = yf.download(tickers=ticker, period='1mo', interval=interval)
    return data

def calculate_moving_averages(data, short_window, long_window):
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    return data

def generate_signals(data):
    data['Signal'] = 0
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
