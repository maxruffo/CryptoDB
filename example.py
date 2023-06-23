
from scr.modules.CryptoDB import CryptoDB


db = CryptoDB(ndays=3,database=True,csv=False, interval=15)



db.connect_database()
dataframe = db.get_price_data()
print(dataframe)