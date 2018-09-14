import tornado.web
from tornado.httpclient import AsyncHTTPClient
import tornado.gen

from utils.book_spider import Spider
from utils.book_spider import Config
from utils import book_spider

import json

spider = Spider()


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("这是一个测试页面")

class SearchHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        用来搜索图书馆馆藏信息
        :param strText: 搜索的内容，如：strText="python"
        :param page: 页数，默认是第一页
        :param onlylendable:是否只查询可借阅书籍，默认为False，传其他任意参数都为True
        :return:一个json数据
        {
            "book_storm":{
                0:["语言","书名","编号","馆藏复本","可借复本","作者","出版社和时间"],
                1:[............],
                2:[............],
                .....
                },
            "cuurent_end_page":current_end_page,#当前到末尾的页数
            "msg":True
        }
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept": "text/html, */*; q=0.01",
        }
        strText = self.get_argument("strText",None)
        page = self.get_argument("page","1")
        onlylendable = self.get_argument("onlylendable","no")

        client = AsyncHTTPClient()
        url = book_spider.search_payload(strText=strText, page=page,onlylendable=onlylendable)          # 构造url
        response = yield client.fetch(url, headers=headers,connect_timeout=10,request_timeout=15)       # yield调用client.fetch
        data = book_spider.search_dispose(response.body)                                                # 处理数据
        self.write(data)

class BookLstHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        用来查询个人借阅情况
        '''
        client = AsyncHTTPClient()
        response = yield client.fetch(Config.book_lst_url, headers=self.headers, connect_timeout=10, request_timeout=15)
        data = book_spider.booklst_dispose(response.body)
        self.write(data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        '''
        用来续借
        '''
        bar_code = self.get_argument("bar_code",None)
        captcha = self.get_argument("captcha",None)
        check = self.get_argument("check",None)

        client = AsyncHTTPClient()
        url = book_spider.renew_parmas(bar_code, captcha, check)
        response = yield client.fetch(url,headers=self.headers,connect_timeout=10,request_timeout=15)
        self.write(response.body)

    @property
    def headers(self):
        '''
        提供查询个人借阅情况以及续借所需的headers（包含构造的cookies）
        :return: headers
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept": "text/html, */*; q=0.01",
        }
        iPlanetDirectoryPro = self.get_argument("iPlanetDirectoryPro", None)
        PHPSESSID = self.get_argument("PHPSESSID", None)
        cookies = "iPlanetDirectoryPro={};PHPSESSID={}".format(iPlanetDirectoryPro, PHPSESSID)
        headers["Cookie"] = cookies
        return headers

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        client = AsyncHTTPClient()
        response = yield client.fetch(Config.book_lst_url,headers=self.headers,connect_timeout=10,request_timeout=15)
        data = book_spider.booklst_dispose(response.body)
        self.write(data)

    @property
    def headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept": "text/html, */*; q=0.01",
        }
        iPlanetDirectoryPro = self.get_argument("iPlanetDirectoryPro", None)
        PHPSESSID = self.get_argument("PHPSESSID", None)
        cookies = "iPlanetDirectoryPro={};PHPSESSID={}".format(iPlanetDirectoryPro, PHPSESSID)
        headers["Cookie"] = cookies
        return headers
