'''
Date: 2021-03-26 00:22:28
LastEditors: LIULIJING
LastEditTime: 2021-03-26 19:52:30
'''
import scrapy
import re
from urllib import parse
from modis_scrapy.items import ModisScrapyItem
from cfg import Conf

class ModisNsidcSpider(scrapy.Spider):
    name = 'modis_nsidc'
    allowed_domains = ['https://n5eil01u.ecs.nsidc.org/']
    start_urls = ['https://n5eil01u.ecs.nsidc.org/MOSA/', 'https://n5eil01u.ecs.nsidc.org/MOST/']
    products = set(['MYD10A1.006','MOD10A1.006'])
    login_urls = 'https://urs.earthdata.nasa.gov/login'
    date_end = '2021.01.01'
    date_beg = '2021.01.03'
    region = ['h2{}v0{}'.format(i, j) for i in range(2, 8) for j in range(4, 7)]
    asia_region = ['h{}v0{}'.format(i, j) for i in range(20, 30) for j in range(1, 8)] + ['h{}v0{}'.format(i, j) for i in range(17, 20) for j in range(1, 5)]
    username = 'Mui0416'
    password = 'zkyygsMui201513'
    key_sets = []
    
    
    headers= {
        'Host':'n5eil01u.ecs.nsidc.org',
        'Referer': allowed_domains[0],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    def __init__(self, name=None, conf:dict=Conf, **kwargs):
        if conf:
            self.date_end = conf.get('date_end', self.date_end)
            self.date_beg = conf.get('date_beg', self.date_beg)
            self.key_sets = conf.get('key_sets', self.key_sets)
            self.products = set(conf.get('products', self.products))
            self.start_urls=conf.get('start_urls', self.start_urls)
            self.region   = conf.get('region', self.region)
        super().__init__(name=name, **kwargs)

    def download_pictures(self, response):
        """ 
        """
        all_urls = response.css("a::attr(href)").extract()
        def find_all_tiles(s, region):
            for tile in region:
                if (s.find(tile) >= 0):
                    return True
            return False
        all_urls = set([parse.urljoin(response.request.url, url) for url in all_urls if (url.endswith('.hdf') or url.endswith('.hdf.xml')) and find_all_tiles(url, self.region)])
        with open("file_list.txt", 'a+') as f:
            f.writelines(str(all_urls))
        
        item = ModisScrapyItem(file_urls=all_urls)
        yield item

    def parse_folder(self, response):
        """ 
        
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = set([parse.urljoin(response.request.url, url) for url in all_urls if (url >= self.date_end and url <= self.date_beg)])
        print("found {} days of pics".format(len(all_urls)))
        with open('list.txt', 'a+') as f:
            f.writelines(all_urls)
        for url in all_urls:
            yield scrapy.Request(url, callback=self.download_pictures, headers=self.headers, dont_filter=True)

    def parse(self, response):
        """ 
        
        """
        pattern = re.compile(r'([A-Z0-9]+\.\w+)')
        products = pattern.findall(response.text)
        for product in products:
            if product in self.products:
                url = parse.urljoin(response.request.url, product)
                yield scrapy.Request(url, dont_filter=True, callback=self.parse_folder, headers=self.headers)
    
    
    
    def start_requests(self):
        return [scrapy.Request('https://urs.earthdata.nasa.gov/home', headers=ModisNsidcSpider.headers, callback=self.login)]
    

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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
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
        print("checking...")
        print(type(response.status))
        if (response.status == 200):
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, callback=self.redirect_req, headers=self.headers)

    def redirect_req(self, response):
        """ 
        访问重定向位置
        """
        text = response.text
        grp = re.match(r'.*id="redir_link" href="(.*?)"', text, re.DOTALL)
        url = grp.group(1)
        return scrapy.Request(url, dont_filter=True, callback=self.parse, headers=self.headers)

        # if (url):
        #     return scrapy.Request(url, callback=)