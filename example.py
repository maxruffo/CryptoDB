
from scr.modules.CryptoDB1 import CryptoDB


db = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3,database=True,csv=False, interval=15)

db.run_app()