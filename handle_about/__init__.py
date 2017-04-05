#coding=utf8
'''
Created on 2017-1-23

@author: xuwei

@summary: 浏览页面
'''
import time,os,re,json
from common.traceback_error import get_err_msg
from common.config import Config
from mysql_contate import MySQLHandler as MysqlHandler
from common.basehandler import NoAuthHandler

class WatchAboutHandler(NoAuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            Message = MysqlHandler.get_about()
            self.render('about.html',Message = Message,IsAdmin = is_admin)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

