import json
import os
import sys
sys.path.append(os.getcwd())  # NOQA

import requests

from datetime import datetime
from src.non_spiders.Base import Base
from src.utils.database.schema import SchemaTopic2
from pymongo.errors import DuplicateKeyError


class Credit(Base):
    def __init__(self) -> None:
        super().__init__()

    def crawl(self, **kwargs):
        """
        This method is used to crawl the data and pushing it to the database

        Args:
        ```
            - headless: bool
            - from_year: int
            - to_year: int
            - from_month: int
            - to_month: int
            - token: str
            - cookie: str
        ```

        Returns:
            ```
            None
            ```
        """
        # Get the keyword arguments
        headless = kwargs.get('headless', True)
        from_year = kwargs.get('from_year', datetime.now().year)
        to_year = kwargs.get('to_year', datetime.now().year)
        from_month = kwargs.get('from_month', 1)
        to_month = kwargs.get('to_month', 12)

        try:
            with open(self.vietstock_config_path, 'r', encoding='utf8') as f:
                config = json.load(f)
                token = config.get('token')
                cookie = config.get('cookie')
            print('Loaded cookie and token from config.json successfully')
        except Exception as e:
            print(f'Loading config.json failed: {str(e)}')
            self.generate_cookie_and_csrf_token_finance_vietstock(
                url='https://finance.vietstock.vn/du-lieu-vi-mo/51/tin-dung.htm',
                headless=headless
            )
            result = self.crawl(from_year=from_year, to_year=to_year, from_month=from_month, to_month=to_month)
            if result['status'] == 'success':
                return
            else:
                return self.crawl(from_year=from_year, to_year=to_year, from_month=from_month, to_month=to_month)

        # Get the credit from post req
        print('Fetching credit from finance.vietstock.vn...')
        url = "https://finance.vietstock.vn/data/reportdatatopbynormtype"
        payload = f"type=2&fromYear={from_year}&toYear={to_year}&from={from_month}&to={to_month}&normTypeID=51&page=0&pages=0&__RequestVerificationToken={token}"
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie,
            'Origin': 'https://finance.vietstock.vn',
            'Referer': 'https://finance.vietstock.vn/du-lieu-vi-mo/51/tin-dung.htm',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        number_of_tried = 0

        while number_of_tried < 5:
            try:
                number_of_tried += 1
                print(f'Try to get credit from {url}: {number_of_tried} time(s)')
                response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue

        if number_of_tried == 5:
            message = f'Cannot fetch credit from {url} after {number_of_tried} times'
            print(message)
            return self.error_handler(message)

        if response.status_code != 200:
            message = f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}'
            print(message)
            return self.error_handler(message)

        # Parse the response and push to the database
        try:
            data_dict = json.loads(response.text)
        except Exception as e:
            # If the response is not in json format, that means the token is invalid
            message = f'Cannot parse the response from {url} to json: {str(e)}'
            print(message)
            print('Getting cookie and csrf token from finance.vietstock.vn...')

            self.generate_cookie_and_csrf_token_finance_vietstock(
                url='https://finance.vietstock.vn/du-lieu-vi-mo/51/tin-dung.htm',
                headless=headless
            )

            result = self.crawl(from_year=from_year, to_year=to_year, from_month=from_month, to_month=to_month)
            if result['status'] == 'success':
                return
            else:
                return self.crawl(from_year=from_year, to_year=to_year, from_month=from_month, to_month=to_month)

        # Process the data

        new_data = []
        founded_month = {}

        # Find the founded month
        for item in data_dict['data']:
            if item.get('NormValue') is None:
                continue
            else:
                report_time: str = item['ReportTime']
                report_time = report_time.replace('Tháng', '').strip()
                if report_time not in founded_month:
                    founded_month[report_time] = {
                        'tin_dung': None,
                        'cung_tien_m2': None,
                        'tang_truong_tin_dung': None,
                        'tang_truong_cung_tien_m2': None
                    }

        if founded_month == {}:
            message = f'No new data found'
            print(message)
            return self.error_handler('no_new_data_found')

        print(f'Found {len(founded_month)} new month data')

        # Find the value of each month
        for item in data_dict['data']:
            if item.get('NormValue') is None:
                continue
            else:
                report_time: str = item['ReportTime']
                report_time = report_time.replace('Tháng', '').strip()

                norm_name = item.get('NormName')
                if norm_name == 'Tăng trưởng Cung tiền M2 (YoY)':
                    founded_month[report_time]['tang_truong_cung_tien_m2'] = item['NormValue']
                elif norm_name == 'Tăng trưởng tín dụng (YoY)':
                    founded_month[report_time]['tang_truong_tin_dung'] = item['NormValue']
                elif norm_name == 'Cung tiền M2 (MoM)':
                    founded_month[report_time]['cung_tien_m2'] = item['NormValue']
                elif norm_name == 'Tín dụng (MoM)':
                    founded_month[report_time]['tin_dung'] = item['NormValue']

        # Prepare the data to push to the database
        for key, value in founded_month.items():
            month, year = key.split('/')
            data = SchemaTopic2().tin_dung(
                date_created=datetime.now(),
                month=int(month),
                year=int(year),
                tin_dung=value['tin_dung'],
                cung_tien_m2=value['cung_tien_m2'],
                tang_truong_tin_dung=value['tang_truong_tin_dung'],
                tang_truong_cung_tien_m2=value['tang_truong_cung_tien_m2']
            )
            try:
                action = self.db.update_collection(collection_name='tin_dung', data=data)
                print('Insert new data to mongodb successfully: ', action)
            except DuplicateKeyError:
                print(f'Data for month {month} and year {year} already existed')
                continue

        return {
            'status': 'success',
            'message': 'Insert new data to mongodb successfully',
            'data': None
        }

    def run(self):
        self.crawl(headless=True)


if __name__ == '__main__':
    credit = Credit()
    credit.crawl(headless=True)
