import os 
import sys 
sys.path.append(os.getcwd())

from bs4 import BeautifulSoup as bs

with open('hello.html', 'r', encoding='utf8') as f:
    html_str = f.read()



print(data)
    