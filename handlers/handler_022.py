# encoding=utf-8
from config.rewrite import RequestHandler
from tornado import gen

class Status500Handler(RequestHandler):
    """该Handler完成编号22协议：|status/500|get|22|无response|No.139|"""

    @gen.coroutine
    def get(self):
        """处理GET请求

        设置500的HTTP状态码和该状态码原因：INTERNAL SERVER ERROR
        """

        self.set_status(status_code=500,reason="INTERNAL SERVER ERROR")
