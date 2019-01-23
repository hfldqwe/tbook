msg={0:"查询结果为空"}

msg={1:"查询失败"}

"msg":{2:"请求失败"}

# 图书馆爬虫使用说明 #
地址：127.0.0.1
端口：8080(根据实际情况决定)

## 查询馆藏：##
地址：http://127.0.0.1:8080/search?strText=查询字符串&page=1&onlylendable=no

返回示例：

[语言，书名，编号，馆藏复本，可借复本，作者，出版社]

```json
{
  "msg": true, 
  "book": {
      "0": {"language": "中文图书", "name": "Python物理建模初学者指南", "code": "TP311.56/C609", "collection_number": "3", "lendable_number": "2", "author": "(美)JesseM.Kinder,(美)PhilipNelson著", "publish_hose": "人民邮电出版社2017"}, 
      "1": {"language": "中文图书", "name": "数据结构:Python语言描述", "code": "TP311.56/C608", "collection_number": "5", "lendable_number": "1", "author": "张光河主编", "publish_hose": "人民邮电出版社2018"}, "2": {"language": "中文图书", "name": "Python与有限元:基于Python编程的有限元分析及应用扩展", "code": "O241.82-39/C103", "collection_number": "5", "lendable_number": "3", "author": "裴尧尧...[等]著", "publish_hose": "中国水利水电出版社2017"}, "3": {"language": "中文图书", "name": "Python应用开发实战", "code": "TP311.56/C606", "collection_number": "5", "lendable_number": "2", "author": "(美)尼纳德·萨斯叶著", "publish_hose": "人民邮电出版社2018"}, "4": {"language": "中文图书", "name": "Python设计模式", "code": "TP311.56/C604", "collection_number": "5", "lendable_number": "4", "author": "(印)ChetanGiridhar著", "publish_hose": "人民邮电出版社2017"}, "5": {"language": "中文图书", "name": "Python数据分析基础", "code": "TP311.56/C605", "collection_number": "5", "lendable_number": "1", "author": "余本国编著", "publish_hose": "清华大学出版社2017"}, "6": {"language": "中文图书", "name": "Python数据可视化之matplotlib实践", "code": "TP311.56/C600", "collection_number": "5", "lendable_number": "2", "author": "刘大成著", "publish_hose": "电子工业出版社2018"}, "7": {"language": "中文图书", "name": "Python网络数据爬取及分析从入门到精通,分析篇", "code": "TP311.56/C581/2", "collection_number": "5", "lendable_number": "1", "author": "杨秀璋，颜娜编著", "publish_hose": "北京航空航天大学出版社2018"}, "8": {"language": "中文图书", "name": "Python核心编程", "code": "TP311.56/C470", "collection_number": "6", "lendable_number": "1", "author": "(美)WesleyChun著", "publish_hose": "人民邮电出版社2016"}, "9": {"language": "中文图书", "name": "Python深度学习实战:75个有关神经网络建模、强化学习与迁移学习的解决方案:over75practicalrecipeso", "code": "TP311.56/C580", "collection_number": "5", "lendable_number": "1", "author": "(荷)英德拉·丹·巴克著", "publish_hose": "机械工业出版社2018"}, "10": {"language": "中文图书", "name": "Python3爬虫、数据清洗与可视化实战", "code": "TP311.56/C589", "collection_number": "5", "lendable_number": "1", "author": "零一,韩要宾,黄园园著", "publish_hose": "电子工业出版社2018"}, "11": {"language": "中文图书", "name": "Python程序设计基础", "code": "TP311.56/C579", "collection_number": "5", "lendable_number": "1", "author": "虞歌主编", "publish_hose": "中国铁道出版社2018"}, "12": {"language": "中文图书", "name": "Python编程基础", "code": "TP311.56/C582", "collection_number": "5", "lendable_number": "1", "author": "张健,张良均主编", "publish_hose": "人民邮电出版社2018"}, "13": {"language": "中文图书", "name": "Python数据分析入门:从数据获取到可视化", "code": "TP311.56/C592", "collection_number": "5", "lendable_number": "1", "author": "沈祥壮著", "publish_hose": "电子工业出版社2018"}, "14": {"language": "中文图书", "name": "Python微控制器编程从零开始:使用MicroPython", "code": "TP311.56/C587", "collection_number": "5", "lendable_number": "3", "author": "(美)唐纳德·诺里斯著", "publish_hose": "清华大学出版社2018"}, "15": {"language": "中文图书", "name": "Python网络编程:Linux", "code": "TP316.89/C291", "collection_number": "5", "lendable_number": "4", "author": "赵宏,包广斌,马栋林编著", "publish_hose": "清华大学出版社2018"}, "16": {"language": "中文图书", "name": "深入浅出Python机器学习", "code": "TP311.56/C596", "collection_number": "5", "lendable_number": "1", "author": "段小手著", "publish_hose": "清华大学出版社2018"}, "17": {"language": "中文图书", "name": "Python数据可视化编程实战", "code": "TP311.56/C447(2018)", "collection_number": "5", "lendable_number": "2", "author": "(爱尔兰)伊戈尔·米洛瓦诺维奇,(法)迪米特里·富雷斯,(意)朱塞佩·韦蒂格利著", "publish_hose": "人民邮电出版社2018"}, "18": {"language": "中文图书", "name": "Python网络数据爬取及分析从入门到精通,爬取篇", "code": "TP311.56/C581/1", "collection_number": "5", "lendable_number": "1", "author": "杨秀璋,颜娜编著", "publish_hose": "北京航空航天大学出版社2018"}, "19": {"language": "中文图书", "name": "Python机器学习基础教程", "code": "TP311.56/C597", "collection_number": "5", "lendable_number": "3", "author": "(德)AndreasC.Muller,(美)SarahGuido著", "publish_hose": "人民邮电出版社2018"}}, 
  "current_page": "1", 
  "end_page": "7"}
```

