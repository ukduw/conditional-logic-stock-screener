import yfinance as yf

def passes_custom_filter(ticker):
    try:
        info = yf.Ticker(ticker).info
        volume = info.get("volume")
        float_shares = info.get("floatShares")

        if volume is None or float_shares is None:
            return false
        return volume > float_shares
    except Exception as e:
        print(f"Error for {ticker}: {e}")
        return false

def filtered_tickers(ticker_list):
    return [t for t in ticker_list if passes_custom_filter(t)]


# TEST
if __name__ == "__main__":
    sample = ["AAPL", "TSLA", "NVDA"]
    print(filtered_tickers(sample))