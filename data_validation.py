from exceptions import *
from models import Candle

def validate_not_empty(candles: list[dict]):
    try:
        len(candles)
    except ValidationError as e:
        raise e('Candle collection is empty')

def validate_schema(candles: list[dict]):
    required_columns = {'asset', 'interval', 'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    for candle in candles:
        try:
            set(candles.keys()).issubset(required_columns) and set(required_columns).issubset(candle.keys())
        except SchemaValidationError(ValidationError) as e:
            raise e('Unexpected candle schema')

def validate_types(candles: list[Candle]):
    pass

def validate_price_logic(candles: list[Candle]):
    for candle in candles:
        try:
            ((candle.low <= candle.open <= candle.high) and
             (candle.low <= candle.close <= candle.high) and
             (candle.low <= candle.high) and
             (candle.volume >= 0))
        except PriceLogicValidationError(ValidationError) as e:
            raise e('Price logic error')