请求方法：GET
参数：
- strText：搜索的关键词
- page：页数，当前页和最后页在查询的时候会给出，所以调用的时候应该根据current_page,end_page这个参数进行判断，如果查询的参数超出了页数，返回的是最后一页
- onlylendable：是否只查询可借阅的书籍，默认为no，传递任意参数可以让它为yes(包括传递no，不过不建议这么做)

**异常情况**  
~~1.查询为空(**此种情况几乎不会出现了，由于后端解析库的修改，所以不能够根据msg字段判断是否为空了**)：~~  
~~- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": {"0": "查询结果为空"}}~~   
~~- 这种情况大多数为用户搜索关键词不存在，但是有少量情况由于图书馆网络问题加载为空，所以碰到这种情况建议重新加载一次，如果还为空则返回查询为空~~

2.请求失败：  
- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": {"2": "请求失败"}}  
- 由于图书馆网络请求等原因，造成无法访问的情况（毕竟学校的服务器经常崩掉）  

3.查询失败
- 返回值：{"book_storm": null, "cuurent_end_page": null, "msg": msg={1:"查询失败"}}


## 查询个人借阅情况： ##
http://127.0.0.1:8000/booklst?username=xxxx&password=password

["bar_code","book","borrow_date","return_date","renewal","collection","annex","check"]

对应含义：

['条码号', '题名/责任者', '借阅日期', '应还日期', '续借量', '馆藏地', '附件', 'check']

返回示例：

'
{
    "msg": true, 
    "booklst": 
        {
        "0":{"bar_code": "2152224", "book": "NumPy攻略:Python科学计算与数据分析", "borrow_date": "2018-12-22", "return_date": "2019-03-04", "renewal": "0", "collection": "逸夫馆信息与控制库", "annex": "无", "check": "68BF2238"}, 
        "1": {"bar_code": "2351606", "book": "GitHub入门", "borrow_date": "2018-12-22", "return_date": "2019-03-04", "renewal": "0", "collection": "逸夫馆信息与控制库", "annex": "无", "check": "DE41D48B"}, "2": {"bar_code": "2444567", "book": "Python性能分析与优化", "borrow_date": "2018-12-22", "return_date": "2019-03-04", "renewal": "0", "collection": "逸夫馆信息与控制库", "annex": "无", "check": "6622C353"}, "3": {"bar_code": "2624730", "book": "Python爬虫开发与项目实战", "borrow_date": "2018-12-22", "return_date": "2019-03-04", "renewal": "0", "collection": "逸夫馆信息与控制库", "annex": "无", "check": "19B5CD10"}}}'

说明：返回了一个json数据，有两个信息info和renew，info里面有借阅的基本情况，不做过多说明，renew里面的参数是续借时需要使用的

请求方法：GET

参数：
- username：账号
- password：密码

