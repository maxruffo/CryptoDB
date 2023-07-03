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
        self.use_database =  kwargs.get("use_database")
        self.use_csv= kwargs.get("use_csv")
        self.ndays=kwargs.get("ndays")
        self.interval= kwargs.get("interval")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.database_folder =  kwargs.get("database_folder")
        self.database_name = kwargs.get("database_name")
        self.pricedata_folder =  kwargs.get("pricedata_folder")
        self.progress = kwargs.get("progress")

        self._check_params()

        try :
            self._connect_database()
        except Exception as e:
            print(e)
            

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
        if self.use_database is None:
            self.use_database = True


        self.scraper = DataDownloader(self.pricedata_folder, self.progress)

        if (self.start_date or self.end_date) and self.ndays:
            raise ValueError("Both start_date/end_date and ndays cannot be specified simultaneously.")
        
        elif self.start_date and self.end_date:
            self.start_date= self.start_date.strftime("%Y-%m-%d")
            self.end_date = self.end_date.strftime("%Y-%m-%d")
            self.ndays = None
        
        elif self.start_date and self.end_date is None:
            self.start_date = self.start_date.strftime("%Y-%m-%d")
            self.end_date = date.today()
        
        elif self.ndays:
            self.start_date = None
            self.end_date = None
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
        
        if self.ndays is not None:
            end_date = datetime.now().date()
        else:
            end_date = self.end_date

        missing_days = self.get_missing_days(end_date)
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
    def get_missing_days(self,end_date):
        missing_days = []

        for ticker in self.tickers:
            last_available_date = self.db.get_last_dates()
            if last_available_date is not None:
                start_date = last_available_date + timedelta(days=1)
                missing_range = pd.date_range(start=start_date, end=end_date)
                missing_days.extend(missing_range)

        missing_days = list(set(missing_days)) 
        return missing_days

    @Logger
    def update_database(self):
        interval = self.db.get_timestamp_distance()
        if interval == None:
            interval = self.interval
        
        missing_tickers = self._get_missing_tickers()
        if missing_tickers:
            if self.ndays == None:
                self.scraper.download_historical_price_data(missing_tickers, self.start_date, self.end_date, self.interval)
            else:
                self.scraper.download_historical_price_data(missing_tickers, self.ndays, self.interval)

            missing_days = self._get_missing_days(self.end_date)
            if missing_days:
                if self.ndays == None:
                    self.scraper.download_historical_price_data(missing_tickers, missing_days, self.interval)





test_db = CryptoDB(tickers=["BTCUSDT","ETHUSDT"],ndays=3,database=True,csv=False, interval=15)
