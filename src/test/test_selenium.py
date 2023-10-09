import os
import shutil
import sys
import time
sys.path.append(os.getcwd())

from src.utils.selenium import ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

proxy = {
    'host' : '168.227.140.130',
    'port' : 12345,
    'username' : 'ebay2023',
    'password' : 'proxyebaylam'
}

driver = ChromeDriver(headless=False, authenticate_proxy=proxy, download_path=os.path.join(os.getcwd(), 'download')).driver

def download(url):
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

    time.sleep(3)

if __name__ == '__main__':
    steel_url = 'https://www.shfe.com.cn/eng/market/futures/metal/rb/'
    copper_url = 'https://www.shfe.com.cn/eng/market/futures/metal/cu/'
    aluminum_url = 'https://www.shfe.com.cn/eng/market/futures/metal/al/' 
    
    shutil.rmtree(os.path.join(os.getcwd(), 'download'))
    os.makedirs(os.path.join(os.getcwd(), 'download'), exist_ok=True)
    
    for i, url in enumerate([steel_url, copper_url, aluminum_url]):
        download(url)
        # Rename the latest downloaded file
        download_folder = os.path.join(os.getcwd(), 'download')
        file_name = f'data_{i}.csv'
        os.rename(os.path.join(download_folder, 'data.csv'), os.path.join(download_folder, file_name))
        