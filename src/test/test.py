from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('test.html', 'r', encoding='utf8') as f:
    html_content = f.read()

soup = bs(html_content, 'html.parser')

info = soup.find('div', {'id': 'infoProduct'})

price = info.find('span', {'class': 'price'})

if price:
    if price.text.strip() == '':
        print('Cannot find price')
    else:
        print(price.text.strip())

# body = table.find('tbody')

# rows = body.find_all('tr')

# for row in rows:
#     cells = row.find_all('td')
#     if cells[2].text.strip == 'UB304':
#         print(cells[3].text.strip())
#         break
