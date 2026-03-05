import pandas as pd
import requests
from datetime import datetime
from urllib.parse import parse_qs
import time


def convert_request_data_to_dict(data, url):
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


def get_candles(url):
    r = requests.get(url, timeout=(3, 10))
    data = r.json().get('data', [])
    candles = []
    for jdata in data:
        candle = convert_request_data_to_dict(jdata, url)
        candles.append(candle)
    return candles


def convert_to_timestamp(datetime_str):
    res = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
    return res


def get_okx_server_time():
    r = requests.get("https://www.okx.com/api/v5/public/time", timeout=(3, 10))
    return int(r.json()['data'][0]['ts'])


def convert_dt_for_interval(dt, interval): # currently up to 4H, >= 1d doesnt work
    # '2020-01-12 17:48:39', '15m'
    # returns -> '2020-01-12 17:45:00'
    # how?
    # mb like this?
    # you can use s, m, H
    d, t = dt[:10], dt[11:]
    trim_value, trim_dim = int(interval[:-1]), interval[-1]
    match trim_dim:
        case 's':
           new_s = str((int(t[-2:]) // trim_value) * trim_value)
           t = t[:-2] + new_s
        case 'm':
            new_m = str((int(t[-5:-3]) // trim_value) * trim_value)
            t = t[:-5] + new_m + ':00'
        case 'H':
            new_H = str((int(t[-8:-6]) // trim_value) * trim_value)
            t = t[:-8] + new_H + ':00:00'
    new_dt = d + ' ' + t
    return new_dt


def fetch_candles(asset, bar, limit, after=None):
    base_url = "https://www.okx.com/api/v5/market/history-candles"
    if after is None:
        url = f"{base_url}?instId={asset}&bar={bar}&limit={limit}"
    else:
        url = f"{base_url}?instId={asset}&after={after}&bar={bar}&limit={limit}"
    return get_candles(url)


def fetch_n_candles(asset, bar, n):
    res = []
    batch_limit = 300
    after = None
    while len(res) < n:
        limit = min(batch_limit, n - len(res))
        cc = fetch_candles(asset, bar, limit=limit, after=after)
        if not cc:
            break
        res.extend(cc)
        # oldest candle
        oldest = cc[-1]['timestamp']
        after = int(oldest.timestamp() * 1000)
    return res
# mb i should not fetch all candles and use okx limit for batches? think about it later