import json
import os
import threading
from datetime import datetime, timedelta
import shutil
from .binance_historcial_data import download_historical_price_data

class DataDownloader:
    def __init__(self, pricedata_folder='resources/pricedata', progress=True):
        self.pricedata_folder = pricedata_folder
        self.progress = progress

    def download_data_for_dates(self, ticker_list, start_date, end_date, interval_minutes):
        '''
        Function that downloads the data for a given ticker_list, start_date, end_date and intervall_minutes and saves it in 
        '''

        if isinstance(ticker_list, str):
            ticker_list = [ticker_list]

        num_threads = min(len(ticker_list), threading.active_count())

        def download_data(ticker):
            download_historical_price_data(ticker, start_date, end_date, interval_minutes, self.pricedata_folder, self.progress)

        threads = []
        for ticker in ticker_list:
            thread = threading.Thread(target=download_data, args=(ticker,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def download_data_for_ndays(self, ticker_list, num_days, interval_minutes):
        '''
        Function that downloads the data for a given ticker_list, start_date, end_date and intervall_minutes and saves it in 
        '''

        if isinstance(ticker_list, str):
            ticker_list = [ticker_list]

        end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=num_days)

        num_threads = min(len(ticker_list), threading.active_count())

        def download_data(ticker):
            download_historical_price_data(ticker, start_date, end_date, interval_minutes, self.pricedata_folder, self.progress)

        threads = []
        for ticker in ticker_list:
            thread = threading.Thread(target=download_data, args=(ticker,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

'''
downloader = DataDownloader(pricedata_folder='resources/pricedata', progress=True)

ticker_list = ['BTCUSDT', 'ETHUSDT']  # Liste der Tickersymbole
num_days = 7  # Anzahl der vergangenen Tage
interval_minutes = 15  # Intervall in Minuten

downloader.download_data_for_ndays(ticker_list, num_days, interval_minutes)
'''