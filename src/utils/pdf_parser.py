import tabula
import sys
import os
import pandas as pd
sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Months to be extracted
months = [1,3,6,9,12,18,24,36]

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
            
            df = df.iloc[2:19, [0,1]]
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
            df = df.iloc[[1,4,5], 2:19]
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

if __name__=='__main__':
    # print(extract_tcb())
    # print(extract_stb())
    print(extract_vpb())
    