import requests
from bs4 import BeautifulSoup

def get_afterhours_gainers_from_tradingview(filter_url):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(filter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")



    print(f"After-hours screen returned {len(tickers)} Tickers")

    
    return tickers




# https://www.tradingview.com/markets/stocks-usa/market-movers-after-hours-gainers/