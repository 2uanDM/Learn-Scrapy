from pathlib import Path
from typing import Any, Iterable, Optional

import scrapy
import os
from scrapy.http import Request

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    HTML_DIR = os.path.join(os.path.dirname(os.getcwd()), 'folder_htmls')
    
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]
    
    
    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        
        print('Initiating spider...')
        
        if not os.path.exists(self.HTML_DIR):
            os.makedirs(self.HTML_DIR)

    def parse(self, response):
        print('Current page: ', response.url)
        for quote in response.css('div.quote'):
            data: dict = {
                "text": quote.css('span.text::text').get(),
                "author" : quote.css('small.author::text').getall(),
                "tags" : quote.css('div.tags a.tag::text').getall()
            }
            yield data
        
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)