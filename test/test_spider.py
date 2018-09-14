import requests
import time
from tornado.httpclient import AsyncHTTPClient
import json

cookies = {
        "iPlanetDirectoryPro": "AQIC5wM2LY4SfcxRbH%2F611nsKDKhEmz%2B8zaRtqY4qeLv7YM%3D%40AAJTSQACMDI%3D%23",
        "PHPSESSID": "ST-416847-puEAtdAuAw6gn4K3ZusD1536930304923-TZz9-cas",
    }

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Accept": "text/html, */*; q=0.01",
    }

def search_payload(strText="python",page=1,onlylendable=None):
    return {
        "strText":strText,
        "page":"2",
        "onlylendable":onlylendable,
    }

def test_search():
    payload = search_payload(strText="python")
    response = requests.get("http://127.0.0.1:8000/search",params = payload)
    print(response.text)

def test_booklst():
    response = requests.get("http://127.0.0.1:8000/booklst",params=cookies)
    print(response.json())
    return response.json()

def async_booklst():
    response = requests.get("http://127.0.0.1:8000/booklst",params=cookies)
    print(response.text)
    return response.text

def test_renew():
    data = test_booklst()
    bar_code = data["renew"]["1"][0]
    check = data["renew"]["1"][1]

    response = requests.get(url = 'http://wiscom.chd.edu.cn:8080/reader/captcha.php',headers=headers,cookies=cookies)

    with open("code.png","wb") as fn:
        fn.write(response.content)

    captcha = input("请输入验证码：")
    data = {
        'bar_code': bar_code,
        'captcha': captcha,
        'check': check,
        'time': int(time.time() * 1000),
        "iPlanetDirectoryPro":cookies["iPlanetDirectoryPro"],
        "PHPSESSID":cookies["PHPSESSID"],
    }
    response = requests.post("http://127.0.0.1:8000/booklst",data=data)
    print(response.text)

def async_renew():
    data = async_booklst()
    data = json.loads(data)
    bar_code = data["renew"]["1"][0]
    check = data["renew"]["1"][1]

    response = requests.get(url='http://wiscom.chd.edu.cn:8080/reader/captcha.php', headers=headers, cookies=cookies)

    with open("code.png", "wb") as fn:
        fn.write(response.content)

    captcha = input("请输入验证码：")
    data = {
        'bar_code': bar_code,
        'captcha': captcha,
        'check': check,
        'time': int(time.time() * 1000),
        "iPlanetDirectoryPro": cookies["iPlanetDirectoryPro"],
        "PHPSESSID": cookies["PHPSESSID"],
    }
    response = requests.post("http://127.0.0.1:8000/booklst", data=data)
    print(response.text)

if __name__ == '__main__':
    async_booklst()