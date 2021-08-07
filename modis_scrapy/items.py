'''
Date: 2021-03-25 22:31:44
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:36:35
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from utils.globals import turn_on_stitch_and_reproject, output_file_mosaic_path
from utils.gdal_proc import get_output_ext
from utils.utilities import yes_no_parser

class ModisScrapyItem(scrapy.Item):
    
    # define the fields for your item here like:
    # name = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    tile_chklist = scrapy.Field()
    headers = scrapy.Field()
    date_tiles = scrapy.Field()
    if yes_no_parser(turn_on_stitch_and_reproject):
        reproject_options = get_output_ext(output_file_mosaic_path)