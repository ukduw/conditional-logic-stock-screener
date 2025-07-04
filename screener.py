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


# screener may be too stringent (e.g. float <50mil); continue testing
# may need additional screen for aftermarket...