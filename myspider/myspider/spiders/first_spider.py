# -*- coding: utf-8 -*-
import scrapy


class FirstSpiderSpider(scrapy.Spider):
    name = 'first_spider'
    allowed_domains = ['www.44txt.com']
    start_urls = ['http://www.44txt.com/xuanhuanqihuan/index_3.html']

    def parse(self, response):
        res=response.xpath('//div[@class="listBox"]//li')
        next_url=response.xpath('//div[@class="tspage"]/b/following-sibling::*/text()')
        digit=int(next_url.extract()[0])
       	print(digit)
       	if  digit<=10:
       		print('当前页码：%s'%(digit))
       		for x in res:
	       		item={}
	       		
	       		item['title']=x.xpath('./a/text()').extract_first()
	        	item['author']=x.xpath('./div[@class="s"]/a/text()').extract_first()
	       		
	       		yield item
	       	next_url="http://www.44txt.com/xuanhuanqihuan/index_%s.html"%(digit)
	       	print('下一页:%s'%(next_url))
       		yield scrapy.Request(
       				next_url,
       				callback=self.parse
       			)
       	else :
       		print('页码大于10')
