# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:15:54 2020

@author: Guilherme
"""


import json
import scrapy

class QuotesWithScroll(scrapy.Spider):
    name = 'quotes-with-scroll'
    base_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [base_url.format(1)]
    
    def parse(self, response):
        json_data = json.loads(response.text)
        for quote in json_data['quotes']:
            yield quote
        if json_data['has_next']:
            yield scrapy.Request(
                self.base_url.format(int(json_data['page']) + 1)
            )