from os import name
import scrapy

from utils import credentials, utilities
from utils.globals import USER_AGENT_LIST, short_name, version, time_start, time_end, bounding_box, \
            polygon, filename_filter, url_list
from modis_scrapy.items import ModisScrapyItem
from cfg import Conf

import logging
import logging.handlers
import random
import json
import ssl
from getpass import getpass

try:
    from urllib.parse import urlparse
    from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
    from urllib.error import HTTPError, URLError
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen, Request, HTTPError, URLError, build_opener, HTTPCookieProcessor


# CMR_URL = 'https://cmr.earthdata.nasa.gov'
# URS_URL = 'https://urs.earthdata.nasa.gov'
# CMR_PAGE_SIZE = 2000
# CMR_FILE_URL = ('{0}/search/granules.json?provider=NSIDC_ECS'
#                 '&sort_key[]=start_date&sort_key[]=producer_granule_id'
#                 '&scroll=true&page_size={1}'.format(CMR_URL, CMR_PAGE_SIZE))

class ModisNsidcSpider(scrapy.Spider):
    name = 'modis_8day'

    LOG_FORMAT="%(asctime)s======%(levelname)s++++++\n%(message)s"
    log = logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.handlers.RotatingFileHandler("logs/modis_nsidc_spider.log", maxBytes=500*1024, backupCount=5)])
    def __init__(self) -> None:
        super().__init__(name=name)
        global short_name, version, time_start, time_end, bounding_box, \
            polygon, filename_filter, url_list

        if 'short_name' in short_name:
            short_name = 'ATL06'
            version = '003'
            time_start = '2018-10-14T00:00:00Z'
            time_end = '2021-01-08T21:48:13Z'
            bounding_box = ''
            polygon = ''
            filename_filter = '*ATL06_2020111121*'
            url_list = []

        self.cmr_query_url = utilities.build_cmr_query_url(short_name, version, time_start, time_end, bounding_box, polygon, filename_filter)
        

    def start_requests(self):
        return self.cmr_search()

    def cmr_search(self, cmr_scroll_id = None):
        global USER_AGENT_LIST
        # 'https://cmr.earthdata.nasa.gov/search/granules.json?provider=NSIDC_ECS&sort_key[]=start_date&sort_key[]=producer_granule_id&scroll=true&page_size=2000&short_name=MOD10A2&version=006&version=06&version=6&temporal[]=2000-02-24T00:00:00Z,2021-07-21T05:48:52Z&bounding_box=62,26,105.0018536,46.000389'
        logging.info('Querying for data:\n\t{0}\n'.format(self.cmr_query_url))

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        if not cmr_scroll_id:
            return [scrapy.Request(self.cmr_query_url, callback=self.cmr_download)] 

    def cmr_download(self, response):
        global url_list, credentials
        text_res = response.text
        search_res = json.loads(text_res)
        url_list = utilities.cmr_filter_urls(search_res)
        item = ModisScrapyItem(file_urls=url_list)
        yield item
    


