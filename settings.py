'''
用来进行设置，读取设置，修改设置等等操作
'''
import os
import time
from utils.config import Application,UrlConfig

run_dir = os.getcwd()
dir = os.path.split(os.path.realpath(__file__))[0]

class Settings(Application):
    def __init__(self):
        redis_password = self.read_conf_values("info.ini","redis_236","password")
        settings = {
            "redis":{
                "host":"127.0.0.1",
                "port":"6379",
                "db":"2",
                "password":redis_password,
            },
        }
        super().__init__(**settings)

class Url(UrlConfig):
    def __init__(self):
        urls = {
            "login_cas":"http://ids.chd.edu.cn/authserver/login", #cas 认证系统
            "login":"http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F", #chd登陆
            "tbook":"http://wiscom.chd.edu.cn:8080/reader/hwthau.php",   # 图书馆链接
            "tbook_index":"http://wiscom.chd.edu.cn:8080/reader/redr_info.php", #  图书馆的首页
            "need_captcha":"http://ids.chd.edu.cn/authserver/needCaptcha.html", # 确认是否需要验证码
            "captcha":"http://ids.chd.edu.cn/authserver/captcha.html",  # 验证码的链接
        }
        super().__init__(**urls)

    def login_cas_url(self,service=None):
        ''' 访问cas服务器的链接，另外用于构造使用此cas服务器的其他服务的链接 '''
        if service:
            return self.urlencode(self.login_cas,service=service)
        else:
            return self.login_cas

    def tbook_url(self):
        ''' 访问图书馆的链接 '''
        return self.tbook

    def tbook_index_url(self):
        ''' 图书馆的首页，用于验证图书馆登陆状况 '''
        return self.tbook_index

    def login_url(self):
        return self.login

    def need_captcha_url(self,username):
        return self.urlencode(self.need_captcha,username=username,_=int(time.time()*1000))

    def captcha_url(self):
        return self.captcha

os.chdir(dir)
settings = Settings()
url = Url()
os.chdir(run_dir)

if __name__ == '__main__':
    settings = Settings()
    url = Url()
    print(settings.redis)

