from models import Candle
import psycopg2
from db.connection import get_connection

# next step: add increment loading (from the last ts to current), batch insert, cleaner architecture

def insert_candles(candles: list[Candle], conn: psycopg2.extensions.connection) -> None:
    with conn:
        with conn.cursor() as cursor:
            for candle in candles:
                cursor.execute('''INSERT INTO ohlcv_data (asset, interval, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (asset, interval, timestamp) DO NOTHING''',
                    (candle.asset, candle.interval, candle.timestamp, candle.open, candle.high, candle.low, candle.close, candle.volume))

def get_last_timestamp(asset: str, interval: str, conn: psycopg2.extensions.connection) -> str:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT MAX(timestamp) FROM ohlcv_data''')
            max_ts = cursor.fetchone()[0]
            return max_ts