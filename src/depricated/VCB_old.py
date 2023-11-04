import pandas as pd


def __parse_excel_file(self, file_dir: str) -> dict:
    '''
        Return data = 
        ```python
        {
            'USD': {
                'buy_cash': 23000,
                'buy_transfer': 23000,
                'sell': 23000
            },
            ...
        }
        ```
    '''
    output: dict = {}

    try:
        df = pd.read_excel(file_dir, engine='openpyxl')
        # Just get the 3 row of USD, EUR, CNY
        df = df.iloc[[21, 7, 5]]
        # Rename columns
        df.columns = ['Name', 'Symbol', 'Buy Cash', 'Buy Transfer', 'Sell']
        # Reset index
        df = df.reset_index(drop=True)
        # Extracting data
        for row in df.iterrows():
            symbols = ['USD', 'EUR', 'CNY']
            current_symbol = row[1]['Symbol']
            if current_symbol in symbols:
                output[current_symbol] = {
                    'buy_cash': row[1]['Buy Cash'],
                    'buy_transfer': row[1]['Buy Transfer'],
                    'sell': row[1]['Sell']
                }

        return output
    except Exception as e:
        return self.error_handler('An error occurs when parsing the exchange rate Excel file: ' + str(e))


def get_exchange_rate_VCB(self, date_dash: str):
    '''
        date_dash: str, format: '%Y-%m-%d'
    '''

    # Download excel files
    print('Downloading exchange rate from VCB website...')

    url = f'https://www.vietcombank.com.vn/api/exchangerates/exportexcel?date={date_dash}'

    try:
        response = requests.get(url=url, timeout=10)
    except Exception as e:
        message = f'An error occurs: {str(e)}'
        return self.error_handler(message)
    if response.status_code != 200:
        message = f'Response status code when fetcing url: {url} is not 200. Status code: {response.status_code}'
        return self.error_handler(message)

    data = json.loads(response.text)
    if data['FileName'] is not None:
        # Download excel file to local
        try:
            file_name = data["FileName"]
            save_folder = os.path.join(os.getcwd(), 'download')
            os.makedirs(save_folder, exist_ok=True)
            save_dir = os.path.join(save_folder, file_name)

            data = base64.b64decode(data['Data'])
            with io.open(save_dir, 'wb') as f:
                f.write(data)

            print(f'Save exchange rate excel file: {file_name} successfully')
        except Exception as e:
            return self.error_handler('An error occurs when saving the exchange rate excel file: ' + str(e))
    else:
        message = f'Does not have exchange rate file for today: {self.date_slash}'
        return self.error_handler(message)

    # Parse excel file
    print('Parsing exchange rate excel file...')
    try:
        data = self.__parse_excel_file(save_dir)
    except Exception as e:
        message = 'An error occurs when parsing the exchange rate excel file: ' + str(e)
        return self.error_handler(message)

    # Delete excel file
    os.remove(save_dir)
    print('Delete exchange rate excel file successfully')

    return {
        'status': 'success',
        'message': 'Get exchange rate successfully',
        'data': data
    }
