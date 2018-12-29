# !/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = '__Rebecca__'

__version__ = '0.0.2'

import os
import json
import time
import requests
import multiprocessing
from bcy_single_climber import bcy_single_climber


'''
链接：https://bcy.net/home/timeline/loaduserposts?since=0&grid_type=timeline&uid=3482886&limit=20
单次最大请求20条
since=0为从头获取
获取第21条时，since=【第20条的id】
当全部获取完时，返回值data为空
'''

class bcy_user_item(object):
    def __init__(self, data):
        self.__data = data
        if not self.__data['tl_type'] == 'item':
            raise Exception('Initlize failed! Format wrong.')
        self.type = self.__data['tl_type']
        self.detail = self.__data['item_detail']
        self.item_id = self.detail['item_id']
        self.user_id = self.detail['uid']
        self.avatar = self.detail['avatar']

        

class bcy_user_climber(object):
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__items = []
        self.__item_get_url = 'https://bcy.net/home/timeline/loaduserposts'
        self.__max_limit = 20


    def get_items(self):
        item_list = []
        last_item = None
        while True:
            params = {  'since':0 if not last_item else last_item.item_id, 
                        'grid_type':'timeline', 
                        'uid':self.__user_id, 
                        'limit':self.__max_limit
                        }
            item_data = requests.get(self.__item_get_url, params=params)
            item_json = json.loads(item_data.text)
            item_data = item_json['data']
            # 若data为空
            if not item_data:
                break
            for i in item_data:
                temp_item = bcy_user_item(i)
                item_list.append(temp_item)
            last_item = item_list[-1]
        self.__items = item_list
        return item_list


    def get_page_url(self):
        if not self.__items:
            self.get_items()
        page_home = 'https://bcy.net/item/detail/'
        url_lst = []
        for i in self.__items:
            temp_url = page_home + i.item_id
            url_lst.append(temp_url)
        return url_lst
    

    def begin_download(self, page_url_list=None):
        if not page_url_list:
            page_url_list = self.get_page_url()
        for i in page_url_list:
            single = bcy_single_climber(url = i)
            single.start()
        return True



if __name__ == '__main__':
    uitem = bcy_user_climber(3482886)
    # back = uitem.begin_download()
    p = multiprocessing.Process(target = uitem.begin_download, args = ())
    p.start()
    p.join()
    print('Hello world')