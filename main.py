'''
Date: 2021-03-26 16:18:46
LastEditors: LIULIJING
LastEditTime: 2021-07-24 00:55:44
'''
from scrapy.cmdline import execute
import os
import sys
import cfg

if __name__=="__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    cfg.init('configuration_{}.json'.format('modis_nsidc'))
    # execute(['scrapy', 'crawl', 'modis_nsidc'])
    # execute(['scrapy', 'crawl', 'modis_nsidc'])
    execute(['scrapy', 'crawl', 'modis_8day'])
