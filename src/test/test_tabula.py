import tabula
import sys
import os

import pandas as pd

sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Read the PDF file
file_path = './download/tcb/tcb.pdf'

pdfData = tabula.read_pdf(file_path, pages=1)

df = pd.DataFrame(pdfData[0])

# Get columns 0 and 2
df = df.iloc[4:40, [0, 2]]

for row in df.iterrows():
    print(row[1][0], row[1][1])