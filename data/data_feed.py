import yfinance as yf

def get_market_data(symbol, interval, period):
    df = yf.download(
        tickers=symbol,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=True
    )

    if df is None or df.empty:
        raise RuntimeError(
            f"No market data returned for symbol {symbol}. "
            "Yahoo often blocks futures. Try QQQ or ^NDX."
        )

    return df