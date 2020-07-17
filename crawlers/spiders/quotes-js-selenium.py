# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:29:37 2020

@author: Guilherme
"""


import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class QuotesJsSpider(scrapy.Spider):
    name = 'quotes-js-selenium'
    start_urls = [
        'http://quotes.toscrape.com/js'
    ]

    def __init__(self, *args, **kwargs):
        # phantomjs binary must be somewhere in your PATH
        #self.driver = webdriver.PhantomJS("tools/drivers/win/phantomjs.exe")
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        
        # for non-headless mode, just remove the options param from the function below
        self.driver = webdriver.Chrome("tools/drivers/win/chromedriver.exe", options = self.chrome_options)
        super(QuotesJsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.driver.get(response.url)
        sel = scrapy.Selector(text=self.driver.page_source)
        for quote in sel.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        next_page = sel.css('li.next > a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))