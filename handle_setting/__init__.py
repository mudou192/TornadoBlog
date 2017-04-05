#coding=utf8
'''
Created on 2017-1-22

@author: xuwei

@summary: 设置页面
'''
import time,os,re,json
from common.traceback_error import get_err_msg
from common.config import Config
from mysql_contate import MySQLHandler as MysqlHandler
from common.basehandler import AuthHandler

class SettingHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            GroupInfos = MysqlHandler.select_group_info(is_admin)
            Message = MysqlHandler.get_about()
            self.render('setting.html',GroupInfos = GroupInfos,AboutInfo = Message,IsAdmin = is_admin)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

class AddGroupHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            groupname = self.get_argument('groupname')
            MysqlHandler.add_group(groupname)
            self.redirect('/setting')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

class EditGroupHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            groupid = self.get_argument('groupid')
            NewGroupName = self.get_argument('groupname')
            MysqlHandler.change_group(groupid, NewGroupName)
            self.write('true')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

class DelGroupHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            groupid = self.get_argument('groupid')
            MysqlHandler.delete_group(groupid)
            self.write('true')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

class EditAboutMeHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('post')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            content = self.get_argument('message')
            MysqlHandler.upload_about(content)
            self.redirect('/setting')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
