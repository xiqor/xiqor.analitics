from data_collecting import fetch_n_candles
from data_validation import validate_not_empty, validate_schema, validate_types, validate_price_logic
from data_normalization import normalize_candles
from db.connection import get_connection
from db.repository import insert_candles, get_last_timestamp
import pandas as pd

candles = fetch_n_candles('BTC-USDT', '4H', 10) # mb there's a way to make it just go brrr and get every candle to the first one
validate_not_empty(candles)
validate_schema(candles)
norm_candles = normalize_candles(candles)
validate_types(norm_candles)
validate_price_logic(norm_candles)

print(norm_candles)

connection = get_connection()

insert_candles(connection, norm_candles)
print(get_last_timestamp('BTC-USDT', '4H', connection))

connection.close()