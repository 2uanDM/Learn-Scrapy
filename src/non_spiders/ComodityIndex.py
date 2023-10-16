import json
import os
import shutil 
import sys
import time
sys.path.append(os.getcwd())

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from src.non_spiders.Base import Base
from src.utils.selenium import ChromeDriver
from datetime import datetime, timedelta

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.database.schema import SchemaTopic2
from src.utils.io import write_csv

class ComodityIndex(Base):
    def __init__(self) -> None:
        return super().__init__()

    def get_price_gasoline_vn(self) -> dict:
        '''
            This method is used to get price of gasolines in Vietnam
            
            Return:
            ```python
            {
                'status': 'success',
                'message': 'Get price of Vietnam gasoline successfully',
                'data': {
                    'RON 95-III': float,
                    'DO 0,05S-II: float,
                }
            }
            ```
        '''
        url = "https://www.pvoil.com.vn/truyen-thong/tin-gia-xang-dau"
        payload = {}
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        number_of_try = 0
        
        while number_of_try < 5:
            try:
                number_of_try += 1
                print(f'Trying to get gasoline price in Vietnam from {url}: {number_of_try} time(s)')
                response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of gasoline price in Vietnam: {str(e)}')

        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        
        html_content = response.text.encode('utf8')
        error_with_table = True
        data = {}
        
        try:
            soup = bs(html_content, 'html.parser')
            xang_vn_table = soup.find('div', {'id': 'cctb-1'})
            tbody = xang_vn_table.find('tbody')
            rows = tbody.find_all('tr')
            
            # RON 95-III
            RON_95_cells = rows[0].find_all('td')
            DO_cells = rows[2].find_all('td')
            
            if RON_95_cells[1].text.strip().find('RON 95-III') != -1 and DO_cells[1].text.strip().find('DO 0,05S-II') != -1:
                data['RON 95-III'] = float(RON_95_cells[2].text.strip()) * 1000
                data['DO 0,05S-II'] = float(DO_cells[2].text.strip()) * 1000
                error_with_table = False
            
            if error_with_table:
                return self.error_handler(f'Cannot find table of gasoline in {url}')
            return {
                'status': 'success',
                'message': 'Get price of Vietnam gasoline successfully',
                'data': data
            }
            
        except Exception as e:
            return self.error_handler(f'Error when extracting price of table gasoline in url {url}: {str(e)}')
    
    def get_price_gold_vn(self) -> dict:
        '''
            Get gold price in Vietnam
        '''

        url = 'https://www.pnj.com.vn/blog/gia-vang/'
        
        number_of_try = 0
        
        while number_of_try < 5:
            try:
                number_of_try += 1
                print(f'Trying to get gold price in Vietnam from {url}: {number_of_try} time(s)')
                response = requests.get(url, timeout=10)
                break
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of gold price in Vietnam: {str(e)}')

        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        try:
            html_content = response.text.encode('utf8')
            soup = bs(html_content, 'html.parser')
            tbody = soup.find('tbody', {'id': 'content-price'})
            sjc_999_row = tbody.find_all('tr')[0]
            sjc_999_cells = sjc_999_row.find_all('td')

            if sjc_999_cells[0].text.strip().find('SJC 999.9') != -1:
                return {
                    'status': 'success',
                    'message': 'Get gold price (SJC 9999) in Vietnam successfully',
                    'data' : float(sjc_999_cells[2].text.strip().replace(',', '.')) * 10000000
                }
            else:
                return self.error_handler(f'Cannot find SJC 9999 in {url}')
        except Exception as e:
            return self.error_handler(f'Error when extracting gold price in url {url}: {str(e)}')
    
    def get_price_steel_vn(self) -> dict:
        '''
            Get steel price in Vietnam (CB240)
            
            Return example:
            ```python
            {
                'status': 'success',
                'message': 'Get steel price in Vietnam successfully',
                'data': float
            }
            ```
        '''
        
        url = "https://steelonline.vn/price-list"

        payload = {}
        headers = {
            'authority': 'steelonline.vn',
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
                print(f'Trying to get steel price in Vietnam from {url}: {number_of_try} time(s)')
                response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
                break 
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of steel price in Vietnam: {str(e)}')
        
        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        # Parse html content
        html_content = response.text.encode('utf8')
        
        try:
            soup = bs(html_content, 'html.parser')
            body = soup.find('body')
            table = body.find_all('table', {'class': 'price-board'})
            rows = table[0].find_all('tr')
            d6_row = rows[2]
            cells = d6_row.find_all('td')
            price_cell = cells
            
            if price_cell[4].text.strip() == '':
                return self.error_handler(f'Cannot find steel price type D6 in {url}')
            else:
                return {
                    'status': 'success',
                    'message': 'Get steel price in Vietnam successfully',
                    'data': float(price_cell[4].text.strip()) * 1000
                }
        except Exception as e:
            return self.error_handler(f'Error when extracting steel price in url {url}: {str(e)}')
        
    def get_price_wall_tile_vn(self) -> dict:
        url = "https://viglaceravietnam.com/gach-lat-nen-viglacera-ub304-30x30cm.htm"
        payload = {}
        headers = {
            'authority': 'viglaceravietnam.com',
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
                print(f'Trying to get wall tile price in Vietnam from {url}: {number_of_try} time(s)')
                response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of wall tile price in Vietnam: {str(e)}')
        
        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        # Parse html content
        
        try:
            html_content = response.text.encode('utf8')
            soup = bs(html_content, 'html.parser')
            info = soup.find('div', {'id': 'infoProduct'})
            price = info.find('span', {'class': 'price'})
            
            if price:
                if price.text.strip() == '':
                    return self.error_handler('Cannot find price')
                else:
                    price = price.text.strip()[:-3]
                    price = price.replace(',', '.')
                    return {
                        'status': 'success',
                        'message': 'Get wall tile price in Vietnam successfully',
                        'data': float(price) * 1000
                    }
            else:
                return self.error_handler('Cannot find price')
        except Exception as e:
            return self.error_handler(f'Error when extracting wall tile price in url {url}: {str(e)}')
            
    def get_price_electricity_vn(self) -> dict:
        '''
            Get the electricity price in Vietnam (type 3)
        '''
        url = "https://calc.evn.com.vn/TinhHoaDon/api/Calculate"
        
        current_date: str = datetime.now().strftime('%d/%m/%Y')
        last_moth_date: str = (datetime.strptime(current_date, '%d/%m/%Y') - timedelta(days=29)).strftime('%d/%m/%Y')

        payload = json.dumps({
            "KIMUA_CSPK": "0",
            "LOAI_DDO": "1",
            "SO_HO": 1,
            "MA_CAPDAP": "1",
            "NGAY_DKY": last_moth_date,
            "NGAY_CKY": current_date,
            "NGAY_DGIA": "01/01/1900",
            "HDG_BBAN_APGIA": [
                {
                "LOAI_BCS": "KT",
                "TGIAN_BANDIEN": "KT",
                "MA_NHOMNN": "SHBT",
                "MA_NGIA": "A"
                }
            ],
            "GCS_CHISO": [
                {
                "BCS": "KT",
                "SAN_LUONG": "101",
                "LOAI_CHISO": "DDK"
                }
            ]
            })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://calc.evn.com.vn',
            'Referer': 'https://calc.evn.com.vn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        number_of_try = 0
        
        while number_of_try < 5:
            try:
                number_of_try += 1
                print(f'Trying to get electricity price in Vietnam from {url}: {number_of_try} time(s)')
                response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of electricity price in Vietnam: {str(e)}')
        
        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        try:
            data = json.loads(response.text)
            if data['Data'] == {}:
                return self.error_handler('Cannot find electricity price. Check the timeframe in payload again!')

            list_prices: list = data['Data']['HDN_HDONCTIET']
            
            # print(json.dumps(list_prices, indent=4))
            price_per_kwh_type_3: float = list_prices[-1]['DON_GIA']

            return {
                'status': 'success',
                'message': 'Get electricity price in Vietnam successfully',
                'data': price_per_kwh_type_3
            }
        except Exception as e:
            return self.error_handler(f'Error when extracting electricity price in url {url}: {str(e)}')
    
    def get_metal_price_shfe(self, headless: bool = True, use_proxy: bool = False) -> dict:
        '''
            Get metal price from shfe website using selenium
        '''
        
        auth_proxy = {
            'host' : '168.227.140.130',
            'port' : 12345,
            'username' : 'ebay2023',
            'password' : 'proxyebaylam'
        }
        
        download_folder = os.path.join(os.getcwd(), 'download', 'shfe')
                
        if use_proxy:
            driver = ChromeDriver(headless=headless, 
                                authenticate_proxy=auth_proxy, 
                                download_path=download_folder).driver
        else:
            driver = ChromeDriver(headless=headless,
                                  download_path=download_folder).driver

        def download_csv(url, driver):
            driver.get(url)

            WebDriverWait(driver,20).until(EC.visibility_of_element_located((
                By.ID,'product_futures_delayMarket_table'
            )))

            driver.execute_script("""
                                // Function to click the button when the table content is loaded
                                function clickButtonWhenTableLoaded() {
                                // Get the table element
                                var table = document.getElementById("product_futures_delayMarket_table");

                                // Check if the table content is loaded
                                if (table && table.rows.length > 0) {
                                    // Get the button element
                                    var button = document.querySelector("#delayedExcel > span");

                                    // Click the button
                                    button.click();
                                } else {
                                    // Table content is not loaded yet, so wait for the DOMContentLoaded event to fire
                                    document.addEventListener("DOMContentLoaded", clickButtonWhenTableLoaded);
                                }
                                }

                                // Call the function initially
                                clickButtonWhenTableLoaded();                     
                                """)

            time.sleep(2)
        
        def parse_csv(type: int):
            '''
                type: int
                    ```
                    0: steel
                    1: copper
                    2: aluminum
                    ```
            '''
            if type not in (0,1,2):
                print(f'Invalid type: {type} when parsing the csv of shfe')
                return self.error_handler(f'Invalid type: {type} when parsing the csv of shfe')
            
            file_names = os.listdir(download_folder)
            file_name = f'data_{type}.csv'
            
            if file_name not in file_names:
                print()
                return self.error_handler(f'Cannot find csv file: {file_name}')
            try:
                # Read csv file using pandas
                df = pd.read_csv(os.path.join(download_folder, file_name), header=1)
                
                # Get the index of row where Contract is "rb2310"
                # if type == 0:
                #     index = df[df['Contract'] == 'rb2310'].index[0]
                # elif type == 1:
                #     index = df[df['Contract'] == 'cu2310'].index[0]
                # else: 
                #     index = df[df['Contract'] == 'al2310'].index[0]

                # HOT FIX: rb2310 -> rb2311
                if type == 0:
                    index = df[df['Contract'] == 'rb2311'].index[0]
                elif type == 1:
                    index = df[df['Contract'] == 'cu2311'].index[0]
                else: 
                    index = df[df['Contract'] == 'al2311'].index[0]
                    
                price = df.iloc[index]['Last']
                
                if price is None or price == '':
                    return self.error_handler(f'Cannot find price in csv file: {file_name}')
                else:
                    return {
                        'status': 'success',
                        'message': 'Get metal price from shfe successfully',
                        'data': price
                    }
            except Exception as e:
                return self.error_handler(f'Error when parsing csv file: {file_name} of shfe: {str(e)}')
        
        steel_url = 'https://www.shfe.com.cn/eng/market/futures/metal/rb/'
        copper_url = 'https://www.shfe.com.cn/eng/market/futures/metal/cu/'
        aluminum_url = 'https://www.shfe.com.cn/eng/market/futures/metal/al/' 
    
        shutil.rmtree(download_folder)
        os.makedirs(download_folder, exist_ok=True)
    
        for i, url in enumerate([steel_url, copper_url, aluminum_url]):
            print(f'Accessing url: ', url)
            download_csv(url, driver)
            file_name = f'data_{i}.csv'
            os.rename(os.path.join(download_folder, 'data.csv'), os.path.join(download_folder, file_name))
        
        driver.quit()
        
        # Now parsing newly downloaded csv files
        print('Parsing csvs...')
        try:
            rb_price = parse_csv(type=0)
            cu_price = parse_csv(type=1)
            al_price = parse_csv(type=2)
        except Exception as e:
            return self.error_handler(f'Error when parsing csv files of shfe: {str(e)}')

        if rb_price['status'] == 'error':
            return self.error_handler(f'Error when parsing csv files of shfe: {rb_price["message"]}')
        if cu_price['status'] == 'error':
            return self.error_handler(f'Error when parsing csv files of shfe: {cu_price["message"]}')
        if al_price['status'] == 'error':
            return self.error_handler(f'Error when parsing csv files of shfe: {al_price["message"]}')
        
        return {
            'status': 'success',
            'message': 'Get metal price from shfe successfully',
            'data': {
                'steel': rb_price['data'],
                'copper': cu_price['data'],
                'aluminum': al_price['data']
            }
        }
    
    def get_result(self, func, args: tuple = None):
        number_of_try = 0
        
        while number_of_try < 5:
            try:
                result = func(*args) if args else func()
                if result.get('status') == 'error':
                    number_of_try += 1
                    print(f'Trying to get {func.__name__} result again since data is None: {number_of_try} time(s)')
                    continue
                else:
                    return result
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when getting {func.__name__} results after 5 times:')
        
        if result.get('status') == 'error':
            return self.error_handler(f'Error when getting {func.__name__} results: {result["message"]}')
    
    def run(self):
        errors = []
        worldwide_gold_price_usd        = None
        vn_gold_price_vnd               = None
        ron95_price_vnd                 = None
        do_price_vnd                    = None
        brent_oil_price_usd             = None
        raw_oil_price_usd               = None
        vn_electric_price_vnd           = None
        worldwide_steel_price_usd       = None
        worldwide_copper_price_usd      = None
        worldwide_aluminium_price_usd   = None
        china_steel_price_cny           = None
        china_copper_price_cny          = None
        china_aluminium_price_cny       = None
        vn_steel_price_vnd              = None 
        wall_tiles_price_vnd            = None
        dji                             = None
        ssec                            = None 
        nikkei                          = None 
        kospi                           = None 
        dax                             = None 
        cac40                           = None 
        ftse100                         = None
        
        # ------------------------------------------------------------
    
        worldwide_gold_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/currencies/xau-usd",1)
        )
        
        if worldwide_gold_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/currencies/xau-usd",1)
            })
        else:
            worldwide_gold_price_usd = worldwide_gold_price_usd['data']
            print('Worldwide gold price', worldwide_gold_price_usd)
        
        # ------------------------------------------------------------
        
        vn_gold_price_vnd = self.get_result(
            self.get_price_gold_vn
        )
        
        if vn_gold_price_vnd['status'] == 'error':
            errors.append({
                'func': self.get_price_gold_vn,
                'args': None
            })
        else:
            vn_gold_price_vnd = vn_gold_price_vnd['data']
            print('VN gold price', vn_gold_price_vnd)
            
        # ------------------------------------------------------------
        gasoline_price_vn = self.get_result(
            self.get_price_gasoline_vn
        )
        
        if gasoline_price_vn['status'] == 'error':
            errors.append({
                'func': self.get_price_gasoline_vn,
                'args': None
            })
        else:
            ron95_price_vnd = gasoline_price_vn['data']['RON 95-III']
            do_price_vnd = gasoline_price_vn['data']['DO 0,05S-II']
            print('Gasoline price', gasoline_price_vn)
            
        # ------------------------------------------------------------
        brent_oil_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/commodities/brent-oil-historical-data",3)
        )
        
        if brent_oil_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/commodities/brent-oil-historical-data",3)
            })
        else:
            brent_oil_price_usd = brent_oil_price_usd['data']
            print('Brent oil price', brent_oil_price_usd)
        
        # ------------------------------------------------------------
        raw_oil_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/currencies/wti-usd",1)
        )
        
        if raw_oil_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/currencies/wti-usd",1)
            })
        else:
            raw_oil_price_usd = raw_oil_price_usd['data']
            print('Raw oil price', raw_oil_price_usd)
        
        # ------------------------------------------------------------
        vn_electric_price_vnd = self.get_result(
            self.get_price_electricity_vn
        )
        
        if vn_electric_price_vnd['status'] == 'error':
            errors.append({
                'func': self.get_price_electricity_vn,
                'args': None
            })
        else:
            vn_electric_price_vnd = vn_electric_price_vnd['data']
            print('VN electricity price', vn_electric_price_vnd)
        
        # ------------------------------------------------------------
        worldwide_steel_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/commodities/us-steel-coil-futures-streaming-chart",2)
        )   
        
        if worldwide_steel_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/commodities/us-steel-coil-futures-streaming-chart",2)
            })
        else:
            worldwide_steel_price_usd = worldwide_steel_price_usd['data']
            print('Worldwide steel price', worldwide_steel_price_usd)
        
        # ------------------------------------------------------------
        worldwide_copper_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/commodities/copper",3)
        )
        
        if worldwide_copper_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/commodities/copper",3)
            })
        else:
            worldwide_copper_price_usd = worldwide_copper_price_usd['data']
            print('Worldwide copper price', worldwide_copper_price_usd)
        
        # ------------------------------------------------------------
        worldwide_aluminium_price_usd = self.get_result(
            self.get_price_vn_investing,
            ("https://vn.investing.com/commodities/aluminum",3)
        )
        
        if worldwide_aluminium_price_usd['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ("https://vn.investing.com/commodities/aluminum",3)
            })
        else:
            worldwide_aluminium_price_usd = worldwide_aluminium_price_usd['data']
            print('Worldwide aluminum price', worldwide_aluminium_price_usd)
        
        # ------------------------------------------------------------
        vn_steel_price_vnd = self.get_result(
            self.get_price_steel_vn
        )
        
        if vn_steel_price_vnd['status'] == 'error':
            errors.append({
                'func': self.get_price_steel_vn,
                'args': None
            })
        else:
            vn_steel_price_vnd = vn_steel_price_vnd['data']
            print('VN steel price', vn_steel_price_vnd)
        
        # ------------------------------------------------------------
        wall_tiles_price_vnd = self.get_result(
            self.get_price_wall_tile_vn
        )
        
        if wall_tiles_price_vnd['status'] == 'error':
            errors.append({
                'func': self.get_price_wall_tile_vn,
                'args': None
            })
        else:
            wall_tiles_price_vnd = wall_tiles_price_vnd['data']
            print('Wall tiles price', wall_tiles_price_vnd)
        
        # ------------------------------------------------------------
        dji = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/us-30-historical-data',3)
        )
        
        if dji['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/us-30-historical-data',3)
            })
        else:
            dji = dji['data']
            print('DJI', dji)
        
        # ------------------------------------------------------------
        ssec = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/shanghai-composite-historical-data',3)
        )
        
        if ssec['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/shanghai-composite-historical-data',3)
            })
        else:
            ssec = ssec['data']
            print('SSEC', ssec)
        
        # ------------------------------------------------------------
        nikkei = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/japan-ni225',3)
        )

        if nikkei['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/japan-ni225',3)
            })
        else: 
            nikkei = nikkei['data']
            print('Nikkei', nikkei)
        
        # ------------------------------------------------------------
        kospi = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/kospi',3)
        )
        
        if kospi['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/kospi',3)
            })
        else:
            kospi = kospi['data']
            print('KOSPI', kospi)
        
        # ------------------------------------------------------------
        dax = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/germany-30',3)
        )
        
        if dax['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/germany-30',3)
            })
        else: 
            dax = dax['data']
            print('DAX', dax)
        
        # ------------------------------------------------------------
        cac40 = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/france-40-historical-data',3)
        )
        
        if cac40['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/france-40-historical-data',3)
            })
        else:
            cac40 = cac40['data']
            print('CAC 40', cac40)
        
        # ------------------------------------------------------------
        ftse100 = self.get_result(
            self.get_price_vn_investing,
            ('https://vn.investing.com/indices/uk-100-historical-data',3)
        )
        
        if ftse100['status'] == 'error':
            errors.append({
                'func': self.get_price_vn_investing,
                'args': ('https://vn.investing.com/indices/uk-100-historical-data',3)
            })
        else:
            ftse100 = ftse100['data']
            print('FTSE 100', ftse100)
        
        # ------------------------------------------------------------
        
        metal_shfe = self.get_result(
            self.get_metal_price_shfe,
            (False, False)
        )
        
        if metal_shfe['status'] == 'error':
            errors.append({
                'func': self.get_metal_price_shfe,
                'args': None
            })
        else: 
            china_steel_price_cny = metal_shfe['data']['steel']
            china_copper_price_cny = metal_shfe['data']['copper']
            china_aluminium_price_cny = metal_shfe['data']['aluminum']
            print('Shfe metal price', metal_shfe['data'])
        
        # ------------------------------------------------------------
        if len(errors) > 0:
            print('*******Errors*******', len(errors))
            # TODO: send email to admin using Telegram bot API
            return
        else:
            print('*******No errors*******')
        
        new_data = SchemaTopic2().chi_so_hang_hoa(
            date=datetime.strptime(self.date_slash.strip(), '%m/%d/%Y'),
            worldwide_gold_price_usd=float(worldwide_gold_price_usd),
            vn_gold_price_vnd=float(vn_gold_price_vnd),
            ron95_price_vnd=float(ron95_price_vnd),
            do_price_vnd=float(do_price_vnd),
            brent_oil_price_usd=float(brent_oil_price_usd),
            raw_oil_price_usd=float(raw_oil_price_usd),
            vn_electric_price_vnd=float(vn_electric_price_vnd),
            worldwide_steel_price_usd=float(worldwide_steel_price_usd),
            worldwide_copper_price_usd=float(worldwide_copper_price_usd),
            worldwide_aluminium_price_usd=float(worldwide_aluminium_price_usd),
            china_steel_price_cny=float(china_steel_price_cny),
            china_copper_price_cny=float(china_copper_price_cny),
            china_aluminium_price_cny=float(china_aluminium_price_cny),
            vn_steel_price_vnd=float(vn_steel_price_vnd),
            wall_tiles_price_vnd=float(wall_tiles_price_vnd),
            dji=float(dji),
            ssec=float(ssec),
            nikkei=float(nikkei),
            kospi=float(kospi),
            dax=float(dax),
            cac40=float(cac40),
            ftse100=float(ftse100)
        )
        
        print('*******New data*******\n', new_data)
        
        # -------------Adding to database-------------------
        self.db.update_collection('chi_so_hang_hoa',new_data)
        print('*******Update database successfully*******')

if __name__ == '__main__':
    comodity_index = ComodityIndex()
    comodity_index.run()
    
    
    
    
    
