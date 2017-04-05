#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 浏览页面
'''
import time,os,re,json
from common.traceback_error import get_err_msg
from common.config import Config
from setting import BlogDataPath
from setting import ImageDataPath
from mysql_contate import MySQLHandler as MysqlHandler
from common.basehandler import NoAuthHandler
from common.basehandler import AuthHandler

class CreateBlogHandler(AuthHandler):
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            group_infos = MysqlHandler.select_group_info(is_admin)
            datetime = time.strftime("%Y-%m-%d %H:%M:%S")
            self.render('createBlog.html',datetime = datetime,Check = '0',Privacy = 0,Subject = '',Content = '',PostUrl = '/saveblog',
                        GroupInfos = group_infos,IsAdmin = is_admin)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class EditBlogHandler(AuthHandler):
    
    def get_url_values(self,urls):
        if len(urls) == 2:
            blogId = urls[1]
        else:
            raise Exception('Request url error')
        return blogId
    
    def get_file_content(self,FileName):
        filename = os.path.join(BlogDataPath,FileName)
        with open(filename,'rb') as fp:
            content = fp.read()
        return content
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            urls = self.get_url_parts()
            BlogId = self.get_url_values(urls)
            info = MysqlHandler.select_blog_info(BlogId,is_admin)
            group_infos = MysqlHandler.select_group_info(is_admin)
            GroupCode = info[0]
            Subject = info[1]
            FileName = info[2]
            datetime = info[3]
            Privacy = info[5]
            if Privacy == 0:
                Privacy = False
            PostUrl = '/uploadblog?blogId=%s&filename=%s'%(BlogId,FileName)
            Content = self.get_file_content(FileName)
            self.render('createBlog.html',datetime = datetime,Check = GroupCode,Privacy = Privacy,Subject = Subject,Content = Content,
                        PostUrl = PostUrl,GroupInfos = group_infos,IsAdmin = is_admin)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')

class SaveBlogHander(AuthHandler):
     
    def save_file(self,message):
        filename = os.path.join(BlogDataPath,time.strftime("%Y%m%d%H%M%S") + ".html")
        with open(filename,'wb') as fp:
            fp.write(message)
        return os.path.split(filename)[1]
     
    def do_something(self):
        try:
            flag = self.check_request_type('post')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            username = self.get_current_user()
            groupcode = self.get_argument('category')
            subject = self.get_argument('subject')
            message = self.get_argument('message')
            privacy = self.get_argument('privacy')
            FileName = self.save_file(message)
            Addtime = time.strftime("%Y-%m-%d %H:%M:%S")
            MysqlHandler.insertdata(subject, username, Addtime, FileName, groupcode, privacy)
            self.redirect('/')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class UploadBlogHander(AuthHandler):
     
    def save_file(self,message,filename):
        filename = os.path.join(BlogDataPath,filename)
        with open(filename,'wb') as fp:
            fp.write(message)
     
    def do_something(self):
        try:
            flag = self.check_request_type('post')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            blogId = self.get_argument('blogId')
            filename = self.get_argument('filename')
            groupcode = self.get_argument('category')
            subject = self.get_argument('subject')
            message = self.get_argument('message')
            privacy = self.get_argument('privacy')
            self.save_file(message,filename)
            UpdateTime = time.strftime("%Y-%m-%d %H:%M:%S")
            MysqlHandler.updatablog(subject,UpdateTime,groupcode,blogId,privacy)
            self.redirect('/')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class WatchBlogHandler(NoAuthHandler):
    
    def get_url_values(self,urls):
        if len(urls) == 2:
            blogId = urls[1]
        else:
            raise Exception('Request url error')
        return blogId
    
    def get_file_content(self,FileName):
        filename = os.path.join(BlogDataPath,FileName)
        with open(filename,'rb') as fp:
            content = fp.read()
        return content
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            urls = self.get_url_parts()
            blogId = self.get_url_values(urls)
            info = MysqlHandler.select_blog_info(blogId,is_admin)
            if info:
                GroupCode = info[0]
                Subject = info[1]
                FileName = info[2]
                datetime = info[3]
                Views = info[4]
                Privacy = info[5]
            else:
                self.redirect('/')
                return
            group_infos = MysqlHandler.select_group_info(is_admin)
            lastpagenum,lasttitle = MysqlHandler.get_last_next_blog_info(blogId,GroupCode,IsLast=True)
            nextpagenum,nexttitle = MysqlHandler.get_last_next_blog_info(blogId,GroupCode,IsLast=False)
            blogdata = self.get_file_content(FileName)
            blogInfo = [Subject,datetime,blogdata,Views]
            self.render('blog.html', BlogInfo = blogInfo,GroupInfos = group_infos,BlogId = blogId,IsAdmin = is_admin,
                            lastpagenum=lastpagenum,lasttitle=lasttitle,nextpagenum=nextpagenum,nexttitle=nexttitle,Privacy = Privacy)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
    
class DelBlogHandler(AuthHandler):
    
    def get_url_values(self,urls):
        if len(urls) == 2:
            blogId = urls[1]
        else:
            raise Exception('Request url error')
        return blogId
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            urls = self.get_url_parts()
            BlogId = self.get_url_values(urls)
            MysqlHandler.del_blog(BlogId)
            self.redirect('/')
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
