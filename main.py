'''
Date: 2021-03-26 16:18:46
LastEditors: LIULIJING
LastEditTime: 2021-07-24 21:35:26
'''
from scrapy.cmdline import execute
import os
import sys
import cfg

if __name__=="__main__":
    execute(['scrapy', 'crawl', 'modis_generic'])
