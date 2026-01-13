import feedparser

def get_news(symbol):
    feed = feedparser.parse(
        f"https://news.google.com/rss/search?q={symbol}+stock+market"
    )
    return [entry.title for entry in feed.entries[:5]]