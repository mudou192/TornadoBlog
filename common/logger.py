#coding=utf-8
'''
Created on 2015-6-3

@author: xhw
'''
import os
import logging.config
#读取配置文件
path = os.path.dirname(__file__)
conf_file = os.path.join(path,"logging.conf")
logging.config.fileConfig(conf_file)

#返回相应的日志对象
root = logging.getLogger("root")
Index_Logger = logging.getLogger("Index")
BlogFinalData_Logger = logging.getLogger("Blog")
Login_Logger = logging.getLogger("Login")
More_Logger = logging.getLogger("More")
Static_Logger = logging.getLogger("Static")
Mysql_logger = logging.getLogger("Mysql")


if __name__ == '__main__':
    #root.error("This is test!!!")
    pass
