import os
import sys 
sys.path.append(os.getcwd())

from src.utils.database.schema import SchemaTopic2
from src.utils.database.mongodb import MongoDB
from datetime import datetime

ty_gia = SchemaTopic2().ty_gia(
    date=datetime.strptime('10/10/2023', '%m/%d/%Y'),
    dollar_index_dxy=1.1,
    usd_vcb='a',
    usd_nhnn=2.2,
    eur_vcb=3.3,
    eur_nhnn=4.4,
    cny_vcb=6.6,
    cny_nhnn=5.5,
)

mongo = MongoDB('topic2')

db = mongo.get_db()

db.ty_gia.insert_one(ty_gia)