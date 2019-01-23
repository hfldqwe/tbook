from lxml import etree
import json
import re
import tornado.web
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from utils.book_spider import Config
from utils import book_spider
from spider.chd import tbook_cookies
from spider.tornado_requests import requests

from log import log
from utils.chaojiying import chaojiying


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("这是一个测试页面")

class BaseHandler(tornado.web.RequestHandler):
    ''' 这个handler作为需要cookies的请求的基类 '''
    executor = ThreadPoolExecutor(20)
    @run_on_executor
    def headers(self):
        '''
        提供查询个人借阅情况以及续借所需的headers（包含构造的cookies）
        :return: headers
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
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

class SearchHandler(tornado.web.RequestHandler):

    async def get(self, *args, **kwargs):
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
        strText = self.get_argument("strText",None)
        page = self.get_argument("page","1")
        onlylendable = self.get_argument("onlylendable","no")

        url = book_spider.search_payload(strText=strText, page=page,onlylendable=onlylendable)          # 构造url
        try:
            data = await self.search(url)       # yield调用client.fetch

        except BaseException as e:
            log.error(str(e) + ":request error : search")
            data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={2: "请求失败"})

        data = json.dumps(data,ensure_ascii=False)
        self.write(data)

    async def search(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept": "text/html, */*; q=0.01",
        }
        data = {}
        response = await requests.get(url, headers=headers,connect_timeout=10,request_timeout=15)       # yield调用client.fetch
        try:
            response = etree.HTML(response.text)
            current_end_page = response.xpath("//span[@class='pagination']//b//text()")
            books = response.xpath("//li[@class='book_list_info']")
            for i in range(len(books)):
                info = books[i].xpath(".//text()")
                info = ["".join(i.split()) for i in info if i.strip()]
                data[i] = {
                    "language":info[0],
                    "name" : info[1].split(".")[1],
                    "code" : info[2],
                    "collection_number":re.compile(r"\d+").findall(info[3])[0],
                    "lendable_number":re.compile(r"\d+").findall(info[4])[0],
                    "author": info[5],
                    "publish_hose":info[6],
                }
            data = {"msg":True,"book":data,"current_page":current_end_page[0],"end_page":current_end_page[-1]}
        except IndexError:
            data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={0: "查询结果为空"})
        except BaseException as e:
            log.error(str(e) + ":parser html error")
            data = book_spider.search_data(book_storm_dict=None, current_end_page=None, msg={1: "查询失败"})  # 处理数据
        return data

class BookLstHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        '''
        用来查询个人借阅情况
        '''
        headers = await self.headers()
        try:
            # 异步爬虫，以及错误处理
            data = await self.booklst(headers)
        except BaseException as e:
            log.error(str(e)+":request error : booklst")
            data = {"msg":{2:"请求失败"}}

        data = json.dumps(data, ensure_ascii=False)
        self.write(data)

    async def booklst(self,headers):
        data = {}
        response = await requests.get(Config.book_lst_url, headers=headers, connect_timeout=10, request_timeout=15)
        response = etree.HTML(response.text)

        # 解析
        book_info = response.xpath("//div[@id='mylib_content']//tr")
        key = ["bar_code","book","borrow_date","return_date","renewal","collection","annex","check"]
        values = [value.xpath(".//td") for value in book_info[1:] ]
        for i in range(len(book_info)-1):
            data[i] = {}
            for j in range(len(key) - 1):
                data[i][key[j]]=values[i][j].xpath(".//text()")[0].strip()
            data[i]["check"] = re.compile("getInLib\('(.*?)','(.*?)'").findall(values[i][-1].xpath(".//@onclick")[0])[0][1]

        return {
            "msg":True,
            "booklst":data,
        }

class RenewHandler(BaseHandler):
    def __init__(self,*args,**kwargs):
        super(RenewHandler, self).__init__(*args,**kwargs)

    async def get(self, *args, **kwargs):
        '''
        用来续借
        '''
        headers = await self.headers()
        bar_code = self.get_argument("bar_code",None)
        check = self.get_argument("check",None)
        captcha = await self.captcha(headers)

        url = book_spider.renew_parmas(bar_code, captcha, check)
        print(url)
        response = await requests.get(url,headers=headers,connect_timeout=10,request_timeout=15)
        self.write(response.body)

    async def captcha(self,headers):
        response = await requests.get(url=Config.renew_image_url,headers=headers,connect_timeout=10,request_timeout=15)
        ''' 这里为阻塞代码，有待优化 '''
        resp = await tornado.ioloop.IOLoop.current().run_in_executor(None,chaojiying.PostPic, response.content, 1004)
        return resp.get("pic_str")

class HistoryHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        '''请求历史借阅'''
        headers = await self.headers()
        try:
            history = await self.history(headers)
        except BaseException as e:
            log.error(str(e) + ":request error : history")
            data = {"msg": {2: "请求失败"}}
        else:
            data = {"msg":True,"history": history}

        data = json.dumps(data, ensure_ascii=False)
        self.write(data)

    async def history(self,headers):
        data = {}
        response = await requests.get(Config.book_hist_url, headers=headers, connect_timeout=10, request_timeout=15)
        response = etree.HTML(response.text)
        trs = response.xpath("//div[@id='mylib_content']//tr")[1:]
        for i in range(len(trs)):
            data[i] = [tr.xpath(".//text()")[0].strip() for tr in trs[i].xpath(".//td")[1:]]
        data = {key:{
            "bar_code" : value[0],
            "name" : value[1],
            "author" : value[2],
            "borrow_date" : value[3],
            "return_date" : value[4],
            "collection" : value[5],
        } for key,value in data.items()}
        return data

class FineHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        '''请求违章缴款'''
        headers = await self.headers()
        try:
            fine = await self.fine(headers)
        except BaseException as e:
            log.error(str(e) + ":request error : fine")
            data = {"msg": {2: "请求失败"}}
        else:
            data = {"msg":True,"fine": fine}

        data = json.dumps(data, ensure_ascii=False)
        self.write(data)

    async def fine(self,headers):
        data = {}
        response = await requests.get(Config.fine_pec_url,headers=headers, connect_timeout=10, request_timeout=15)
        response = etree.HTML(response.text)
        trs = response.xpath("//div[@id='mylib_content']//tr")[1:]
        for i in range(len(trs)):
            data[i] = [tr.xpath(".//text()")[0].strip() for tr in trs[i].xpath(".//td")]

        data = {key:{
            "bar_code":value[0],
            "code" : value[1],
            "name":value[2],
            "author" : value[3],
            "borrow_date" : value[4],
            "return_date" : value[5],
            "collection" : value[6],
            "pay" : value[7],
            "real_pay" : value[8],
            "status" : value[9],
        } for key,value in data.items()}
        return data
