# encoding=utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop
from handlers import url
from tornado.options import define, options
from config import setting

define("port", default=8008, help="run on the given port", type=int)

application = tornado.web.Application(
    handlers = url.urls,
    **setting.file_setting
)

def run():
    '''创建web应用、服务，并开启IOLoop'''

    tornado.options.parse_command_line()
    app = application
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()