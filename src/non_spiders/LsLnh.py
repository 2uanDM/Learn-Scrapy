import json
import os 
import sys
sys.path.append(os.getcwd())

from src.utils.crawler import run_crawler
from src.non_spiders.Base import Base
from src.utils.database.schema import SchemaTopic2
from src.utils.io import write_csv
from datetime import datetime

class LsLnh(Base):
    temp_res_dir = os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results')
    output_file_path = os.path.join(os.getcwd(), 'results', 'lai_suat_lien_ngan_hang.csv')
    
    def __init__(self) -> None:
        super().__init__()
        
    def crawl(self):
        run_crawler(
            filename='ls_lnh.jsonl', 
            spider_name='NHNN_LS_LNH', 
            overwrite=True, 
            nolog=True, 
            save_folder=os.path.join(os.getcwd(), 'src', 'non_spiders', 'temp_results')
        )
    
    def run(self):
        # ----------------- Crawl data -----------------
        self.crawl()
        
        
        # ----------------- Read data from jsonl file -----------------
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
        
        new_data = SchemaTopic2().lai_suat_lnh(
            date=datetime.strptime(self.date_slash.strip(), '%m/%d/%Y'),
            ls_quadem=response['data']['lai_suat']['Qua đêm'],
            ls_1tuan=response['data']['lai_suat']['1 Tuần'],
            ls_2tuan=response['data']['lai_suat']['2 Tuần'],
            ls_1thang=response['data']['lai_suat']['1 Tháng'],
            ls_3thang=response['data']['lai_suat']['3 Tháng'],
            ls_6thang=response['data']['lai_suat']['6 Tháng'],
            ls_9thang=response['data']['lai_suat']['9 Tháng'],
            ls_12thang=response['data']['lai_suat'].get('12 Tháng', None),
            ds_quadem=response['data']['doanh_so']['Qua đêm'],
            ds_1tuan=response['data']['doanh_so']['1 Tuần'],
            ds_2tuan=response['data']['doanh_so']['2 Tuần'],
            ds_1thang=response['data']['doanh_so']['1 Tháng'],
            ds_3thang=response['data']['doanh_so']['3 Tháng'],
            ds_6thang=response['data']['doanh_so']['6 Tháng'],
            ds_9thang=response['data']['doanh_so']['9 Tháng'],
            ds_12thang=response['data']['doanh_so'].get('12 Tháng', None)
        )
        
        # ----------------- Write data to csv -----------------
        print('Exporting data... to csv')
        try:
            data_write_csv = new_data.copy()
            data_write_csv['date'] = self.date_slash
            write_csv(file_name=self.output_file_path, data=data_write_csv)
            print('Write data to csv successfully')
        except Exception as e:
            print('An error occurs when writing data to csv: ' + str(e))
            return self.error_handler('An error occurs when writing data to csv: ' + str(e))

        # ----------------- Update data to database -----------------
        print('Updating data to database...')
        try:
            self.db.update_collection('lai_suat_lien_ngan_hang', new_data)
            print('Update data to database successfully')
        except Exception as e:
            print('An error occurs when updating data to database: ' + str(e))
            return self.error_handler('An error occurs when updating data to database: ' + str(e))
        
if __name__ == '__main__':
    ls_lnh = LsLnh()
    ls_lnh.run()