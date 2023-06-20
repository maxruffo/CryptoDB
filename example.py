
from scr.modules.CryptoDB import CryptoDB


db = CryptoDB(ndays=30,database=True,csv=False, interval=15)

db.run_app()