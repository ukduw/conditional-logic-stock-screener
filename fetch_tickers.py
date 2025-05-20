from yahooquery import Screener

# REPLACE screener_slug WITH CUSTOM SCREENER'S SLUG
def get_tickers_from_yahoo(screener_slug="day_gainers", count=100):
    try:
        s = Screener()
        results = s.get_screeners(screener_slug, count=count)
        tickers = [item['symbol'] for item in results[screener_slug]['quotes']]
        return tickers
    except Exception as e:
        print(f"Error fetching tickers: {e}")
        return []


# TEST
if __name__ == "__main__":
    print(get_tickers_from_yahoo("day_gainers"))