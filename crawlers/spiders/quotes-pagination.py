# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:10:25 2020

@author: Guilherme
"""

import scrapy

class QuotesPaginationSpider(scrapy.Spider):
    name = "quotes-pagination"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.selector.xpath('//div[@class="quote"]'):
            yield {
                'text': (quote.xpath('span[1]/text()').extract_first())[1:-1],
                'author': quote.xpath('span[2]/small/text()').extract_first(),
                'tags': quote.xpath('div/a/text()').extract()
            }
            
        next_page = response.selector.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)