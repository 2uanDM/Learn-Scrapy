from typing import Iterable
import scrapy
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from pathlib import Path


class NHNN_LS_LNH(scrapy.Spider):
    name = 'NHNN_LS_LNH'
    url = 'https://www.sbv.gov.vn/webcenter/portal/vi/menu/rm/ls/lsttlnh'

    output = {
        'status': None,
    }

    def start_requests(self):
        print(f'Start requesting {self.url}')
        yield Request(url=self.url, callback=self.parse, errback=self.handle_error, dont_filter=True, meta={'download_timeout': 10})

    def parse(self, response):
        print('Parsing response')

        table_html: str = response.css('table.jrPage').get()
        data: dict = self.extract_data(table_html)

        if data:
            print('Extract data successfully')
            self.output['status'] = 'success'
            self.output['data'] = data
        else:
            print('Cannot extract data')
            self.output['status'] = 'error'
            self.output['message'] = 'Cannot extract data'
            self.output['data'] = None

        yield self.output

    def extract_data(self, table_html: str):
        data = {
            'lai_suat': {},
            'doanh_so': {},
        }

        soup = bs(table_html, 'html.parser')

        # Remove all the style attributes
        for tag in soup.find_all(True):
            tag.attrs = {}

        rows = soup.find_all('tr')
        for row in rows[3:10]:
            cells = row.find_all('td')

            thoi_han = cells[0].text.strip()
            lai_suat = cells[1].text.strip()
            doanh_so = cells[2].text.strip()

            if thoi_han == '' or lai_suat == '' or doanh_so == '':
                return None

            # Convert lai_suat to float
            if lai_suat.find('(*)') != -1:
                lai_suat = lai_suat.replace('(*)', '')
            lai_suat = lai_suat.replace(',', '.')
            lai_suat = float(lai_suat)

            # Convert doanh_so to float
            if doanh_so.find('(*)') != -1:
                doanh_so = doanh_so.replace('(*)', '')
            number, decimal = doanh_so.split(',')
            number = number.replace('.', '')
            doanh_so = float(number.strip() + '.' + decimal.strip())

            data['lai_suat'][thoi_han] = lai_suat
            data['doanh_so'][thoi_han] = doanh_so

        print(data)

        return data

    def handle_error(self, failure):
        self.output['status'] = 'error'
        self.output['message'] = repr(failure)
        self.output['data'] = None
        yield self.output
