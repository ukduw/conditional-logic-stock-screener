import yfinance as yf
import datetime, pytz

est = pytz.timezone('US/Eastern')
today = datetime.datetime.now(est)
tomorrow = today + datetime.timedelta(days=1)


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


def filtered_tickers(ticker_list, aftermarket_list):
    shortlist = [t for t in ticker_list if passes_custom_filter(t) and t not in aftermarket_list]
    full_list = list(set(ticker_list + aftermarket_list))

    test_list = []
    test_after_list = []

    for ticker in full_list:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=f"{str(today.date())}", end=f"{str(tomorrow.date())}", interval="1h", prepost=True)
        
        if hist.empty:
            test_list.append(ticker)
            continue
            # 1.
        
        candle_data = {
            "high": hist["High"].tolist(),
            "low": hist["Low"].tolist(),
            "close": hist["Close"].tolist()
        }

        if not candle_data["high"] or not candle_data["low"] or not candle_data["close"]:
            test_list.append(ticker)
            continue
            # 2. in either case, keep the ticker with incomplete data - decision needs to be made manually...

        day_high = max(candle_data["high"])
        day_low = min(candle_data["low"])
        last_close = candle_data["close"][-1]

        if last_close == 0:
            test_list.append(ticker)
            continue

        perc_range = ((day_high - day_low) / last_close) * 100
        if ticker in shortlist and perc_range > 70: # TWEAK
            test_list.append(ticker)
        if ticker in aftermarket_list and perc_range > 50: # TWEAK
            test_after_list.append(ticker)

    return shortlist, test_list, test_after_list


# note: no otc coverage on finviz, but alpaca can't trade otc's anyways...
    # ibkr can - for now, just keep an eye on otcs and continue testing...