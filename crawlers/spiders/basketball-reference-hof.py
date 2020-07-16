# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:35:44 2020

@author: Guilherme
"""


import scrapy

class BasketballReferenceHOF(scrapy.Spider):
    name = "basketball-reference-hof"
    start_urls = ['https://www.basketball-reference.com/']
    
    def parse(self, response):
        for hall_of_famer in response.selector.xpath('//*[@id="players"]/form[2]/div[1]/div/select/option')[1:]:
            item = {
                'player_name': hall_of_famer.xpath('text()').extract_first()
            }
            
            player_profile = hall_of_famer.xpath('@value').extract_first()
            yield scrapy.Request(
                response.urljoin(player_profile),
                meta = {'item': item},
                dont_filter = True,
                callback = self.parse_player_profile
            )
        
    def parse_player_profile(self, response):
        item = response.meta.get('item', {})
        item['stats'] = {
            'games_played': int(response.selector.xpath('//div[@class="p1"]/div[1]/p/text()').extract_first()),
            'points_per_game': float(response.selector.xpath('//div[@class="p1"]/div[2]/p/text()').extract_first()),
            'rebounds_per_game': float(response.selector.xpath('//div[@class="p1"]/div[3]/p/text()').extract_first()),
            'assists_per_game': float(response.selector.xpath('//div[@class="p1"]/div[4]/p/text()').extract_first())
        }
        
        yield item
    