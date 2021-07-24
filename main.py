'''
Date: 2021-03-26 16:18:46
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:46:05
'''
from scrapy.cmdline import execute

if __name__=="__main__":
    execute(['scrapy', 'crawl', 'modis_generic'])
