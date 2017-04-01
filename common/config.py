#coding=utf-8
'''
Created on 2015-5-28

@author: Administrator
'''
from ConfigParser import ConfigParser
import os

path  = os.path.dirname(__file__)
path = os.path.dirname(path)
ConfigFile = os.path.join(path,'setting.ini')

class MyConfigParser(ConfigParser):
    def __init__(self,defaults=None):  
        ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):  
        return optionstr
    
class Config(object):
    
    def __init__(self,configfile = ConfigFile):
        with open(configfile,'rb') as f:
            content = f.read()
        content = content.replace("\xef\xbb\xbf","")
        with open(configfile,'wb') as f:
            f.write(content)
        self.file_name = configfile
        self.config = MyConfigParser()
        self.config.read(configfile)
    
    def get(self,section,option):
        ret = self.config.get(section, option)
        return ret
    
    def set(self,section,option,value):
        self.config.set(section, option, value)
        self.config.write(open(self.file_name,"w"))
        
    def getOptions(self,section):
        options = self.config.options(section)
        return options
        
            
        

if __name__ == '__main__':
    path  = os.path.dirname(__file__)
    path = os.path.dirname(path)
    configfile = os.path.join(path,'setting.ini')
    A = Config(configfile)
    host = A.get('mysqlconf','MySqlhost')
    A.set('mysqlconf', 'test', 11)
    print host