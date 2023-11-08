import json
import os
import sys
sys.path.append(os.getcwd())  # NOQA

import requests

from src.utils.logger import logger
from bs4 import BeautifulSoup as bs
from datetime import datetime

from src.utils.database.mongodb import MongoDB
from src.utils.selenium import ChromeDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Base():

    vietstock_config_path = os.path.join(os.getcwd(), 'config', 'vietstock.json')

    def __init__(self) -> None:
        self.date_slash = datetime.now().strftime('%m/%d/%Y')
        self.date_dash = datetime.now().strftime('%Y-%m-%d')
        self.data_today = ''
        self.db = MongoDB('topic2')

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
            3: Price block is defined by class "text-5xl/9 font-bold md:text-[42px] md:leading-[60px] text-[#232526]"
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

        number_of_try = 0

        while number_of_try < 5:
            try:
                number_of_try += 1
                print(f'Try to get price from vn investing from {url}: {number_of_try} time(s)')
                response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue

        if number_of_try == 5:
            message = f'Cannot fetch vn investing html from {url} after {number_of_try} times'
            return self.error_handler(message)

        if response.status_code != 200:
            message = f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}'
            return self.error_handler(message)

        # Ensure that beautifulsoup can parse unicode characters
        soup = bs(response.content.decode('utf-8'), 'html.parser')

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
        elif type == 3:
            price_selector = soup.find('div', {'class': 'text-5xl'})

            if price_selector is None or price_selector == '':
                # Handle special case
                result = self.__handle_special_case_type_3(response.content.decode('utf-8'))
                if result['status'] == 'error':
                    message = f'Cannot find price selector (type {type}) in {url}'
                    return self.error_handler(message)
                else:
                    price = result['data']
            else:
                price: str = price_selector.text.strip()
        else:
            message = f'Type of selector must be 1,2 or 3 in {url}. Value: {type}'
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get price from vn investing successfully',
            'data': float(price.replace(',', ''))
        }

    def generate_cookie_and_csrf_token_finance_vietstock(self, url: str, headless: bool = True):
        # Get csrf token from finance.vietstock.vn
        self.driver = ChromeDriver(headless=headless).driver

        number_of_tried = 0

        while number_of_tried < 5:
            try:
                number_of_tried += 1

                print(f'Try to get cookie and csrf token from {url}: {number_of_tried} time(s)')

                self.driver.get(url=url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "__CHART_AjaxAntiForgeryForm"))
                )
                break
            except Exception as e:
                continue

        if number_of_tried == 5:
            message = f'Cannot get cookie and csrf token from {url} after {number_of_tried} times'
            return self.error_handler(message)

        # Get the page source
        try:
            html_str = self.driver.page_source
            soup = bs(html_str, 'html.parser')
            form = soup.find('form', {'id': '__CHART_AjaxAntiForgeryForm'})
            token: str = form.find('input', {'name': '__RequestVerificationToken'}).get('value')
            print(f'****Token founded****')
        except Exception as e:
            message = f'Cannot get page source from {url}: {str(e)}'
            print(message)
            return self.error_handler(message)

        # Get the cookie
        try:
            cookie = self.driver.get_cookies()

            # Parse the cookie into a string that can be used in the header
            cookie_str = ''
            for c in cookie:
                cookie_str += f"{c['name']}={c['value']}; "
            cookie_str = cookie_str[:-2]

            print(f'****Cookie founded****')
        except Exception as e:
            message = f'Cannot get cookie from {url}: {str(e)}'
            print(message)
            return self.error_handler(message)

        self.driver.quit()

        with open(self.vietstock_config_path, 'w', encoding='utf8') as f:
            f.write(json.dumps({'cookie': cookie_str, 'token': token}, indent=4, ensure_ascii=False))

        print('Generate new cookie and csrf token of finance.vietstock.vn successfully')

    def __handle_special_case_type_3(self, html_str: str):
        # Search for the first occurence of the string '<div class="text-5xl'
        try:
            start_index_open_div = html_str.find('<div class="text-5xl')
            end_index_open_div = html_str.find('>', start_index_open_div)

            # Search for the first occurence of the string '</div>'
            start_index_close_div = html_str.find('</div>', end_index_open_div)

            soup = bs(html_str[start_index_open_div: start_index_close_div + len('</div>')], 'html.parser')
            price = soup.find('div').text.strip()
        except Exception as e:
            message = f'An error occurs: {str(e)}'
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get price from vn investing successfully',
            'data': price
        }
