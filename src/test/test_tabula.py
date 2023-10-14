import tabula
import sys
import os

sys.path.append(os.getcwd())

# Add path to environment variable
path = os.path.join(os.getcwd(), 'jre', 'bin')
os.environ['JAVA_HOME'] = path

# Read the PDF file
file_path = './src/test/sacom.pdf'

pdfData = tabula.read_pdf(file_path, pages=1)

# Extract the data to csv
tabula.convert_into(file_path, "sacom.csv", output_format="csv", pages=1)

print(pdfData)