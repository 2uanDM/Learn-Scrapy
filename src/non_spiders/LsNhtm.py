import os
import shutil 
import sys
import time

import requests
sys.path.append(os.getcwd())

from src.non_spiders.Base import Base

from src.utils.selenium import ChromeDriver
from src.utils.pdf_parser import extract_tcb, extract_stb

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

class LsNhtm(Base):
    def __init__(self):
        super().__init__()
        
    def parse_vcb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table', {'class': 'table-responsive'})
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            
            data = {}
            
            for row in rows:
                cells = row.find_all('td')
                ky_han = cells[0].text.strip()
                rate = float(cells[1].text.replace('%', '').strip())
                
                if ky_han == 'Không kỳ hạn':
                    ky_han = 'khong_ky_han'
                else:
                    ky_han = ky_han.replace(' tháng', '_thang')
                
                if ky_han == '48_thang':
                    break
                
                if ky_han == '12_thang':
                    data[ky_han] = rate
                    data['18_thang'] = None
                    
                data[ky_han] = rate
            
            del data['7 ngày']
            del data['14 ngày']
            del data['2_thang']
            
            return {
                'status': 'success',
                'message': 'Parse VCB successfully',
                'data': data
            }
        except Exception as e:
            message = f'Error when parse LS NHTM VCB: {str(e)}'
            print(message)
            return self.error_handler(message)
        
    def parse_mb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            # Remove all attribute in html tag
            for tag in soup.find_all(True):
                tag.attr = {}
            block = soup.find('div', {'id':'card-info0'})
            block_2 = block.find('div' ,{'class' : 'detail-panel-body'})
            table = block_2.find('table')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')

            data = {}

            for row in rows[1:]:
                cells = row.find_all('td')
                ky_han = cells[0].text.strip()
                lai_tra_sau: float = float(cells[1].text.strip().replace('%', ''))
                
                if ky_han == 'KKH':
                    ky_han = 'khong_ky_han'
                else:
                    number: int = int(ky_han.split(' ')[0])
                    ky_han = f'{number}_thang'
                
                if ky_han == '48_thang':
                    break
                
                data[ky_han] = lai_tra_sau
            
            # Remove unnecessary data
            del data['2_thang']
            del data['4_thang']
            del data['5_thang']
            del data['7_thang']
            del data['8_thang']
            del data['10_thang']
            del data['11_thang']
            del data['13_thang']
            del data['15_thang']
            
            return {
                'status': 'success',
                'message': 'Parse MB successfully',
                'data': data
            }
        except Exception as e:
            message = f'Error when parse LS NHTM MB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_tcb(self, html_str: str):
        try:
            # -----------------------Get the link to download pdf file-----------------------
            soup = bs(html_str, 'html.parser')
            div_link = soup.find('div', {'class': 'PreviewPdf_buttonOpenDialog__jTAky previewPdfMode'})
            link = div_link.find('a')['href']

            # Check if the link is valid
            if link.find('techcombank.com') == -1:
                raise Exception('Link is not valid')
        
            # -----------------------Download the pdf file to temp folder-----------------------
            download_folder = os.path.join(os.getcwd(), 'download', 'tcb')
            shutil.rmtree(download_folder)
            os.makedirs(download_folder)
            
            headers = {
                'authority': 'techcombank.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
            }           
            
            response = requests.request("GET", link, headers=headers, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f'Error when download pdf file from {link}')
            
            with open(os.path.join(download_folder, 'tcb.pdf'), 'wb') as f:
                f.write(response.content)
            
            # -----------------------Parse the pdf file-----------------------
            time.sleep(1)
            result = extract_tcb()
            
            if result['status'] == 'error':
                raise Exception(result['message'])
            
            return result
            
        except Exception as e:
            message = f'Error when parse LS NHTM TCB: {str(e)}'
            print(message)
            return self.error_handler(message)
        
    def parse_stb(self, html_str: str):
        try:
            # -----------------------Get the link to download pdf file-----------------------
            soup = bs(html_str, 'html.parser')
            div_link = soup.find('div', {'class': 'div-download__lang--wrapper'})
            data_href = div_link.find('p')['data-href']
            link = f'https://www.sacombank.com.vn{data_href}'
            
            if link.find('sacombank/files/cong-cu/lai-suat') == -1:
                raise Exception('Link is not valid')
            
            # -----------------------Download the pdf file to temp folder-----------------------
            download_folder = os.path.join(os.getcwd(), 'download', 'stb')
            shutil.rmtree(download_folder)
            os.makedirs(download_folder)
            
            headers = {
                'authority': 'www.sacombank.com.vn',
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
            
            response = requests.request("GET", link, headers=headers, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f'Error when download pdf file from {link}')
            
            with open(os.path.join(download_folder, 'stb.pdf'), 'wb') as f:
                f.write(response.content)
            
            # -----------------------Parse the pdf file-----------------------
            result = extract_stb()
            
            if result['status'] == 'error':
                raise Exception(result['message'])
            
            return result
            
        except Exception as e:
            message = f'Error when parse LS NHTM STB: {str(e)}'
            print(message)
            return self.error_handler(message)    
    
    def parse_agribank(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table') # Find the first table
            tbody = table.find('tbody')
            
            rows = tbody.find_all('tr')
            
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            # Khong ky han data 
            khong_ky_han = float(rows[0].find_all('td')[1].text.strip().replace('%', ''))
            data = {'khong_ky_han': khong_ky_han}
            
            # The rest data
            rest_rows = rows[1:]
            
            for row in rest_rows[:-1]:
                cells = row.find_all('td')
                
                num_month = int(cells[0].text.strip().split(' ')[0])
                
                if num_month in months:
                    lai_suat = float(cells[1].text.strip().replace('%', ''))
                    data[f'{num_month}_thang'] = lai_suat
            
            data['36_thang'] = None
            
            return {
                'status': 'success',
                'message': 'Parse Agribank successfully',
                'data': data
            }
                
        except Exception as e:
            message = f'Error when parse LS NHTM Agribank: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_bid(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            div_table = soup.find('div', {'id': 'rates'})
            tbody = div_table.find('tbody')
            
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            data = {}
            rows = tbody.find_all('tr')
            
            # Khong ky han data
            khong_ky_han = float(rows[1].find_all('td')[3].text.strip().replace('%', ''))
            data['khong_ky_han'] = khong_ky_han
            
            # The rest data
            for row in rows[2:]:
                cells = row.find_all('td')
                num_month = int(cells[1].text.strip().split(' ')[0])
                
                if num_month in months:
                    lai_suat = float(cells[3].text.strip().replace('%', ''))
                    data[f'{num_month}_thang'] = lai_suat
            
            return {
                'status': 'success',
                'message': 'Parse BID successfully',
                'data': data
            }
        
        except Exception as e:
            message = f'Error when parse LS NHTM BID: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_ctg(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table', {'id': 'hor-ex-b'})
            tbody = table.find('tbody')
            
            rows = tbody.find_all('tr')
            
            data = {}
            
            # Khong ky han data
            khong_ky_han = float(rows[3].find_all('td')[1].text.strip().replace(',', '.'))
            data['khong_ky_han'] = khong_ky_han
            
            # 1 thang data
            mot_thang = float(rows[5].find_all('td')[1].text.strip().replace(',', '.'))
            data['1_thang'] = mot_thang
            
            # 3 thang data
            ba_thang = float(rows[7].find_all('td')[1].text.strip().replace(',', '.'))
            data['3_thang'] = ba_thang
            
            # 6 thang data
            sau_thang = float(rows[10].find_all('td')[1].text.strip().replace(',', '.'))
            data['6_thang'] = sau_thang
            
            # 9 thang data
            chin_thang = float(rows[13].find_all('td')[1].text.strip().replace(',', '.'))
            data['9_thang'] = chin_thang
            
            # 12 thang data
            mot_nam = float(rows[16].find_all('td')[1].text.strip().replace(',', '.'))
            data['12_thang'] = mot_nam
            
            # 18 thang data
            muoi_ky = float(rows[18].find_all('td')[1].text.strip().replace(',', '.'))
            data['18_thang'] = muoi_ky
            
            # 24 thang data
            hai_nam = float(rows[19].find_all('td')[1].text.strip().replace(',', '.'))
            data['24_thang'] = hai_nam
            
            # 36 thang data
            ba_nam = float(rows[20].find_all('td')[1].text.strip().replace(',', '.'))
            data['36_thang'] = ba_nam
            
            return {
                'status': 'success',
                'message': 'Parse CTG successfully',
                'data': data
            }
        
        except Exception as e:
            message = f'Error when parse LS NHTM CTG: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_tpb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table', {'class': 'table_laisuat'})
            
            tbody = table.find('tbody')
            
            rows = tbody.find_all('tr')
            
            data = {}
            
            # Khong ky han data
            data['khong_ky_han'] = None
            
            # 1 thang data
            mot_thang = float(rows[0].find_all('td')[2].text.strip())
            data['1_thang'] = mot_thang
            
            # 3 thang data
            ba_thang = float(rows[1].find_all('td')[2].text.strip())
            data['3_thang'] = ba_thang
            
            # 6 thang data
            sau_thang = float(rows[2].find_all('td')[2].text.strip())
            data['6_thang'] = sau_thang
            
            # 9 thang data
            data['9_thang'] = None
            
            # 12 thang data
            mot_nam = float(rows[3].find_all('td')[2].text.strip())
            data['12_thang'] = mot_nam
            
            # 18 thang data
            muoi_ky = float(rows[4].find_all('td')[2].text.strip())
            data['18_thang'] = muoi_ky
            
            # 24 thang data
            hai_nam = float(rows[5].find_all('td')[2].text.strip())
            data['24_thang'] = hai_nam
            
            # 36 thang data
            ba_nam = float(rows[6].find_all('td')[2].text.strip())
            data['36_thang'] = ba_nam
            
            return {
                'status': 'success',
                'message': 'Parse TPB successfully',
                'data': data
            }
            
            
        except Exception as e:
            message = f'Error when parse LS NHTM TPB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def __crawl(self, driver, type: str, url: str):
        # Get the the page
        driver.get(url)
        
        parse_by_pdf = ['tcb', 'stb']
        parse_by_bs4 = ['vcb', 'mb','bid', 'agribank']
        
        if type in parse_by_bs4:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'table')) # Wait for the table to load
            ) 
        elif type in parse_by_pdf:
            # Wait for all elements loaded
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'a')) # Wait for the link to download pdf file
            )
        
        time.sleep(2)
        
        html_str = driver.page_source
        
        if type == 'vcb':
            return self.parse_vcb(html_str)
        elif type == 'mb':
            return self.parse_mb(html_str)
        elif type == 'tcb':
            return self.parse_tcb(html_str)
        elif type == 'stb':
            return self.parse_stb(html_str)
        elif type == 'agribank':
            return self.parse_agribank(html_str)
        elif type == 'bid':
            return self.parse_bid(html_str)
        elif type == 'ctg':
            return self.parse_ctg(html_str)
        elif type == 'tpb':
            return self.parse_tpb(html_str)


        time.sleep(0.5)

    def crawl_selenium(self) -> dict:
        """
            This method used to crawl pages which required to use selenium
            
            Return 
            ```python
            {
                'status': 'success',
                'message': 'Crawl Selenium pages successfully',
                'data' : {
                    'vcb': {
                        'khong_ky_han': float,
                        '1_thang': float,
                        '3_thang': float,
                        '6_thang': float,
                        ...
                    }
                }
            }
            ```
        """
        
        driver = ChromeDriver(headless=False).driver
        
        vcb_url = 'https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/KHCN---Lai-suat'
        mb_url = 'https://www.mbbank.com.vn/Fee'
        tcb_url = 'https://techcombank.com/cong-cu-tien-ich/bieu-phi-lai-suat'
        stb_url = 'https://www.sacombank.com.vn/cong-cu/lai-suat.html/cf/lai-suat/tien-gui.html'
        agribank_url = 'https://www.agribank.com.vn/vn/lai-suat'
        bid_url = 'https://bidv.com.vn/vn/tra-cuu-lai-suat'
        ctg_url = 'https://www.vietinbank.vn/khaixuandonloc/lai-suat/'
        tpb_url = 'https://tpb.vn/cong-cu-tinh-toan/lai-suat'
        
        # print(self.__crawl(driver, 'vcb', vcb_url))
        # print(self.__crawl(driver, 'mb', mb_url))
        # print(self.__crawl(driver, 'tcb', tcb_url))
        # print(self.__crawl(driver, 'stb', stb_url)) 
        # print(self.__crawl(driver, 'agribank', agribank_url))
        # print(self.__crawl(driver, 'bid', bid_url))
        # print(self.__crawl(driver, 'ctg', ctg_url))
        # print(self.__crawl(driver, 'tpb', tpbank_url))
        
        
        driver.quit()
        
        return
    
    def run(self):
        self.crawl_selenium()

if __name__=='__main__':
    lsnhtm = LsNhtm()
    lsnhtm.crawl_selenium()
        
        