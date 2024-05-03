import base64

from tests import *
import os
import redis

if __name__ == '__main__':
    r = redis.Redis(
        host='192.168.123.11',
        port=36379,
        db=0)

    # hello = r.hget('hash_test', 'hello')
    # print(hello)
    # print(type(hello))

    data = {
        'dog': {
            'scientific-name': 'Canis familiaris'
        }
    }

    r.json().set('json_test', '$', data)
    doc = r.json().get('json_test', '$')
    print(doc)
    dog = r.json().get('json_test', '$.dog')
    print(dog)
    scientific_name = r.json().get('json_test', '$..scientific-name')
    print(scientific_name)
