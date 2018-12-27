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


'''
链接：https://bcy.net/home/timeline/loaduserposts?since=0&grid_type=timeline&uid=3482886&limit=20
单次最大请求20条
since=0为从头获取
获取第21条时，since=【第20条的id】
当全部获取完时，返回值data为空
'''