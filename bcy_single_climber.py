# !/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = '__Rebecca__'

__version__ = '0.0.2'


import os
import json
import time
import requests
import threading
from bs4 import BeautifulSoup
from threading_control import threading_control


# 通过url下载半次元图片
class bcy_single_climber(object):
    def __init__(self, url, cookie=None, path=None, name_prefix=None, callback=None):
        self.url = url
        self.response = None
        self.cookie = cookie
        self.path = path
        self.name_prefix = name_prefix
        self.callback = callback
    
    def start(self):
        ssr_json = self.get_download_url_json()
        down_lst = self.get_download_list(ssr_json)
        return self.download_with_list(down_lst, path=self.path, name_prefix=self.name_prefix, callback=self.callback)
    
    # 分割含有'window.__ssr_data'字段的脚本中的json信息
    def get_download_url_json(self):
        headers = {'Cookie':str(self.cookie)}
        self.response = requests.get(self.url, headers=headers)
        context = self.response.text
        soup = BeautifulSoup(context, 'html.parser')
        html_script = soup.find_all('script')
        aim_script = ''
        for i in html_script:
            if 'window.__ssr_data' in i.text:
                aim_script = i
                break
        if not aim_script:
            return None
        json_str = aim_script.text.split(';')[0].split('JSON.parse(')[1][:-1]
        json_str = eval(json_str)
        return json_str
    
    # 通过ssr_json获取下载列表
    def get_download_list(self, ssr_json):
        ssr_dic = json.loads(ssr_json)
        multi = ssr_dic['detail']['post_data']['multi']
        # 相册ID
        self.__item_id = ssr_dic['detail']['post_data']['item_id']
        # coser昵称
        self.__coser_name = ssr_dic['detail']['detail_user']['uname']
        # 设置文件存储文件夹默认名
        self.__auto_filename = 'bcyc-' + self.__coser_name
        # 设置默认文件名前缀
        self.__auto_prefix = 'IMG'
        download_list = []
        for i in multi:
            download_list.append(i['original_path'])
        return download_list
    
    # 通过下载列表下载图片（开启多线程，下载完毕返回True）
    def download_with_list(self, download_list, path=None, name_prefix=None, callback=None):
        '''
        download_list : 下载列表，为元素仅包含str(url)的list类型\n
                 path : 下载目录，该参数若缺省则为当前目录下的coser名的项目id下\n
          name_prefix : 下载文件名字前缀，默认为IMG\n
             callback : 回调函数，为单个文件下载完成后所调用的函数，参数只能有一个为下载文件路径\n
        '''
        path = os.path.abspath(path)+'\\\\' if path else os.path.abspath(self.__auto_filename)+'\\'+self.__item_id+'\\'
        name_prefix = name_prefix if name_prefix else self.__auto_prefix+'_'
        if not os.path.exists(path):
            os.makedirs(path)
        down_list_str = ''
        for i in download_list:
            down_list_str = down_list_str + i + '\n'
        list_path = (path + '/download_list.txt').replace('\\', '/')
        fp = open(list_path, 'w')
        fp.write(down_list_str)
        fp.close()
        def download_single(url, path, name, callback=None):
            headers =   {   'Cookie'  : 'AspxAutoDetectCookieSupport=1', 
                            'User-Agent'    : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
                            'Upgrade-Insecure-Requests'         : '1'
                        }
            data = requests.get(url, headers = headers)
            con = data.content
            path = (path + name + '.' + url.split('.')[-1]).replace('\\', '/')
            with open(path, 'wb+') as f:
                f.write(con)
                f.close()
            if callable(callback):
                try:
                    callback(path)
                except Exception as e:
                    print(e)
        thread_list = []
        for i in download_list:
            t = threading.Thread(target=download_single, args=(i, path, name_prefix+str(download_list.index(i)+1)))
            thread_list.append(t)
        tc = threading_control(thread_list, 30)
        tc.start()
        return True

if __name__ == '__main__':
    bcy = bcy_single_climber('https://bcy.net/item/detail/6632162902138683652')
    print("Success!") if bcy.start() else print('Fail!')
