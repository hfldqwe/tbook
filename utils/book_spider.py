import requests
import re
from bs4 import BeautifulSoup as bs
import json
import time
from tornado.httpclient import AsyncHTTPClient

from urllib.parse import urlencode

from log import log


class Config():
    headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    book_url = 'http://ids.chd.edu.cn/authserver/login?service=http://wiscom.chd.edu.cn:8080/reader/hwthau.php'
    book_lst_url = 'http://wiscom.chd.edu.cn:8080/reader/book_lst.php'
    book_hist_url = "http://wiscom.chd.edu.cn:8080/reader/book_hist.php"
    search_url = 'http://wiscom.chd.edu.cn:8080/opac/openlink.php'

    renew_image_url = 'http://wiscom.chd.edu.cn:8080/reader/captcha.php'
    renew_url = 'http://wiscom.chd.edu.cn:8080/reader/ajax_renew.php'

    fine_pec_url = "http://wiscom.chd.edu.cn:8080/reader/fine_pec.php"  # 罚款

def search_payload(strText, page, onlylendable=None):
    '''
    为search这个方法构造参数,提供给异步客户端使用
    '''
    url = Config.search_url
    payload = {
        'strSearchType': 'title',
        'match_flag': 'forward',
        'historyCount': '1',
        'strText': '%s' % (strText,),
        'doctype': 'ALL',
        'with_ebook': 'on',
        'displaypg': '20',
        'showmode': 'list',
        'sort': 'CATA_DATE',
        'orderby': 'desc',
        'location': 'ALL',
        'page': str(page),
    }
    if onlylendable:
        payload["onlylendable"] = "yes"
    params = urlencode(payload)
    return url+"?"+params

def search_data(book_storm_dict,current_end_page,msg=True):
    '''
    提供给异步客户端使用
    合成最终的数据
    :param book_storm_dict:
    :param current_end_page:
    :param msg:
    :return:
    '''
    search_book_data = {
        "book_storm": book_storm_dict,
        "cuurent_end_page": current_end_page,
        "msg": msg,
    }
    search_book_data = json.dumps(search_book_data, ensure_ascii=False)
    return search_book_data

def search_dispose(response):
    '''
    提供给异步客户端使用
    处理爬取下来的数据，提取相应的信息
    :param response: 原始响应,应该已经转化成字符串格式的
    :return: 一个json数据，正如search方法中写的那样
    '''
    book_storm_dict = {0: ["语言", "书名", "编号", "馆藏复本", "可借复本", "作者", "出版社和时间"]}

    result = bs(response, 'lxml')
    book_storm = result.find_all("li", class_='book_list_info')
    current_end_page = result.find_all("span", class_='pagination')[0].b.text

    for index in range(len(book_storm)):
        info = []
        for p_string in book_storm[index].stripped_strings:
            info.append(p_string)
        language = info[0]
        title = info[1]
        serial_number = info[2]
        amount = info[3]
        usable_amount = info[4]
        author = info[5]
        press_year = info[6].strip()
        book_storm_dict[index + 1] = [language, title, serial_number, amount, usable_amount, author, press_year]
    return search_data(book_storm_dict,current_end_page)

def booklst_dispose(response):
    '''
    用来处理查询个人借阅书籍之后的返回值，提供给异步代码使用
    :param cookies:认证的cookies
        :return:一个元祖，包含两个json数据....如：
            {
            "msg":True,
            "info":{
                0: ["编号", "书名/作者", "借阅日期", "到期时间", "续借量", "馆藏地", "附件"]，
                1:[......],
                2:[........]},
                }
            {"1": ["1472812", "FB034555"], "2": ["2189351", "A0DD22D9"], "3": ["2578219", "7CD008B2"], "4": ["2624672", "1B344A47"]}
    '''
    info_dict = {0: ["编号", "书名/作者", "借阅日期", "到期时间", "续借量", "馆藏地", "附件"]}
    renew_book = {}  # 存储续借信息的字典
    result = bs(response, "lxml")
    book_lst = result.find_all("td", class_="whitetext")

    for i in range(int(len(book_lst) / 8)):  # 将抓到的标签进行分组
        info_dict[i + 1] = book_lst[i * 8:(i + 1) * 8]

    for index, value in info_dict.items():
        if index == 0:
            continue
        #   ["编号", "书名", "借阅时间", "归还时间", "续借量", "馆藏地", "附件"]
        value[0] = value[0].text
        value[1] = value[1].text
        value[2] = value[2].text.strip()
        value[3] = value[3].font.text.strip()
        value[4] = value[4].text
        value[5] = value[5].text
        value[6] = value[6].text
        renew_info = value[7].div.input["onclick"]  # 用于续借的参数
        renew_book[index] = re.compile("getInLib\('(.*?)','(.*?)'").findall(renew_info)[0]
        value.remove(value[7])  # 第七个值不需要返回给前端，所以去掉
    info_dict = {
        "msg": True,
        "info": info_dict,
    }
    data = {
        "info": info_dict,
        "renew": renew_book
    }
    return data

def renew_parmas(bar_code, captcha, check):
    '''
    构造续借的url
    :param bar_code:
    :param captcha:
    :param check:
    :return:
    '''
    url = Config.renew_url
    payload = {
        'bar_code': bar_code,
        'check': check,
        'captcha': captcha,
        'time': str(int(time.time() * 1000)),
    }
    url = url+"?"+urlencode(payload)
    return url


if __name__ == '__main__':
    print(search_payload("python","2"))