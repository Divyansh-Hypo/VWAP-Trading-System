#Full VWAP code
import yfinance as yf
from datetime import date, time
import pandas as pd
import math

def fetch_trades():
    symbol = 'NVDA'
    data = yf.download(symbol, period = '1d', interval = '5m')
    if data.empty:
        print('DATA NOT FOUND')
        return[]
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if data.index.tz is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('Asia/Kolkata')
    print("TZ changed")
    
    market_open = time(20, 00, 00)
    market_c2 = time(1, 30, 00)
    mask = ((data.index.time >= market_open) | (data.index.time <= market_c2))
    data_box = data[mask].copy()
    

    trades = []
    for idx, row in data_box.iterrows():
        trades.append({
            'timestamp' : idx,
            'price': (row['High'] + row['Low'] + row['Close'])/3,
            'volume': row['Volume']
        })
    return trades

def calculate_vwap_bands(incoming_trades):
    if not incoming_trades:
        print('no data')
        return []
    
    vwap_values = []
    total_vp = 0
    total_v = 0
    total_p2_v = 0
    prev_day = None
    day_count = 0

    for trade in incoming_trades:
        current_timestamp = trade['timestamp']
        current_day = current_timestamp.date()
        price = trade['price']

        if prev_day is not None and current_day != prev_day:
            print(f"New trade data detected {current_day}")

            total_vp = 0
            total_v = 0
            total_p2_v = 0
            UP_band = 0
            LW_band = 0

        total_vp += trade['volume'] * trade['price']
        total_p2_v += (trade['price'] ** 2) * trade['volume']
        total_v += trade['volume']
        
        if total_v > 0:
            current_vwap = (total_vp / total_v)
            vwap_values.append(current_vwap)
        
            variation = (total_p2_v / total_v) - (current_vwap ** 2)
            std_dev = math.sqrt(max(0, variation))

            UP_band = current_vwap + (2 * std_dev)
            LW_band = current_vwap - (2 * std_dev)

            band_w = (UP_band - LW_band)
            trade['vwap'] = current_vwap
            trade['UP_band'] = UP_band
            trade['LW_band'] = LW_band


            print(f"Time: {current_timestamp.strftime('%H:%M'):<10}) | Price: {price:10.2f} | VWAP: {current_vwap:10.4f} | UP_b: {UP_band:10.4f} | LW_b: {LW_band:10.4f} | Band_W: {band_w:10.3f}")

        prev_day = current_day 
    return incoming_trades
if __name__ == "__main__":
    print("Fetching data and calculating VWAP...")
    all_trades = fetch_trades()
    if all_trades:
        calculate_vwap_bands(all_trades)
    vwap_data = calculate_vwap_bands(all_trades)
    
    if vwap_data:
        print(f"Plotting {len(vwap_data)} data points ... ")    

#Visulization part

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize = (12, 6))

        price = [d['price'] for d in vwap_data]
        vwap = [d['vwap'] for d in vwap_data]
        Time = [d['timestamp'] for d in vwap_data]
        up = [d['UP_band'] for d in vwap_data]
        lw = [d['LW_band'] for d in vwap_data]
  
        ax.plot(Time, price, label = 'Price', color = 'grey', alpha = 0.5)
        ax.plot(Time, vwap, label = 'VWAP', color = 'blue', linewidth = 1.5)
        ax.plot(Time, up, label = 'Upper_band', color = 'black', linestyle = '--')
        ax.plot(Time, lw, label = 'Lower_band', color = 'red', linestyle = '--' )

        ax.set_xlabel('Time')
        ax.set_ylabel('Price ($)')
        ax.set_title('Real [VWAP DATA] visulization')

        ax.legend()
        plt.show()
        ax.grid(True)
    else:
        print('No VWAP data caluculated')
else:
    print('proces is stoped because no trade data is not found[lost]')





