'''
Date: 2021-03-25 22:31:44
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:49:22
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import random
from utils import credentials
from utils.globals import USER_AGENT_LIST
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from urllib.parse import urlparse
import os

class ModisScrapyPipeline(FilesPipeline):
    def get_media_requests(self, item, info):

        header = {'User-Agent': random.choice(USER_AGENT_LIST), 'Authorization': 'Basic {}'.format(credentials.get_credentials())}
        for file_url in item['file_urls']:
            req = Request(file_url, headers=header)
            yield req
    def file_path(self, request, response=None, info=None, *, item=None):
        path = urlparse(request.url).path
        base_name = os.path.basename(path)
        save_folder, _, _ = base_name.partition('.')
        
        return os.path.join(save_folder, base_name)