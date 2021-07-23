'''
Date: 2021-03-25 22:31:44
LastEditors: LIULIJING
LastEditTime: 2021-03-26 18:50:37
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import random
import re

from scrapy.http.headers import Headers
from utils import credentials
from utils.globals import USER_AGENT_LIST

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from urllib.parse import urlparse
import os

class ModisScrapyPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        # ('Authorization', 'Basic MTA3OTA4NTgxMFdzdGFyOlJhZGkxMjM0NTY=')
        header = {'Authorization': 'Basic {}'.format(credentials.get_credentials())}
        for file_url in item['file_urls']:
            req = Request(file_url, headers=header)
            print(req.headers.to_string(), req.url, req.method)
            yield req
    def file_path(self, request, response=None, info=None, *, item=None):
        path = urlparse(request.url).path
        save_name = os.path.basename(path)
        return save_name