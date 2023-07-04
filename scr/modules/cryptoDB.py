"""update_parameters

create_database


connect_database

check_database_status


get_missing_tickers

get_missing_days


update_database

run_app"""


from datetime import datetime, timedelta, date
import pandas as pd
from scraper.scraper_interface import DataDownloader
from database.database_interface import DatabaseManager
from logger.logging import Logger

class CryptoDB:
    @Logger
    def __init__(self, **kwargs):
        self.tickers = kwargs.get("tickers")
        self.ndays=kwargs.get("ndays")
        self.interval= kwargs.get("interval")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.database_folder =  kwargs.get("database_folder")
        self.database_name = kwargs.get("database_name")
        self.pricedata_folder =  kwargs.get("pricedata_folder")
        self.progress = kwargs.get("progress")

        self._check_params()

        
        self._connect_database()
        
            

    @Logger
    def _check_params(self):
        if self.pricedata_folder is None:
            self.pricedata_folder = 'resources/pricedata'
        if self.database_folder is None:
            self.database_folder = 'resources/database'
        if self.database_name is None:
            self.database_name = 'database.db'
        if self.progress is None:
            self.progress = True
        


        self.scraper = DataDownloader(self.pricedata_folder, self.progress)

        if (self.start_date or self.end_date) and self.ndays:
            raise ValueError("Both start_date/end_date and ndays cannot be specified simultaneously.")
    
        elif self.start_date and self.end_date:
            if isinstance(self.start_date, str):
                self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
            if isinstance(self.end_date, str):
                self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d")
            self.ndays = None
        
        elif self.start_date and self.end_date is None:
            if isinstance(self.start_date, str):
                self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
            self.end_date = date.today()
    @Logger
    def _connect_database(self):
        self.db = DatabaseManager(self.database_name, self.database_folder)
        self.db.connect_to_existing_database()

        if self._check_database_status_for_missing_data():
            self.update_database()

    @Logger
    def _check_database_status_for_missing_data(self):

        
        missing_tickers = self.get_missing_tickers()
        if missing_tickers:
            return True
        

        missing_days = self.get_missing_days()
        if missing_days:
            return True


    @Logger
    def get_missing_tickers(self):
        available_tickers = self.db.get_tickers()
        if available_tickers:
            missing_tickers = [ticker for ticker in self.tickers if ticker not in available_tickers]
            return missing_tickers
        
        return False
    
    @Logger
    def get_missing_days(self):
        last_date = self.db.get_last_date()
        if last_date == date.today():
            return False
        else:
            return self.db.get_last_date()
    

    @Logger
    def update_database(self):
        interval = self.db.get_timestamp_distance()
        if interval == None:
            interval = self.interval
        
        missing_tickers = self.get_missing_tickers()
        if missing_tickers:
            self.db.insert_tickers(missing_tickers)
            if self.ndays == None:
                self.scraper.download_data_for_dates(missing_tickers, self.start_date, self.end_date, interval)
            else:
                self.scraper.download_data_for_ndays(missing_tickers, self.ndays, self.interval)

        missing_days = self.get_missing_days()
        if missing_days:
            if self.ndays == None:
                self.scraper.download_data_for_dates(self.tickers, missing_days, self.end_date, self.interval)
            else:
                self.scraper.download_data_for_ndays(self.tickers, self.ndays, self.interval)





#test_db = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3,database=True,csv=False, interval=15)
start_date = datetime(2021,1,1)
end_date = datetime(2021,1,3)

print(start_date)
print(end_date)



test_db2 = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],start_date=start_date,end_date=end_date, interval=15)