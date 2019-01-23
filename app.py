import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from handler import main

define('port', default=8005, help='run port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handler = [
            ('/',main.IndexHandler),
            ('/search',main.SearchHandler),
            ('/booklst',main.BookLstHandler),
            ('/history',main.HistoryHandler),
            ('/fine',main.FineHandler),
            ('/renew',main.RenewHandler),
        ]
        settings = dict(
            debug = False,
            template_path = "templates",
            static_path = 'static',
        )
        super(Application, self).__init__(handler,**settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()