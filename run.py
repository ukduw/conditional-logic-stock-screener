from fetch_tickers import get_all_finviz_tickers
from screener import filtered_tickers

base_url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,sh_curvol_o1000,sh_price_u20,sh_relvol_o2"

tickers = get_all_finviz_tickers(base_url)
filtered = filtered_tickers(tickers)

print("Filtered List:")
for ticker in filtered:
    print(ticker)