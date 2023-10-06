import os 
import sys
sys.path.append(os.getcwd())

import requests

from src.utils.logger import logger
from bs4 import BeautifulSoup as bs
from datetime import datetime

class Base():
    def __init__(self) -> None:
        self.date_slash = datetime.now().strftime('%m/%d/%Y')
        self.date_dash = datetime.now().strftime('%Y-%m-%d')
        self.data_today = f'{self.date_slash}'
    
    def error_handler(self, message: str) -> dict:
        """
            This method is used to handle error in the class
        Args:
            message (str): The error message

        Returns:
            ```python
            {
                'status': 'error',
                'message': message,
                'data': None
            }
            ```
        """
        logger(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }
    
    def get_price_vn_investing(self, url: str, type: int):
        '''
            This method is used to get price from vn.investing.com (whose price block is defined by class "instrument-price_last")
            
            Args:
            - `url`: The url to get price
            - `type`: The type of price block
            
            ```python
            1: Price block is defined by class "instrument-price_last"
            2: Price block is defined by id "last_last"
            ```
            
            Return 
            ```python
            {
                'status': 'success',
                'message': 'Get gold price worldwide successfully',
                'data': price: str
            }
            ```
        '''
        payload = {}
        headers = {
            'authority': 'vn.investing.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        try:
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
        except Exception as e:
            message = f'An error occurs: {str(e)}'
            return self.error_handler(message)

        soup = bs(response.text, 'html.parser')
        
        if type == 1:
            price_block = soup.find('div', {'data-test': 'instrument-header-details'})
            
            if price_block is None:
                message = f'Cannot find price block (type {type}) in {url}'
                return self.error_handler(message)
            
            price_selector = price_block.find('span', {'data-test': 'instrument-price-last'})
            
            if price_selector is None or price_selector.text.strip() == '':
                message = f'Cannot find price selector (type {type}) in {url}'
                return self.error_handler(message)
            
            price: str = price_selector.text.strip()
        elif type == 2:
            # Get the text of element with id="last_last"
            price_selector = soup.find(id='last_last')
            
            if price_selector is None or price_selector == '':
                message = f'Cannot find price selector (type {type}) in {url}'
                return self.error_handler(message)

            price: str = price_selector.text.strip()
        else:
            message = f'Type of selector must be 1 or 2 in {url}. Value: {type}'
            return self.error_handler(message)
        
        return {
            'status': 'success',
            'message': 'Get price from vn investing successfully',
            'data': price
        }