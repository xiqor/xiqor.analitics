from data_collecting import fetch_n_candles
from data_normalization import normalize_candles
import pandas as pd

candles = fetch_n_candles('BTC-USDT', '4H', 300) # mb there's a way to make it just go brrr and get every candle to the first one
norm_candles = normalize_candles(candles)
# validation :)


print(norm_candles)