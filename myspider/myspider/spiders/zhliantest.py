# -*- coding: utf-8 -*-
import scrapy


class ZhiliantestSpider(scrapy.Spider):
    name = 'zhiliantest'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou']

    def start_requests(self):
        print(123)
        new_url=self.start_urls[0]
        print(new_url)
        formdata = {
            'start': 0,
            'pageSize': '90',
            'cityId': 931,
            'workExperience': -1,
            'education': -1,
            'companyType': -1,
            'employmentType': -1,
            'jobWelfareTag': -1,
            'kw': 'python',
            'kt': 3,
            '_v': '0.00882343',
            'x-zp-page-request-id': '',
            'x-zp-client-id': ''
        }
        yield scrapy.FormRequest(url=new_url, formdata=formdata, callback=self.parse)
    def parse(self, response):
        print(333)
    #     new_url=self.start_urls[0]
    #     # print(self.new_url)
    #     formdata = {
    #             'start': start,
    #              'pageSize': '90',
    #              'cityId': cityId,
    #              'workExperience': -1,
    #              'education': -1,
    #              'companyType': -1,
    #              'employmentType': -1,
    #              'jobWelfareTag': -1,
    #              'kw': search_keywords,
    #              'kt': 3,
    #              '_v': '0.00882343',
    #              'x-zp-page-request-id': '',
    #              'x-zp-client-id': ''
    #         }
    #     yield scrapy.FormRequest(url=new_url, formdata=formdata, callback=self.parse)
    # def detai(self, response):
    #     print(response.text)