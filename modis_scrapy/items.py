'''
Date: 2021-03-25 22:31:44
LastEditors: LIULIJING
LastEditTime: 2021-03-26 17:13:22
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ModisScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
