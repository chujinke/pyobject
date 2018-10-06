# encoding=utf-8
import unittest
import requests
import sys

class Testhttp(unittest.TestCase):
    '''单元测试类'''
    def setUp(self):
        self.host = "http://127.0.0.1:8008"

    def test_get_noarg(self):
        '''测试无参数的get请求'''
        url = self.host+"/httpbin/get"
        data = {}
        test = Public()
        test.get(url, data, "args")

    def test_getarg(self):
        '''测试多个参数，一个参数含一个值的get请求'''
        url = self.host+"/httpbin/get"
        data = {"type": "1", "page": "2"}
        test = Public()
        test.get(url, data, "args")

    def test_getargs(self):
        '''测试多个参数，一个参数含多个值的get请求'''
        url = self.host+"/httpbin/get"
        data = {"k1": ["v1","v3"], "k2": "v2"}
        test = Public()
        test.get(url,data,"args")



    def test_postform(self):
        '''测试多个参数，一个参数含多个值的post请求'''
        url = self.host+"/httpbin/post"
        data = { "k1": ["v1","v3"], "k2": "v2"}
        test = Public()
        test.post(url,data,"form")

    def test_postforms(self):
        '''测试指定headers，且有多个参数，一个参数含多个值的post请求'''
        url = self.host+"/httpbin/post"
        data = {'custname':u'博雅大数据学院','custtel':'010-62756975','custemail': 'service@boyabigdata.cn','delivery':'18:00','comments':u'北京市海淀区北四环西路67号中关村国际创新大厦603','size':'large','topping':['mushroom','cheese']}
        headers = {'Accept': '*/*',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                 'Cache-Control': 'no-cache',
                 'Connection': 'keep-alive',
                 'Dnt': '1',
                 'Host': 'hackdata.cn',
                 'Origin': 'http://httpbin.org',
                 'Pragma': 'no-cache',
                 'Referer': 'http://httpbin.org/forms/post',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0'}
        reqr = requests.post(url,data=data,headers=headers)
        test_url = reqr.url
        self.assertEqual(reqr.status_code, 200)
        data_set = reqr.json()
        for items in data:
            self.assertEqual(data_set["form"][items], data[items])
        for item in headers:
            self.assertEqual(data_set["headers"][item], headers[item])
        self.assertEqual(data_set["origin"], "192.168.1.1")
        print(data_set["url"],test_url)
        #self.assertEqual(data_set["url"],test_url)

    def test_getheaders(self):
        """指定headers并验证的get请求"""
        url = self.host+"/httpbin/headers"
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Accept-Encoding': 'gzip, deflate',
                     'Host': 'httpbin.org',
                     'Referer': 'http://httpbin.org',
                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        reqr = requests.get(url,headers=headers)
        self.assertEqual(reqr.status_code,200)
        data_set = reqr.json()
        for item in headers:
            self.assertEqual(data_set["headers"][item],headers[item])

    def test_index(self):
        '''验证豆瓣首页内容'''
        url = self.host+"/douban/"
        test = Public()
        test.html(url,"首页")

    def test_yingguo_xiju_2015(self):
        '''验证英国 喜剧 2015页内容'''
        url = self.host+"/douban/tag/%E8%8B%B1%E5%9B%BD%20%E5%96%9C%E5%89%A7%202015?start=20&type=S"
        test = Public()
        test.html(url,"英国 喜剧 2015")

    def test_xiju(self):
        '''验证喜剧页内容'''
        url = self.host+"/douban/tag/%E5%96%9C%E5%89%A7"
        test = Public()
        test.html(url,"喜剧")

    def test_donghua(self):
        '''验证动画页内容'''
        url = self.host+"/douban/tag/%E5%8A%A8%E7%94%BB"
        test = Public()
        test.html(url,"动画")

    def test_juqing(self):
        '''验证剧情页内容'''
        url = self.host+"/douban/tag/%E5%89%A7%E6%83%85"
        test = Public()
        test.html(url,"剧情")

    def test_kehuan(self):
        '''验证科幻页内容'''
        url = self.host+"/douban/tag/%E7%A7%91%E5%B9%BB"
        test = Public()
        test.html(url,"科幻")

    def test_status201(self):
        """验证201状态码"""
        url = self.host+"/httpbin/status/201"
        test = Public()
        test.status_code(url,201 )

    def test_status400(self):
        """验证400状态码"""
        url = self.host+"/httpbin/status/400"
        test = Public()
        test.status_code(url,400 )

    def test_status(self):
        """验证500状态码"""
        url = self.host+"/httpbin/status/500"
        test = Public()
        test.status_code(url,500 )

    def test_setcookie(self):
        '''验证cookie设置是否成功'''
        url = self.host+"/httpbin/cookies/set?passport=boyabigdata"
        reqr = requests.get(url)
        self.assertEqual(reqr.status_code, 200)
        data = reqr.json()
        self.assertEqual(data["cookies"]["passport"],"boyabigdata")

    def runTest(self):
        pass


class Public(Testhttp):
    """公共方法类"""

    def get(self,url,data,testunit):
        """get请求公共方法"""
        reqr = requests.get(url,data)
        test_url = reqr.url
        self.assertEqual(reqr.status_code,200)
        data_set = reqr.json()
        for item in data:
            self.assertEqual(data_set[testunit][item],data[item])
        self.assertEqual(data_set["origin"],"192.168.1.1")
        self.assertEqual(data_set["url"],test_url)


    def post(self,url,data,testunit):
        """post请求公共方法"""
        reqr = requests.post(url, data)
        self.assertEqual(reqr.status_code, 200)
        test_url = reqr.url
        data_set = reqr.json()
        for item in data:
            self.assertEqual(data_set[testunit][item], data[item])
        self.assertEqual(data_set["origin"],"192.168.1.1")
        self.assertEqual(data_set["url"],test_url)

    def html(self,url,type):
        '''验证返回的HTML'''
        reqr = requests.get(url)
        self.assertEqual(reqr.status_code, 200)
        data = reqr.text
        data_list = data.replace('\r','').split('\n')
        name = "./htmlfiles/" + type + ".htm"
        if sys.version[0:3] == "2.7":
            name = name.decode('utf8')
            with open(name,"r",) as f:
                string = f.read().decode('utf-8')
                str_list = string.replace('\r','').split("\n")
                length = len(str_list)
                for i in range(length):
                    self.assertEqual(data_list[i].strip(), str_list[i].strip())
        else:
            with open(name, "r", encoding='utf-8') as f:
                string = f.read()
                str_list = string.replace('\r', '').split("\n")
                length = len(str_list)
                for i in range(length):
                    self.assertEqual(data_list[i].strip(), str_list[i].strip())

    def status_code(self,url,code):
        """验证访问的错误页的状态码"""
        reqr = requests.get(url)
        self.assertEqual(reqr.status_code, code)


if __name__=="__main__":
    unittest.main()
