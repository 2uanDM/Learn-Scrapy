import tabula
import sys
import os

import pandas as pd

sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Read the PDF file
file_path = r'C:\Users\Thinkbook 14 G3 ACL\Documents\GitHub\Kaxim-Stocks-Topic-2\download\hdb\hdb.pdf'

pdfData = tabula.read_pdf(file_path, pages=1, multiple_tables=True, encoding='utf-8')

df = pd.DataFrame(pdfData[0])

# Khong ky han data

# df = df.iloc[[1,4,5], 2:19]

# Reset the index
# df.reset_index(drop=True, inplace=True)

print(df)