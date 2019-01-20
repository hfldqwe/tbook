import redis,json
import time
import random

from utils.config import Single
from settings import settings


class BaseRedis(Single):
    def __init__(self):
        ''' 只会调用一次，防止多次进行连接浪费资源 '''
        if not hasattr(self,"red"):
            config = settings.redis
            self.red = redis.Redis(host=config["host"],port=int(config["port"]),db=int(config["db"]),password=config["password"])

    def set_cookies(self,username,cookies):
        ''' 建立cookies '''
        self.red.hmset(username,cookies)
        self.red.expire(username,3600*24*1)

    def get_cookies(self,username):
        ''' 获取cookies '''
        cookies_bytes = self.red.hgetall(username)
        if cookies_bytes:
            cookies = {k.decode(): v.decode() for k, v in cookies_bytes.items()}
            return cookies
        return None

if __name__ == '__main__':
    red = BaseRedis()
    cookies = red.get_cookies(username=2017905714)
    print(cookies)