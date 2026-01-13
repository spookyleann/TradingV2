def daily_bias(df):
    open_price = df.iloc[0]["Open"]
    current_price = df.iloc[-1]["Close"]

    bias = ((current_price - open_price) / open_price) * 100
    return round(bias, 2)