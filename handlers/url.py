# encoding=utf-8
from handlers import handler_001,handler_002,handler_003,handler_004

urls = [

        #云图请求
       (r'/wordcloud', handler_001.GetHandler),

       #词频
       (r'/words', handler_002.GetHandler),

        #文本聚类
       (r'/julei', handler_003.PostHandler),

        #关联性、回归分析
       (r'/regression', handler_004.GetHandler),


      ]