**异常情况：**  
返回数据为空：正常的返回值，只是没有数据
- 这种情况有部分可能是由于图书馆网络请求的问题，也算一个之后更改的地方吧（目前测试这种情况几乎不存在）

网络请求错误：{"msg":{2:"请求失败"}}
- 这种情况一般由于图书馆网络问题造成

查询出现错误：{"msg":{1:"查询失败"}}
- 这种情况一般不会出现

## 历史借阅 ##
http://127.0.0.1:8000/history?username=xxxx&password=password

返回示例：

["条码号", "题名", "责任者", "借阅日期", "归还日期", "馆藏地"]

```json
{
  "msg": true, 
 "history": {
        "0": {"bar_code": "2152224", "name": "NumPy攻略:Python科学计算与数据分析", "author": "(印尼) Ivan Idris著", "borrow_date": "2018-11-19", "return_date": "2018-12-22", "collection": "逸夫馆信息与控制库"}, 
        "1": {"bar_code": "2351606", "name": "GitHub入门", "author": "Peter Bell, Brent Beer著", "borrow_date": "2018-11-19", "return_date": "2018-12-22", "collection": "逸夫馆信息与控制库"}, "2": {"bar_code": "2444567", "name": "Python性能分析与优化", "author": "(乌拉圭) Fernando Doglio著", "borrow_date": "2018-11-19", "return_date": "2018-12-22", "collection": "逸夫馆信息与控制库"}, "3": {"bar_code": "2624730", "name": "Python爬虫开发与项目实战", "author": "范传辉编著", "borrow_date": "2018-11-19", "return_date": "2018-12-22", "collection": "逸夫馆信息与控制库"}, "4": {"bar_code": "2444556", "name": "Python数据分析实战", "author": "(意) Fabio Nelli著", "borrow_date": "2018-10-17", "return_date": "2018-10-24", "collection": "逸夫馆信息与控制库"}, "5": {"bar_code": "2432719", "name": "精通Python设计模式", "author": "(荷) Sakis Kasampalis著", "borrow_date": "2018-10-17", "return_date": "2018-11-19", "collection": "逸夫馆信息与控制库"}, "6": {"bar_code": "1472812", "name": "UNIX网络编程,套接口API", "author": "(美) W. Richard Stevens, Bill Fenner, Andrew M. Rudoff著", "borrow_date": "2018-09-03", "return_date": "2018-10-24", "collection": "逸夫馆信息与控制库"}, "7": {"bar_code": "2189351", "name": "编写高质量代码:改善Python程序的91个建议:91 suggestions to improve your Python program", "author": "张颖, 赖勇浩著", "borrow_date": "2018-09-03", "return_date": "2018-10-24", "collection": "逸夫馆信息与控制库"}, "8": {"bar_code": "2578219", "name": "Python数据分析实战", "author": "(印)伊凡·伊德里斯(Ivan Idris)著", "borrow_date": "2018-09-03", "return_date": "2018-11-19", "collection": "逸夫馆信息与控制库"}, "9": {"bar_code": "2624672", "name": "Python机器学习", "author": "(美) 塞巴斯蒂安·拉施卡著", "borrow_date": "2018-09-03", "return_date": "2018-10-24", "collection": "逸夫馆信息与控制库"}, "10": {"bar_code": "2573612", "name": "Python程序设计与算法基础教程", "author": "江红，余青松主编", "borrow_date": "2018-07-01", "return_date": "2018-09-03", "collection": "逸夫馆信息与控制库"}, "11": {"bar_code": "2393773", "name": "Python数据可视化编程实战", "author": "(爱尔兰) Igor Milovanovic著", "borrow_date": "2018-07-01", "return_date": "2018-09-03", "collection": "逸夫馆信息与控制库"}, "12": {"bar_code": "2229988", "name": "HTML 5和CSS 3编程从基础到应用", "author": "祝红涛, 赵喜来编著", "borrow_date": "2018-05-21", "return_date": "2018-06-30", "collection": "逸夫馆信息与控制库"}, "13": {"bar_code": "2606263", "name": "Selenium自动化测试之道", "author": "Ping++测试团队编著", "borrow_date": "2018-05-21", "return_date": "2018-07-13", "collection": "逸夫馆信息与控制库"}, "14": {"bar_code": "2529015", "name": "Django开发宝典", "author": "王友钊, 黄静编著", "borrow_date": "2018-05-21", "return_date": "2018-06-30", "collection": "逸夫馆信息与控制库"}, "15": {"bar_code": "2189351", "name": "编写高质量代码:改善Python程序的91个建议:91 suggestions to improve your Python program", "author": "张颖, 赖勇浩著", "borrow_date": "2018-05-21", "return_date": "2018-07-13", "collection": "逸夫馆信息与控制库"}, "16": {"bar_code": "2391256", "name": "JavaScript+jQuery程序开发实用教程", "author": "李雨亭, 吕婕, 王泽璘编著", "borrow_date": "2018-05-21", "return_date": "2018-06-30", "collection": "逸夫馆信息与控制库"}, "17": {"bar_code": "2216608", "name": "Python计算机视觉编程", "author": "(美) Jan Erik Solem著", "borrow_date": "2018-05-21", "return_date": "2018-07-13", "collection": "逸夫馆信息与控制库"}, "18": {"bar_code": "2152224", "name": "NumPy攻略:Python科学计算与数据分析", "author": "(印尼) Ivan Idris著", "borrow_date": "2018-03-28", "return_date": "2018-05-20", "collection": "逸夫馆信息与控制库"}, "19": {"bar_code": "2444557", "name": "Python数据分析实战", "author": "(意) Fabio Nelli著", "borrow_date": "2018-03-28", "return_date": "2018-05-20", "collection": "逸夫馆信息与控制库"}}}
```
说明：返回了一个json数据，有两个信息info和renew，info里面有借阅的基本情况，不做过多说明，renew里面的参数是续借时需要使用的

