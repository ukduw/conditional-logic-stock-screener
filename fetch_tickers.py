import time, random
import requests
from bs4 import BeautifulSoup

def get_all_finviz_tickers(filter_url, max_pages=20):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    for page in range(max_pages):
        start_row = 1 + page * 20
        paged_url = f"{filter_url}&r={start_row}"

        time.sleep(random.uniform(0.3, 0.6)) 

        response = requests.get(paged_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.select('a.tab-link')
        ticker_links = links[4:-7] if len(links) > 11 else []

        page_tickers = [a.text.strip() for a in ticker_links if a.get('href', '').startswith('quote.ashx')]
        print(f'Found {len(page_tickers)} tickers on page {page+1}')

        if len(page_tickers) == 1:
            break

        tickers.extend(page_tickers)

    return tickers


