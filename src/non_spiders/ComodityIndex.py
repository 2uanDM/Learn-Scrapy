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
    print('Gold', worldwide_gold_price_usd)
    
    raw_oil_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/currencies/wti-usd",
        type=1
    )
    print('Raw oil', raw_oil_price_usd)
    
    steel_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/commodities/us-steel-coil-futures-streaming-chart",
        type=2
    )
    print('Steel', steel_price_usd)
    
    copper_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/commodities/copper",
        type=3
    )
    
    print('Copper', copper_price_usd)
    
    aluminum_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/commodities/aluminum",
        type=3
    )
    print('Aluminium', aluminum_price_usd)
    
    brent_oil_price_usd = comodity_index.get_price_vn_investing(
        url="https://vn.investing.com/commodities/brent-oil-historical-data",
        type=3
    )
    print('Brent oil', brent_oil_price_usd)
    
    dji_price_usd = comodity_index.get_price_vn_investing(
        url = 'https://vn.investing.com/indices/us-30-historical-data',
        type = 3
    )
    print('DJI', dji_price_usd)
    
    
    
    
    
    
    
