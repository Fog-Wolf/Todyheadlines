# -*- coding: utf-8 -*-
import scrapy


class TodyimageSpider(scrapy.Spider):
    name = 'TodyImage'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://toutiao.com/']

    def parse(self, response):
        pass
