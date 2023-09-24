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
        'https://quotes.toscrape.com/page/2/',
    ]
    
    
    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        
        if not os.path.exists(self.HTML_DIR):
            os.makedirs(self.HTML_DIR)
    
    # def start_requests(self) -> Iterable[Request]:
    #     urls = [
    #         'https://quotes.toscrape.com/page/1/',
    #         'https://quotes.toscrape.com/page/2/',
    #     ]

    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            data: dict = {
                "text": quote.css('span.text::text').get(),
                "author" : quote.css('small.author::text').getall(),
                "tags" : quote.css('div.tags a.tag::text').getall()
            }
            yield data