import customtkinter as ctk
from utils.config import SYMBOL, TIMEFRAME, LOOKBACK
from data.data_feed import get_market_data
from data.news_feed import get_news
from model.market_structure import detect_bos, detect_fvg
from model.bias_model import daily_bias
from ui.dashboard import Dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1100x700")
app.title("Futures Trading Model")

data = get_market_data(SYMBOL, TIMEFRAME, LOOKBACK)
news = get_news("NASDAQ")
bos = detect_bos(data)
fvg = detect_fvg(data)
bias = daily_bias(data)

Dashboard(app, data, bias, news, bos, fvg)

app.mainloop()
