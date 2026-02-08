# 1-Import data ('yfinance')
import yfinance as yf                  
from datetime import date, time
import pandas as pd
import math
# 2-specifying "what Data we need"(NVDA-nvidia)
def fetch_trades():
    symbol = 'NVDA' 
    data = yf.download(symbol, period = '1d', interval = '5m')
    if data.empty:   
        print('DATA NOT FOUND')  # 3-used if "NO" data found 
        return[]                 #this is important so that you know what is the issue
    # 4-Fix multi_index columns if they exist
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    # 5-It converts the (Tz-Time_Zone) as per India-UTC
    if data.index.tz is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('Asia/Kolkata')
    print("TZ changed")
    # 6-Filters for US market Hours
    market_open = time(20, 00, 00)
    market_c2 = time(1, 30, 00)
    mask = ((data.index.time >= market_open) | (data.index.time <= market_c2))
    data_box = data[mask].copy()
    
    # 7-Sum up all the things needed for the visulization
    trades = []
    for idx, row in data_box.iterrows():
        trades.append({
            'timestamp' : idx,
            'price': (row['High'] + row['Low'] + row['Close'])/3,
            'volume': row['Volume']
        })
    return trades
