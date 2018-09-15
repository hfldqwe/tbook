import logging
from functools import lru_cache
import os
import glob

@lru_cache(maxsize=1)
def new_log():
    '''
    使用日志
    :return:
    '''
    pid = str(os.getpid())

    log = logging.getLogger("spider")
    logFileHandler = logging.FileHandler(filename="spider-{}.log".format(pid))
    format = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s',datefmt='%Y/%m/%d %I:%M:%S')
    log.addHandler(logFileHandler)
    logFileHandler.setFormatter(format)

    # 下面检索spider日志文件，判断日志数量
    log_list = glob.glob("*.log")
    log_list.remove("previous.log")
    log_list_sorted = sorted(log_list,key=os.path.getctime)

    if len(log_list_sorted) >3:
        with open("previous.log","a+") as previous_log:
            for file in log_list_sorted[0:-3]:
                with open(file,"r") as fn:              # 将这个日志文件中的内容写入到previous.log文件中
                    content = fn.read()
                    previous_log.write(content)
                os.remove(file)                         # 删除这个日志文件
    return log

log = new_log() # 实例化一个配置好的日志对象