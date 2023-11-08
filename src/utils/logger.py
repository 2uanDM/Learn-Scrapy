from datetime import datetime
import os
import sys
sys.path.append(os.getcwd())


def logger(message: str):
    with open(os.path.join(os.getcwd(), 'error', 'error.log'), 'a', encoding='utf8') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ERROR: {message}\n')
