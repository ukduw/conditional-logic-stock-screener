import requests
from bs4 import BeautifulSoup

def get_afterhours_gainers_from_tradingview(filter_url):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(filter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    for row in table.find_all("tr"):
        gains = row.find("span", class_="positive-p_QIAEOQ")

        if gains is not None:
            gain = gains.get_text(strip=True)
            gain_cleaned = gain[1:-1]

            if float(gain_cleaned) > 20: # 20% gain, tweak later
                ticker_containers = row.find_all("a")
                for t in ticker_containers:
                    ticker = t.get_text(strip=True)
                    tickers.append(ticker)
            else:
                break

    print(f"After-hours screen returned {len(tickers)} Tickers")


    return tickers

