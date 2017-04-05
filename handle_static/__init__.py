#coding=utf8
'''
Created on 2016-12-8

@author: xuwei

@summary: 处理静态文件
'''
import posixpath
import time,os
from common.traceback_error import get_err_msg
from setting import ImageDataPath
from common.basehandler import NoAuthHandler,AuthHandler

import mimetypes
if not mimetypes.inited:
        mimetypes.init() 
extensions_map = mimetypes.types_map.copy()
extensions_map.update({'': 'application/octet-stream', '.py': 'text/plain', '.c': 'text/plain', '.h': 'text/plain',})


class UploadImageHander(AuthHandler):
     
    def do_something(self):
        try:
            flag = self.check_request_type('post')
            if not flag:
                raise Exception('Request type error')
            is_admin = self.check_admin()
            if not is_admin:
                raise Exception('No permission error')
            CKEditorFuncNum = self.get_argument("CKEditorFuncNum", '')
            num = 0
            for upfile in self.request.files:
                num += 1
                filedict = self.request.files[upfile][0]
                sourcefilename = filedict.get('filename')
                suffix = sourcefilename.split(".")[-1]
                filename = time.strftime("%Y%m%d%H%M%S_") + str(num) + "." + suffix
                if not os.path.exists(ImageDataPath):
                    os.mkdir(ImageDataPath)
                savefilename = os.path.join(ImageDataPath,filename)
                with open(savefilename,'wb') as fp:
                    fp.write(filedict['body']) 
                returnurl = "/ImagePath/%s"%(filename)
                returnstr = '''<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(%s, '%s','Upload Sucress');</script>'''%(CKEditorFuncNum,returnurl)
            self.write(returnstr)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
            
class ImagePathHandler(NoAuthHandler):
    '''使用服务器后可以配置该静态文件路径，然后将该模块url注释'''
    
    def do_something(self):
        try:
            filename = self.request.uri.split('/')[-1]
            filename = os.path.join(ImageDataPath,filename)
            with open(filename,'rb') as fp:
                Content = fp.read()
            self.set_header("Content-type", self.guess_type(filename))
            self.write(Content)
        except:
            get_err_msg()
            self.render('error.html',message = 'Something wrong with the server.')
    
    def guess_type(self,path):
        base, ext = posixpath.splitext(path)
        if ext in extensions_map:
            return extensions_map[ext]
        ext = ext.lower()
        if ext in extensions_map:
            return extensions_map[ext]
        else:
            return extensions_map['']
