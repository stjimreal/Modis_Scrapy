'''
Date: 2021-07-24 00:57:16
LastEditors: LIULIJING
LastEditTime: 2021-07-24 03:28:43
'''
from os import name
import scrapy
from scrapy.http import headers

from utils import credentials, utilities
from utils.globals import USER_AGENT_LIST, meta_proxy, short_name, version, time_start, time_end, bounding_box, \
            polygon, filename_filter
from modis_scrapy.items import ModisScrapyItem

import logging
import logging.handlers
import json

class ModisNsidcSpider(scrapy.Spider):
    name = 'modis_generic'

    LOG_FORMAT="%(asctime)s======%(levelname)s++++++\n%(message)s"
    log = logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.handlers.RotatingFileHandler("logs/modis_nsidc_spider.log", maxBytes=500*1024, backupCount=5)])
    def __init__(self) -> None:
        super().__init__(name=name)
        global short_name, version, time_start, time_end, bounding_box, \
            polygon, filename_filter, url_list

        if 'short_name' in short_name:
            short_name = ['ATL06']
            version = '003'
            time_start = '2018-10-14T00:00:00Z'
            time_end = '2021-01-08T21:48:13Z'
            bounding_box = ''
            polygon = ''
            filename_filter = '*ATL06_2020111121*'
            url_list = []

        self.cmr_query_url = [utilities.build_cmr_query_url(nm, version, time_start, time_end, bounding_box, polygon, filename_filter) for nm in short_name]
        

    def start_requests(self):
        return self.cmr_search()

    def cmr_search(self, cmr_scroll_id = None):
        global USER_AGENT_LIST
        # 'https://cmr.earthdata.nasa.gov/search/granules.json?provider=NSIDC_ECS&sort_key[]=start_date&sort_key[]=producer_granule_id&scroll=true&page_size=2000&short_name=MOD10A2&version=006&version=06&version=6&temporal[]=2000-02-24T00:00:00Z,2021-07-21T05:48:52Z&bounding_box=62,26,105.0018536,46.000389'
        logging.info('Querying for data:\n\t{0}\n'.format(self.cmr_query_url))

        if not cmr_scroll_id:
            return [scrapy.Request(query_url, callback=self.get_credentials) for query_url in self.cmr_query_url] 

    def cmr_download(self, response):
        item = ModisScrapyItem(file_urls=response.meta['url_list'])
        yield item

    def get_credentials(self, response):
        """Get user credentials from .netrc or prompt for input."""
        global meta_proxy
        text_res = response.text
        search_res = json.loads(text_res)
        url_list = utilities.cmr_filter_urls(search_res)
        url = url_list[0]
        header = {'Authorization': 'Basic {0}'.format(credentials.get_credentials())}

        return scrapy.Request(url, callback=self.cmr_download, headers=header, meta= {'proxy': meta_proxy, 'url_list': url_list}, dont_filter=True)


