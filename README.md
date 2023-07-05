<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/maxruffo/CryptoDB">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">CryptoDB</h3>
  <p align="center">
    Get a simple SQLite Database with PriceData for Cryptocurrencies
    <br />
  </p>
</div>

## Install the Requiriments

```sh
pip install -r requirements.txt
```

## How to use it

```py
from cryptodb import CryptoDB

db = CryptoDB(tickers=['BTCUSDT', 'ETHUSDT'], ndays=10, interval=30, progress=False, use_database=True, use_csv=False)
OR
db = CryptoDB(tickers=['BTCUSDT', 'ETHUSDT'], start_date='2021-01-01', end_date='2021-01-10', interval=30, progress=False, use_database=True, use_csv=False)

# get the availabke ticker symbols
tickersymbols = db.get_available_ticker_symbols()
print(tickersymbols)

# get price data for one ticker
pricedata = db.get_price_data('BTCUSDT')

# get price data for multiple tickers
pricedata = db.get_price_data(['BTCUSDT','ETHUSDT'])

# start the SQL GUI
db.start_sqlite_GUI()

```

### You can also see this in the example.ipynb

## Used Techstack
- SQlite
- APIs -> Binance Api
- Threading
