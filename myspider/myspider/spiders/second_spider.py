# -*- coding: utf-8 -*-
import scrapy


class SecondSpiderSpider(scrapy.Spider):
    name = 'second_spider'
    allowed_domains = ['www.44txt.com']
    start_urls = ['http://www.44txt.com/xuanhuanqihuan/index_3.html']

    def parse(self, response):
        res=response.xpath('//div[@class="listBox"]//li')
        next_url=response.xpath('//div[@class="tspage"]/b/following-sibling::*/text()')
        print(next_url)
        for x in res:
        	item={}
        	item['title']=x.xpath('./a/text()').extract_first()
        	item['author']=x.xpath('./div[@class="s"]/a/text()').extract_first()
        	yield item
