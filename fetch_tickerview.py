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

get_finviz_tickers_from_tickerview('https://finviz.com/screener.ashx?v=411&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o2000%2Csh_float_u50%2Csh_price_u20%2Csh_relvol_o3&o=-change')
