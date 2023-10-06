import os 
import sys
sys.path.append(os.getcwd())

import requests
from bs4 import BeautifulSoup as bs

from src.non_spiders.Base import Base

class ComodityIndex(Base):
    def __init__(self) -> None:
        return super().__init__()
    
    

if __name__ == '__main__':
    comodity_index = ComodityIndex()
    worldwide_gold_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/currencies/xau-usd",
        type=1
    )
    print(worldwide_gold_price_usd)
    
    raw_oil_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/currencies/wti-usd",
        type=1
    )
    print(raw_oil_price_usd)
    
    steel_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/commodities/us-steel-coil-futures-streaming-chart",
        type=2
    )
    print(raw_oil_price_usd)
    
    
    
