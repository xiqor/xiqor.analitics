from exceptions import *
from models import Candle
from datetime import datetime

def validate_not_empty(candles: list[dict]):
    try:
        len(candles)
    except ValidationError as e:
        raise e('Candle collection is empty')

def validate_schema(candles: list[dict]):
    required_columns = {'asset', 'interval', 'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    for candle in candles:
        try:
            set(candle.keys()).issubset(required_columns) and set(required_columns).issubset(candle.keys())
        except SchemaValidationError as e:
            raise e('Unexpected candle schema')

def validate_types(candles: list[Candle]):
    for candle in candles:
        try:
            ((isinstance(candle.asset, str)) and
             (isinstance(candle.interval, str)) and
             (isinstance(candle.timestamp, datetime)) and
             (isinstance(candle.open, float)) and
             (isinstance(candle.high, float)) and
             (isinstance(candle.low, float)) and
             (isinstance(candle.close, float)) and
             (isinstance(candle.volume, float)))
        except TypeValidationError as e:
            raise e('Invalid type for candle field')

def validate_price_logic(candles: list[Candle]):
    for candle in candles:
        try:
            ((candle.low <= candle.open <= candle.high) and
             (candle.low <= candle.close <= candle.high) and
             (candle.low <= candle.high) and
             (candle.volume >= 0))
        except PriceLogicValidationError as e:
            raise e('Invalid candle price logic')
