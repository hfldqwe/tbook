from tornado.httpclient import HTTPClient
import urllib.parse

data = urllib.parse.urlencode({"wd":"123"})

client = HTTPClient()

print(data)
response = client.fetch(request="https://www.baidu.com",method="POST",body=data)
print(response.body.decode())