# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:19:50 2020

@author: Guilherme
"""

import scrapy

class QuotesPaginationSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
    
    def parse(self, response):
        # Visits authors' details pages
        for link in response.selector.xpath('//div[@class="quote"]/span[2]/a/@href').extract():
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_author_page
            )        
        
        # Navigates to the next listing page
        next_page = response.selector.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(
                url = response.urljoin(next_page),
                callback=self.parse
            )

    # Extracts the author data            
    def parse_author_page(self, response):
        yield {
            'name': response.selector.xpath('//h3[@class="author-title"]/text()').extract_first(default='').strip(),
            'birth_date': response.selector.xpath('//span[@class="author-born-date"]/text()').extract_first(),
            'birth_place': str(response.selector.xpath('//span[@class="author-born-location"]/text()').extract_first())[3:]
        }