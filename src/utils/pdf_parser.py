import re
import traceback
import tabula
import sys
import os
import pandas as pd
sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Months to be extracted
months = [1, 3, 6, 9, 12, 18, 24, 36]


def extract_tcb() -> dict:
    try:
        tcb_folder = os.path.join(os.getcwd(), 'download', 'tcb')
        files = os.listdir(tcb_folder)
        if 'tcb.pdf' not in files:
            return {
                'status': 'error',
                'message': 'File tcb.pdf not found',
                'data': None
            }
        else:
            file_path = os.path.join(tcb_folder, 'tcb.pdf')
            pdfData = tabula.read_pdf(file_path, pages=1)
            df = pd.DataFrame(pdfData[0])
            df = df.iloc[4:40, [0, 2]]

            data = {'khong_ky_han': None}

            for row in df.iterrows():
                ky_han: int = int(row[1][0].strip().replace('M', ''))
                lai_suat: float = float(row[1][1])

                if ky_han in months:
                    data[f'{ky_han}_thang'] = lai_suat

            return {
                'status': 'success',
                'message': 'Parse TCB successfully',
                'data': data
            }
    except Exception as e:
        message = f'Error when parse LS NHTM TCB: {str(e)}'
        print(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


def extract_stb():
    try:
        stb_folder = os.path.join(os.getcwd(), 'download', 'stb')
        files = os.listdir(stb_folder)

        if 'stb.pdf' not in files:
            raise Exception('File stb.pdf not found')
        else:
            file_path = os.path.join(stb_folder, 'stb.pdf')
            pdfData = tabula.read_pdf(file_path, pages=1)
            df = pd.DataFrame(pdfData[0])

            df = df.iloc[2:19, [0, 1]]
            data = {'khong_ky_han': None}

            for label, series in df.iterrows():
                ky_han = series[0]
                lai_suat = float(series[1].replace('%', ''))

                num_month = int(ky_han.split(' ')[0])
                if num_month in months:
                    data[f'{num_month}_thang'] = lai_suat

            return {
                'status': 'success',
                'message': 'Parse STB successfully',
                'data': data
            }

    except Exception as e:
        message = f'Error when parse LS NHTM STB: {str(e)}'
        print(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


def extract_vpb():
    try:
        vpb_folder = os.path.join(os.getcwd(), 'download', 'vpb')
        files = os.listdir(vpb_folder)

        if 'vpb.pdf' not in files:
            raise Exception('File vpb.pdf not found')
        else:
            file_path = os.path.join(vpb_folder, 'vpb.pdf')
            pdfData = tabula.read_pdf(file_path, pages=2, multiple_tables=True, encoding='utf-8')
            df = pd.DataFrame(pdfData[1])
            df = df.iloc[[1, 4, 5], 2:19]
            df.reset_index(drop=True, inplace=True)

            # Set the header of the dataframe by the first row
            df.columns = df.iloc[0]

            data = {'khong_ky_han': None}
            for col in df.columns:
                num_month = col.replace('T', '').strip()

                if int(num_month) in months:
                    data[f'{num_month}_thang'] = float(df[col][1])

            return {
                'status': 'success',
                'message': 'Parse VPB successfully',
                'data': data
            }

    except Exception as e:
        message = f'Error when parse LS NHTM VPB: {str(e)}'
        print(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


def extract_hdb():
    try:
        hdb_folder = os.path.join(os.getcwd(), 'download', 'hdb')
        files = os.listdir(hdb_folder)

        if 'hdb.pdf' not in files:
            raise Exception('File "hdb.pdf" not found !')
        else:
            file_path = os.path.join(hdb_folder, 'hdb.pdf')
            pdfData = tabula.read_pdf(file_path, pages=1, multiple_tables=True, encoding='utf-8')
            df = pd.DataFrame(pdfData[0])

            # print(df)

            # Extract the data
            data = {}

            data['khong_ky_han'] = None
            data['1_thang'] = df.iloc[9, 1]
            data['3_thang'] = df.iloc[11, 1]
            data['6_thang'] = df.iloc[14, 1]
            data['9_thang'] = df.iloc[17, 1]
            data['12_thang'] = df.iloc[23, 1]
            data['18_thang'] = df.iloc[31, 1]
            data['24_thang'] = df.iloc[32, 1]
            data['36_thang'] = df.iloc[33, 1]

            for key, value in list(data.items()):
                data[key] = float(value.replace(',', '.')) if value is not None else None

            return {
                'status': 'success',
                'message': 'Parse HDB successfully',
                'data': data
            }

    except Exception as e:
        message = f'Error when parse LS NHTM HDB: {str(e)}'
        print(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


def extract_eib():
    option: int = 1
    try:
        eib_folder = os.path.join(os.getcwd(), 'download', 'eib')
        files = os.listdir(eib_folder)
        if 'eib.pdf' not in files:
            raise Exception('File eib.pdf not found')
        else:
            file_path = os.path.join(eib_folder, 'eib.pdf')
            pdfData = tabula.read_pdf(file_path, pages=1, multiple_tables=True, encoding='utf-8')
            df = pd.DataFrame(pdfData[0])

            print(df)

            lai_suat_khong_ky_han = df.iloc[5, 3]

            # Check if lai_suat_khong_ky_han is not nan
            if not pd.isna(lai_suat_khong_ky_han):
                if not isinstance(lai_suat_khong_ky_han, float):
                    lai_suat_khong_ky_han = float(lai_suat_khong_ky_han.replace(',', '.'))
            else:
                option = 2
                print('Option 1 is not available, use option 2 instead')
                lai_suat_khong_ky_han = df.iloc[4, 6]
                if pd.isna(lai_suat_khong_ky_han):
                    raise Exception('Both option 1 and option 2 are not available')
                else:
                    if not isinstance(lai_suat_khong_ky_han, float):
                        lai_suat_khong_ky_han = float(lai_suat_khong_ky_han.replace(',', '.'))

            data = {'khong_ky_han': lai_suat_khong_ky_han}

            months = [1, 3, 6, 9, 12, 18, 24, 36]

            if option == 1:
                cutted_df = df.iloc[5:25, [0, 3]]
            elif option == 2:
                cutted_df = df.iloc[5:25, [0, 6]]

            # print(cutted_df)

            cutted_df.columns = ['ky_han', 'lai_suat']
            cutted_df.reset_index(drop=True, inplace=True)

            # Create a regex pattern that has the format "\d+ tháng"
            pattern = re.compile(r'\d+ tháng')

            for idx, row in cutted_df.iterrows():
                if pattern.search(row['ky_han']) is None:
                    continue
                else:
                    ky_han = pattern.search(row['ky_han']).group(0)
                    lai_suat = row['lai_suat']
                    num_month = int(ky_han.split(' ')[0])
                    if num_month in months:
                        data[f'{num_month}_thang'] = float(lai_suat.replace(',', '.')) if lai_suat is not None else None

            return {
                'status': 'success',
                'message': 'Parse EIB successfully',
                'data': data
            }

    except Exception as e:
        message = f'Error when parse LS NHTM EIB: {str(e)}'
        print(traceback.format_exc())
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


def extract_vbb():
    try:
        vbb_folder = os.path.join(os.getcwd(), 'download', 'vbb')
        files = os.listdir(vbb_folder)
        if 'vbb.pdf' not in files:
            raise Exception('File vbb.pdf not found')
        else:
            file_path = os.path.join(vbb_folder, 'vbb.pdf')
            pdfData = tabula.read_pdf(file_path, pages=1, encoding='utf-8')
            df = pd.DataFrame(pdfData[0])

            cutted_df = df.iloc[2:22, [0, 1]]
            cutted_df.columns = ['ky_han', 'lai_suat']
            cutted_df.reset_index(drop=True, inplace=True)

            data = {}
            months = [1, 3, 6, 9, 12, 18, 24, 36]

            # Khong ky han data
            data['khong_ky_han'] = None

            # The rest
            for idx, row in cutted_df.iterrows():
                ky_han = row['ky_han']
                lai_suat = row['lai_suat']

                num_month = int(ky_han.split()[0])
                if num_month in months:
                    data[f'{num_month}_thang'] = float(lai_suat.replace('%', '')) if lai_suat != '-' else None

            return {
                'status': 'success',
                'message': 'Parse VBB successfully',
                'data': data
            }

    except Exception as e:
        message = f'Error when parse LS NHTM VBB: {str(e)}'
        print(message)
        return {
            'status': 'error',
            'message': message,
            'data': None
        }


if __name__ == '__main__':
    # print(extract_tcb())
    # print(extract_stb())
    # print(extract_vpb())
    # print(extract_hdb())
    print(extract_eib())
    # print(extract_vbb())
