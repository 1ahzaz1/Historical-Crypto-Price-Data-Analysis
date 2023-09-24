import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Get the list of all files in the 'data' folder
data_folder = 'data'
data_files = os.listdir(data_folder)


lookback_intervals = list(range(40, 91, 10))

def calculate_trades(df, lookback_interval, forecast_interval, threshold):
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df.dropna(subset=['close'], inplace=True)

    SHIFT = lookback_interval
    fore = -1 * forecast_interval

    pre_ratio = (df["close"]/ df["close"].shift(SHIFT) )

    post_ratio = df["close"].shift(fore) / df["close"]


    prefore = pd.DataFrame(columns=['date-time', 'pre_ratio', 'post_ratio'])
    prefore['pre_ratio'] = pre_ratio
    prefore['post_ratio'] = post_ratio
    prefore['date-time'] = df['date-time']
    prefore.dropna(inplace=True)

    signalled=prefore[prefore['pre_ratio'] > 1 + (threshold/100)] 
    signalled.dropna(inplace=True)

    num_winners = (signalled['post_ratio']>1).sum()
    profit_loss = (signalled['post_ratio']-1).sum()
    total_trades = signalled.shape[0]
    time = signalled['date-time'].str[:10] #Testing only the days needed. remove this slice late

    return time, profit_loss, total_trades, num_winners


# Loop over each file in the 'data' folder
for data_file in data_files:
    file_path = os.path.join(data_folder, data_file)
    print(f"Processing {data_file}...")

    #read csv
    df = pd.read_csv(file_path, header=None, names=['date-time', 'close'])

    # input threshold
    threshold = float(input("Enter the threshold percentage: "))

    # Loop over each lookback interval

    plt.figure()
    for lookback_interval in lookback_intervals:
        forecast_interval = lookback_interval // 2

        # calculate trades for current coin and update coin_total_avg_gains and coin_total_trades
        time, total_gain_loss, num_trades, num_winners = calculate_trades(df, lookback_interval, forecast_interval, threshold)
        
        print(time)
        # plot each coin
        plt.scatter(lookback_interval, total_gain_loss, marker='o')
        plt.xlabel('Lookback Interval (minutes)')
        plt.ylabel('TOTAL Gain/Loss')
        plt.title(f'TOTAL Gain/Loss and Total Trades for {data_file}\n(Threshold: {threshold}%)')
        plt.grid(True)
        plt.annotate(f'T= {num_winners} / {num_trades}', (lookback_interval, total_gain_loss), textcoords="offset points", xytext=(0, 10), ha='center')


plt.show()