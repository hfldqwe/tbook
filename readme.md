

msg={0:"查询结果为空"}

msg={1:"查询失败"}

"msg":{2:"请求失败"}

# 图书馆爬虫使用说明 #
地址：127.0.0.1
端口：8080(根据实际情况决定)

## 查询馆藏：##
地址：http://127.0.0.1:8080/search?strText=查询字符串&page=1&onlylendable=no
返回示例：
{
    "book_storm":{
        0:["语言","书名","编号","馆藏复本","可借复本","作者","出版社和时间"],
        1:[............],
        2:[............],
        .....
        },
    "cuurent_end_page":"2 / 4",#当前到末尾的页数
    "msg":True
    }
请求方法：GET
参数：
- strText：搜索的关键词
- page：页数，当前页和最后页在查询的时候会给出，所以调用的时候应该根据cuurent_end_page这个参数显示后续的页数，如果查询的参数超出了页数，返回的是最后一页
- onlylendable：是否只查询可借阅的书籍，默认为no，传递任意参数可以让它为yes(包括传递no，不过不建议这么做)

**异常情况**  
1.查询为空：  
- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": {"0": "查询结果为空"}}  
- 这种情况大多数为用户搜索关键词不存在，但是有少量情况由于图书馆网络问题加载为空，所以碰到这种情况建议重新加载一次，如果还为空则返回查询为空

2.请求失败：
- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": {"2": "请求失败"}}
- 由于图书馆网络请求等原因，造成无法访问的情况（毕竟学校的服务器经常崩掉）

3.查询失败
- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": msg={1:"查询失败"}}






## 查询个人借阅情况： ##
http://127.0.0.1:8000/booklst?username=xxxx&password=password
返回示例：
{'info':
    {
        'msg': True, 
        'info': 
            {
                '0': ['编号', '书名/作者', '借阅日期', '到期时间', '续借量', '馆藏地', '附件'],
                '1': ['1472812', 'UNIX网络编程.套接口API / (美) W. Richard Stevens, Bill Fenner, Andrew M. Rudoff著', '2018-09-03', '2018-11-02', '0', '逸夫馆信息与控制库', '无'], 
                '2': 。。。。。。。。。。。。。。}}, 
'renew': {'1': ['这是续借使用的参数bar_code', '这是续借使用的参数check'], '2': ['2189351', 'A0DD22D9'], '3': ['2578219', '7CD008B2'], '4': ['2624672', '1B344A47']}}
说明：返回了一个json数据，有两个信息info和renew，info里面有借阅的基本情况，不做过多说明，renew里面的参数是续借时需要使用的
参数：
- iPlanetDirectoryPro：cookies中需要的参数，cookies中只有两个参数是必要的，其他的可以不用传过来
- PHPSESSID：另一个cookies里面的参数

**异常情况：**  
返回数据为空：正常的返回值，只是没有数据
- 这种情况有部分可能是由于图书馆网络请求的问题，也算一个之后更改的地方吧
网络请求错误：{"msg":{2:"请求失败"}}
- 这种情况一般由于图书馆网络问题造成
查询出现错误：{"msg":{1:"查询失败"}}
- 这种情况一般不会出现




## 续借： ##
http://127.0.0.1:8000/booklst

{
"bar_code":"xxx",  
"check":"xxx",  
"captcha":"xxx",  
"username":"xxx",  
"username":"xxx"，  
}

请求方法：POST  

说明：首先需要携带cookies访问网址（前端直接使用ajax加载这个图片就可以）：http://wiscom.chd.edu.cn:8080/reader/captcha.php获取用户输入的验证码captcha

参数：
- bar_code：包含在查询个人借阅的返回信息中  
- check：包含在查询个人借阅的返回信息中  
- captcha：这个由用户填写  
- captcha$iPlanetDirectoryPro：一个cookies参数，同上  
- PHPSESSID：一个cookies参数，同上  

返回值：  

<font color=red>不到续借时间，不得续借！</font>

错误的验证码(wrong check code)

没有测试成功的情况，所以不是很清楚


