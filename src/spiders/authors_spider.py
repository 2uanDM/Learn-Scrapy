from typing import Any

import scrapy
from datetime import datetime
import os
from scrapy.http import Request

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    RESULT_DIR = os.path.join(os.path.dirname(os.getcwd()), 'results')
    
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]
    
    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        print('Initializing spider...')
        
        if not os.path.exists(self.RESULT_DIR):
            os.makedirs(self.RESULT_DIR)
        
    def parse(self, response):
        print('-'*90)
        print('Parsing response in url:', response.url)
        
        # Parse author data in current page
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        # # Parse next page (recursive)
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
            
        # Parse all pages 
        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)
        
    def parse_author(self, response):
        print('Parsing author in url:', response.url)
        
        author_name = response.css('.author-title::text').get()
        
        born_date: str = response.css('.author-born-date::text').get()
        born_year: str = born_date.split(',')[1].strip()
        born_month: str = born_date.split(',')[0].split()[0].strip() # January, February, etc.
        born_day: str = born_date.split(',')[0].split()[1].strip()
        
        # Convert into suitable format
        dob = datetime.strptime(f'{born_year} {born_month} {born_day}', '%Y %B %d').date()
        dob_str = datetime.strftime(dob, '%d/%m/%Y')

        born_location: str = response.css('.author-born-location::text').get()
        born_location: str = born_location.replace('in','').strip()
        
        bio: str = response.css(".author-description::text").get().strip()
        
        # Save author data
        data = {
            'name': author_name,
            'dob' : dob_str,
            'born_location': born_location,
            'bio': bio
        }
        
        yield data