#Program currently being used to understand how to implement the trading strategy into live trading via Binance API

import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import asyncio


async def main():
    client = Client("lNtYl8xT5T9rDZPQYY3MNPVhOwvW3EbjNVdqvukDz2g0qn6lIeHp0yk6LbsALpiB", "WPeEEuXwcZpMC7mcD1xofI64zrOpSCIHji5YYcBBo4EHFKhfmGlM20aJ2DGWmmBH")
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket('XRPUSDT')
    
    async with socket as s:
        while True:
            msg = await s.recv()
            print(msg)

if __name__ == "__main__":
    asyncio.run(main())