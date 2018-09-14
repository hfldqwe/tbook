import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handler import main

define('port', default=8000, help='run port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handler = [
            ('/',main.IndexHandler),
            ('/search',main.SearchHandler),
            ('/booklst',main.BookLstHandler),
            ('/async',main.AsyncHandler),
        ]
        settings = dict(
            debug = True,
            template_path = "templates",
            static_path = 'static',
            cookie_secret = 'qdsgrj45DAews2awe5',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': '120.79.197.180',
                    'port': '6379',
                    'password': 'redis_py123',
                    'db_sessions': 5,  # redis db index
                    # 'db_notifications':11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            },
        )
        super(Application, self).__init__(handler,**settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()