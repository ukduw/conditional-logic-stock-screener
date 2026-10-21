import requests
from bs4 import BeautifulSoup

def get_finviz_tickers_from_tickerview(filter_url):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(filter_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    a_tags = soup.find_all("a")
    #tickers_only = a_tags[3:-1]

    for ticker in a_tags:
        if ticker.get("data-ticker"):
            tickers.append(ticker.get("data-ticker"))

    print(f"Initial screen returned {len(tickers)} Tickers")
    print(tickers)

    
    return tickers


#get_finviz_tickers_from_tickerview("https://finviz.com/screener/stocks?v=411&f=geo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o3&o=-change")