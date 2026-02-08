#Visualization part non API but real data
        #---matplotlib is basically used for visualization so that's why---
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize = (12, 6)) #--this is for the frame size 
        #--these are all final variables what we are defining so that we can plot as visual
        price = [d['price'] for d in vwap_data]
        vwap = [d['vwap'] for d in vwap_data]
        Time = [d['timestamp'] for d in vwap_data]
        up = [d['UP_band'] for d in vwap_data]
        lw = [d['LW_band'] for d in vwap_data]
        #--plotting with micro details like-(label, color , style)
        ax.plot(Time, price, label = 'Price', color = 'grey', alpha = 0.5)
        ax.plot(Time, vwap, label = 'VWAP', color = 'blue', linewidth = 1.5)
        ax.plot(Time, up, label = 'Upper_band', color = 'black', linestyle = '--')
        ax.plot(Time, lw, label = 'Lower_band', color = 'red', linestyle = '--' )
        #--labeling X & Y axis
        ax.set_xlabel('Time')
        ax.set_ylabel('Price ($)')
        ax.set_title('Real [VWAP DATA] visualization')

        ax.legend()
        plt.show()
        ax.grid(True)
    else:
        print('No VWAP data caluculated') #same as you can read what it is used
else:
    print('proces is stoped because no trade data is not found[lost]')

