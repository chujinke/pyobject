# encoding=utf-8
from config.rewrite import RequestHandler
from tornado import gen

class Status201Handler(RequestHandler):
    """该Handler完成编号20协议：|/status/201|get|20|无response|No.139|"""

    @gen.coroutine
    def get(self):
        """处理GET请求

        设置201的HTTP状态码和该状态码原因：CREATED
        """
        self.set_status(status_code=201,reason="CREATED")
