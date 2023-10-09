from typing import Iterable
import scrapy
from bs4 import BeautifulSoup as bs
from scrapy.http import Request

class NHNN_ExchangeRate(scrapy.Spider):
    name = 'NHNN_ExchangeRate'
    start_urls = ['https://www.sbv.gov.vn/TyGia/faces/TyGia.jspx']
    output = {
        'status': None,
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, errback=self.handle_error)
    
    def parse(self, response):
        print('Parsing the table where contain the exchange rate data...')
        tables = response.css('.jrPage')
        
        if len(tables) != 3:
            print('The number of tables is not 3')
            return

        # Table contains the exchange rate data of USD and EUR
        table_USD_EUR: str = tables[1].css('tbody').get()
        response = self.extract_table_usd_eur(table_USD_EUR)
        if response is None:
            message = 'Cannot find USD or EUR'
            print(message)
            self.output['status'] = 'error'
            self.output['message'] = message
            self.output['data'] = None
            yield self.output
            return
        else:
            self.output.update(response)
        
        # Table contains the exchange rate data of CNY
        table_CNY: str = tables[2].css('tbody').get()
        response = self.extract_table_cny(table_CNY)
        if response is None:
            message = 'Cannot find CNY'
            print(message)
            self.output['message'] = message
            self.output['data'] = None
            yield self.output
            return
        else:
            self.output.update(response)
        
        # Update status and return
        self.output['status'] = 'success'
        yield self.output
    
    def extract_table_usd_eur(self, table_html: str) -> dict:
        soup = bs(table_html, 'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        
        data = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:
                data.append({
                    'no': cells[1].text.strip(),
                    'symbol': cells[2].text.strip(),
                    'name': cells[3].text.strip(),
                    'buy': cells[4].text.strip(),
                    'sell': cells[5].text.strip()
                })
        
        usd_sell = None
        eur_sell = None
        
        # Scan for USD and EUR
        for row in data:
            if row['symbol'] == 'USD':
                usd_sell = row['sell']
            if row['symbol'] == 'EUR':
                eur_sell = row['sell']
        
        if usd_sell is None or eur_sell is None:
            return None
        else:
            return {
                'USD': usd_sell,
                'EUR': eur_sell
            }
    
    def extract_table_cny(self, table_html: str) -> dict:
        soup = bs(table_html, 'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        
        data = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:
                data.append({
                    'no': cells[1].text.strip(),
                    'symbol': cells[2].text.strip(),
                    'name': cells[3].text.strip(),
                    'exchange_rate': cells[4].text.strip(),
                })
        
        cny_exchange_rate = None
        
        # Scan for USD and EUR
        for row in data:
            if row['symbol'] == 'CNY':
                cny_exchange_rate = row['exchange_rate']
        
        if cny_exchange_rate is None:
            return None
        else:
            return {
                'CNY': cny_exchange_rate
            }
    
    def handle_error(self, failure):
        self.output['status'] = 'error'
        self.output['message'] = repr(failure)
        self.output['data'] = None
        yield self.output