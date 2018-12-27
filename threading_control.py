# !/usr/bin/env python
# -*- coding:UTF-8 -*-

import time
import threading

class threading_control(object):
    def __init__(self, threading_pool=None, max_threading=10):
        self.threading_pool = threading_pool
        self.max_threading = max_threading
        self.__alive = []
        self.__death = []

    @property
    def alive(self):
        temp = []
        for i in self.threading_pool:
            if i.is_alive():
                temp.append(i)
        self.__alive = temp
        return self.__alive

    @alive.setter
    def alive(self, alive):
        if not isinstance(alive, list):
            raise TypeError('Invalid Type: Variable "alive" required list.')
        self.__alive = alive
    
    def start(self):
        for i in self.threading_pool:
            while not (len(self.alive) < self.max_threading):
                time.sleep(3)
            i.start()
        alive_list = self.alive
        for i in alive_list:
            if i.is_alive():
                i.join()
        return True
    
    def __del__(self):
        pass



if __name__ == '__main__':
    a = threading_control()
    pass
    
