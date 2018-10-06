# encoding=utf-8
from config.rewrite import RequestHandler

class Request(RequestHandler):
    """获取的用户请求基本信息，集合成字典并返回"""

    def get_result1(self):
         """在GET请求处理并返回信息"""
         data = {}
         args = {}
         url = self.request.full_url()
         dicts = self.request.arguments
         key_set = sorted(dicts.keys())
         for key in key_set:
             values = self.get_query_arguments(key)
             if len(values)==1:
                 values = "".join(values)
             args[key] = values

         ##根据请求修改data里的数据
         data['args'] = args
         data['headers'] = dict(self.request.headers)
         data['origin'] = "192.168.1.1"
         data['url'] = url
         data['headers']['Host'] = "hackdata.cn"
         data['headers']['Connection'] = "close"
         return data



    def post_result1(self,data):
         """在POST请求处理并返回信息"""
         form = {}
         url = self.request.full_url()
         dicts = self.request.arguments
         key_set = sorted(dicts.keys())
         for key in key_set:
             values = self.get_body_arguments(key)
             if len(values)==1:
                 values = "".join(values)
             form[key] = values
         ##根据请求修改data里的数据
         data['form'] = form
         data['headers'] = dict(self.request.headers)
         data['headers']['Host'] = "hackdata.cn"
         data['origin'] = "192.168.1.1"
         data['url'] = url
         return data


    def verification_query(self):
        """验证豆瓣tag页面请求链接参数是否符合要求"""
        try:
            start = self.get_query_argument("start")
            type = self.get_query_argument("type")
            if start=='20' and type=='S':
                return True
            else:return False
        except:
            return False






