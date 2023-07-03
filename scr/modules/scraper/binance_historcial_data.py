import os
import requests
import csv
from datetime import datetime, timedelta


# implement in the function download_historical_price_data that before it downloads the data it checks with get_binance_ticker_symbols if the ticker is valid
# if not raise an exception

def download_historical_price_data(ticker, start_date, end_date, interval_minutes,pricedata_folder = 'resources/pricedata', progress=True):
    '''
    Function that with a given ticker saves the data in the given pricedata_folder
    '''

    url = "https://api.binance.com/api/v3/klines"

    valid_tickers = get_binance_ticker_symbols()
    if ticker not in valid_tickers:
        raise Exception("Invalid ticker symbol")

    output_folder = os.path.join(pricedata_folder,f'{ticker}')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if start_date > end_date:
        raise Exception("Start date is after the End date")
    
    valid_intervals = [1, 3, 5, 15, 30]
    if interval_minutes not in valid_intervals:
        raise Exception("This is intervall isnt available, please use: [1, 3, 5, 15, 30]")

   
    current_date = start_date

    while current_date <= end_date:

        start_timestamp = int(current_date.timestamp() * 1000)
        next_date = current_date + timedelta(days=1)
        end_timestamp = int(next_date.timestamp() * 1000)

        parameters = {
            "symbol": ticker,
            "interval": f"{interval_minutes}m",
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": 1000  
        }

        try:
            response = requests.get(url, params=parameters)

            if response.status_code == 200:
                data = response.json()
                date_str = current_date.strftime('%Y-%m-%d')
                filename = f"{ticker}_{date_str}.csv"
                filepath = os.path.join(output_folder, filename)

                with open(filepath, 'w', newline='') as file:
                    writer = csv.writer(file)
                    header = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Kline_Close_Time", "Quote_Asset_Volume", "Number_of_Trades", "Taker_Buy_Base_Asset_Volume", "Taker_Buy_Quote_Asset_Volume"]
                    writer.writerow(header)

                    for row in data:
                        timestamp = datetime.fromtimestamp(row[0] / 1000) 
                        kline_close_time = datetime.fromtimestamp(row[6] / 1000) 
                        modified_row = [timestamp] + row[1:6] + [kline_close_time] + row[7:-1] 
                        writer.writerow(modified_row)

                if progress == True:
                    print(f"Historische Preisdaten für {ticker} am {date_str} wurden gespeichert.")

        except requests.exceptions.RequestException as e:

            if progress == True:
                print(f"Fehler bei der API-Anfrage für {ticker} am {current_date.strftime('%Y-%m-%d')}: {e}")

        current_date = next_date





def get_binance_ticker_symbols():
    url = 'https://api.binance.com/api/v3/exchangeInfo'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [symbol['symbol'] for symbol in data['symbols']]
        return symbols
    
    except requests.exceptions.RequestException as e:
        print('Error occurred:', e)















'''# Beispielaufruf für Bitcoin (BTC) vom 1. Januar 2022 bis 31. Dezember 2022 mit einem Intervall von 30 Minuten
start_date = datetime(2022, 12, 20)
end_date = datetime(2022, 12, 31)"""
interval_minutes = 1'''



