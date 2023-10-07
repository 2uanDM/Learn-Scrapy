from bs4 import BeautifulSoup as bs
import os
import sys
sys.path.append(os.getcwd())

with open('test_brent-oil-historical-data.html', 'r', encoding='utf8') as f:
    html_content = f.read()

start_index_open_div = html_content.find('<div class="text-5xl')
end_index_open_div = html_content.find('>', start_index_open_div)

# Search for the first occurence of the string '</div>'
start_index_close_div = html_content.find('</div>', end_index_open_div) + len('</div>')

div_str = html_content[start_index_open_div: start_index_close_div]

soup = bs(div_str, 'html.parser')
print(soup.find('div').text.strip())
