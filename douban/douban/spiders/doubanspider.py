# -*- coding: utf-8 -*-
import scrapy


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanspider'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.fruitfuler.com/sitemap.xml']

    def parse(self, response):
        pass
