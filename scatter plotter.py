import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

data_folder = 'data'
data_files = os.listdir(data_folder)



def calculate_trades(df, lookback_interval, forecast_interval,coin):
   
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    SHIFT = lookback_interval
    fore = -1 * forecast_interval

    pre_ratio = (df["close"]/ df["close"].shift(SHIFT) )
    post_ratio = df["close"].shift(fore) / df["close"]
    df.dropna(subset=['close'], inplace=True)


    plt.figure()
    plt.scatter(pre_ratio, post_ratio)
    plt.axhline(y=1)


    title = f"Lookback: {SHIFT} minutes, Forecast: {abs(fore)} minutes\n coin:{coin[:3]}"

    plt.title(title, fontsize=10, color='black')



for data_file in data_files:
    file_path = os.path.join(data_folder, data_file)
    print(f"Processing {data_file}...")

    #read csv
    df = pd.read_csv(file_path, header=None, names=['date-time', 'close'])

    for lookback_interval in range(30, 91, 10):
        forecast_interval = lookback_interval // 2
        calculate_trades(df, lookback_interval, forecast_interval,data_file)

plt.show()