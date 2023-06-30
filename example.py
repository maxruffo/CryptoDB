
from scr.modules.CryptoDB import CryptoDB


db = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3,database=True,csv=False, interval=15)

