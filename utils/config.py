from configparser import ConfigParser

from utils import urlconf

def read_conf(filename,section,*options):
    ''' 读取配置文件信息,返回一个元组 '''
    config = ConfigParser()
    config.read(filename)
    data = {option:config.get(section,option) for option in options}
    return data

class Single():
    ''' 单例模式 '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

class Application(Single):
    def __init__(self,*args,**kwargs):
        self.set(**kwargs)

    def set(self,**kwargs):
        ''' 设置属性 '''
        for key,value in kwargs.items():
            setattr(self,key,value)

    def read_conf_dict(self,filename, section, *options):
        ''' 读取配置文件信息,返回一个含有这些参数的字典(option作为键，value作为值) '''
        config = ConfigParser()
        config.read(filename)
        data = {option: config.get(section, option) for option in options}
        return data

    def read_conf_values(self,filename, section, *options,return_tuple=False):
        '''
            单个字段返回一个值，多个字段返回一个列表
        :param filename: 文件名
        :param section: 节点名
        :param options: 配置参数名
        :param return_type: 返回类型，bool，如果为True，那么
        :return:
        '''
        config = ConfigParser()
        config.read(filename)
        data = [config.get(section, option) for option in options]
        if not return_tuple and len(data)==1:
            return data[0]
        return data

    def set_conf(self, filename, section, *options):
        ''' 将ini文件中的参数设置为属性 '''
        data = self.read_conf(filename,section,*options)
        self.set(**data)


class UrlConfig(Application):
    ''' 用来配置url '''
    def urlencode(self,url,**kwargs):
        return urlconf.urlencode(url,kwargs)

    def headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }




