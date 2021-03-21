import socket
import uuid

import redis as redis
import requests

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

if __name__ == '__main__':
    print('---- 主机信息 ---')
    # 主机信息
    # hostname = socket.getfqdn(socket.gethostname())
    # address = socket.gethostbyname(hostname)
    # print(hostname, address)
    # print(socket.gethostname())
    # print(socket.getfqdn())

    # kv = {'wd': 'IP'}
    # resp = requests.get("http://www.baidu.com/s", params=kv)
    # print('status_code', resp.status_code)
    # print('text', resp.text)

    # addressinfo = socket.gethostbyname_ex(socket.gethostname())
    # print(addressinfo)
    # print(addressinfo[2])
    # ip_arr = addressinfo[2]
    # for ip in ip_arr:
    #     addr = socket.gethostbyaddr(ip)
    #     print(ip, ' ===>: ', addr)

    # hostname = socket.gethostname()
    # resp = requests.get('https://api.ipify.org')
    # ip = resp.text
    # print(ip)
    #
    # print(get_mac_address())

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('ip: ', s.getsockname()[0], ', port: ', s.getsockname()[1], sep='')
    s.close()

