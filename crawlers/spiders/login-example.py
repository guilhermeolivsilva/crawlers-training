# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:42:29 2020

@author: Guilherme
"""


import scrapy

class SpiderWithLogin(scrapy.Spider):
    name = 'login-example'
    start_urls = ['http://quotes.toscrape.com/login']
    
    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'any', 'password': 'doesntmatter'},
            callback=self.after_login,
        )
        
    def after_login(self, response):
        for quote in response.selector.xpath('//div[@class="quote"]'):
            yield {
                'text': (quote.xpath('span[1]/text()').extract_first())[1:-1],
                'author': quote.xpath('span[2]/small/text()').extract_first(),
                'goodreads_profile': quote.xpath('span[2]/a[2]/@href').extract_first(),
                'tags': quote.xpath('div/a/text()').extract()
            }
            
        next_page = response.selector.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.after_login)