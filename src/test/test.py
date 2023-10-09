from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('test.html', 'r', encoding='utf8') as f:
    html_content = f.read()

soup = bs(html_content, 'html.parser')

# Remove all the style attributes

for tag in soup.find_all(True):
    tag.attrs = {}

rows = soup.find_all('tr')

for row in rows[3:10]:
    cells = row.find_all('td')
    for cell in cells: 
        print(cell.text.strip(), end='||')
    
    print()