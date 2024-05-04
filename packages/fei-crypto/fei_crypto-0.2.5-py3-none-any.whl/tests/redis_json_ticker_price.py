import redis

if __name__ == '__main__':
    r = redis.Redis(
        host='192.168.123.11',
        port=36379,
        db=0)

    doc = r.json().get('binance_v2_ticker_price', '$')
    print(doc)
