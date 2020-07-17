# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 09:58:54 2020

@author: Guilherme
"""


import scrapy
import js2xml

class HMJs2XmlSpider(scrapy.Spider):
    name = 'hm-js2xml'
    start_urls = ['https://www2.hm.com/en_gb/productpage.0437668004.html']
    
    def parse(self, response):
        js_code = response.xpath('//script[contains(., "productArticleDetails")]/text()').extract_first()
        parsed_js = js2xml.parse(js_code)
        product_details = parsed_js.xpath('//var[@name="productArticleDetails"]/object')[0]
        data = js2xml.jsonlike.make_dict(product_details)
        
        for product in (v for k, v in data.items() if k.isdigit()):
            yield {
                'description': product['description'],
                'original_price': product['whitePriceValue'],
                #'discounted_price': product['redPriceValue'],
                'color': product['name'],
                'url': product['url']
            }