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

    def get_exchange_rate_VCB(self):
        """
            Run the spider to get the exchange rate from VCB website in form of jsonl file
        """
        print('Getting exchange rate from VCB website...')
        save_folder = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results')
        run_crawler(spider_name='VCB_ExchangeRate', nolog=True,
                    filename='vcb_exchange_rate.jsonl', save_folder=save_folder, overwrite=True)

        try:
            with open(os.path.join(save_folder, 'vcb_exchange_rate.jsonl'), 'r') as f:
                data = json.load(f)
        except Exception as e:
            message = 'An error occurs when reading the exchange rate jsonl file: ' + str(e)
            return self.error_handler(message)

        if data['status'] == 'error':
            message = 'An error occurs when getting the exchange rate from VCB website:' + data['message']
            return self.error_handler(message)

        # Process data:
        exrate_to_get = {}

        try:
            exchange_rate_prices: list = data['data']['ExrateList']['Exrate']

            for item in exchange_rate_prices:
                currency_code = item['@CurrencyCode']
                if currency_code in ['USD', 'EUR', 'CNY']:
                    exrate_to_get[currency_code] = item['@Sell']

        except Exception as e:
            message = 'An error occurs when processing the exchange rate data: ' + str(e)
            return self.error_handler(message)

        print('Get exchange rate from VCB website successfully')
        return {
            'status': 'success',
            'message': 'Get exchange rate from VCB successfully',
            'data': exrate_to_get
        }

    def get_exchange_rate_NHNN(self):
        print('Getting exchange rate from NHNN website...')
        save_folder = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results')
        run_crawler(spider_name='NHNN_ExchangeRate', nolog=True,
                    filename='nhnn_exchange_rate.jsonl', save_folder=save_folder, overwrite=True)

        try:
            with open(os.path.join(save_folder, 'nhnn_exchange_rate.jsonl'), 'r') as f:
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
            'data': data['data']
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
        response_VCB = self.get_exchange_rate_VCB()
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
            usd_vcb=self.__parse_float_for_VCB(data_VCB['USD']),
            usd_nhnn=self.__parse_float_for_NHNN(data_NHNN['USD']),
            eur_vcb=self.__parse_float_for_VCB(data_VCB['EUR']),
            eur_nhnn=self.__parse_float_for_NHNN(data_NHNN['EUR']),
            cny_vcb=self.__parse_float_for_VCB(data_VCB['CNY']),
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

    def __parse_float_for_NHNN(self, value: str) -> float:
        if value.find(',') != -1:
            integer, decimal = value.split(',')
            integer = integer.replace('.', '')
            return float(f'{integer}.{decimal}')
        else:
            integer = value.replace('.', '')
            return float(integer)

    def __parse_float_for_VCB(self, value: str) -> float:
        return float(value.replace(',', ''))


if __name__ == '__main__':
    exchange_rate = ExchangeRate()
    exchange_rate.run()

    # data = exchange_rate.get_exchange_rate_VCB()
    # data1 = exchange_rate.get_exchange_rate_NHNN()
    # print(json.dumps(data, indent=4, ensure_ascii=True))
