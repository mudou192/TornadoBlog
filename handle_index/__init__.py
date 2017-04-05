#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 
'''
import os
import re
import math
import time
from common.traceback_error import get_err_msg
from setting import ShowBlogNum,BlogDataPath
from mysql_contate import MySQLHandler as MysqlHandler
from common.basehandler import NoAuthHandler


class IndexHandler(NoAuthHandler):
    '''主页面'''
    
    def get_blog_index(self,blogs_info):
        blogs_index = []
        if not blogs_info:
            return blogs_info
        for info in blogs_info:
            filename = info[1]
            filename = os.path.join(BlogDataPath,filename)
            with open(filename,'rb') as fp:
                content = fp.read()
            content = re.sub('''(?is)<[\s\S]*?>''','',content)
            content = re.sub('''(?is)&.{2,5};''','',content)
            try:
                content = content.decode('utf-8')
            except:pass
            content = content[:500] + " ... "
            blogs_index.append((info[0],content,info[3],info[4]))
        return blogs_index
    
    def get_url_values(self,urls):
        if len(urls) == 0:
            groupcode = None
            pagenum = 1
        elif len(urls) == 1:
            groupcode = urls[0]
            pagenum = 1
        elif len(urls) == 2:
            groupcode = urls[1]
            pagenum = 1
        elif len(urls) == 3:
            groupcode = urls[1]
            pagenum = urls[2]
        else:
            raise Exception('Request url error')
        return groupcode,pagenum
    
    def do_something(self):
        try:
            flag = self.check_request_type('get')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            urls = self.get_url_parts()
            #print urls
            groupcode,pagenum = self.get_url_values(urls)
            if not groupcode.isdigit():
                groupcode = None
            page = int(pagenum)
            '''获取笔记组信息'''
            group_infos = MysqlHandler.select_group_info(is_admin)
            skip = ShowBlogNum * (page - 1)
            '''`CategoryCode`,`Subject`,`FileName`,`AddTime`,`Id`,`Views`'''
            '''获取笔记索引列表信息'''
            blogs_info = MysqlHandler.select_blogs_info(groupcode, skip,is_admin)
            blogs_index = self.get_blog_index(blogs_info)
            allnum = MysqlHandler.get_group_num(groupcode)
            pagenum = int(math.ceil(float(allnum)/ShowBlogNum))
            self.render('index.html',GroupInfos = group_infos,BlogIndexs = blogs_index,IsAdmin = is_admin,
                        AllPageNum = pagenum,NowPage = page,GroupCode = groupcode)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
    
    
   
        

