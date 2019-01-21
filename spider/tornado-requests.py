import urllib.parse
import collections.abc
from tornado.httpclient import AsyncHTTPClient

class Single():
    ''' 单例模式 '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

class Response():
    def __init__(self,request):
        self._content = None
        self.encoding = None
        self.request = request

    # 生成response对象
    @classmethod
    def _response(cls,response,request):
        resp = cls(request)
        ''' 这个地方可能有些问题，这个request对象应该返回我们封装的request对象，而不是tornado中的request对象
            但由于暂时request对象没有封装好，所以，暂时保留tornado中的request的对象，所以说，现在的request在之后会被替换
        '''
        resp.__dict__.update(response.__dict__)
        return resp

    @property
    def content(self):
        if self.buffer is None:
            return None
        elif self._body is None:
            self._body = self.buffer.getvalue()

        return self._body

    @property
    def text(self):
        if not self.encoding:
            self.encoding = "utf-8"
        return self.content.decode(encoding=self.encoding,errors="ignore")

    @property
    def status(self):
        return self.code

class Request(Single):
    def __init__(self):
        if not hasattr(self,"client"):
            self.client = AsyncHTTPClient()

    async def requests(self,method,url,**kwargs):
        body = kwargs.get("body")
        if body:
            if isinstance(body,collections.abc.MutableMapping):
                body = urllib.parse.urlencode(body)
                kwargs["body"] = body
        response = await self.client.fetch(url,method=method,**kwargs)
        resp = Response._response(response=response,request=self)
        return resp

    async def get(self,url,**kwargs):
        return await self.requests(method="GET",url=url,**kwargs)

    async def post(self,url,**kwargs):
        return await self.requests(method="POST", url=url,**kwargs)


requests = Request()