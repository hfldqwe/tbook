import requests
from lxml import etree
from PIL import Image
from io import BytesIO

from settings import settings,url
from models.redis_handler import BaseRedis
from utils.chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('chdliutao', 'chdliutao', '898470')  #用户中心>>软件ID 生成一个替换 96001

red = BaseRedis()

class Login():
    def __init__(self,username=None,password=None,*args,**kwargs):
        self.username = username
        self.password = password

    def captcha(self,cookies):
        response = requests.get(url.need_captcha_url(username=self.username),headers=url.headers(),cookies=cookies)
        if response.text.strip() == "true":
            captcha_response = requests.get(url=url.captcha_url(),headers=url.headers(),cookies=cookies)
            return captcha_response
        else:
            return None
    def captcha_data(self,response,cas_cookies):
        '''
        通过验证码验证
        :param response: 初步访问的response
        :param cas_cookies: 初步访问增加的cookies
        :return: data一个字典，用于后面登陆的参数
        '''
        captcha_response = self.captcha(cookies=cas_cookies)
        if captcha_response:
            captcha = chaojiying.PostPic(captcha_response.content, 1004).get("pic_str")
            data = self.login_data_captcha(response, captcha)
        else:
            data = self.login_data(response)
        return data

    def login_cas(self):
        '''
        用来进行登陆
        :return: 返回的是登陆后的response对象，调用完成之后，self.cookies为cookies
        '''
        cas_cookies = {}
        #登陆之前的一个get请求，获取参数
        response = requests.get(url.login_cas_url(),headers=url.headers())
        cas_cookies.update(dict(response.cookies))

        # 进行验证码确认，是否需要验证码,并且得到相应的data
        data = self.captcha_data(response,cas_cookies)

        #进行登陆第一步，或者iPlanetDirectoryPro和CASTGC的值
        response = requests.post(url.login_cas_url(),headers=url.headers(),data=data,cookies=response.cookies,allow_redirects=False)

        cas_cookies["CASTGC"] = response.cookies.get("CASTGC")
        cas_cookies["iPlanetDirectoryPro"] = response.cookies.get("iPlanetDirectoryPro")
        return cas_cookies

    def login_tbook(self,cas_cookies,service=None):
        ''' 使用ST进行验证登陆，返回对应网站的cookies '''
        cas_service = url.login_cas_url(service=service)
        response = requests.get(url=cas_service,headers=url.headers(),cookies=cas_cookies,allow_redirects=False)

        # 解析出跳转地址，也就是使用cas服务器生成的ST
        cookies = {"iPlanetDirectoryPro":cas_cookies.get("iPlanetDirectoryPro")}
        ST_url = response.headers.get("Location")

        response = requests.get(url=ST_url,headers=url.headers(),cookies=cookies,allow_redirects=False)
        cookies.update(dict(response.cookies))

        # 这一步的进行还是很有必要的，因为不进行这一步，实际过程中还是会强行跳转到此
        common_url = response.headers.get("Location")
        requests.get(url=common_url,headers=url.headers(),cookies=cookies)

        return cookies

    def login_data(self,response):
        response = etree.HTML(response.text)

        lt = response.xpath("//input[@name='lt']//@value")[0]
        dllt = response.xpath("//input[@name='dllt']//@value")[0]
        execution = response.xpath("//input[@name='execution']//@value")[0]
        _eventId = response.xpath("//input[@name='_eventId']//@value")[0]
        rmShown = response.xpath("//input[@name='rmShown']//@value")[0]

        formdata = {
            "username": self.username,
            "password": self.password,
            "lt": lt,
            "dllt": dllt,
            "execution": execution,
            "_eventId": _eventId,
            "rmShown": rmShown,
            "btn": "",
        }
        return formdata

    def login_data_captcha(self,response,captcha):
        ''' 在有验证的情况下调用这个方法 '''
        data = self.login_data(response)
        data["captchaResponse"] = captcha
        return data

    def login_chd(self,response):
        ''' 这段代码需要小小的修改，暂时不可用 '''
        #进行登陆第二步
        login_url2 = response.headers.get("Location")   #这一步不知道什么用，但是获取了一个MOD_AUTH_CAS的cookies
        response = requests.get(login_url2,headers=url.headers(),cookies=response.cookies,allow_redirects=False)
        self.cookie_jar.set(name="MOD_AUTH_CAS",value=response.cookies.get("MOD_AUTH_CAS"))

        #进行登陆的第三步
        login_url3 = response.headers.get("Location")   #这一步进入算是成功进入信息门户(portal)，有新的cookies
        response = requests.get(login_url3,headers=url.headers(),cookies=self.cookie_jar,allow_redirects=False)

        cookies = {
            "JSESSIONID":response.cookies.get("JSESSIONID"),
            "route":response.cookies.get("route"),
        }
        return cookies

class Cookies():
    def set_cookies(self,username,cookies,type="cas"):
        '''
        将cookies存储在redis中
        :param username: 用户的账号
        :param cookies: 用户的cookies
        :param type: 用户对应的cookies的类型，tbook,对应长安大学图书馆; info，对应长安大学信息门户; cas，对应长安大学cas服务器，这个为默认值
        :return: None
        '''
        username = str(username) + "_" + type
        red.set_cookies(username=username,cookies=cookies)

    def get_cookies(self,username,type="cas"):
        '''
        根据参数，返回不同类型的cookies,数据结构为dict,如果没有返回None
        :param type 有如下选项：tbook,对应长安大学图书馆; info，对应长安大学信息门户; cas，对应长安大学cas服务器，这个为默认值
        '''
        username = str(username)+"_"+type
        cookies = red.get_cookies(username=username)
        return cookies

cookies = Cookies()

def tbook_cookies(username,password):
    ''' 用来查询图书馆的cookies，如果没有则请求建立，如果有，则直接使用 '''
    cookies_tbook = cookies.get_cookies(username,type="tbook")
    if cookies_tbook:
        return cookies_tbook

    cookies_cas = cookies.get_cookies(username,type="cas")
    login = Login(username, password)

    # 检查是否有cas的cookies
    if cookies_cas:
        cookies_tbook = login.login_tbook(cas_cookies=cookies_cas,service=url.tbook_url())
        cookies.set_cookies(username=username,cookies=cookies_tbook,type="tbook")
        return cookies_tbook
    else:
        cookies_cas = login.login_cas()
        cookies_tbook = login.login_tbook(cas_cookies=cookies_cas,service=url.tbook_url())
        cookies.set_cookies(username=username,cookies=cookies_cas,type="cas")
        cookies.set_cookies(username=username,cookies=cookies_tbook,type="tbook")
        return cookies_tbook

if __name__ == '__main__':
    pass
    # login = Login(2017905714,xx)
    # cookies = login.login_cas()
    # print(login.login_tbook(cas_cookies=cookies,service=url.tbook_url()))

    # print(tbook_cookies(username=2017905714,password=xxxx))

