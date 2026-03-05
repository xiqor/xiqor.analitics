from data_collecting import fetch_n_candles
import pandas as pd

candles = fetch_n_candles('BTC-USDT', '4H', 18000) # mb there's a way to make it just go brrr and get every candle to the first one
df = pd.DataFrame(candles)
print(df.tail())