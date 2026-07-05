import yfinance as yf
import time


def calc_30d_perc_range(candle_data):
    if candle_data:
        if not candle_data or "high" not in candle_data or "low" not in candle_data or "close" not in candle_data:
            raise ValueError("Invalid candle_data: must contain 'high', 'low', 'close' keys")

        highs = candle_data["high"]
        lows = candle_data["low"]
        closes = candle_data["close"]

        if not highs or not lows or not closes:
            raise ValueError("Empty price data")
        
        if len(highs) < 2 or len(lows) < 2 or len(closes) < 2:
            raise ValueError("Insufficient data: need at least 2 data points")
        

        max_high = max(highs)
        min_low = min(lows)
        last_close = closes[-1]

        if last_close == 0:
            raise ValueError("Last close price is zero")
        
        percent_range  = ((max_high - min_low) / last_close) * 100
        return round(percent_range, 2)
    
    else:
        return None


def enrich_with_yf_data(ticker_list):
    list_of_dicts = []

    for ticker in ticker_list:
        try:
            print(f"Fetching data for {ticker}")

            etf = yf.Ticker(ticker)
            hist = etf.history(period="1mo", interval="1d")

            if hist.empty:
                print(f"No yf data available for {ticker}")
                break

            candle_data = {
                "high": hist["High"].tolist(),
                "low": hist["Low"].tolist(),
                "close": hist["Close"].tolist()
            }

            list_of_dicts.append({
                "symbol": ticker,
                "percent_range": calc_30d_perc_range(candle_data)
            })

            time.sleep(2)

        except Exception as e:
            print(f"Error for {ticker}: {e}")

    return list_of_dicts


def sort_by_volatility(ticker_list):
    print("Sorting by volatility...")

    def sort_key(etf):
        # Sort key function: (is_none, percentage_range)
        percent_range = etf.get("percent_range")

        if percent_range is None:
            return (1, 0) # None goes last

        return(0, -percent_range)
    

    sorted_etfs = sorted(ticker_list, key=sort_key)

    return sorted_etfs

