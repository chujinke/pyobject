# encoding=utf-8
from handlers.public import Request
from tornado import gen

class PostHandler(Request):
    """该Handler完成编号3，5,10协议：/httpbin/post|post|3|JSON|No.137<br> body{ "k1": "v1", "k2": "v2"} |
                             和/httpbin/post|post|5|JSON|No.141<br>带参数<br>{'k2': 'v2', 'k1': ['v1', 'v3']}|
                             和|/httpbin/post|post|10|JSON|No.145<br>post内容：
                                    {'custname':'博雅大数据学院','custtel':'010-62756975','custemail': 'service@boyabigdata.cn','delivery':'18:00',
                                    'comments':'北京市海淀区北四环西路67号中关村国际创新大厦603',
                                    'size':'large','topping':'mushroom','cheese'}|
    """

    @gen.coroutine
    def post(self):
        """处理POST请求 """

        ##数据初始化
        data = {
              "args": {},
              "data": "",
              "files": {},
              "form": {},
              "headers": {},
              "json": None,
              "origin": "",
              "url": ""
              }
        res_data = Request.post_result1(self,data)
        self.write(res_data)
