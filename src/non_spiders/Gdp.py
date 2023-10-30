import json
import os
import re
import sys
import time
sys.path.append(os.getcwd())  # NOQA

from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime

from src.non_spiders.Base import Base
from src.utils.selenium import ChromeDriver
from src.utils.database.schema import SchemaTopic2


class Gdp(Base):
    def __init__(self, headless=True) -> None:
        super(Gdp, self).__init__()
        self.headless = headless

        self.quarter_mapping: dict = {1: 'Q4', 2: 'Q4', 3: 'Q4', 4: 'Q1', 5: 'Q1',
                                      6: 'Q1', 7: 'Q2', 8: 'Q2', 9: 'Q2', 10: 'Q3', 11: 'Q3', 12: 'Q3'}

    def _parse_table(self, page_source: str) -> dict:
        """
            Parse the table in the page source to get the latest gdp in each quarter
        Args:
            - page_source (str): the HTML page source

        Returns:
            ```python
            {
                'status': 'success',
                'message': 'Get GDPs successfully',
                'data' : [A list of dict]
            }
            ```
        """
        try:
            soup = bs(page_source, 'html.parser')
            history_tab = soup.find('div', {'class': 'historyTab'})
            table = history_tab.find('table')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')

            # Define the regex of day: DD/MM/YYYY
            day_regex = r'\d{2}/\d{2}/\d{4}'

            data: list = []

            # Loop through each row to get the data
            for row in rows:
                cells = row.find_all('td')
                date: str = cells[0].text.strip()
                if cells[2].text.strip() == '':
                    continue
                value: float = float(cells[2].text.strip().replace('%', ''))

                # Find the date in the first cell using regex
                date = re.findall(day_regex, date)[0]
                date_datetime = datetime.strptime(date, '%d/%m/%Y')
                day, month, year = list(map(int, date.split('/')))

                # Get the quarter and year from the date
                if month in (1, 2, 3):
                    quarter = 'Q4'
                    year = year - 1
                else:
                    quarter = self.quarter_mapping[month]
                    year = year

                # Search for existing quarter
                existed_quarter = False
                for item in data:
                    if item['year'] == year and item['quarter'] == quarter:
                        existed_quarter = True
                        if date_datetime > item['date_created']:
                            item['date_created'] = date_datetime
                            item['gdp'] = value
                        break

                if not existed_quarter:
                    data.append({
                        'date_created': date_datetime,
                        'quarter': quarter,
                        'year': year,
                        'gdp': value,
                    })

            return {
                'status': 'success',
                'message': 'Get GDPs successfully',
                'data': data
            }

        except Exception as e:
            message = f'Error while parsing the table: {str(e)}'
            print(message)
            return self.error_handler(message)

    def _crawl_vn_investing_gdp(self, driver, url: str) -> dict:
        try:
            driver.set_page_load_timeout(5)
            # Open the url
            print(f'- Opening the url: {url}...')
            driver.get(url=url)
        except TimeoutException:
            pass

        time.sleep(1)

        try:
            print('- Clicking on the "Show more" button...')

            for i in range(60):
                print(f'---- Clicked {i+1} times ')
                driver.execute_script("""
                    div_button = document.getElementsByClassName('showMoreReplies block')[0];
                    div_button.click(); 
                                      """)
                time.sleep(0.05)

            time.sleep(1)

            print('- Getting the page source...')
            page_source = driver.page_source

            print('- Parsing the page source...')
            result = self._parse_table(page_source=page_source)

            print('Done')

            return result

        except Exception as e:
            message = f'Error while crawling {url}: {str(e)}'
            print(message)
            return self.error_handler(message)

    def crawl_VN_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/vietnamese-gdp-1853'
        )

        if result['status'] == 'error':
            message = f'Error while crawling VN GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get VN GDP successfully',
            'data': result['data']
        }

    def crawl_US_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/gdp-375'
        )

        if result['status'] == 'error':
            message = f'Error while crawling US GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get US GDP successfully',
            'data': result['data']
        }

    def crawl_CN_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/chinese-gdp-461'
        )

        if result['status'] == 'error':
            message = f'Error while crawling CN GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get CN GDP successfully',
            'data': result['data']
        }

    def crawl_JP_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/gdp-1053'
        )

        if result['status'] == 'error':
            message = f'Error while crawling JP GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get JP GDP successfully',
            'data': result['data']
        }

    def crawl_UK_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/gdp-728'
        )

        if result['status'] == 'error':
            message = f'Error while crawling UK GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get UK GDP successfully',
            'data': result['data']
        }

    def crawl_GER_GDP(self, driver):
        result = self._crawl_vn_investing_gdp(
            driver=driver,
            url='https://vn.investing.com/economic-calendar/german-gdp-738'
        )

        if result['status'] == 'error':
            message = f'Error while crawling GER GDP: {result["message"]}'
            print(message)
            return self.error_handler(message)

        return {
            'status': 'success',
            'message': 'Get GER GDP successfully',
            'data': result['data']
        }

    def run(self):
        driver = ChromeDriver(headless=self.headless, disable_images=True).driver

        print('----------------------Start crawling VN GDP----------------------')
        vn_gdp = self.crawl_VN_GDP(driver=driver)
        print(vn_gdp)

        print('----------------------Start crawling US GDP----------------------')
        us_gdp = self.crawl_US_GDP(driver=driver)
        print(us_gdp)

        print('----------------------Start crawling CN GDP----------------------')
        cn_gdp = self.crawl_CN_GDP(driver=driver)
        print(cn_gdp)

        print('----------------------Start crawling JP GDP----------------------')
        jp_gdp = self.crawl_JP_GDP(driver=driver)
        print(jp_gdp)

        print('----------------------Start crawling UK GDP----------------------')
        uk_gdp = self.crawl_UK_GDP(driver=driver)
        print(uk_gdp)

        print('----------------------Start crawling GER GDP----------------------')
        ger_gdp = self.crawl_GER_GDP(driver=driver)
        print(ger_gdp)

        # Close the driver
        driver.quit()

        # Save to database
        data_push = []
        date_crawled = datetime.strptime(self.date_slash.strip(), '%m/%d/%Y')

        if vn_gdp['status'] == 'success':
            for item in vn_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='VN',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for VN GDP successfully')

        if us_gdp['status'] == 'success':
            for item in us_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='US',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for US GDP successfully')

        if cn_gdp['status'] == 'success':
            for item in cn_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='CN',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for CN GDP successfully')

        if jp_gdp['status'] == 'success':
            for item in jp_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='JP',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for JP GDP successfully')

        if uk_gdp['status'] == 'success':
            for item in uk_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='UK',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for UK GDP successfully')

        if ger_gdp['status'] == 'success':
            for item in ger_gdp['data']:
                data_dict = SchemaTopic2().gdp(
                    date_crawled=date_crawled,
                    date_created=item['date_created'],
                    quarter=item['quarter'],
                    year=item['year'],
                    country='GER',
                    gdp=item['gdp']
                )
                data_push.append(data_dict)
            print('Prepare data for GER GDP successfully')

        print('----------------------Push data to database----------------------')
        self.db.update_collection('gdp', data_push)
        print('Push data to database successfully')


if __name__ == '__main__':
    gdp_crawler = Gdp()
    gdp_crawler.run()
