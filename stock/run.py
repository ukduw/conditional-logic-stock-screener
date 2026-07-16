from fetch_tickers import get_all_finviz_tickers
from fetch_tickerview import get_finviz_tickers_from_tickerview
from fetch_afterhours import get_afterhours_gainers_from_tradingview
from screener import filtered_tickers
import csv, json
import datetime, calendar, pytz
from pathlib import Path

base_url = "https://finviz.com/screener.ashx?v=411&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o3&o=-change"
    # initial screener
    # https://finviz.com/screener.ashx?v=111&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o2&o=-change
    # initial screener + 3x r.vol, TICKER ONLY
    # https://finviz.com/screener.ashx?v=411&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o3&o=-change
base_url2 = "https://www.tradingview.com/markets/stocks-usa/market-movers-after-hours-gainers"


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

file_path = Path(f"/home/edhkm/edliu/conditional-logic-stock-scre/home/edhkm/edliu/market-holiday-json-writer/market-holidays.jsonener/weekly-csv/{current_year}/week_beginning_{num_to_month}_{first_mon}.csv")
file_path.parent.mkdir(parents=True, exist_ok=True)


with open('/home/edhkm/edliu/market-holiday-json-writer/market-holidays.json', 'r') as f:
    market_holiday_list = json.load(f)

eastern = pytz.timezone("US/Eastern")
current_eastern = datetime.datetime.now(eastern)

rounded_sec = (current_date - datetime.timedelta(microseconds=current_date.microsecond // 1000 * 1000))
without_milli = rounded_sec.replace(microsecond=0)


if str(current_eastern.date()) in market_holiday_list:  # fine, actually, since screener should still run on * holidays
    print(f"=== {without_milli} ===")
    print("Market holiday")

    with file_path.open(mode='a', newline='') as file:
        writer = csv.writer(file)
        file.write("-")
        file.write("\n\n")

else:
    # tickers = get_all_finviz_tickers(base_url)
    tickers = get_finviz_tickers_from_tickerview(base_url)
    filtered = filtered_tickers(tickers)
    afters = get_afterhours_gainers_from_tradingview(base_url2)

    print(f"=== {without_milli} ===")
    print(f"Filtered List({len(filtered)}):")
    print(filtered)
    print(f"After-hours Gainers({len(afters)}):")
    print(afters, "\n")


    filtered_with_count = [len(filtered)] + filtered
    afters_with_count = [len(afters)] + afters

    with file_path.open(mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(filtered_with_count + [" - "] + afters_with_count)
        file.write("\n\n")
