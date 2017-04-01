#coding=utf-8
'''
Created on 2015-5-28

@author: Administrator
'''
import traceback,cStringIO,time
def get_err_msg():
    f = cStringIO.StringIO()
    traceback.print_exc( file = f )
    f.seek( 0 )
    err = f.read()
    #写日志
    print err
    return err


if __name__ == '__main__':
    try:
        a = 18 -'12313'
    except:
        pass
