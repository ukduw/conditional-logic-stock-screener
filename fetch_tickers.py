import time, random
import requests
from bs4 import BeautifulSoup

def get_all_finviz_tickers(filter_url, max_pages=6):
    tickers = []
    headers = {'User-Agent': "Mozilla/5.0"}

    for page in range(max_pages):
        start_row = 1 + page * 20
        paged_url = f"{filter_url}&r={start_row}"

        time.sleep(random.uniform(0.3, 0.6)) 

        response = requests.get(paged_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.select('a.tab-link')
        ticker_links = links[5:-7] if len(links) > 12 else []

        page_tickers = [a.text.strip() for a in ticker_links if a.get('href', '').startswith('quote.ashx')]
        print(f'Found {len(page_tickers)} tickers on page {page+1}')

        if not page_tickers:
            break

        tickers.extend(page_tickers)

    return tickers


# TEST
# base_url = "https://finviz.com/screener.ashx?v=111&f=cap_smallunder%2Cgeo_usa%2Csh_curvol_o1000%2Csh_price_u20%2Csh_relvol_o2&o=-change"

# tickers = get_all_finviz_tickers(base_url)
# print(f"Found {len(tickers)} tickers")
# print(tickers[:10]) # preview first 10...