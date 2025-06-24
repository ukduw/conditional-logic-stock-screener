import yfinance as yf

def passes_custom_filter(ticker):
    try:
        info = yf.Ticker(ticker).info
        volume = info.get("volume")
        float_shares = info.get("floatShares")
        dollar_volume = info.get("currentPrice") * volume # regularMarketPrice?
        market_cap = info.get("marketCap")

        # 1) Float rotation check, 2) $Vol > MCap", 3) 
        return (volume > float_shares and dollar_volume > market_cap) if float_shares is not None else (dollar_volume > market_cap)
    except Exception as e:
        print(f"Error for {ticker}: {e}")
        return False

def filtered_tickers(ticker_list):
    return [t for t in ticker_list if passes_custom_filter(t)]


# continue testing; occassional miss may have been addressed when i fixed the incorrect slice in fetch_tickers
    # will not have addressed the volume issue on the loser side...
    # remains to be seen if this is a real problem