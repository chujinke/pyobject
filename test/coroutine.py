from gevent import monkey; monkey.patch_socket()
import gevent
import requests


lis = []
def f(req_url):
    try:
        reqr = requests.get(req_url)
        text = reqr.json()
    except Exception as e:
        lis.append(1)
        length = len(lis)
        len1 =  int(len(lis)*0.1)
        print("*"*len1,length,e)
spa_list = []
for i in range(1000):
    url =  'http://192.168.100.119:8008/httpbin/get?i='+str(i)
    spa_list.append(gevent.spawn(f,url))
gevent.joinall(spa_list)
