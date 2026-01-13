def daily_bias(df):
    if df is None or len(df) == 0:
        return 0.0

    open_price = df.iloc[0]["Open"]
    current_price = df.iloc[-1]["Close"]

    return round(((current_price - open_price) / open_price) * 100, 2)