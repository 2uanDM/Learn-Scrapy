from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('hihi.html', 'r', encoding='utf8') as f:
    html_content = f.read()

soup = bs(html_content, 'html.parser')

body = soup.find('body')

table = body.find_all('table', {'class': 'price-board'})

rows = table[0].find_all('tr')

for row in rows: 
    cells = row.find_all('td')
    for cell in cells:
        print(cell.text.strip(), end='||')
    print()



# for cell in first_row.find_all('td'):
#     print(cell.text.strip())

