from exceptions import *

def validate_not_empty(candles):
    try:
        len(candles)
    except ValidationError as e:
        raise e('Candle collection is empty')

def validate_schema(candles):
    required_columns = {'asset', 'interval', 'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    for candle in candles:
        try:
            set(candles.keys()).issubset(required_columns) and set(required_columns).issubset(candle.keys())
        except SchemaValidationError(ValidationError) as e:
            raise e('Unexpected candle schema')
