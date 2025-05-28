
## Install and Run:
-pip install -r requirements.txt   
-python3 run.py


## Conditional Logic Stock Screener (CLSS)
1. The CLSS first scrapes a Finviz screener, building an array of tickers. The Finviz screener has the following conditions:
    - USA Exchanges only
    - Market Cap < 2bil
    - Relative Volume > 2
    - Intraday Volume > 1mil
    - Price < $20   

Note that there is no "% Change" condition and that this screener will return a large number of stocks (~100).


2. The CLSS then uses Yahoo Finance API for market data. This data is used to further filter the array with conditional logic, which is a feature not available in the vast majority of screeners. The additional filters include:
    - Intraday Volume > Shares Float
    - Dollar Volume > Market Cap   

The first condition, for example, checks for any degree of Float Rotation.  

This returns a very short list of stocks (typically <10). The purpose of this screener is to return only stocks that have exhibited disproportionate activity, regardless of % Gain. It also takes into account how significant the activity is relative to the size of the stock (i.e. 60d average volume, market cap, shares float, intraday price).

- Rather than only returning the Top Gainers, the CLSS will also return:
    - Stocks that spiked, then sold off, losing most/all of their gains - these stocks are typically filtered out by % Gain conditions and cannot be captured by using other screeners' basic Range filter, which, again, cannot be used conditionally (e.g. Range >= 30% Intraday Price)
    - Top Losers with disproportionate/significant activity

CLSS is especially useful for traders with multiple strategies and/or traders with strategies with high fake-out rates.


3. The final output is written to a CSV file for easy export