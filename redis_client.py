import uuid

import redis as redis


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

if __name__ == '__main__':
    # redis
    print('redis')

    # host = '127.0.0.1'
    host = '192.168.232.130'
    port = 6379

    r = redis.Redis(host=host, port=port, db=3)
    r.set('host:mac', get_mac_address(), ex=10)


