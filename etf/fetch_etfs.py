from bs4 import BeautifulSoup


HTML_FILE = "etf/html-cache/etfcom.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")


def get_etfs_from_etfcom_cache():
    filtered_etfs = []

    for row in soup.select("table tbody tr"):
        symbol = row.find("div", class_="w-[60px] text-center text-base-green cursor-pointer").get_text(strip=True)
        #print(symbol)
        filtered_etfs.append(symbol)
    
    #print(filtered_etfs)
    print(f"ETF screen returned {len(filtered_etfs)} symbols")
    return filtered_etfs


#get_etfs_from_etfcom_cache()