import tabula
import sys
import os

import pandas as pd

sys.path.append(os.getcwd())

# Add path to environment variable (For windows)
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Window path
file_path = r'C:\Users\Thinkbook 14 G3 ACL\Documents\GitHub\Kaxim-Stocks-Topic-2\download\hdb\hdb.pdf'

# Linux path
file_path = r'/home/hokage321xxx/Documents/GitHub/Kaxim-Stocks-Topic-2/src/test/tech.pdf'

pdfData = tabula.read_pdf(file_path, pages=1, multiple_tables=True, encoding='utf-8')

df = pd.DataFrame(pdfData[0])

print(df)
