import json
import os
import sys
sys.path.append(os.getcwd())  # NOQA

import requests

from src.non_spiders.Base import Base


class Gdp(Base):
    def __init__(self, headless=True) -> None:
        super(Gdp, self).__init__()
        self.headless = headless

    def crawl_VN_GDP(self):
        # Getting cookie and token for finance.vietstock.vn request
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
                headless=self.headless
            )

            # TODO: recursively call this function until success

        # Request to finance.vietstock.vn
        url = "https://finance.vietstock.vn/data/reportdatabydisplay"

        payload = f"type=true&__RequestVerificationToken={token}"

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://finance.vietstock.vn',
            'Referer': 'https://finance.vietstock.vn/du-lieu-vi-mo',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cookie': cookie
        }

        number_of_tried = 0
        while number_of_tried < 5:
            try:
                number_of_tried += 1
                print(f'Trying to crawl VN_GDP for the {number_of_tried}th time(s)')
                response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue

        if number_of_tried == 5:
            message = f'Failed to crawl VN_GDP after {number_of_tried} times'
            print(message)
            return self.error_handler(message)

        if response.status_code != 200:
            message = f'Failed to crawl VN_GDP: status code {response.status_code}'
            print(message)
            return self.error_handler(message)

        try:
            data = response.json()

            if not isinstance(data, list):
                raise Exception('Response is not a valid list')

            report_term: list = data[1]['ReportTerm'].replace('Quý ', '').split('/')
            quarter: int = report_term[0]
            year: int = report_term[1]

            value: float = data[1]['Value']

            return {
                'status': 'success',
                'message': 'Crawled VN_GDP successfully',
                'data': {
                    'year': year,
                    'quarter': quarter,
                    'value': value
                }
            }

        except Exception as e:
            message = f'Failed to parse response to json: {str(e)}'
            print(message)
            return self.error_handler(message)

    def crawl_US_GDP(self):
        pass

    def crawl_CN_GDP(self):
        pass

    def crawl_JP_GDP(self):
        pass

    def crawl_UK_GDP(self):
        pass

    def crawl_GER_GDP(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    gdp_crawler = Gdp()
    print(gdp_crawler.crawl_VN_GDP())
