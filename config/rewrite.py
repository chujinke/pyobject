# encoding=utf-8
import tornado.web

class RequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        pass
