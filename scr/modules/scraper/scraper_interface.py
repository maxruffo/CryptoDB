import json
import os
import threading
from datetime import datetime, timedelta
import shutil
from .binance_historcial_data import download_historical_price_data

class DataDownloader:
    def __init__(self, pricedata_folder='resources/pricedata', progress=True):
        self.progress = progress
        self.pricedata_folder = pricedata_folder

        if pricedata_folder is not None:
            if not os.path.exists(pricedata_folder):
                os.makedirs(pricedata_folder)
        if pricedata_folder is None:
            self.pricedata_folder = 'resources/pricedata'

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
            

    def delete_pricedata(self):
        '''
        Function that deletes the pricedata
        '''

        if os.path.exists(self.pricedata_folder):
            shutil.rmtree(self.pricedata_folder)
            print(f"Pricedata deleted")
        else:
            print(f"Pricedata does not exist")