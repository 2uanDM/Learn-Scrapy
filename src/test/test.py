from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('test.html', 'r', encoding='utf8') as f:
    html_content = f.read()

soup = bs(html_content, 'html.parser')

