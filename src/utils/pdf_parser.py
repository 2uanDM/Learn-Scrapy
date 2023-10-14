import tabula
import sys
import os
import pandas as pd
sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

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
            
            months = [1,3,6,9,12,18,24,36]
            data = {}
            
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

if __name__=='__main__':
    print(extract_tcb())
    