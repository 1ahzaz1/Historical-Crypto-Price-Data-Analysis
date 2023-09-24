from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta

# Initialize Binance API client
api_key = #input 'Key' here
api_secret = #input 'Secret' here
client = Client(api_key, api_secret)

def get_historical_data(symbol, interval, start_date, end_date):
    klines = client.get_historical_klines(symbol, interval, start_str=start_date, end_str=end_date)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df.index.name = None

    df['close'] = df['close'].astype(float).round(2) #Round to 2 decimal places (nearest 1 cent)
    return df[['close']]


end_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')  #downloads data from time of running to 365 days prior


symbol = input("Enter a symbol name (e.g., BTCUSDT): ").strip().upper()
interval = Client.KLINE_INTERVAL_1MINUTE
df = get_historical_data(symbol, interval, start_date, end_date)


file_name = f"{symbol.lower()}_historical_data.csv"
df.to_csv(file_name)

print(f"Data for {symbol} has been saved to {file_name}.")

