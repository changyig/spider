# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['www.qidian.com']

    start_urls = ['https://www.qidian.com/all?orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0']

    def parse(self, response):
        data={}
        # print(response.text)

        res=response.xpath('//ul[@class="all-img-list cf"]')
        # res = response.xpath('//table[@class="rank-table-list all"]//tr[@data-rid]"]')
        # res = response.xpath('//div[@class="cleafix"]//*')
        print(res)
        with open("test3.html", "w", encoding='utf-8') as f:
            f.write(response.text)
        # for i in res:

        #     title=i.xpath('//span[@class="j_th_tit"]').extract_first()
        #     time = i.xpath('//span[@class="threadlist_reply_date pull_right j_reply_data"]').extract_first()
        #     pirnt(title)
        #     print(time)
        # pass