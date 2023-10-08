import os 
import sys
sys.path.append(os.getcwd())

import requests
from bs4 import BeautifulSoup as bs
from src.non_spiders.Base import Base

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
                print(f'Trying to get gasoline price in Vietnam: {number_of_try} time(s)')
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
                print(f'Trying to get gold price in Vietnam: {number_of_try} time(s)')
                response = requests.get(url)
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
                print(f'Trying to get steel price in Vietnam: {number_of_try} time(s)')
                response = requests.request("GET", url, headers=headers, data=payload, timeout=20),
                break 
            except Exception as e:
                continue
        
        if number_of_try == 5:
            return self.error_handler(f'Error when fetching url: {url} of steel price in Vietnam: {str(e)}')
        
        if response.status_code != 200:
            return self.error_handler(f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}')
        
        # Parse html content
        html_content = response.text.encode('utf8')
        soup = bs(html_content, 'html.parser')
        
        
        
            
    def run(self):
        worldwide_gold_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/currencies/xau-usd",
            type=1
        )
        print('Gold', worldwide_gold_price_usd)
        
        raw_oil_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/currencies/wti-usd",
            type=1
        )
        print('Raw oil', raw_oil_price_usd)
        
        steel_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/commodities/us-steel-coil-futures-streaming-chart",
            type=2
        )       
        print('Steel', steel_price_usd)
        
        copper_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/commodities/copper",
            type=3
        )
    
        print('Copper', copper_price_usd)
        
        aluminum_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/commodities/aluminum",
            type=3
        )
        print('Aluminium', aluminum_price_usd)
        
        brent_oil_price_usd = self.get_price_vn_investing(
            url="https://vn.investing.com/commodities/brent-oil-historical-data",
            type=3
        )
        print('Brent oil', brent_oil_price_usd)
        
        dji_price_usd = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/us-30-historical-data',
            type = 3
        )
        print('DJI', dji_price_usd)
        
        ssec_price_cny = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/shanghai-composite-historical-data',
            type = 3
        )
        print('SSEC', ssec_price_cny)
        
        nikkei_price_jpy = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/japan-ni225',
            type = 3
        )
        print('Nikkei', nikkei_price_jpy)
        
        kospi_price_krw = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/kospi',
            type = 3
        )
        print('KOSPI', kospi_price_krw)
        
        dax_price_eur = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/germany-30',
            type = 3
        )
        print('DAX', dax_price_eur)
        
        cac_40_price_eur = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/france-40-historical-data',
            type = 3
        )
        print('CAC 40', cac_40_price_eur)
        
        ftse_100_price_gbp = self.get_price_vn_investing(
            url = 'https://vn.investing.com/indices/uk-100-historical-data',
            type = 3
        )
        print('FTSE 100', ftse_100_price_gbp)


if __name__ == '__main__':
    comodity_index = ComodityIndex()
    
    comodity_index.run()
    print(comodity_index.get_price_gasoline_vn())
    print(comodity_index.get_price_gold_vn())
    
    
    
    
    
