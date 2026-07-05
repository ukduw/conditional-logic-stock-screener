from fetch_etfs import get_etfs_from_etfcom_cache
from enrich import enrich_with_yf_data, sort_by_volatility
import json
import datetime


tickers = get_etfs_from_etfcom_cache()
enriched = enrich_with_yf_data(tickers)
sorted_list = sort_by_volatility(enriched)

file_path = "etf_volatility.json"
with open(file_path, "w") as f:
    json.dump(sorted_list, f)


current_date = datetime.datetime.now()

rounded_sec = (current_date - datetime.timedelta(microseconds=current_date.microsecond // 1000 * 1000))
without_milli = rounded_sec.replace(microsecond=0)

# FOR LOGS
print(f"=== {without_milli} ===")
print(f"Filtered List({len(sorted_list)}):")
print(sorted_list)

