import json
import requests
import os
import sys
sys.path.append(os.getcwd())  # NOQA

from src.non_spiders.Base import Base
from src.utils.database.schema import SchemaTopic2
from src.utils.io import write_csv
from datetime import datetime


class LsCafef(Base):
    def __init__(self):
        super().__init__()

    def crawl(self):
        # Fetch data
        number_of_tries = 0

        while number_of_tries < 5:
            try:
                url = "https://msh-pcdata.cafef.vn/graphql"
                payload = "{\"query\":\"query {\\n                      interestRates {\\n                        name\\n                        lastUpdated\\n                        symbol\\n                        interestRates {\\n                          deposit\\n                          value\\n                        }\\n                      }\\n                    }\",\"variables\":{}}"
                headers = {
                    'authority': 'msh-pcdata.cafef.vn',
                    'accept': '*/*',
                    'accept-language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
                    'content-type': 'application/json',
                    'origin': 'https://s.cafef.vn',
                    'referer': 'https://s.cafef.vn/',
                    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
                }

                number_of_tries += 1
                print(f'Fetching data from cafef {url}: {number_of_tries} time(s)')
                response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
                break
            except Exception as e:
                number_of_tries += 1
                continue

        if number_of_tries == 5:
            print('Cannot fetch data from cafef')
            self.error_handler('Cannot fetch data from cafef')

        if response.status_code != 200:
            print('Cannot fetch data from cafef')
            self.error_handler('Cannot fetch data from cafef')

        # Parse data
        data_dict = json.loads(response.text)
        print(data_dict)
        data = data_dict['data']['interestRates']

        abbank = None
        acb = None
        bacabank = None
        bidv = None
        bvbank = None
        viettinbank = None
        eximbank = None
        hdbank = None
        kienlongbank = None
        lienvietpostbank = None
        mbbank = None
        msb = None
        namabank = None
        ncb = None
        ocb = None
        pgbank = None
        saigonbank = None
        shb = None
        seabank = None
        sacombank = None
        techcombank = None
        tpbank = None
        vietabank = None
        vietbank = None
        vietcombank = None
        vib = None
        vpbank = None
        agribank = None

        for bank in data:
            if bank['symbol'] == 'ABB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        abbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'ACB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        acb = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'BAB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        bacabank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'BID':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        bidv = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'BVB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        bvbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'CTG':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        viettinbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'EIB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        eximbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'HDB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        hdbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'KLB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        kienlongbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'LPB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        lienvietpostbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'MBB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        mbbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'MSB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        msb = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'NAB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        namabank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'NVB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        ncb = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'OCB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        ocb = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'PGB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        pgbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'SGB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        saigonbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'SHB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        shb = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'SSB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        seabank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'STB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        sacombank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'TCB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        techcombank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'TPB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        tpbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'VAB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        vietabank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'VBB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        vietbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'VCB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        vietcombank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'VIB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        vib = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'VPB':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        vpbank = float(deposit['value']) if deposit['value'] != None else None
            elif bank['symbol'] == 'agribank':
                for deposit in bank['interestRates']:
                    if deposit['deposit'] == 12:
                        agribank = float(deposit['value']) if deposit['value'] != None else None

        # Get the schema

        new_data = SchemaTopic2().lai_suat_cafef(
            date=datetime.strptime(self.date_slash.strip(), '%m/%d/%Y'),
            abbank=abbank,
            acb=acb,
            bacabank=bacabank,
            bidv=bidv,
            bvbank=bvbank,
            viettinbank=viettinbank,
            eximbank=eximbank,
            hdbank=hdbank,
            kienlongbank=kienlongbank,
            lienvietpostbank=lienvietpostbank,
            mbbank=mbbank,
            msb=msb,
            namabank=namabank,
            ncb=ncb,
            ocb=ocb,
            pgbank=pgbank,
            saigonbank=saigonbank,
            shb=shb,
            seabank=seabank,
            sacombank=sacombank,
            techcombank=techcombank,
            tpbank=tpbank,
            vietabank=vietabank,
            vietbank=vietbank,
            vietcombank=vietcombank,
            vib=vib,
            vpbank=vpbank,
            agribank=agribank
        )

        # Write data to csv
        print('Exporting data... to csv')

        try:
            file_name = 'lai_suat_cafef.csv'
            file_path = os.path.join(os.getcwd(), 'results', file_name)

            data_write_csv = new_data.copy()
            data_write_csv['date'] = self.date_slash

            if not os.path.exists(file_path):
                header = {
                    'date': 'date',
                    'abbank': 'ABB',
                    'acb': 'ACB',
                    'bacabank': 'BABA',
                    'bidv': 'BID',
                    'bvbank': 'BVB',
                    'viettinbank': 'CTG',
                    'eximbank': 'EIB',
                    'hdbank': 'HDB',
                    'kienlongbank': 'KLB',
                    'lienvietpostbank': 'LPB',
                    'mbbank': 'MBB',
                    'msb': 'MSB',
                    'namabank': 'NAB',
                    'ncb': 'NVB',
                    'ocb': 'OCB',
                    'pgbank': 'PGB',
                    'saigonbank': 'SGB',
                    'shb': 'SHB',
                    'seabank': 'SSB',
                    'sacombank': 'STB',
                    'techcombank': 'TCB',
                    'tpbank': 'TPB',
                    'vietabank': 'VAB',
                    'vietbank': 'VBB',
                    'vietcombank': 'VCB',
                    'vib': 'VIB',
                    'vpbank': 'VPB',
                    'agribank': 'agribank'
                }
                write_csv(file_name=file_path, data=header, mode='w')
                write_csv(file_name=file_path, data=data_write_csv, mode='a')
            else:
                write_csv(file_name=file_path, data=data_write_csv, mode='a')

            print('Write data to csv successfully')
        except Exception as e:
            print('An error occurs when writing data to csv: ' + str(e))
            self.error_handler('An error occurs when writing data to csv: ' + str(e))

        # Update data to database
        print('Updating data to database...')
        try:
            self.db.update_collection(collection_name='lai_suat_cafef', data=new_data)
            print('Update data to database successfully')
        except Exception as e:
            print('An error occurs when updating data to database: ' + str(e))
            self.error_handler('An error occurs when updating data to database: ' + str(e))

    def run(self):
        self.crawl()


if __name__ == '__main__':
    ls_cafef = LsCafef()
    ls_cafef.run()
