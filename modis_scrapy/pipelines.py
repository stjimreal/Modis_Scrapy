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

from modis_scrapy import settings
from utils import credentials
from utils.globals import USER_AGENT_LIST, save_julian_date, turn_on_stitch_and_reproject
from utils.globals import ALL_DONE_FILE_OUTPUT_PATH, output_type, subset
from utils.globals import save_origin_file, save_stitch_file
from utils.utilities import yes_no_parser, parse_save_url, get_date_normal, get_date_julian
from utils.gdal_proc import stitch_and_reproject

from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.utils.misc import md5sum


import random
from urllib.parse import urlparse
import os
from io import BytesIO


class ModisScrapyPipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse_output_date = get_date_julian if yes_no_parser(
                        save_julian_date) else get_date_normal
        proc_or_not = yes_no_parser(turn_on_stitch_and_reproject)
        self.file_downloaded =  self._transform_downloaded if proc_or_not else self._file_downloaded
        if proc_or_not:
            os.makedirs(ALL_DONE_FILE_OUTPUT_PATH, 0o755, exist_ok=True)

    def get_media_requests(self, item, info):

        header = {'User-Agent': random.choice(USER_AGENT_LIST), 'Authorization': 'Basic {}'.format(credentials.get_credentials())}
        item.fields.setdefault('date_tiles', dict())
        for file_url in item['file_urls']:
            req = Request(file_url, headers=header)
            yield req

    def file_path(self, request, response=None, info=None, *, item=None):
        _, path = parse_save_url(request.url)
        return path

    def _file_downloaded(self, response, request, info, *, item):
        path = self.file_path(request)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)

        return checksum
    
    def _transform_downloaded(self, response, request, info, *, item):
        date_code, origin_path = parse_save_url(request.url)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(origin_path, buf, info)
        if not origin_path.endswith("xml"):
            date_code = os.path.dirname(urlparse(request.url).path)
            item.fields['date_tiles'].setdefault(date_code, set())
            item.fields['date_tiles'][date_code].add(origin_path)
            if item.fields['date_tiles'][date_code] == item['tile_chklist'][date_code]:
                product = os.path.dirname(origin_path)
                tile_list =  [os.path.join(settings.FILES_STORE, v) for v in 
                                    item.fields['date_tiles'][date_code]]
                stitch_and_reproject(tile_list, 
                                    ALL_DONE_FILE_OUTPUT_PATH, 
                                    product=product,
                                    date=self.parse_output_date(request.url),
                                    reproject_options=item.reproject_options,
                                    subset=subset,
                                    outformat=output_type, 
                                    save_stitch_file= yes_no_parser(save_stitch_file))
                item.fields['date_tiles'].pop(date_code)

        return checksum
