import pandas as pd
import base64
import io
import json
import requests
import os
import sys
sys.path.append(os.getcwd())  # NOQA

from datetime import datetime
from src.utils.io import write_csv
from src.utils.database.schema import SchemaTopic2
from src.utils.crawler import run_crawler
from src.non_spiders.Base import Base


class ExchangeRate(Base):
    def __init__(self) -> None:
        return super().__init__()

    def get_dollar_index_DXY(self):
        print('Getting dollar index DXY')
        url = "https://vn.investing.com/currencies/us-dollar-index-historical-data"

        return self.get_price_vn_investing(url=url, type=2)

    def __parse_excel_file(self, file_dir: str) -> dict:
        '''
            Return data = 
            ```python
            {
                'USD': {
                    'buy_cash': 23000,
                    'buy_transfer': 23000,
                    'sell': 23000
                },
                ...
            }
            ```
        '''
        output: dict = {}

        try:
            df = pd.read_excel(file_dir, engine='openpyxl')
            # Just get the 3 row of USD, EUR, CNY
            df = df.iloc[[21, 7, 5]]
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
        except Exception as e:
            return self.error_handler('An error occurs when parsing the exchange rate Excel file: ' + str(e))

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
            return self.error_handler(message)
        if response.status_code != 200:
            message = f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}'
            return self.error_handler(message)

        data = json.loads(response.text)
        if data['FileName'] is not None:
            # Download excel file to local
            try:
                file_name = data["FileName"]
                save_folder = os.path.join(os.getcwd(), 'download')
                os.makedirs(save_folder, exist_ok=True)
                save_dir = os.path.join(save_folder, file_name)

                data = base64.b64decode(data['Data'])
                with io.open(save_dir, 'wb') as f:
                    f.write(data)

                print(f'Save exchange rate excel file: {file_name} successfully')
            except Exception as e:
                return self.error_handler('An error occurs when saving the exchange rate excel file: ' + str(e))
        else:
            message = f'Does not have exchange rate file for today: {self.date_slash}'
            return self.error_handler(message)

        # Parse excel file
        print('Parsing exchange rate excel file...')
        try:
            data = self.__parse_excel_file(save_dir)
        except Exception as e:
            message = 'An error occurs when parsing the exchange rate excel file: ' + str(e)
            return self.error_handler(message)

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
        save_folder = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results')
        run_crawler(spider_name='NHNN_ExchangeRate', nolog=True,
                    filename='exchange_rate.jsonl', save_folder=save_folder, overwrite=True)

        try:
            with open(os.path.join(save_folder, 'exchange_rate.jsonl'), 'r') as f:
                data = json.load(f)
        except Exception as e:
            message = 'An error occurs when reading the exchange rate jsonl file: ' + str(e)
            return self.error_handler(message)

        if data['status'] == 'error':
            message = 'An error occurs when getting the exchange rate from NHNN website:' + data['message']
            return self.error_handler(message)

        print('Get exchange rate from NHNN website successfully')
        return {
            'status': 'success',
            'message': 'Get exchange rate from NHNN successfully',
            'data': data
        }

    def run(self):
        # ---------====================Parse the dollar index DXY====================---------
        print('-'*100)
        response_dollar_index = self.get_dollar_index_DXY()

        if response_dollar_index['status'] == 'error':
            print(response_dollar_index['message'])
            return
        print(f'Dollar index DXY: {response_dollar_index["data"]}')

        # ---------====================Parse the exchange rate from VCB====================---------
        print('-'*100)
        response_VCB = self.get_exchange_rate_VCB(self.date_dash)
        if response_VCB['status'] == 'error':
            print(response_VCB['message'])
            return
        print(f'Exchange rate from VCB: {json.dumps(response_VCB["data"], indent=4, ensure_ascii=False)}')

        # ---------====================Parse the exchange rate from NHNN====================---------
        print('-'*100)
        response_NHNN = self.get_exchange_rate_NHNN()
        if response_NHNN['status'] == 'error':
            print(response_NHNN['message'])
            response_NHNN['data'] = {
                'USD': '0,0',
                'EUR': '0,0',
                'CNY': '0,0'
            }
        print(f'Exchange rate from NHNN: {json.dumps(response_NHNN["data"], indent=4, ensure_ascii=False)}')

        # ---------====================Merge the data====================---------
        print('-'*100)
        data_VCB = response_VCB['data']
        data_NHNN = response_NHNN['data']

        new_data = SchemaTopic2().ty_gia(
            date=datetime.strptime(self.date_slash.strip(), '%m/%d/%Y'),
            dollar_index_dxy=float(response_dollar_index['data']),
            usd_vcb=data_VCB['USD']['sell'],
            usd_nhnn=self.__parse_float_for_NHNN(data_NHNN['USD']),
            eur_vcb=data_VCB['EUR']['sell'],
            eur_nhnn=self.__parse_float_for_NHNN(data_NHNN['EUR']),
            cny_vcb=data_VCB['CNY']['sell'],
            cny_nhnn=self.__parse_float_for_NHNN(data_NHNN['CNY']),
        )

        print(new_data)

        # Push the data to mongodb
        try:
            self.db.update_collection(
                collection_name='ty_gia',
                data=new_data
            )
            print('Insert new data to mongodb successfully')

        except Exception as e:
            print('An error occurs when creating new data for mongodb: ' + str(e))
            return self.error_handler('An error occurs when creating new data for mongodb: ' + str(e))

    def __parse_float_for_NHNN(self, value: str):
        if value.find(',') != -1:
            integer, decimal = value.split(',')
            integer = integer.replace('.', '')
            return float(f'{integer}.{decimal}')
        else:
            integer = value.replace('.', '')
            return float(integer)


if __name__ == '__main__':
    exchange_rate = ExchangeRate()
    exchange_rate.run()
