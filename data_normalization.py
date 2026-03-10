from models import Candle


def normalize_candles(candles: list[dict]) -> list[Candle]:
    return [Candle.from_dict(c) for c in candles]