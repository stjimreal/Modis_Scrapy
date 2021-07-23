'''
Date: 2021-03-26 19:20:38
LastEditors: LIULIJING
LastEditTime: 2021-03-26 21:43:28
'''
import json

def init(cfg):
    global Conf
    Conf = json.load(open(cfg))

def get(value, default):
    return Conf.get(value, default)
