'''
Date: 2021-03-26 00:22:28
LastEditors: LIULIJING
LastEditTime: 2021-03-26 22:08:02
'''
import scrapy
import re
from urllib import parse
from modis_scrapy.items import ModisScrapyItem
import cfg
import json
import logging
import logging.handlers

def isLeapYear(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            True       # 非整百年能被4整除的为闰年
    else:
        False


class ModisNsidcSpider(scrapy.Spider):
    name = 'modis_L1B'
    allowed_domains = ['https://ladsweb.modaps.eosdis.nasa.gov/']
    start_urls = ['https://n5eil01u.ecs.nsidc.org/MOSA/', 'https://n5eil01u.ecs.nsidc.org/MOST/']
    products = set(['MYD10A1.006','MOD10A1.006'])
    login_urls = 'https://urs.earthdata.nasa.gov/login'
    date_end = '2021.01.01'
    date_beg = '2021.01.03'
    hosts = 'ladsweb.modaps.eosdis.nasa.gov'
    region = set(['h2{}v0{}'.format(i, j) for i in range(2, 8) for j in range(4, 7)])
    asia_region = set(['h{}v0{}'.format(i, j) for i in range(20, 30) for j in range(1, 8)] + ['h{}v0{}'.format(i, j) for i in range(17, 20) for j in range(1, 5)])
    username = 'Mui0416'
    password = 'zkyygsMui201513'
    key_sets = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    LOG_FORMAT="%(asctime)s======%(levelname)s++++++\n%(message)s"
    log = logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.handlers.RotatingFileHandler("logs/modis_nsidc_spider.log", maxBytes=500*1024, backupCount=5)])
    
    headers= {
        'Host': hosts,
        'Referer': allowed_domains[0],
        'User-Agent': user_agent,
    }

    def __init__(self, name=None, **kwargs):
        self.date_end = cfg.get('date_end', self.date_end)
        self.date_beg = cfg.get('date_beg', self.date_beg)
        self.key_sets = cfg.get('key_sets', self.key_sets)
        self.products = set(cfg.get('products', self.products))
        self.start_urls=cfg.get('start_urls', self.start_urls)
        self.hosts = cfg.get('hosts', self.hosts)
        self.allowed_domains = cfg.get('allowed_domains', self.allowed_domains)
        self.region   = cfg.get('region', self.region)
        super().__init__(name=name, **kwargs)

    def download_pictures(self, response):
        """ 
        """
        all_urls = response.css("tr::attr(data-name)").extract()
        remach = re.compile(r'\.([0-9]{2}[0-9]{2})\.')
        find_all_tiles = lambda target:(remach.findall(target)[0]) in self.region
        all_urls = set([parse.urljoin(response.request.url, url) for url in all_urls if (url.endswith('.hdf') or url.endswith('.hdf.xml')) and find_all_tiles(url)])
        
        item = ModisScrapyItem(file_urls=all_urls)
        yield item

    def parse_folder(self, response):
        """ 
        
        """
        all_urls = response.css("tr::attr(data-name)").extract()
        all_urls = set([parse.urljoin(response.request.url, url) for url in all_urls if url >= self.date_end and url <= self.date_beg])
        logging.info("found {} years of pics".format(len(all_urls)))
        for url in all_urls:
            yield scrapy.Request(url, callback=self.download_pictures, headers=self.headers, dont_filter=True)

    def parse(self, response):
        """ 
        
        """
        # pattern = re.compile(r'([A-Z0-9]+\.\w+)')
        # products = set(pattern.findall(response.text))
        products = set(response.css("tr::attr(data-name)").extract())
        for product in self.products & products:
            for year in range(int(self.date_end), int(self.date_beg) + 1):
                if (isLeapYear(year)):
                    endDay = 366
                else:
                    endDay = 365
                for day in range(1, endDay + 1):
                    url = parse.urljoin(response.request.url, product + '/' + str(year) + '/' + str(day).zfill(3))
                    yield scrapy.Request(url, dont_filter=True, callback=self.download_pictures, headers=self.headers)
    
    
    
    def start_requests(self):
        return [scrapy.Request('https://urs.earthdata.nasa.gov/home', headers=self.headers, callback=self.login)]
    

    def login(self, response):
        text = response.text
        def parse_form(text, regex):
            match_obj = re.findall(regex, text, re.DOTALL)
            if match_obj:
                return match_obj
            return None
        xsrf_token = parse_form(text, r'.*name="csrf-token" content="(.*?)"')[0]
        
        if xsrf_token:
            post_url = self.login_urls
            login_headers = {
                'Host':'urs.earthdata.nasa.gov',
                'User-Agent': self.user_agent,
            }
            post_data= {
                    "authenticity_token": xsrf_token,
                    "username": self.username,
                    "password": self.password,
                    'commit': 'Log in',
                }
            return [scrapy.FormRequest(
                url = post_url,
                formdata= post_data,
                headers = login_headers,
                callback= self.check_login,
                dont_filter=True,
            )]

    def check_login(self, response):
        """ 
        判断是否登录成功
        """
        logging.info("checking...")
        logging.info(type(response.status))
        if (response.status == 200):
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, callback=self.parse, headers=self.headers)

    def redirect_req(self, response):
        """ 
        访问重定向位置
        """
        text = response.text
        grp = re.match(r'.*id="redir_link" href="(.*?)"', text, re.DOTALL)
        url = grp.group(1)
        return scrapy.Request(url, dont_filter=True, callback=self.parse, headers=self.headers)
 
# referer order 4:files
# 'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MYD02HKM--6/2017-01-01..2021-04-27/DB/Tile:H27V6,H26V6,H27V7,H28V6,H28V7,H29V7,H30V7,H27V8,H28V8,H29V8,H30V8,H28V9,H29V9,H30V9,H31V9,H32V9,H29V6,H26V7,H33V9'
