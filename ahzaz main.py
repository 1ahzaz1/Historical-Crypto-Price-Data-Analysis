import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Get the list of all files in the 'data' folder
data_folder = 'data'
data_files = os.listdir(data_folder)

# input threshold
threshold = float(input("Enter the threshold percentage: "))


lookback_intervals = list(range(2, 22, 2))
total_avg_gains = []

def calculate_trades(df, lookback_interval, forecast_interval, threshold, interval):
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df.dropna(subset=['close'], inplace=True)

    SHIFT = lookback_interval
    fore = -1 * forecast_interval

    pre_ratio = df["close"] / df["close"].shift(SHIFT)
    post_ratio = df["close"] / df["close"].shift(fore)

    profitable_trades = (pre_ratio > 1 + threshold / 100) & (post_ratio > 1)
    unprofitable_trades = (pre_ratio > 1 + threshold / 100) & (post_ratio < 1)

    profitable_gains = (post_ratio[profitable_trades] - 1) * 100
    unprofitable_losses = (1 - post_ratio[unprofitable_trades]) * 100

    total_gain_loss = profitable_gains.sum() - unprofitable_losses.sum()
    total_num_trades = profitable_trades.sum() + unprofitable_trades.sum()

    return total_gain_loss, total_num_trades


# Loop over each file in the 'data' folder
for data_file in data_files:
    file_path = os.path.join(data_folder, data_file)
    print(f"Processing {data_file}...")

    # get interval from the filename
    interval = int(data_file.split('m')[0][-1])

    #read csv
    df = pd.read_csv(file_path, header=None, names=['date-time', 'close'])

    #starting with empty list every new coin
    coin_total_avg_gains = []
    coin_total_trades = []

    # Loop over each lookback interval

    plt.figure()
    for lookback_interval in lookback_intervals:
        forecast_interval = lookback_interval // 2

        # calculate trades for current coin and update coin_total_avg_gains and coin_total_trades
        total_avg_gain_loss, num_trades = calculate_trades(df, lookback_interval, forecast_interval, threshold, interval)

        # plot each coin
        plt.scatter(lookback_interval, total_avg_gain_loss, marker='o')
        plt.xlabel('Lookback Interval (minutes)')
        plt.ylabel('TOTAL Average Gain/Loss')
        plt.title(f'TOTAL Average Gain/Loss and Total Trades for {data_file}\n(Threshold: {threshold}%)')
        plt.grid(True)
        plt.annotate(f'T={num_trades}', (lookback_interval, total_avg_gain_loss), textcoords="offset points", xytext=(0, 10), ha='center')


plt.show()

