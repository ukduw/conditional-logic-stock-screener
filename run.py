from fetch_tickers import get_tickers_from_yahoo
from screener import filtered_tickers

# REPLACE WITH CUSTOM SLUG
screener_slug = "day_gainers"

tickers = get_tickers_from_yahoo(screener_slug, count=100)
filtered = filtered_tickers(tickers)

print("Filtered List:")
for ticker in filtered:
    print(ticker)