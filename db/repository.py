from models import Candle
import psycopg2
from db.connection import get_connection

# next step: add increment loading (from the last ts to current), batch insert, clean architecture

def insert_candles(conn: psycopg2.extensions.connection, candles: list[Candle]) -> None:
    cursor = conn.cursor()
    for candle in candles:
        cursor.execute('''INSERT INTO ohlcv_data (asset, interval, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (asset, interval, timestamp) DO NOTHING''',
            (candle.asset, candle.interval, candle.timestamp, candle.open, candle.high, candle.low, candle.close, candle.volume))
    conn.commit()
    cursor.close()