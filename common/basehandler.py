#coding=utf8
'''
Created on 2017-1-12

@author: xuwei

@summary: 
'''
import urllib
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from setting import Admin

class BaseHandler(tornado.web.RequestHandler):
    
    def get_url_parts(self):
        current_url = self.request.uri.strip('/')
        current_url = urllib.unquote(current_url)
        partlist = current_url.split('/')
        return partlist
    
    def check_admin(self):
        if Admin == self.get_secure_cookie('username'):
            return True
        else:
            return False
    
    def get_current_user(self):
        return self.get_secure_cookie("username")
    
    @run_on_executor
    def _handle(self):
        self.do_something()
    
    def check_request_type(self,reqtype):
        if reqtype.upper() == self.request.method:
            return True
        else:
            return False
            
    def do_something(self):
        '''在实例中实现（可以在这个方法中判断请求类型是否正确）
        flag = self.check_request_type('post')
        if not flag:
            self.render('error.html')
            return
        pass
        '''
        pass


'''处理非认证服务基类'''
class NoAuthHandler(BaseHandler):
    
    executor = ThreadPoolExecutor(5)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield self._handle()
        self.finish()
    
    executor = ThreadPoolExecutor(5)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        yield self._handle()
        self.finish()
    
    

'''处理认证服务基类'''
class AuthHandler(BaseHandler):
    
    executor = ThreadPoolExecutor(5)
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield self._handle()
        self.finish()
    
    executor = ThreadPoolExecutor(5)
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        yield self._handle()
        self.finish()
    
