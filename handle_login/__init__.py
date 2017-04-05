#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 登录
'''
import time,os,re,json
from common.traceback_error import get_err_msg
from common.basehandler import NoAuthHandler
from common.basehandler import AuthHandler
from mysql_contate import MySQLHandler as MysqlHandler

class LoginHandler(NoAuthHandler):
        
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            self.render('login.html',username = "", password = "",message = "",IsAdmin = is_admin)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class CheckUserHander(NoAuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('post')
            if not flag:
                raise Exception('Request type error')
            username = self.get_argument('username')
            username = username.strip()
            password = self.get_argument('password')
            password = password.strip()
            flag = MysqlHandler.checkuser( username, password)
            if flag:
                self.set_secure_cookie("username", self.get_argument("username"))
                self.redirect('/')
            else:
                self.render("login.html",username = username, password = "",message = u"用户名或密码错误",IsAdmin = False)  
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class SignOutHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            if not self.check_admin():
                raise Exception('No permission error')
            self.clear_cookie("username")
            self.redirect('/')
            #self.render("login.html",username = '', password = "",message = u"",IsAdmin = False)  
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
