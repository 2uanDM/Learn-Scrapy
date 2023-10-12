import os 
import sys
import time
sys.path.append(os.getcwd())

import requests

from src.utils.logger import logger
from bs4 import BeautifulSoup as bs
from datetime import datetime

from src.utils.database.mongodb import MongoDB
from src.utils.selenium import ChromeDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Get csrf token from finance.vietstock.vn
def run(headless, url):
    driver = ChromeDriver(headless=headless).driver

    number_of_tried = 0

    while number_of_tried < 5:
        try:
            number_of_tried += 1
            
            print(f'Try to get cookie and csrf token from {url}: {number_of_tried} time(s)')
            
            driver.get(url=url)
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "__CHART_AjaxAntiForgeryForm"))
            # )
            break
        except Exception as e:
            print(str(e))
            continue

    if number_of_tried == 5:
        message = f'Cannot get cookie and csrf token from {url} after {number_of_tried} times'
        return None

    # Get the page source
    try:
        html_str = driver.page_source
        soup = bs(html_str, 'html.parser')
        form = soup.find('form', {'id': '__CHART_AjaxAntiForgeryForm'})
        token: str = form.find('input', {'name': '__RequestVerificationToken'}).get('value')
        print(f'Found token: {token}')
    except Exception as e:
        message = f'Cannot get page source from {url}: {str(e)}'
        print(message)
        return None

    # Get the cookie
    try:
        cookie = driver.get_cookies()
        
        # Parse the cookie into a string that can be used in the header
        cookie_str = ''
        for c in cookie:
            cookie_str += f"{c['name']}={c['value']}; "
        cookie_str = cookie_str[:-2]

        print(f'Found cookie: {cookie_str}')
    except Exception as e:
        message = f'Cannot get cookie from {url}: {str(e)}'
        print(message)
        return None

    driver.quit()

    print('Get cookie and csrf token successfully')

    return {
        'status': 'success',
        'message': 'Get cookie and csrf token successfully',
        'data': {
            'cookie': cookie_str,
            'token': token
        }
    }
    
run(
    url='https://finance.vietstock.vn/du-lieu-vi-mo/51/tin-dung.htm',
    headless=True
)