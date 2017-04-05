#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: mysql 连接
'''
import copy
import MySQLdb
from common.logger import root
from common.traceback_error import get_err_msg
from common.MysqlConnectionPool import MysqlConnectionPoolHandler as MySQLAccess
from common.config import Config

class MysqlHandler(object):
    def __init__(self):
        self.config = Config()
        self.host = self.config.get('mysqlconf','MySqlhost')
        self.user = self.config.get('mysqlconf','MySqluser')
        self.password = self.config.get('mysqlconf','MySqlpwd')
        self.dbname = self.config.get('mysqlconf','MySqldb')
        self.initMysql()
        
    def initMysql(self):
        try:
            self.MySQLAccess = MySQLAccess(self.host,self.user,self.password,self.dbname)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        
    def checkuser(self,UserName,PassWord):
        '''
        @summary: 和数据库中的用户信息进行匹配
        '''
        try:
            UserName = MySQLdb.escape_string(UserName)
            PassWord = MySQLdb.escape_string(PassWord)
            sql = '''SELECT `UserName`,`PassWord` FROM UserInfo WHERE `UserName` = '%s' AND `PassWord` = '%s' '''%(UserName,PassWord)
            data = self.MySQLAccess.select(sql)
            if data and UserName == data[0][0] and PassWord == data[0][1]:
                return True
            else:
                return False
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return False
            
    def select_blogs_info(self,GroupCode = None,Skip = 0,IsAdmin = False):
        '''
        @summary: 查询日志列表
        '''
        data_list = []
        try:
            Skip = MySQLdb.escape_string(str(Skip))
            if GroupCode:
                GroupCode = MySQLdb.escape_string(str(GroupCode))
                if IsAdmin:
                    sql = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Id`,`Views` FROM `BlogData` 
                    WHERE GroupCode = %s AND IsDelete = 0 ORDER BY `AddTime` ASC LIMIT %s,20;'''%(GroupCode,Skip)
                else:
                    sql = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Id`,`Views` FROM `BlogData` 
                    WHERE GroupCode = %s AND IsDelete = 0 AND Privacy = 0 ORDER BY `AddTime` ASC LIMIT %s,20;'''%(GroupCode,Skip)
            else:
                if IsAdmin:
                    sql = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Id`,`Views` FROM `BlogData` 
                    WHERE IsDelete = 0 ORDER BY `AddTime` DESC LIMIT %s,20;'''%(Skip)
                else:
                    sql = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Id`,`Views` FROM `BlogData` 
                    WHERE IsDelete = 0 AND Privacy = 0 ORDER BY `AddTime` DESC LIMIT %s,20;'''%(Skip)
            data = self.MySQLAccess.select(sql)
            for d in data:
                ret_data = (d[1],d[2],d[3],d[4],d[5])
                data_list.append(copy.deepcopy(ret_data))
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return data_list
    
    def select_group_info(self,is_admin = False):
        '''
        @summary: 查询所有博客的名称，编码，条目
        '''
        datatuple = ()
        try:
            if is_admin:
                sql = '''SELECT `GroupName`,`GroupCode`,`Count` FROM `GroupInfo` WHERE IsDelete = 0;'''
            else:
                sql = '''SELECT `GroupName`,`GroupCode`,`Count` FROM `GroupInfo` WHERE Privacy = 0 AND IsDelete = 0;'''
            datatuple = self.MySQLAccess.select(sql)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return datatuple
    
    def select_blog_info(self,BlogId,IsAdmin = None):
        '''
        @summary: 查询当前文件的信息
        '''
        datatuple = ()
        try:
            BlogId = MySQLdb.escape_string(BlogId)
            if IsAdmin:
                sql1 = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Views`,`Privacy` FROM `BlogData` WHERE Id = %s AND IsDelete = 0;'''%BlogId
            else:
                sql1 = '''SELECT `GroupCode`,`Subject`,`FileName`,`AddTime`,`Views`,`Privacy` FROM `BlogData` WHERE Id = %s AND IsDelete = 0 AND Privacy = 0;'''%BlogId
            sql2 = '''UPDATE `BlogData` SET Views = Views + 1 WHERE `Id` = %s'''%BlogId
            self.MySQLAccess.execute(sql2)
            data = self.MySQLAccess.select(sql1)
            if data:
                datatuple = data[0]
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return datatuple
    
    def get_last_next_blog_info(self,FileId,GroupCode,IsLast = False):
        '''
        @summary: 获取上一页下一页Id和名称
        '''
        datatuple = (None,None)
        try:
            FileId = MySQLdb.escape_string(FileId)
            GroupCode = MySQLdb.escape_string(str(GroupCode))
            if IsLast:
                sql = '''SELECT `Id`,`Subject` FROM `BlogData` WHERE Id < %s AND GroupCode = %s ORDER BY `Id` Desc limit 1;'''%(FileId,GroupCode)
            else:
                sql = '''SELECT `Id`,`Subject` FROM `BlogData` WHERE Id > %s AND GroupCode = %s ORDER BY `Id` Asc limit 1;;'''%(FileId,GroupCode)
            data = self.MySQLAccess.select(sql)
            if data:
                datatuple = data[0]
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return datatuple
        
    def add_group(self,GroupName):
        GroupName = MySQLdb.escape_string(GroupName)
        sql1 = '''SELECT MAX(Id) FROM GroupInfo WHERE Id < 100;'''
        try:
            data = self.MySQLAccess.select(sql1)
            maxId = data[0][0] + 1
            sql2 = '''INSERT INTO GroupInfo (GroupName,GroupCode) VALUES ('%s',%s);'''%(GroupName,str(maxId))
            print sql2
            self.MySQLAccess.execute(sql2)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        
    def change_group(self,GroupId,NewGroupName):
        GroupId = MySQLdb.escape_string(GroupId)
        NewGroupName = MySQLdb.escape_string(NewGroupName)
        sql = '''UPDATE GroupInfo SET GroupName = '%s' WHERE GroupCode = %s;'''%(NewGroupName,GroupId)
        try:
            self.MySQLAccess.execute(sql)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
            
    def delete_group(self,GroupId):
        GroupId = MySQLdb.escape_string(GroupId)
        sql1 = '''UPDATE GroupInfo SET IsDelete = 1 WHERE GroupCode = %s;'''%GroupId
        sql2 = '''UPDATE BlogData SET IsDelete = 1 WHERE GroupCode = %s;'''%GroupId
        try:
            self.MySQLAccess.execute(sql1)
            self.MySQLAccess.execute(sql2)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
    
    def upload_about(self,Content):
        Content = MySQLdb.escape_string(Content)
        sql = '''UPDATE About SET Content = '%s' WHERE Id = 1;'''%Content
        try:
            self.MySQLAccess.execute(sql)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
    
    def get_about(self):
        message = None
        sql = '''SELECT Content FROM About WHERE Id = 1;'''
        try:
            data = self.MySQLAccess.select(sql)
            message = data[0][0]
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return message
    
    def insertdata(self,Subject,UserName,AddTime,FileName,GroupCode,Privacy):
        '''
        @summary: 插入博客信息
        '''
        try:
            Subject = MySQLdb.escape_string(Subject)
            UserName = MySQLdb.escape_string(UserName)
            AddTime = MySQLdb.escape_string(AddTime)
            FileName = MySQLdb.escape_string(FileName)
            GroupCode = MySQLdb.escape_string(GroupCode)
            sql1 = '''INSERT IGNORE INTO BlogData (Subject,UserName,AddTime,FileName,GroupCode,Views,Privacy) VALUES ('%s','%s','%s','%s',%s,0,%s)'''%(Subject,UserName,AddTime,FileName,GroupCode,Privacy)
            sql2 = '''UPDATE GroupInfo SET `Count` = `Count` + 1 WHERE GroupCode = %s'''%GroupCode
            self.MySQLAccess.execute(sql1)
            self.MySQLAccess.execute(sql2)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
    
    def updatablog(self,Subject,UpdateTime,GroupCode,blogId,Privacy):
        '''
        @summary: 更新博客信息
        '''
        try:
            Subject = MySQLdb.escape_string(Subject)
            UpdateTime = MySQLdb.escape_string(UpdateTime)
            GroupCode = MySQLdb.escape_string(GroupCode)
            blogId = MySQLdb.escape_string(blogId)
            sql = '''UPDATE BlogData SET Subject = '%s',ChangeTime = '%s',GroupCode = %s,Privacy = %s where Id = %s; '''%(Subject,UpdateTime,GroupCode,Privacy,blogId)
            self.MySQLAccess.execute(sql)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)

    def del_blog(self,BlogId):
        BlogId = MySQLdb.escape_string(BlogId)
        sql = '''UPDATE BlogData SET IsDelete = 1 WHERE Id = %s'''%BlogId
        try:
            self.MySQLAccess.execute(sql)
        except:
            err_msg = get_err_msg()
            root.error(err_msg)

    def get_group_num(self,GroupCode = None):
        '''
        @summary: 获取该类别博客数目
        '''
        Count = 0
        try:
            if not GroupCode:
                sql = '''SELECT COUNT(*) FROM `BlogData` WHERE IsDelete = 0;'''
            else:
                GroupCode = MySQLdb.escape_string(str(GroupCode))
                sql = '''SELECT COUNT(*) FROM `BlogData` WHERE GroupCode = %s AND IsDelete = 0;'''%GroupCode
            data = self.MySQLAccess.select(sql)
            Count = data[0][0]
        except:
            err_msg = get_err_msg()
            root.error(err_msg)
        return Count
    
    
        
MySQLHandler = MysqlHandler()
        
