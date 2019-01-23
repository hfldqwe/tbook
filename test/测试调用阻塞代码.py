import tornado
import tornado.ioloop
import time

def sleep():
    time.sleep(10)
    return 1

async def func():
    a = await tornado.ioloop.IOLoop.current().run_in_executor(None,func=sleep)
    print(a)


if __name__ == '__main__':
    loop = tornado.ioloop.IOLoop.current()
    loop.run_in_executor(None,sleep)
    loop.start()