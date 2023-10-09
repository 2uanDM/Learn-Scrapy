import requests
from datetime import datetime, timedelta

def main(proxy: str):
    ip, port, username, password = proxy.split(':')
    proxy_config = {
        'https': f'http://{username}:{password}@{ip}:{port}',
        'http': f'http://{username}:{password}@{ip}:{port}',
    }
    
    response = requests.get('https://www.shfe.com.cn/eng/market/futures/metal/rb/', proxies=proxy_config, timeout=20)
    
    with open('test.html', 'w', encoding='utf8') as f:
        f.write(response.text)
        
if __name__ == '__main__':
    proxy = '168.227.140.130:12345:ebay2023:proxyebaylam'
    main(proxy)