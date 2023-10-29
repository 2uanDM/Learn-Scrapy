import json
import os
import sys
import time
sys.path.append(os.getcwd())  # NOQA

from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from src.non_spiders.Base import Base
from src.utils.selenium import ChromeDriver


class Gdp(Base):
    def __init__(self, headless=True) -> None:
        super(Gdp, self).__init__()
        self.headless = headless

    def _parse_table(self, page_source: str):
        soup = bs(page_source, 'html.parser')

        history_tab = soup.find('div', {'class': 'historyTab'})
        table = history_tab.find('table')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                print(cell.text, end='|')
            print()

    def _crawl_vn_investing_gdp(self, driver, url: str):
        try:
            driver.set_page_load_timeout(5)
            # Open the url
            driver.get(url=url)
        except TimeoutException:
            pass

        time.sleep(1)

        try:
            print('- Clicking on the "Show more" button...')

            for i in range(40):
                print(f'---- Clicked {i+1} times ')
                driver.execute_script("""
                    div_button = document.getElementsByClassName('showMoreReplies block')[0];
                    div_button.click(); 
                                      """)
                time.sleep(0.1)

            time.sleep(1)

            print('- Getting the page source...')
            page_source = driver.page_source

            print('- Parsing the page source...')
            self._parse_table(page_source=page_source)

        except Exception as e:
            message = f'Error while crawling {url}: {str(e)}'
            print(message)
            return self.error_handler(message)

    def crawl_VN_GDP(self):
        pass

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
    # print(gdp_crawler.crawl_VN_GDP())

    driver = ChromeDriver(headless=True, disable_images=True).driver

    gdp_crawler._crawl_vn_investing_gdp(
        driver=driver,
        url='https://vn.investing.com/economic-calendar/gdp-375'
    )
