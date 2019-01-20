import tornado.web
from tornado.httpclient import AsyncHTTPClient
import tornado.gen

from utils.book_spider import Config
from utils import book_spider
from spider.chd import tbook_cookies

from log import log


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

        try:
            response = yield client.fetch(url, headers=headers,connect_timeout=10,request_timeout=15)       # yield调用client.fetch
        except BaseException as e:
            log.error(str(e) + ":request error : search")
            data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={2: "请求失败"})
        else:
            try:
                # 处理爬下来的代码
                data = book_spider.search_dispose(response.body)
            except IndexError:
                data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={0: "查询结果为空"})
            except BaseException as e:
                log.error(str(e) + ":parser html error")
                data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={1: "查询失败"})             # 处理数据
        self.write(data)

class BookLstHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        用来查询个人借阅情况
        '''
        client = AsyncHTTPClient()
        try:
            # 异步爬虫，以及错误处理
            response = yield client.fetch(Config.book_lst_url, headers=self.headers, connect_timeout=10, request_timeout=15)
        except BaseException as e:
            log.error(str(e)+":request error : booklst")
            return {"msg":{2:"请求失败"}}
        else:
            # 对爬取的数据进行解析
            try:
                data = book_spider.booklst_dispose(response.body)
            except BaseException as e:
                log.error(str(e)+":booklst处理出现错误:"+response.text)
                return {"msg":{1:"查询失败"}}
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
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        cookies = tbook_cookies(username=username,password=password)
        iPlanetDirectoryPro = cookies.get("iPlanetDirectoryPro")
        PHPSESSID = cookies.get("PHPSESSID")

        if iPlanetDirectoryPro and PHPSESSID:
            cookies = "iPlanetDirectoryPro={};PHPSESSID={}".format(iPlanetDirectoryPro, PHPSESSID)
            headers["Cookie"] = cookies
            return headers
        else:
            log.error("cookies为空")
            return None

# class AsyncHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self, *args, **kwargs):
#         client = AsyncHTTPClient()
#         response = yield client.fetch(Config.book_lst_url,headers=self.headers,connect_timeout=10,request_timeout=15)
#         data = book_spider.booklst_dispose(response.body)
#         self.write(data)
#
#     @property
#     def headers(self):
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
#             "Accept": "text/html, */*; q=0.01",
#         }
#         iPlanetDirectoryPro = self.get_argument("iPlanetDirectoryPro", None)
#         PHPSESSID = self.get_argument("PHPSESSID", None)
#         cookies = "iPlanetDirectoryPro={};PHPSESSID={}".format(iPlanetDirectoryPro, PHPSESSID)
#         headers["Cookie"] = cookies
#         return headers
