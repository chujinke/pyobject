# encoding=utf-8
from handlers.public import Request
from tornado import gen

class GetHandler(Request):
    """该Handler完成编号15协议：|/douban/robots.txt|get|15|txt|No.154|"""

    @gen.coroutine
    def get(self):
        """处理GET请求,传出robots.txt"""

        #设置Content-Type值为text/plain以纯文本格式发送
        self.set_header("Content-Type", "text/plain")
        self.render("robots.txt")


