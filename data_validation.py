from exceptions import *

def validate_schema(df):
    bench_columns = ['asset', 'interval', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
    try:
        set(df.columns).issubset(bench_columns) and set(bench_columns).issubset(df.columns)
    except SchemaValidationError(ValidationError) as e:
        raise e('Unexpected candle schema')
