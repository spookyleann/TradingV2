import numpy as np

def detect_bos(df):
    highs = df["High"].values
    lows = df["Low"].values

    bos = []
    for i in range(2, len(df)):
        if highs[i] > highs[i-1] and highs[i-1] > highs[i-2]:
            bos.append((df.index[i], "Bullish BOS"))
        elif lows[i] < lows[i-1] and lows[i-1] < lows[i-2]:
            bos.append((df.index[i], "Bearish BOS"))
    return bos


def detect_fvg(df):
    fvg = []
    for i in range(2, len(df)):
        if df["Low"][i] > df["High"][i-2]:
            fvg.append((df.index[i], "Bullish FVG"))
        elif df["High"][i] < df["Low"][i-2]:
            fvg.append((df.index[i], "Bearish FVG"))
    return fvg