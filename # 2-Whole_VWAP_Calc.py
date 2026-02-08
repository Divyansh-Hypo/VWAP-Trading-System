def calculate_vwap_bands(incoming_trades):
    if not incoming_trades:  #---same as stops if some problem comes---
        print('no data')
        return []
    #---Main VWAP-calculation---
    #---All Variables named---
    # v = volume, p = price
    vwap_values = []
    total_vp = 0
    total_v = 0
    total_p2_v = 0
    prev_day = None
    day_count = 0
    #---Verifying variables for the data---
    for trade in incoming_trades:
        current_timestamp = trade['timestamp']
        current_day = current_timestamp.date()
        price = trade['price']
        # ---VWAP Reset Logic for new Day---
        if prev_day is not None and current_day != prev_day:
            print(f"New trade data detected {current_day}")

            total_vp = 0
            total_v = 0
            total_p2_v = 0
            UP_band = 0
            LW_band = 0
        #-imp-Calculation
        total_vp += trade['volume'] * trade['price']
        total_p2_v += (trade['price'] ** 2) * trade['volume']
        total_v += trade['volume']
        #---this is used so that final trade data will not come in '0'---
        if total_v > 0:
            current_vwap = (total_vp / total_v)
            vwap_values.append(current_vwap)
            #calculating 'variation' is important for VWAP-bands
            variation = (total_p2_v / total_v) - (current_vwap ** 2)
            std_dev = math.sqrt(max(0, variation))

            UP_band = current_vwap + (2 * std_dev)
            LW_band = current_vwap - (2 * std_dev)
            #this is band width calculation
            band_w = (UP_band - LW_band)
            #-specifying this so that our visulization part works perfect
            trade['vwap'] = current_vwap
            trade['UP_band'] = UP_band
            trade['LW_band'] = LW_band

            #---This is the full printing part 
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
