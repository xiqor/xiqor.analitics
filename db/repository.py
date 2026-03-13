from models import Candle
import psycopg2
# не проверяй дубликаты здесь, медленно, лучше сделай unique в postgres и с помощью ON CONFLICT DO NOTHING пропускай дубликаты

def insert_candles(conn, candles: list[Candle]) -> None:


    pass