import os 
import sys
import time
sys.path.append(os.getcwd())

from src.non_spiders.Base import Base

from src.utils.selenium import ChromeDriver
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
                rate_type = cells[0].text.strip()
                rate = float(cells[1].text.replace('%', '').strip())
                
                if rate_type == 'Không kỳ hạn':
                    rate_type = 'khong_ky_han'
                else:
                    rate_type = rate_type.replace(' tháng', '_thang')
                
                if rate_type == '48_thang':
                    break
                    
                data[rate_type] = rate
            
            del data['7 ngày']
            del data['14 ngày']
            del data['2_thang']

            data['18_thang'] = None
            
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
    
    def __crawl(self, driver, type: str, url: str):
        # Get the the page
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
        )
        html_str = driver.page_source
        
        if type == 'vcb':
            return self.parse_vcb(html_str)
        elif type == 'mb':
            return self.parse_mb(html_str)

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
        
        driver = ChromeDriver(headless=True).driver
        
        vcb_url = 'https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/KHCN---Lai-suat'
        mb_url = 'https://www.mbbank.com.vn/Fee'
        
        print(self.__crawl(driver, 'vcb', vcb_url))
        print(self.__crawl(driver, 'mb', mb_url))

if __name__=='__main__':
    lsnhtm = LsNhtm()
    lsnhtm.crawl_selenium()
        
        