import json

with open('exchange_rate.jsonl', 'r') as f:
    data = json.load(f)

print(data)