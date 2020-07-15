# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:00:20 2020

@author: Guilherme
"""


import scrapy

class QuotesAuthorsSpider(scrapy.Spider):
    name = "quotesnauthors"
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    
    def parse(self, response):
        for quote in response.selector.xpath('//div[@class="quote"]'):
            item = {
                'text': (quote.xpath('span[1]/text()').extract_first())[1:-1],
                'tags': quote.xpath('div/a/text()').extract()
            }
            
            author_url = quote.xpath('span[2]/a/@href').extract_first()
            yield scrapy.Request(
                response.urljoin(author_url),
                meta = {'item': item},
                dont_filter = True,
                callback = self.parse_author_page
            )
        
        next_page = response.selector.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)
            
    def parse_author_page(self, response):
        item = response.meta.get('item', {})
        item['author'] = {
            'name': response.selector.xpath('//h3[@class="author-title"]/text()').extract_first(default='').strip(),
            'birth_date': response.selector.xpath('//span[@class="author-born-date"]/text()').extract_first(),
            'birth_place': str(response.selector.xpath('//span[@class="author-born-location"]/text()').extract_first())[3:]
        }
        
        yield item