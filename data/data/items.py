# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    # define the fields for your item here like:
    createtime = scrapy.Field()
    url = scrapy.Field()
    keyword = scrapy.Field()
    info = scrapy.Field()
    # pass
