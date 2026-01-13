import yfinance as yf
import pandas as pd

def get_market_data(symbol, interval, period):
    data = yf.download(
        tickers=symbol,
        interval=interval,
        period=period,
        progress=False
    )
    data.dropna(inplace=True)
    return data