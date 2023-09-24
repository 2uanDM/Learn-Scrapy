from pathlib import Path

import scrapy
import os

class AuthorSpider(scrapy.Spider):
    name = 'authors'
    RESULT_DIR = os.path.join(os.path.dirname(os.getcwd()), 'results')
    
    
    
    start_urls = [
        
    ]
    
    def __init__(self, name, **kwargs):
        super().init(name, **kwargs)
        print('Initializing spider...')
        
        if not os.path.exists(self.RESULT_DIR):
            os.makedirs(self.RESULT_DIR)
        
    