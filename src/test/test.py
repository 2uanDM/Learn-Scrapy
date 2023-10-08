from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('test.html', 'r', encoding='utf8') as f:
    html_content = f.read()

soup = bs(html_content, 'html.parser')

xang_vn_table = soup.find('div', {'id': 'cctb-1'})

tbody = xang_vn_table.find('tbody')

rows = tbody.find_all('tr')

for row in rows:
    cells = row.find_all('td')
    if cells[1].text.strip() == 'Xăng RON 95-III':
        print(cells[2].text.strip())
        break

