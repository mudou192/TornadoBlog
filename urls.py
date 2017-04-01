#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 
'''
import tornado.web
import os.path
from setting import UrlHandlers

class Application(tornado.web.Application):
    def __init__(self):
        handlers = UrlHandlers
        
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            #debug = True,
            #加密秘钥
            cookie_secret = "ADnCasdVhGoDebDWsw23XsDL",
            xsrf_cookies = True,
            #验证不通过后重定向的页面
            login_url = "/login.html",
            #禁止转意
            autoescape = None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)