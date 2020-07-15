# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:38:42 2020

@author: Guilherme
"""

import scrapy
import re

#%%
"""
First approach

class BooksSpider(scrapy.Spider):
    name = "books"
            
    def start_requests(self):
        urlList = open('misc/urls.txt', 'r').readlines()
        requests = []
        
        for url in urlList:
            requests.append(scrapy.Request(url = url, callback = self.parse))
        
        return requests
    
    def parse(self, response):
        self.log(f'I have just visited {response.url}')

"""
#%%
class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = open('misc/urls.txt', 'r').readlines()
    ratingsDict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
        
    def parse(self, response):
        title = response.selector.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        rating = str(re.findall(
                                "[A-Z].*", 
                                response.selector.xpath('//p[contains(@class, "star-rating")]/@class').extract_first()
                               )[0]
                    )
        
        
        
        price = float(re.findall(
                                "[\d].\.[\d].",
                                response.selector.xpath('//div[@class="col-sm-6 product_main"]/p/text()').extract_first()
                                )[0]
                     )
        stock = int(re.findall(
                                "[\d].",
                                response.selector.xpath('//p[@class="instock availability"]/text()').extract()[1]
                              )[0]
                    )
        category = response.selector.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').extract_first()
        
        yield {
            'title': title,
            'rating': self.ratingsDict.get(rating),
            'price': price,
            'stock': stock,
            'category': category
        }