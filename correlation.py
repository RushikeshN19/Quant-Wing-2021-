import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np


tickers = ['AAPL', 'TWTR', 'IBM', 'MSFT','FB','GOOG','GOOGL','TSLA','NVDA','JPM','JNJ','NFLX','VZ','INTC','ADBE','PYPL','HD','PG','MA','UNH','V']
start = dt.datetime(2020, 1, 1)

data = pdr.get_data_yahoo(tickers, start)

data.head()
data = data['Adj Close']
data.head()
log_returns = np.log(data/data.shift())
print(log_returns)
log_returns.corr()
sp500 = pdr.get_data_yahoo("^GSPC", start)
log_returns['SP500'] = np.log(sp500['Adj Close']/sp500['Adj Close'].shift())
log_returns.corr()

def test_correlation(ticker):
    df = pdr.get_data_yahoo(ticker, start)
    lr = log_returns.copy()
    lr[ticker] = np.log(df['Adj Close']/df['Adj Close'].shift())
    return lr.corr()

test_correlation("LQD")

test_correlation("TLT")

import matplotlib.pyplot as plt
%matplotlib notebook

def visualize_correlation(ticker1, ticker2):
    df = pdr.get_data_yahoo([ticker1, ticker2], start)
    df = df['Adj Close']
    df = df/df.iloc[0]
    fig, ax = plt.subplots()
    df.plot(ax=ax)

visualize_correlation("AAPL", "TLT")

visualize_correlation("^GSPC", "TLT")