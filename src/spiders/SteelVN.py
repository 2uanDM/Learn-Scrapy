from typing import Any, Iterable
import scrapy
from bs4 import BeautifulSoup as bs
from pathlib import Path


class SteelVN(scrapy.Spider):
    name = 'SteelVN'
    
    start_urls = ['https://steelonline.vn/price-list']
    
    def parse(self, response) -> Any:
        filename = 'hihi.html'
        
        # Decode the response content to utf-8
        html_content = response.content.decode('utf-8')
        
        Path(filename).write_text(html_content)
        self.log(f'Saved file {filename}')