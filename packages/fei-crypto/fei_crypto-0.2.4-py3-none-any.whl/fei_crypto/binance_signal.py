import datetime
import os
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

    ms = milliseconds()
    with connection:
        for item in doc:
            for p_item in pre_doc[0]:
                symbol = item["symbol"]
                if p_item["symbol"] == symbol:
                    if not str.endswith(symbol, "USDT"):
                        break
                    price_diff = (float(item["price"]) - float(p_item["price"])) / float(p_item["price"])
                    timestamp_diff = item["time"] - p_item["time"]
                    if 0 < ms - item["time"] < 20000 and 30 * 60 * 1000 > timestamp_diff >= 60 * 1000 and abs(
                            price_diff) > ratio:

                        print(f'🔥【{symbol}】')

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
