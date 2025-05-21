from fetch_tickers import get_tickers_from_yahoo
from screener import filtered_tickers

screener_slug = "c7689407-8938-457e-b899-523599febde1"

tickers = get_tickers_from_yahoo(screener_slug, count=100)
filtered = filtered_tickers(tickers)

print("Filtered List:")
for ticker in filtered:
    print(ticker)