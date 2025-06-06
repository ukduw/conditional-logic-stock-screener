from fetch_tickers import get_all_finviz_tickers
from screener import filtered_tickers
import csv
import datetime, calendar

base_url = "https://finviz.com/screener.ashx?v=111&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o2&o=-change"

tickers = get_all_finviz_tickers(base_url)
filtered = filtered_tickers(tickers)

print(f"Filtered List({len(filtered)}):")
print(filtered)


current_date = datetime.datetime.now()
current_year = int(current_date.strftime("%Y")) # 2025...
current_month_num = int(current_date.strftime("%m")) # 01-12
current_day_num = int(current_date.strftime("%d")) # 01-31
current_weekday = current_date.weekday() # 0-6 - 0 is Monday

first_mon = current_day_num - current_weekday
num_to_month = calendar.month_abbr[current_month_num]
cal = calendar.Calendar()
if first_mon < 1:
    num_to_month = calendar.month_abbr[current_month_num - 1]
    first_mon = first_mon + max(cal.itermonthdays(current_year, current_month_num-1))


file_path = f"weekly-csv/week_beginning_{num_to_month}_{str(first_mon)}.csv"
filtered_with_count = [len(filtered)] + filtered

with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(filtered_with_count)
    file.write("\n\n")
