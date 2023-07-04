
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

        self.scraper = DataDownloader(self.pricedata_folder, self.progress)
        self.db = DatabaseManager(self.database_name, self.database_folder)
    
        self._check_params()

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

    def _create_database(self):
        self.db.create_database()
    
    def _delete_database(self):
        self.db.delete_database()

    def _download_pricedata(self):
        if self.ndays == None:
            self.scraper.download_data_for_dates(self.tickers, self.start_date, self.end_date, self.interval)
        else:
            self.scraper.download_data_for_ndays(self.tickers, self.ndays, self.interval)
    
    def _delete_pricedata(self):
        self.scraper.delete_pricedata(self.tickers)

    def _insert_data_to_database(self):
        self.db.insert_data_to_database(self.pricedata_folder)

    def start_sqlite_GUI(self):
        self.db.start_database_app_GUI()



        





#test_db = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3,database=True,csv=False, interval=15)
start_date = datetime(2021,1,1)
end_date = datetime(2021,2,3)

print(start_date)
print(end_date)



test_db2 = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3, interval=15)
test_db2._delete_database()
test_db2._download_pricedata()
test_db2._create_database()
test_db2._insert_data_to_database()
test_db2._delete_pricedata()
test_db2.start_sqlite_GUI()
