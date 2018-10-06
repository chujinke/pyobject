# encoding=utf-8
from config.rewrite import RequestHandler
from tornado import gen

class Status400Handler(RequestHandler):
    """该Handler完成编号21协议：|/status/400|get|21|无response|No.139|"""

    @gen.coroutine
    def get(self):
        """处理GET请求

        设置400的HTTP状态码和该状态码原因：BAD REQUEST
        """
        self.set_status(status_code=400,reason="BAD REQUEST")
