from fetch_tickers import get_all_finviz_tickers
from screener import filtered_tickers
import csv

base_url = "https://finviz.com/screener.ashx?v=111&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o2&o=-change"

tickers = get_all_finviz_tickers(base_url)
filtered = filtered_tickers(tickers)


print("Filtered List:")
for ticker in filtered:
    print(ticker)

with open('filtered_tickers.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ticker'])
    for ticker in filtered:
        writer.writerow([ticker])