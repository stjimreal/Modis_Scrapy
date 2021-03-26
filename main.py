'''
Date: 2021-03-26 16:18:46
LastEditors: LIULIJING
LastEditTime: 2021-03-26 16:20:14
'''
from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'modis_nsidc'])