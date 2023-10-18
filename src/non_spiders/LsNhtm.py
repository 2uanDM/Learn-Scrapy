import os
import re
import shutil 
import sys
import time

import requests
sys.path.append(os.getcwd())

from src.non_spiders.Base import Base

from src.utils.selenium import ChromeDriver
from src.utils.pdf_parser import extract_tcb, extract_stb, extract_vpb, extract_hdb

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from datetime import datetime

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
    
    def parse_acb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find_all('div', {'class': 'cumulative_saving_tables table-responsive'})[2]
            print('Found table')
            tbody = table.find('tbody')
            print('Found tbody')
            
            rows = tbody.find_all('tr')
            print('Found rows')
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            data = {}
            
            # Khong ky han data
            data['khong_ky_han'] = None
            
            # 1 thang data
            mot_thang = float(rows[5].find_all('td')[2].text.strip().replace(',', '.'))
            data['1_thang'] = mot_thang
            
            # The rest data
            for row in rows[6:]:
                cells = row.find_all('td')
    
                ky_han = cells[0].text.strip().replace('T','')
    
                if int(ky_han) in months:
                    lai_suat = float(cells[1].text.strip().replace(',', '.'))
                    data[f'{ky_han}_thang'] = lai_suat
            
            return {
                'status': 'success',
                'message': 'Parse ACB successfully',
                'data': data
            }
            
        except Exception as e:
            message = f'Error when parse LS NHTM ACB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_vpb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            
            # Find the link to the pdf file
            h3_tag = soup.find(lambda tag: tag.name == 'h3' and 'KHCN - Bảng lãi suất huy động' in tag.string)
            a_tag= h3_tag.find_next('a')
            href= a_tag['href']
            full_url = f'https://www.vpbank.com.vn{href}'
            
            # ---------------Download the pdf file-----------------------
            headers = {
                'authority': 'www.vpbank.com.vn',
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
            
            response = requests.request("GET", full_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f'Error when download pdf file from {full_url}')
            
            download_folder = os.path.join(os.getcwd(), 'download', 'vpb')
            shutil.rmtree(download_folder)
            os.makedirs(download_folder, exist_ok=True)
            
            with open(os.path.join(download_folder, 'vpb.pdf'), 'wb') as f:
                f.write(response.content)
            
            # -----------------------Parse the pdf file-----------------------
            result = extract_vpb()
            
            if result['status'] == 'error':
                raise Exception(result['message'])
            else:
                return result
            
        except Exception as e:
            message = f'Error when parse LS NHTM VPB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_vib(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('div', {'class': 'bx-wrapper'})
            col = table.find_all('div', {'class': 'vib-v2-box-slider-expression'})[1]
            cells = col.find_all('div', {'class': 'vib-v2-line-box-table-expression'})
            
            if len(cells) != 15:
                raise Exception('The structure of the page VIB has changed')
            
            data = {}
            
            # Khong ky han data
            data['khong_ky_han'] = None
            
            data['1_thang'] = float(cells[0].text.strip().replace('%',''))
            data['3_thang'] = float(cells[4].text.strip().replace('%',''))
            data['6_thang'] = float(cells[1].text.strip().replace('%',''))
            data['9_thang'] = float(cells[7].text.strip().replace('%',''))
            data['12_thang'] = float(cells[10].text.strip().replace('%',''))
            data['18_thang'] = float(cells[12].text.strip().replace('%',''))
            data['24_thang'] = float(cells[13].text.strip().replace('%',''))
            data['36_thang'] = float(cells[14].text.strip().replace('%',''))
            
            return {
                'status': 'success',
                'message': 'Parse VIB successfully',
                'data': data
            }
            
        except Exception as e:
            message = f'Error when parse LS NHTM VIB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_bab(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            tbody = soup.find('tbody')
            rows = tbody.find_all('tr')
            
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            # Khong ky han data
            data['khong_ky_han'] = float(rows[0].find_all('td')[3].text.strip())
            
            for row in rows[1:]:
                ky_han = row.find_all('td')[0].text.strip()
                num_month = int(ky_han.split(' ')[0])
                
                if num_month in months:
                    lai_suat = float(row.find_all('td')[3].text.strip())
                    data[f'{num_month}_thang'] = lai_suat
            
            return {
                'status': 'success',
                'message': 'Parse BAB successfully',
                'data': data
            }      
                
        except Exception as e:
            message = f'Error when parse LS NHTM BAB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_hdb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            
            # Find all the link to the pdf file
            a_tags = soup.find_all(lambda tag: tag.name == 'a' and 'BIỂU LÃI SUẤT TIỀN GỬI KHÁCH HÀNG CÁ NHÂN' in tag.text)
            
            list_tags = [] # Store the href and its date
            
            # Get the link which is the latest
            for tag in a_tags:
                href = tag['href']
                date_str = tag.text.strip().replace('BIỂU LÃI SUẤT TIỀN GỬI KHÁCH HÀNG CÁ NHÂN', '').strip()
                date = datetime.strptime(date_str, '%d-%m-%Y')
                list_tags.append((href, date))
            
            # Sort the list by date
            list_tags.sort(key=lambda x: x[1], reverse=True)
            link = list_tags[0][0]
            
            # -----------------------Download the pdf file to temp folder-----------------------
            headers = {
                'authority': 'hdbank.com.vn',
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
            
            download_folder = os.path.join(os.getcwd(), 'download', 'hdb')
            shutil.rmtree(download_folder)
            os.makedirs(download_folder, exist_ok=True)
            
            with open(os.path.join(download_folder, 'hdb.pdf'), 'wb') as f:
                f.write(response.content)
            
            # -----------------------Parse the pdf file-----------------------
            result = extract_hdb()
            if result['status'] == 'error':
                raise Exception(result['message'])
            else:
                return result
            
        except Exception as e:
            message = f'Error when parse LS NHTM HDB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_nab(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            selector = soup.find('select', {'id' : '259'})
            
            options = selector.find_all('option')
            
            href = None
            
            for option in options:
                if option.text.strip() == 'Lãi suất Tiền gửi VND (%/năm)':
                    href = option['data-news-href']
                    break
            
            if href is None:
                raise Exception('Cannot find the link to the table of NAB')

            # Go to the link and get the html string
            response = requests.request("GET", f'https://www.namabank.com.vn{href}', timeout=10)
            soup = bs(response.text, 'html.parser')
            
            table = soup.find('table')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            
            # for row in rows:
            #     cells = row.find_all('td')
            #     for cell in cells:
            #         print(cell.text.strip(),  end = '|')
            #     print()
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            for row in rows:
                cells = row.find_all('td')
                for cell in cells:
                    print(cell.text.strip(),  end = '|')
                print('-' * 50)
            
            for row in rows:
                cells = row.find_all('td')
                ky_han = cells[0].text.strip()
                lai_suat = cells[1].text.strip()
                if ky_han == 'KKH':
                    data['khong_ky_han'] = float(lai_suat) if lai_suat != '-' else None
                else:
                    # Use regex to check if the ky han has 'tháng' in it, then extract the number
                    if re.search(r'\d+ tháng', ky_han):
                        num_month = int(re.findall(r'\d+', ky_han)[0])
                        if num_month in months:
                            data[f'{num_month}_thang'] = float(lai_suat) if lai_suat != '-' else None
                
            return {
                'status': 'success',
                'message': 'Parse NAB successfully',
                'data': data
            }
            
        except Exception as e:
            message = f'Error when parse LS NHTM NAB: {str(e)}'
            print(message)
            return 
    
    def parse_klb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table_1 = soup.find('table', {'class': 'table'} )
            table_2 = soup.find('table', {'class': 'table table-responsive'})
            
            tbody_1 = soup.find('tbody')
            tbody_2 = table_2.find('tbody')
            
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            # Get the khong ky han data
            rows = tbody_1.find_all('tr')
            lai_suat_khong_ky_han = float(rows[1].find_all('td')[1].text.strip())
            data['khong_ky_han'] = lai_suat_khong_ky_han
            
            # Get the other data
            rows = tbody_2.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                ky_han = cells[0].text.strip().split()[0]
                
                if int(ky_han) in months:
                    data[f'{int(ky_han)}_thang'] = float(cells[1].text.strip())
            
            return {
                'status': 'success',
                'message': 'Parse KLB successfully',
                'data': data
            }
                
        except Exception as e:
            message = f'Error when parse LS NHTM KLB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_lpb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find_all('table')[1]
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            data['khong_ky_han'] = None
            
            for row in rows[2:]:
                cells = row.find_all('td')
                ky_han = cells[0].text.strip().split()[0]
                lai_suat = cells[4].text.strip()
                
                if int(ky_han) in months:
                    data[f'{int(ky_han)}_thang'] = float(lai_suat) if lai_suat != '-' else None
                
            return {
                'status': 'success',
                'message': 'Parse LPB successfully',
                'data': data
            }
            
        except Exception as e:
            message = f'Error when parse LS NHTM LPB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_ssb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table')
            tbody = soup.find('tbody')
            rows = tbody.find_all('tr')
            
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            data['khong_ky_han'] = None
            
            for row in rows:
                cells = row.find_all('td')
                ky_han = cells[1].text.strip().split()[0]
                lai_suat = cells[2].text.strip().replace('%', '')
                
                if int(ky_han) in months:
                    data[f'{int(ky_han)}_thang'] = float(lai_suat) if isinstance(lai_suat, str) else None
            
            return {
                'status': 'success',
                'message': 'Parse SSB successfully',
                'data': data
            }
                
        except Exception as e:
            message = f'Error when parse LS NHTM SSB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def parse_pgb(self, html_str: str):
        try:
            soup = bs(html_str, 'html.parser')
            table = soup.find('table')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            
            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]
            
            data['khong_ky_han'] = None
            
            for row in rows:
                cells = row.find_all('td')
                
                ky_han: str = cells[0].text.strip()
                lai_suat: str = cells[1].text.strip()
                
                num_month = int(ky_han.split()[0])
                if num_month in months:
                    if lai_suat != '' or lai_suat != None:
                        data[f'{num_month}_thang'] = float(lai_suat)
                    else:
                        data[f'{num_month}_thang'] = None
            
            return {
                'status': 'success',
                'message': 'Parse PGB successfully',
                'data': data
            }
                
        except Exception as e:
            message = f'Error when parse LS NHTM PGB: {str(e)}'
            print(message)
            return self.error_handler(message)
    
    def __crawl(self, driver, type: str, url: str):
        # Get the the page
        driver.get(url)
        
        parse_by_pdf = ['tcb', 'stb', 'vpb', 'hdb']
        parse_by_bs4 = ['vcb', 'mb', 'bid', 'agribank', 'ctg', 'tpb', 'acb', 'vib', 'bab', 'nab', 'klb', 'lpb', 'ssb', 'pgb']
        
        if type in parse_by_bs4:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'table')) # Wait for the table to load
            ) 
        elif type in parse_by_pdf:
            # Wait for all elements loaded
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'a')) # Wait for the link to download pdf file
            )
        
        time.sleep(2.5)
        
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
        elif type == 'acb':
            try:
                button = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, 'rcc-confirm-button'))
                print('Found button to accept cookie policy')
                button.click()
                time.sleep(2)
                html_str = driver.page_source
            except Exception:
                print('No button to accept cookie policy, continue')
                html_str = driver.page_source
            return self.parse_acb(html_str)
        elif type == 'vpb':
            return self.parse_vpb(html_str)
        elif type == 'vib':
            return self.parse_vib(html_str)
        elif type == 'bab':
            driver.execute_script("""
            var dropdown = document.getElementById("ctl00_PlaceHolderMain_g_3d987530_2758_4587_b052_bda8fbe88390_ctl00_DDL_LS");

            dropdown.options[2].selected = true;

            dropdown.dispatchEvent(new Event('change'));
                                  """)
            time.sleep(2)
            html_str = driver.page_source
            return self.parse_bab(html_str)
        elif type == 'hdb':
            return self.parse_hdb(html_str)
        elif type == 'nab':
            return self.parse_nab(html_str)
        elif type == 'klb':
            return self.parse_klb(html_str)
        elif type == 'lpb':
            return self.parse_lpb(html_str)
        elif type == 'ssb':
            return self.parse_ssb(html_str)
        elif type == 'pgb':
            return self.parse_pgb(html_str)

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
        acb_url = 'https://www.acb.com.vn/lai-suat-tien-gui'
        vpb_url = 'https://www.vpbank.com.vn/tai-lieu-bieu-mau#category_3'
        vib_url = 'https://www.vib.com.vn/vn/tiet-kiem/bieu-lai-suat-tiet-kiem-tai-quay'
        bab_url = 'https://www.baca-bank.vn/SitePages/website/lai-xuat.aspx?ac=L%u00e3i+su%u1ea5t&s=LX'
        hdb_url = 'https://hdbank.com.vn/vi/personal/cong-cu/interest-rate'
        nab_url = 'https://www.namabank.com.vn/lai-suat'
        klb_url = 'https://laisuat.kienlongbank.com/lai-suat-ca-nhan'
        lpb_url = 'https://lpbank.com.vn/lai-suat-2/'
        ssb_url = 'https://www.seabank.com.vn/interest'
        pgb_url = 'https://www.pgbank.com.vn/lai-suat-tiet-kiem/ca-nhan-vnd'
        
        # print(self.__crawl(driver, 'vcb', vcb_url))
        # print(self.__crawl(driver, 'mb', mb_url))
        # print(self.__crawl(driver, 'tcb', tcb_url))
        # print(self.__crawl(driver, 'stb', stb_url)) 
        # print(self.__crawl(driver, 'agribank', agribank_url))
        # print(self.__crawl(driver, 'bid', bid_url))
        # print(self.__crawl(driver, 'ctg', ctg_url))
        # print(self.__crawl(driver, 'tpb', tpb_url))
        # print(self.__crawl(driver, 'acb', acb_url))
        # print(self.__crawl(driver, 'vpb', vpb_url))
        # print(self.__crawl(driver, 'vib', vib_url))
        # print(self.__crawl(driver, 'bab', bab_url))
        # print(self.__crawl(driver, 'hdb', hdb_url))
        # print(self.__crawl(driver, 'nab', nab_url))
        # print(self.__crawl(driver, 'klb', klb_url))
        # print(self.__crawl(driver, 'lpb', lpb_url))
        # print(self.__crawl(driver, 'ssb', ssb_url))
        print(self.__crawl(driver, 'pgb', pgb_url))
        
        driver.quit()
        
        return
    
    def run(self):
        self.crawl_selenium()

if __name__=='__main__':
    lsnhtm = LsNhtm()
    lsnhtm.run()
        
        