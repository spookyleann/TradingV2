# ==============================
# NASDAQ FUTURES TRADING MODEL
# ALL-IN-ONE STREAMLIT APP
# ==============================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import feedparser

# ==============================
# CONFIG
# ==============================
st.set_page_config(
page_title="NASDAQ Futures Market Model",
layout="wide"
)

# ==============================
# DATA LOADER
# ==============================
@st.cache_data
def load_data():
df = yf.download("NQ=F", interval="15m", period="5d")
df.dropna(inplace=True)
return df

# ==============================
# DAILY BIAS MODEL
# ==============================
def daily_bias(df):
prev_high = df['High'].iloc[-96:-1].max()
prev_low = df['Low'].iloc[-96:-1].min()
price = df['Close'].iloc[-1]

ema = df['Close'].ewm(span=50).mean().iloc[-1]

bull, bear = 0, 0

if price > prev_high:
bull += 40
if price < prev_low:
bear += 40

if price > ema:
bull += 30
else:
bear += 30

return min(bull, 100), min(bear, 100)

# ==============================
# SMART MONEY CONCEPTS
# ==============================
def detect_bos(df):
bos = []
for i in range(2, len(df)):
if df['High'][i] > df['High'][i-1] > df['High'][i-2]:
bos.append((df.index[i], "Bullish BOS"))
if df['Low'][i] < df['Low'][i-1] < df['Low'][i-2]:
bos.append((df.index[i], "Bearish BOS"))
return bos

def detect_fvg(df):
zones = []
for i in range(2, len(df)):
if df['Low'][i] > df['High'][i-2]:
zones.append((df.index[i-2], df.index[i], "Bullish FVG"))
if df['High'][i] < df['Low'][i-2]:
zones.append((df.index[i-2], df.index[i], "Bearish FVG"))
return zones

def detect_orderblocks(df):
obs = []
for i in range(3, len(df)):
if df['Close'][i-3] < df['Open'][i-3] and df['Close'][i] > df['High'][i-1]:
obs.append((df.index[i-3], "Bullish OB"))
if df['Close'][i-3] > df['Open'][i-3] and df['Close'][i] < df['Low'][i-1]:
obs.append((df.index[i-3], "Bearish OB"))
return obs

def detect_liquidity_sweep(df):
sweeps = []
for i in range(1, len(df)):
if df['High'][i] > df['High'][i-1] and df['Close'][i] < df['High'][i-1]:
sweeps.append((df.index[i], "Buy-side Sweep"))
if df['Low'][i] < df['Low'][i-1] and df['Close'][i] > df['Low'][i-1]:
sweeps.append((df.index[i], "Sell-side Sweep"))
return sweeps

# ==============================
# NEWS
# ==============================
def get_news():
feed = feedparser.parse(
"https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5ENDX&region=US&lang=en-US"
)
return feed.entries[:8]

# ==============================
# UI
# ==============================
st.title("📈 NASDAQ Futures – Institutional Market Model")

df = load_data()
bull_bias, bear_bias = daily_bias(df)

c1, c2, c3 = st.columns(3)
c1.metric("Bullish Bias", f"{bull_bias}%")
c2.metric("Bearish Bias", f"{bear_bias}%")
c3.metric("Last Price", round(df['Close'].iloc[-1], 2))

# ==============================
# CHART
# ==============================
fig = go.Figure()

fig.add_candlestick(
x=df.index,
open=df['Open'],
high=df['High'],
low=df['Low'],
close=df['Close'],
name="NQ"
)

# BOS
for t, label in detect_bos(df):
fig.add_vline(x=t, line_width=1, line_dash="dash",
line_color="green" if "Bullish" in label else "red")

st.plotly_chart(fig, use_container_width=True)

# ==============================
# MARKET STRUCTURE PANEL
# ==============================
st.subheader("📊 Market Structure Signals")

col1, col2, col3 = st.columns(3)

with col1:
st.write("**Order Blocks**")
for ob in detect_orderblocks(df)[-5:]:
st.write(ob)

with col2:
st.write("**FVG / IFVG**")
for fvg in detect_fvg(df)[-5:]:
st.write(fvg)

with col3:
st.write("**Liquidity Sweeps**")
for sweep in detect_liquidity_sweep(df)[-5:]:
st.write(sweep)

# ==============================
# NEWS PANEL
# ==============================
st.subheader("📰 NASDAQ / Tech News")

for item in get_news():
st.markdown(f"**{item.title}**")
st.caption(item.published)
st.markdown(f"[Read more]({item.link})")
st.divider()

st.caption(
"This is general information only and not financial advice. "
"For personal guidance, please talk to a licensed professional."
)
