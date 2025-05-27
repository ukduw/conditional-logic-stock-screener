import requests
from bs4 import BeautifulSoup

def get_all_finviz_tickers(filter_url, max_pages=100):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}
    page = 0

    while True:
        start_row = 1 + page * 20
        paged_url = f"{filter_url}&r={start_row}"
        print(f"Fetching: {paged_url}")

        response = requests.get(paged_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all('a', class_='screener-link-primary')
        page_tickers = [a.text.strip() for a in table]

        if not page_tickers or page >= max_pages:
            break

        tickers.extend(page_tickers)
        page += 1

    return tickers

base_url = "https://finviz.com/screener.ashx?v=111&f=geo_usa,sh_curvol_o1000,sh_price_u20,sh_relvol_o2"

tickers = get_all_finviz_tickers(base_url)
print(f"Found {len(tickers)} tickers")
print(tickers[:10]) # preview first 10...