# encoding=utf-8
from handlers import handler_001,handler_003,handler_004,handler_012,handler_013,handler_015,handler_020,handler_021,handler_022,handler_023

urls = [

        #处理get请求
       (r'/httpbin/get', handler_001.GetHandler),

        #处理post请求
       (r'/httpbin/post', handler_003.PostHandler),

        #指定headers的请求
       (r'/httpbin/headers', handler_004.GetHandler),

        #处理豆瓣首页页请求
       (r'/douban/?', handler_013.GetHandler),

        #处理豆瓣tag页面请求
       (r'/douban/tag/(?P<tag_name>.*?)', handler_012.GetHandler),

        #处理豆瓣tag页面请求
       (r'/douban/robots.txt', handler_015.GetHandler),

        #发送201状态码
       (r'/httpbin/status/201',handler_020.Status201Handler),

        #发送400状态码
       (r'/httpbin/status/400',handler_021.Status400Handler),

        #发送500状态码
       (r'/httpbin/status/500',handler_022.Status500Handler),

        #设置cookies
       (r'/httpbin/cookies/set',handler_023.Set_cookiesHandler),

        #设置cookies后的重定向url
       (r'/httpbin/cookies',handler_023.Get_cookiesHandler)

      ]