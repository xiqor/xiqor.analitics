from datetime import datetime
from dataclasses import dataclass
import pandas as pd

@dataclass
class Candle:
    asset: str
    interval: str # or mb use enum?
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    @classmethod
    def from_dict(cls, data: dict):
        ts = data["timestamp"]
        if isinstance(ts, pd.Timestamp):
            ts = ts.to_pydatetime()
        return cls(
            asset=data["asset"],
            interval=data["interval"],
            timestamp=ts,
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"])
        )