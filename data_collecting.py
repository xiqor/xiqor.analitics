import pandas as pd
import requests
from datetime import datetime
from urllib.parse import parse_qs
import time


"""UTILITY FUNCTIONS"""


def get_okx_server_time() -> int:
    r = requests.get("https://www.okx.com/api/v5/public/time", timeout=(3, 10))
    return int(r.json()['data'][0]['ts'])


"""DATA COLLECTING FUNCTIONS"""


def convert_request_data_to_dict(data: list[dict], url: str) -> dict:
    parsed = requests.utils.urlparse(url)
    query_params = parse_qs(parsed.query)
    asset, interval = query_params.get('instId', [None])[0], query_params.get('bar', [None])[0]
    res_dict = {'asset': asset,
                'interval': interval,
                'timestamp': pd.to_datetime(int(data[0]), utc=False, unit='ms'),
                'open': data[1],
                'high': data[2],
                'low': data[3],
                'close': data[4],
                'volume': data[5]}
    return res_dict


def get_candles(url: str) -> list[dict]:
    r = requests.get(url, timeout=(3, 10))
    data = r.json().get('data', [])
    candles = []
    for jdata in data:
        candle = convert_request_data_to_dict(jdata, url)
        candles.append(candle)
    return candles


def fetch_candles(asset: str, interval: str, limit: int, after: int = None) -> list[dict]:
    base_url = "https://www.okx.com/api/v5/market/history-candles"
    if after is None:
        url = f"{base_url}?instId={asset}&bar={interval}&limit={limit}"
    else:
        url = f"{base_url}?instId={asset}&after={after}&bar={interval}&limit={limit}"
    return get_candles(url)


def fetch_n_candles(asset: str, interval: str, n: int) -> list[dict]:
    res = []
    batch_limit = 300
    after = None
    while len(res) < n:
        limit = min(batch_limit, n - len(res))
        cc = fetch_candles(asset, interval, limit=limit, after=after)
        if not cc:
            break
        res.extend(cc)
        # oldest candle
        oldest = cc[-1]['timestamp']
        after = int(oldest.timestamp() * 1000)
    return res
# mb i should not fetch all candles and use okx limit for batches? think about it later