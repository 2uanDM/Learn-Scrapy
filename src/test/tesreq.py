import requests

def main():
    url = "https://viglaceravietnam.com/gach-lat-nen-viglacera-ub304-30x30cm.htm"

    payload = {}
    headers = {
    'authority': 'viglaceravietnam.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    
    response = requests.request("GET", url, headers=headers, data = payload)
    
    with open('test.html', 'w', encoding='utf8') as f:
        f.write(response.text)

if __name__ == '__main__':
    main()