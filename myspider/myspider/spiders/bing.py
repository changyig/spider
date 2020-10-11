# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode

class ZhilianSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ['www.bing.com']

    start_urls = ['https://www.bing.com/search?q=rubber+tyred+mobile+crusher+in+india+koshima']

    def parse(self, response):
        data={}
        print('开始')
        print(response.text)