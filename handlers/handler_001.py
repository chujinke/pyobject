# encoding=utf-8
from handlers.public import Request
from tornado import gen

class GetHandler(Request):
    '''该Handler完成编号1、2、6、7、8、9协议：
            |/httpbin/get|get|1|JSON|No.136|，以及链接中含参数
    '''
    @gen.coroutine
    def get(self):
        """处理GET请求,允许url带参数"""

        res_data = Request.get_result1(self)
        self.write( res_data)



