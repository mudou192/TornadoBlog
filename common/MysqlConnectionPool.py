#coding=utf8
'''
Created on 2016-6-24

@author: xuwei

@summary: Mysql的连接池
'''
import MySQLdb,time,traceback
from Queue import Queue
from mysql_access import MySQLAccess

class MysqlConnectionPoolHandler(object):
    def __init__(self,host,user,pwd,db,ConnectNum = 3):
        self.ConnectNum = ConnectNum
        self.Pool = Queue(self.ConnectNum)
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = "utf8"
        self.init_connect_queue()
        
    def init_connect_queue(self):
        for i in range(self.ConnectNum):
            print "Init Mysql Connect:",i
            MysqlHandler = MySQLAccess(self.host,self.user,self.pwd,self.db,self.charset)
            self.Pool.put(MysqlHandler)
        
    def select(self,sql):
        try:
            MysqlHandler = self.Pool.get()
            data = MysqlHandler.select(sql)
            self.Pool.put(MysqlHandler)
            return data
        except Exception,error:
            self.Pool.put(MysqlHandler)
            raise Exception(str(error))
    
    def execute(self,sql):
        try:
            MysqlHandler = self.Pool.get()
            flag =  MysqlHandler.execute(sql)
            self.Pool.put(MysqlHandler)
            return flag
        except Exception,error:
            self.Pool.put(MysqlHandler)
            raise Exception(str(error))
        
    
    def execute_many(self,sql,data):
        try:
            MysqlHandler = self.Pool.get()
            flag = MysqlHandler.execute_many(sql,data)
            self.Pool.put(MysqlHandler)
            return flag
        except Exception,error:
            self.Pool.put(MysqlHandler)
            raise Exception(str(error))


