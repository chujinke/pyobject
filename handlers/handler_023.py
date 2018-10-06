# encoding=utf-8
from handlers.public import Request
from tornado import gen

class  Set_cookiesHandler(Request):
    """该Handler完成编号23协议
            根据query参数设置cookies，并显示
    """
    @gen.coroutine
    def get(self):

        self.clear_all_cookies()
        dicts = self.request.arguments
        key_set = sorted(dicts.keys())
        for key in key_set:
            values = self.get_query_arguments(key)
            if len(values)==1:
                values = "".join(values)
            self.set_cookie(key,values)

        #设置重定向
        self.set_status(302)
        self.set_header("Location",r"/httpbin/cookies")


class Get_cookiesHandler(Request):
    '''显示cookies,主要是显示url:/httpbin/cookies/set设置的cookies'''

    @gen.coroutine
    def get(self):
        get_cookies = self.request.headers["Cookie"]
        cookies_list = get_cookies.split("; ")
        cookies_lists = [item.split("=") for item in cookies_list]
        cookies = dict(cookies_lists)
        data = {'cookies':cookies}
        self.write(data)

