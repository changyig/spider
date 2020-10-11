# -*- coding: utf-8 -*-
import scrapy

import datetime
from data.items import DataItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.urbanjournalism.de']
    start_urls = ['https://www.urbanjournalism.de/sitemap.xml']

    # allowed_domains = ['www.44txt.com']
    # start_urls = ['http://www.44txt.com/xuanhuanqihuan/index_3.html']
    def get_keyword(self, response):
        item = DataItem()
        url = response.meta['url']
        keyword = response.xpath('//h1/text()').extract()[0]
        # info = response.xpath('//div[@class="baseshow"]/p//text()').extract()[0]
        item['url'] = url
        item['keyword'] = keyword
        item['info'] = ''
        item['createtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(item)
        # yield item
        print('存储数据')

    def get_keyword_url(self, response):
        num = 0
        print('keyword')
        text = response.text.replace('<![CDATA[', '').replace(']]>', '')
        sel = scrapy.Selector(text=text)
        keyword_list = sel.xpath('//loc/text()')
        # print(keyword_list)
        for i in keyword_list:
            url= i.extract()
            yield scrapy.Request(url=url, callback=self.get_keyword, meta={'url': url})
            print('进行下一个关键词url地址：'+url)
            if num > 5:
                break
            num = num + 1

    def parse(self, response):
        text = response.text.replace('<![CDATA[', '').replace(']]>', '')
        sel = scrapy.Selector(text=text)
        sitemap_list = sel.xpath('//loc/text()')
        print(sitemap_list)
        for i in sitemap_list:
            url=i.extract()
            print(url)
            # yield scrapy.Request(url=url, callback=self.get_keyword_url)
        #     print('进行下一个sitemap地址:'+i)
        print('停止运行')

        # next_url = response.xpath('//div[@class="tspage"]/b/following-sibling::*/text()')
