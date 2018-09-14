import logging
from functools import lru_cache
import os

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
    return log

log = new_log() # 实例化一个配置好的日志对象