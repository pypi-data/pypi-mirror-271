import datetime
import os
import time

import requests
import redis
import pymysql.cursors

from fei_crypto.time import milliseconds

KEY = "binance_v2_ticker_price"
ENV_PREFIX = "BINANCE_SIGNAL_"
r = redis.Redis(
    host='192.168.123.11',
    port=36379,
    db=0)

connection = pymysql.connect(host='192.168.123.11',
                             port=3306,
                             user='root',
                             password=os.getenv(f'{ENV_PREFIX}MYSQL_PASSWORD'),
                             database='bot_tx',
                             cursorclass=pymysql.cursors.DictCursor)


def binance_ticker_price() -> requests.Response:
    proxies = None
    proxy = os.getenv(f'{ENV_PREFIX}HTTP_PROXY')
    if proxy is not None:
        proxies = {"http": proxy, "https": proxy, }

    return requests.get("https://fapi.binance.com/fapi/v2/ticker/price", proxies=proxies, timeout=20)


def find_nearest_minutes(minute_number: int, dt: datetime.datetime):
    minute = dt.minute
    remainder = minute % minute_number
    if remainder == 0:
        return dt
    elif remainder <= 5:
        return dt - datetime.timedelta(minutes=remainder)
    else:
        return dt + datetime.timedelta(minutes=minute_number - remainder)


def binance_signal(ratio: float):
    resp = binance_ticker_price()
    if resp.status_code != 200:
        print(f'ERR:binance_ticker_price response code【{resp.status_code}】\n{resp.content}')
        return

    key = KEY

    doc = resp.json()
    pre_doc = r.json().get(key, '$')
    result = r.json().set(key, '$', doc)
    if result is False:
        print("ERR:redis json set failure")
        return
    if pre_doc is None:
        print("ERR:pre doc is None")
        return

    with connection:
        for item in doc:
            symbol = item["symbol"]
            if not str.endswith(symbol, "USDT"):
                continue
            for p_item in pre_doc[0]:
                if p_item["symbol"] == symbol:
                    price = float(item["price"])
                    pre_price = float(p_item["price"])
                    price_diff = (price - pre_price) / pre_price
                    ts = item["time"]
                    pre_ts = p_item["time"]
                    timestamp_diff = ts - pre_ts
                    if 60 * 1000 <= timestamp_diff < 30 * 60 * 1000 and abs(
                            price_diff) > ratio:
                        print(
                            f'🔥【{symbol}】'
                            f'【{pre_price}-{price}】'
                            f'【{pre_ts}-{ts}】')

                        pos_side = "LONG"
                        if price_diff < 0:
                            pos_side = "SHORT"

                        with connection.cursor() as cursor:
                            sql = "INSERT INTO `binance_signals` (`created_at`,`pos_side`,`symbol`,`price_diff`,`timestamp_diff`) VALUES (%s,%s,%s,%s,%s)"
                            cursor.execute(sql, (
                                datetime.datetime.now(),
                                pos_side,
                                symbol,
                                format(price_diff, ".4f"),
                                timestamp_diff))

                        connection.commit()
                    break

    print("🐸 执行成功")


if __name__ == '__main__':
    binance_signal(0.017)
