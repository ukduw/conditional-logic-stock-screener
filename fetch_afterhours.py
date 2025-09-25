import requests
from bs4 import BeautifulSoup

def get_afterhours_gainers_from_tradingview(filter_url):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(filter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all("table")[1]

    for row in enumerate(table.find_all("tr")):
        gains = row.find_all("span", class_="positive-p_QIAEOQ")
        for g in gains:
            gain = g.get_text(strip=True)
            gain_cleaned = gain[1:-1]

            if int(gain_cleaned) > 30: # 30% gain, tweak later
                ticker_containers = row.find_all("a")
                for t in ticker_containers:
                    ticker = t.get_text(strip=True)
                    ticker.append(ticker)

    print(f"After-hours screen returned {len(tickers)} Tickers")

    
    return tickers

