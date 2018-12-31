# !/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = '__Rebecca__'

__version__ = '0.0.2'

import os
import json
import time
import requests
import threading
from bcy_single_climber import bcy_single_climber

class re_downloads(object):
    def __init__(self, download_lists, download_path, rbp=True, block_size=1048576):
        '''初始化对象
            为init方法

            Args:
                download_lists: 下载链接列表,为list或者tuple类型
                download_path: 文件下载路径
                rbp:即Resume BreakPoint.是否开启断点续传,为bool类型
                block_size: 断点续传块大小,缺省默认为1M
            
            Returns:
                None

            Raises:
                None
        '''
        if not isinstance(download_lists, list) or isinstance(download_lists, tuple):
            raise Exception('Lists type error: List or Tuple required.')
        self.__download_lists = download_lists
        download_path = os.path.abspath(download_path)
        if not os.path.isdir(download_path):
            raise Exception('Path Error: Parameter \'download_path\' is not a path.')
        self.__path = download_path.replace('\\', '/')
        if not isinstance(rbp, bool):
            raise Exception('rbp type error: bool required.')
        self.__rbp = rbp
        self.__block_size = block_size
        # 缓存文件文件名
        self.__ctrl_file_name = os.path.basename(self.__path) + '.rdtp'
        # 缓存文件路径
        self.__cf_path = self.__path + self.__ctrl_file_name
        # 缓存文件文件指针
        if not os.path.exists(self.__cf_path):
            f = open(self.__cf_path, 'wb')
            f.close()
        self.__cf = open(self.__cf_path, 'r+b')
        # 创建读写线程锁
        self.__tlock = threading.Lock()
    
    def get_cf_data(self):
        '''读取配置文件中的信息
        '''
        # 开启读写锁
        self.__tlock.acquite()
        self.__cf.seek(0, whence=0)         # 将文件指针指向文件头部
        data = self.__cf.read()
        data_str = data.decode('UTF-8')
        data_dic = json.loads(data_str)
        self.__cf.seek(0, whence=0)
        # 关闭读写锁
        self.__tlock.release()
        return data_dic
    
    def set_cf_data(self, dic):
        '''更新配置文件中的信息
        '''
        # 开启读写锁
        self.__tlock.acquite()
        self.__cf.seek(0, whence=0)         # 将文件指针指向文件头部
        data_str = json.dumps(dic)
        data = data_str.encode('UTF-8')
        # 更新缓存区
        self.__cf.flush()
        self.__cf.seek(0, whence=0)
        # 关闭读写锁
        self.__tlock.release()
        return data
    
    def __del__(self):
        self.__cf.close()
    
    


if __name__ == '__main__':
    print('Hello world!')