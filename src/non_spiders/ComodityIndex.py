import os 
import sys
sys.path.append(os.getcwd())

import requests
from bs4 import BeautifulSoup as bs

from src.non_spiders.Base import Base

class ComodityIndex(Base):
    def __init__(self) -> None:
        return super().__init__()
    
    def get_gold_price_worldwide(self):
        '''
            This method is used to get gold price worldwide
            ```python
            {
                'status': 'success',
                'message': 'Get gold price worldwide successfully',
                'data': price: str
            }
            ```
        '''
        print('Getting gold price worldwide...')
        
        url = "https://vn.investing.com/currencies/xau-usd"

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
        
        price_block = soup.find('div', {'data-test': 'instrument-header-details'})
        
        price_selector = price_block.find('span', {'data-test': 'instrument-price-last'})
        
        if price_selector is None:
            # Address of this line of code:
            message = f'Cannot find price block in {url}'
            return self.error_handler(message)
        
        price: str = price_selector.text.strip()
        
        return {
            'status': 'success',
            'message': 'Get gold price worldwide successfully',
            'data': price
        }


if __name__ == '__main__':
    comodity_index = ComodityIndex()
    worldwide_gold_price_usd = comodity_index.get_gold_price_worldwide()
    
    print(worldwide_gold_price_usd)
