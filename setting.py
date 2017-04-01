#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''获取本机IP，CKEdit上传的时候使用'''
import socket
hostIp = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

'''其他一些默认配置'''
BlogDataPath = r'/data/TornadoProject/DataPath/HtmlPath'
ImageDataPath = r'/data/TornadoProject/DataPath/ImagePath'
#BlogDataPath = r'E:\work_space\TornadoProjectNew\DataPath\HtmlPath'
#ImageDataPath = r'E:\work_space\TornadoProjectNew\DataPath\ImagePath'
ShowBlogNum = 20
ShowSaysNum = 20
Admin = 'zhilengnuanx@sina.com'

from handle_index import IndexHandler
from handle_about import WatchAboutHandler
from handle_blog import CreateBlogHandler,EditBlogHandler,SaveBlogHander,\
                        WatchBlogHandler,UploadBlogHander,DelBlogHandler
from handle_login import LoginHandler,CheckUserHander,SignOutHandler
from handle_static import UploadImageHander,ImagePathHandler
from handle_setting import SettingHandler,AddGroupHandler,EditGroupHandler,\
                        DelGroupHandler,EditAboutMeHandler
                        



UrlHandlers = [
            (r"/", IndexHandler),   #主页
            (r"/index/{0,1}.*", IndexHandler), #主页
            
            (r"/createblog", CreateBlogHandler), #新增页面
            (r"/saveblog",SaveBlogHander),  #保存操作
            (r"/blog/{0,1}.*",WatchBlogHandler),#查看博客内容
            (r"/editblog/{0,1}.*",EditBlogHandler),#修改博客
            (r"/uploadblog",UploadBlogHander),#保存修改博客内容
            (r"/delblog/{0,1}.*",DelBlogHandler),

            (r"/login",IndexHandler),  #直接登录会跳转到首页
            (r"/checkuser",CheckUserHander),    #登陆操作
            (r"/signout",SignOutHandler),#退出登录
            (r"/login/admin/xhw",LoginHandler),#防止别人登录 
            
            (r"/setting",SettingHandler),
            (r"/change_group",EditGroupHandler),
            (r"/remove_group",DelGroupHandler),
            (r"/add_group",AddGroupHandler),
            (r"/upload_aboutme",EditAboutMeHandler),
            
            (r"/about",WatchAboutHandler),
            (r"/actions/ckeditorUpload",UploadImageHander),
            (r"/ImagePath/.*",ImagePathHandler),
               ]
