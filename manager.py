#coding=utf8
'''
Created on 2016-2-25

@author: Administrator
'''
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from urls import Application

define("port", default=81, help="run on the given port", type=int)
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
