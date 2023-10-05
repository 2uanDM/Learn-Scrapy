import os 
import sys
sys.path.append(os.getcwd())

import requests
import json
import io
import base64
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup as bs
from src.utils.logger import logger
from src.utils.crawler import run_crawler

class ExchangeRate:
    def __init__(self) -> None:
        self.date_slash = datetime.now().strftime('%Y/%m/%d')
        self.date_dash = datetime.now().strftime('%Y-%m-%d')
        self.data_today = f'{self.date_slash}'
        
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

    def __parse_excel_file(self, file_dir: str) -> dict:
        '''
            Return data = {
                'USD': {
                    'buy_cash': 23000,
                    'buy_transfer': 23000,
                    'sell': 23000
                },
                ...
            }
        '''
        output: dict = {}
        
        df = pd.read_excel(file_dir, engine='openpyxl')

        # Just get the 3 row of USD, EUR, CNY
        df = df.iloc[[21,7,5]]
        # Rename columns
        df.columns = ['Name', 'Symbol', 'Buy Cash', 'Buy Transfer', 'Sell']
        # Reset index
        df = df.reset_index(drop=True)
        # Extracting data
        for row in df.iterrows():
            symbols = ['USD', 'EUR', 'CNY']
            current_symbol = row[1]['Symbol']
            if current_symbol in symbols:
                output[current_symbol] = {
                    'buy_cash': row[1]['Buy Cash'],
                    'buy_transfer': row[1]['Buy Transfer'],
                    'sell': row[1]['Sell']
                }
        
        return output
            
    def get_exchange_rate_VCB(self, date_dash: str):
        '''
            date_dash: str, format: '%Y-%m-%d'
        '''
        
        # Download excel files 
        print('Downloading exchange rate from VCB website...')
        
        url = f'https://www.vietcombank.com.vn/api/exchangerates/exportexcel?date={date_dash}'
        
        try:
            response = requests.get(url=url, timeout=10)
        except Exception as e:
            message = f'An error occurs: {str(e)}'
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }
        
        data = json.loads(response.text)
        if data['FileName'] is not None:
            # Download excel file to local
            try:
                file_name = f'{data["FileName"]}.xlsx'
                save_dir = os.path.join(os.getcwd(), 'download', file_name)
                
                data = base64.b64decode(data['Data'])
                with io.open(save_dir, 'wb') as f:
                    f.write(data)
                    
                print(f'Save exchange rate excel file: {file_name} successfully')
            except Exception as e:
                message = 'An error occurs when downloading the exchange rate excel file: ' +  str(e)
                print(message)
                logger(message)
                return {
                    'status': 'error',
                    'message': message,
                    'data': None
                }
        else:
            message = f'Does not have exchange rate file for today: {self.date_slash}'
            print(message)
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }

        # Parse excel file
        print('Parsing exchange rate excel file...')
        try:
            data = self.__parse_excel_file(save_dir)
        except Exception as e:
            message = 'An error occurs when parsing the exchange rate excel file: ' +  str(e)
            print(message)
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }
        
        # Delete excel file
        os.remove(save_dir)
        print('Delete exchange rate excel file successfully')
        
        return {
            'status': 'success',
            'message': 'Get exchange rate successfully',
            'data': data
        }
        
    def get_exchange_rate_NHNN(self):
        print('Getting exchange rate from NHNN website...')
        save_folder = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results', 'NHNN')
        run_crawler(spider_name='NHNN', nolog=True, filename='exchange_rate.jsonl', save_folder=save_folder, overwrite=True)
        print('Get exchange rate from NHNN website successfully')
        
        try:
            with open(os.path.join(save_folder, 'exchange_rate.jsonl'), 'r') as f:
                data = json.load(f)
        except Exception as e:
            message = 'An error occurs when reading the exchange rate jsonl file: ' +  str(e)
            print(message)
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }
        
        if data['status'] == 'error':
            message = 'An error occurs when getting the exchange rate from NHNN website'
            print(message)
            logger(message)
            return {
                'status': 'error',
                'message': message,
                'data': None
            }
        
        return {
            'status': 'success',
            'message': 'Get exchange rate successfully',
            'data': data
        }
    
    def run(self):
        response = self.get_dollar_index_DXY()
        
        if response['status'] == 'success':
            self.data_today += f',{response["data"]}'
        else:
            print(response['message'])
            return
        
        response = self.get_exchange_rate_VCB(self.date_dash)
        
        if response['status'] == 'success':
            self.data_today += f',{response["data"]["USD"]["buy_cash"]},{response["data"]["EUR"]["buy_cash"]},{response["data"]["CNY"]["buy_cash"]}'

if __name__=='__main__':
    exchange_rate = ExchangeRate()
    print(exchange_rate.get_exchange_rate_NHNN())