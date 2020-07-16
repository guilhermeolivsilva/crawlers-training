# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:45:19 2020

@author: Guilherme
"""


import scrapy

class MyFirstPostSpider(scrapy.Spider):
    name = 'my-first-post-spider'
    
    def start_requests(self):
        formdata= {
            'custname': 'Teste',
            'custtel': '111333',
            'custemail': '123@mail.com',
            'size': 'small',
            'topping': ['bacon', 'cheese', 'mushroom'],
            'delivery': '12:30',
            'comments': '!'
        }
        
        yield scrapy.FormRequest(
            'http://httpbin.org/post',
            formdata = formdata,
            callback = self.parse_form_results
        )
        
    def parse_form_results(self, response):
        self.log(response.body)