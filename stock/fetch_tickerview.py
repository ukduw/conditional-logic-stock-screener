import requests
from bs4 import BeautifulSoup

def get_finviz_tickers_from_tickerview(filter_url):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(filter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    bold_tags = soup.find_all("b")
    tickers_only = bold_tags[3:-1]

    for ticker in tickers_only:
        text = ticker.get_text(strip=True)
        tickers.append(text)

    print(f"Initial screen returned {len(tickers)} Tickers")

    
    return tickers

