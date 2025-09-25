
## Install and Run:
`python3 -m venv venv`   
`source venv/bin/activate`   

`pip install -r requirements.txt`   

`python3 run.py`

NOTE: RE-WRITE README

## Conditional Logic Stock Screener (CLSS)
1. **The CLSS first scrapes a Finviz screener, building an array of tickers. The Finviz screener has the following conditions:**
    - USA Exchanges only
    - Market Cap < 2bil
    - Relative Volume > 2
    - Intraday Volume > 1mil
    - Price < $20   

Note that there is no "% Change" condition and that **this screener will return a large number of stocks (~100)**.


2. **The CLSS then uses Yahoo Finance API for fundamental data. This data is used to further filter the array with data-data conditional logic, which is a feature not available in the vast majority of screeners. The additional filters include:**
    - Intraday Volume > Shares Float
    - Dollar Volume > Market Cap   

The first condition, for example, checks for any degree of Float Rotation.  

**This returns a very short list of stocks (typically ~10)**. The purpose of this screener is to return only stocks that have exhibited disproportionate activity, regardless of % Gain. It takes into account how significant this activity is relative to the size of the stock itself (i.e. 60d average volume vs current volume, market cap vs $volume, shares float vs intraday volume).

- Rather than only returning the **Top Gainers**, the CLSS will also return:
    - **Stocks that spiked, then sold off**, losing most/all of their gains - these stocks are typically filtered out by % Gain conditions and **cannot be captured by using other screeners**' basic Range filter, which, again, cannot be used conditionally (e.g. Range >= 30% Intraday Price)
        - For example, a $2 range is nothing for Tesla, but is massive for a $0.50 stock - yet, other screeners can only filter for $2 range in absolute terms, not as a percentage of a stock's price.
    - **Top Losers with disproportionate activity**

CLSS is especially useful for traders with **multiple strategies** and/or traders with **strategies with high fake-out rates**.


3. **The final output is written to a CSV file for easy export. The files are automatically named after the starting date of the week, grouping the screener outputs by trading week. A count of the number of tickers returned is included with each row.**
    - Some example CSVs, each with a week's worth of results, are included in the "weekly-csv" file

This feature can be used to generate statistics or to keep a record of tickers by date.


&nbsp;
---
### Plans
I plan on using the CSV exports, along with trade data and historical market data, to train an AI model to set trade parameters according to my strategies and use them with my Python scripts to autonomously build watchlists and structure trades.