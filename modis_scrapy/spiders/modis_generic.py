'''
Date: 2021-07-24 00:57:16
LastEditors: LIULIJING
LastEditTime: 2021-07-24 19:02:13
'''
from os import name
import scrapy

from utils import credentials, utilities
from utils.globals import USER_AGENT_LIST, meta_proxy, short_name, version, time_start, time_end, \
            bounding_box, polygon, filename_filter
from modis_scrapy.items import ModisScrapyItem

import logging
import logging.handlers
import random
import json

class ModisNsidcSpider(scrapy.Spider):
    name = 'modis_generic'

    LOG_FORMAT="%(asctime)s======%(levelname)s++++++\n%(message)s"
    log = logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.handlers.RotatingFileHandler("logs/modis_nsidc_spider.log", maxBytes=5000*1024, backupCount=5)])
    logging.disable(logging.DEBUG)
    def __init__(self) -> None:
        super().__init__(name=name)
        global USER_AGENT_LIST, short_name, version, time_start, time_end, bounding_box, \
            polygon, filename_filter

        if 'short_name' in short_name:
            short_name = ['ATL06']
            version = '003'
            time_start = '2018-10-14T00:00:00Z'
            time_end = '2021-01-08T21:48:13Z'
            bounding_box = ''
            polygon = ''
            filename_filter = '*ATL06_2020111121*'

        self.cmr_query_url = [utilities.build_cmr_query_url(nm, version, time_start, time_end, bounding_box, polygon, filename_filter) for nm in short_name]
        self.header = {'User-Agent': random.choice(USER_AGENT_LIST)}
        self.search_header = {'User-Agent': random.choice(USER_AGENT_LIST)}

    def start_requests(self):
        logging.info('Querying for data:\n\t{0}\n'.format(self.cmr_query_url))
        for query_url in self.cmr_query_url:
            yield scrapy.Request(query_url, callback=self.cmr_search, headers=self.header)

    def cmr_search(self, response):
        search_list = utilities.cmr_filter_urls(json.loads(response.text))
        if not 'url_list' in response.meta:
            hits = response.headers['cmr-hits']
            logging.info('Found {0} matches.'.format(hits))
        if search_list:
            url_list = response.meta.get('url_list', search_list)
            url_list += search_list

            header = self.header
            header['cmr-scroll-id'] = response.headers['cmr-scroll-id']
            return [scrapy.Request(query_url, callback=self.cmr_search, headers=header, meta={'url_list': url_list}, dont_filter=True) for query_url in self.cmr_query_url]
        else:
            return self.get_credentials(response.meta['url_list'])

    def cmr_download(self, response):
        item = ModisScrapyItem(file_urls=response.meta['url_list'])
        yield item

    def get_credentials(self, url_list):
        """Get user credentials from .netrc or prompt for input."""
        url = url_list[0]
        header = {'User-Agent': random.choice(USER_AGENT_LIST), 'Authorization': 'Basic {0}'.format(credentials.get_credentials())}

        return scrapy.Request(url, callback=self.cmr_download, headers=header, meta= {'proxy': meta_proxy, 'url_list': url_list}, dont_filter=True)
