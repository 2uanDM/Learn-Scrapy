import requests

url = "https://bidv.com.vn/ServicesBIDV/InterestDetailServlet"

payload = {}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7',
  'Connection': 'keep-alive',
  'Content-Length': '0',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://bidv.com.vn',
  'Referer': 'https://bidv.com.vn/vn/tra-cuu-lai-suat',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)
