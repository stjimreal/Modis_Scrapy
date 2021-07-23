'''
Date: 2021-03-25 22:31:44
LastEditors: LIULIJING
LastEditTime: 2021-07-25 02:03:36
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import os


class ModisScrapyPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        path = urlparse(request.url).path
        return os.path.basename(path)
