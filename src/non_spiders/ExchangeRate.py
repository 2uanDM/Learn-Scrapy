import os 
import sys
sys.path.append(os.getcwd())
import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
import pandas as pd

from src.utils.logger import logger

class ExchangeRate:
    def __init__(self) -> None:
        self.date_slash = datetime.now().strftime('%Y/%m/%d')
        self.date_dash = datetime.now().strftime('%Y-%m-%d')
        
    def get_dollar_index_DXY(self):
        print('Getting dollar index DXY')
        
        url = "https://vn.investing.com/currencies/us-dollar-index-historical-data"

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
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }

        # Parse the response using BeautifulSoup
        soup = bs(response.text, 'html.parser')
        
        # Get the text of element with id="last_last"
        dollar_index: str = soup.find(id='last_last')
        
        if dollar_index is not None and dollar_index != '':
            return {
                'status': 'success',
                'message': 'Get dollar index DXY successfully',
                'data': dollar_index.text
            }
        else:
            logger('Cannot get valid dollar index DXY')
            return {
                'status': 'error',
                'message': 'Cannot get valid dollar index DXY',
                'data': None
            }


    def get_exchange_rate(self):
        pass

    def run(self):
        response = self.get_dollar_index_DXY()
        print(response)

if __name__=='__main__':
    exchange_rate = ExchangeRate()
    exchange_rate.run()