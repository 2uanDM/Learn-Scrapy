import json
import os 
import sys
sys.path.append(os.getcwd())

import subprocess

from src.utils.logger import logger
from src.utils.crawler import run_crawler
from src.non_spiders.Base import Base

class LS_LNH(Base):
    temp_res_dir = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results', 'NHNN')
    output_file_path = os.path.join(os.getcwd(), 'results', 'lai_suat_lien_ngan_hang.csv')
    
    def __init__(self) -> None:
        super().__init__()
        
    def crawl(self):
        run_crawler(
            filename='ls_lnh.jsonl', 
            spider_name='NHNN_LS_LNH', 
            overwrite=True, 
            nolog=True, 
            save_folder=os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results', 'NHNN')
        )
    
    def run(self):
        if not os.path.exists(os.path.join(self.temp_res_dir, 'ls_lnh.jsonl')):
            print('Cannot find ls_lnh.jsonl file')
            return self.error_handler('Cannot find ls_lnh.jsonl file')
        
        try:
            with open(os.path.join(self.temp_res_dir, 'ls_lnh.jsonl'), 'r', encoding='utf8') as f:
                response = json.load(f)
        except Exception as e:
            print('An error occurs when reading ls_lnh.jsonl file: ' + str(e))
            return self.error_handler('An error occurs when reading ls_lnh.jsonl file: ' + str(e))
        
        if response['status'] == 'error':
            print('Cannot get ls_lnh data:' + response['message'])
            return self.error_handler('Cannot get ls_lnh data:' + response['message'])
        
        print('-'*100)
        print('Exporting data... to csv')
        # TODO: pushing to mongodb
        
        data_today = f'{self.date_slash}'
        
        for x in response['data']['lai_suat']:
            data_today += f',{response["data"]["lai_suat"][x]}'
        
        data_today += ','
        
        for x in response['data']['doanh_so']:
            data_today += f',{response["data"]["doanh_so"][x]}'
        
        try:
            with open(self.output_file_path, 'a', encoding='utf8') as f:
                f.write(data_today)
            print('Export data to csv successfully')
        except Exception as e:
            print('An error occurs when extracting data to csv: ' + str(e))
            return self.error_handler('An error occurs when extracting data to csv: ' + str(e))
        
if __name__ == '__main__':
    ls_lnh = LS_LNH()
    ls_lnh.crawl()
    ls_lnh.run()