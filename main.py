import numpy as np
import pandas as pd
import yfinance as yf
import ta
import threading
import time

def get_data(symbol, interval):
    return yf.download(symbol, interval=interval)

def rsi_strategy(df):
    rsi = ta.momentum.RSIIndicator(df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    df['Signal'] = np.where(df['RSI'] < 30, 1, 0)
    df['Buy_Signal'] = np.where((df['Signal'].shift(1) == 0) & (df['Signal'] == 1), 1, 0)
    df['Sell_Signal'] = np.where((df['Signal'].shift(1) == 1) & (df['Signal'] == 0), 1, 0)
    return df

def trade(symbol, interval, capital):
    df = get_data(symbol, interval)
    rsi_df = rsi_strategy(df)
    buy_price = 0
    shares = 0
    for i in range(1, len(rsi_df)):
        if rsi_df['Buy_Signal'][i] == 1:
            shares = capital / rsi_df['Close'][i]
            buy_price = rsi_df['Close'][i]
        elif rsi_df['Sell_Signal'][i] == 1:
            capital = shares * rsi_df['Close'][i]
            shares = 0
        elif i == len(rsi_df) - 1:
            capital = shares * rsi_df['Close'][i]
            shares = 0
    return capital

def run_tradebot(symbol, interval, capital):
    start_time = time.time()
    result = trade(symbol, interval, capital)
    end_time = time.time()
    print(f"TE Result: ${result:.2f}")
    print(f"Time Elapsed: {end_time - start_time:.2f} seconds")

def run_realtime_data(symbol, interval, capital):
    while True:
        try:
            result = trade(symbol, interval, capital)
            print(f"TE Result: ${result:.2f}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

if __name__ == '__main__':
    symbol = 'AAPL'
    interval = '1d'
    capital = 10000
    
    # Run tradebot once
    run_tradebot(symbol, interval, capital)
    
    # Run tradebot with real-time data streaming
    threading.Thread(target=run_realtime_data, args=(symbol, interval, capital)).start()
