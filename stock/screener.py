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

# def filtered_tickers(ticker_list):
#     return [t for t in ticker_list if passes_custom_filter(t)]


def filtered_tickers(ticker_list):
    shortlist = [t for t in ticker_list if passes_custom_filter(t)]

    test_list = []
    for ticker in shortlist:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="1d")
        
        if hist.empty:
            test_list.append(ticker)
            continue
            # 1.
        
        high = hist["High"].tolist()
        low = hist["Low"].tolist()
        close = hist["Close"].tolist()
            # i think i remember the api returns numpy arrays...

        if not high or not low or not close:
            test_list.append(ticker)
            continue
            # 2. in either case, keep the ticker with incomplete data - decision needs to be made manually...

        perc_range = ((high[0] - low[0]) / close[0]) * 100
        if perc_range > 70: # TWEAK
            # UPDATE: works as intended; 70% may be too strict... needs more testing
                # doesn't seem to work(?) for aftermarket gainers (maybe because high/low are DAY high/low?)
                # but that's fine, since separate aftermarket list is always kept...
            test_list.append(ticker)

    return shortlist, test_list


# note: no otc coverage on finviz, but alpaca can't trade otc's anyways...
    # ibkr can - for now, just keep an eye on otcs and continue testing...