请求方法：GET

参数：
- username：账号
- password：密码

**异常情况**

{"msg": {2: "请求失败"}}


## 违章缴款 ##
http://127.0.0.1:8000/fine?username=xxxx&password=password

返回示例：

["条码号", "索书号", "题名", "责任者", "借阅日", "应还日", "馆藏地", "应缴", "实缴", "状态"]

```json
{
"msg": true, 
"fine": {
      "0": {"bar_code": "2393773", "code": "TP311.56/C447", "name": "Python数据可视化编程实战", "author": "(爱尔兰) Igor Milovanovic著", "borrow_date": "2018-03-11", "return_date": "2018-05-10", "collection": "逸夫馆信息与控制库", "pay": "0.50", "real_pay": "0.50", "status": "处理完毕"}, 
      "1": {"bar_code": "2432718", "code": "TP311.56/C456", "name": "精通Python设计模式", "author": "(荷) Sakis Kasampalis著", "borrow_date": "2018-03-11", "return_date": "2018-05-10", "collection": "逸夫馆信息与控制库", "pay": "0.50", "real_pay": "0.50", "status": "处理完毕"}, "2": {"bar_code": "2503752", "code": "TP311.56/C493", "name": "Python数据科学指南", "author": "(印度) Gopi Subramanian著", "borrow_date": "2018-03-11", "return_date": "2018-05-10", "collection": "逸夫馆信息与控制库", "pay": "0.50", "real_pay": "0.50", "status": "处理完毕"}, "3": {"bar_code": "2578219", "code": "TP311.56/C508", "name": "Python数据分析实战", "author": "(印)伊凡·伊德里斯(Ivan Idris)著", "borrow_date": "2018-09-03", "return_date": "2018-11-02", "collection": "逸夫馆信息与控制库", "pay": "0.85", "real_pay": "0.80", "status": "处理完毕"}}}
```
说明：返回了一个json数据，有两个信息info和renew，info里面有借阅的基本情况，不做过多说明，renew里面的参数是续借时需要使用的

请求方法：GET

参数：
- username：账号
- password：密码

**异常情况**

{"msg": {2: "请求失败"}}

## 续借： ##
http://127.0.0.1:8000/renew?username=xxx&password=xxx&bar_code=xxx&check=xxx

请求方法：GET  

说明：首先需要携带cookies访问网址（前端直接使用ajax加载这个图片就可以）：http://wiscom.chd.edu.cn:8080/reader/captcha.php获取用户输入的验证码captcha

参数：
- bar_code：包含在查询个人借阅的返回信息中  
- check：包含在查询个人借阅的返回信息中  
- ~~captcha：这个由用户填写(已废弃，变为自动打码)~~  
- username：username 
- password：password

返回值：  

<font color=red>不到续借时间，不得续借！</font>

错误的验证码(wrong check code)

没有测试成功的情况，所以不是很清楚


