#coding=utf-8
'''
Created on 2015-5-28
@author: Administrator
如果sql执行间隔时间过长，导致连接断开，可以调用再次调用 init_sql()，需要根据返回状态选择相应的错误处理
'''
from common import logger as log
from common.traceback_error import get_err_msg
import MySQLdb

class MySQLAccess:
    def __init__(self,host,user,pwd,db,charset="utf8"):
        self.conn = None
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset
        self.init_sql()
        
    def init_sql(self):
        tryMax = 100
        num = 0
        while num < tryMax:
            num += 1
            try:
                self.conn = MySQLdb.connect(host = self.host, user = self.user, passwd = self.pwd, db = self.db, charset=self.charset)
                break
            except:
                errmsg = get_err_msg()
                log.root.debug(errmsg)
    
    def select(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            self.conn.commit()
            return data
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except Exception,error:
            cursor.close()
            raise Exception(str(error) +"\n"+str(sql))
    
    def execute(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            return True
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception,error:
            self.conn.rollback()
            raise Exception(str(error) +"\n"+str(sql))
    
    def execute_many(self,sql,data):
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql,data)
            self.conn.commit()
            return True
        except MySQLdb.OperationalError:
            self.init_sql()
            cursor.executemany(sql,data)
            self.conn.commit()
            return True
        except Exception,error:
            self.conn.rollback()
            raise Exception(str(error) +"\n"+str(sql))
        
    def __del__(self):
        if self.conn:
            self.conn.close()
            
if __name__ == "__main__":
    A = MySQLAccess('192.168.1.230','webuser','test','quanzhi')
    sql = "select id from App_UserCode_Bind"        
    data,flag = A.select(sql) 
    if not flag:
        print "error"   
    print data

