from spider.tornado_requests import requests
import asyncio

async def get():
    response = await requests.post("http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F",headers={"user-agent":"ss"},cookies={"aaa":123},data={"wd":"123"})
    print(response.request.headers)
    print(response.headers)
    print(response.text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get())