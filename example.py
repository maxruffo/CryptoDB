
from scr.modules.CryptoDB import CryptoDB


db = CryptoDB(ndays=3,database=True,csv=False, interval=15)

dataframes = db.get_price_data()
print(dataframes)

db.run_app()