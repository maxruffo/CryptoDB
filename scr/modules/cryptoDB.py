
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

        #that it Prints the progress of the download and insert process
        self.progress = kwargs.get("progress")
        
        # if store in database
        self.use_database = kwargs.get("use_database")
        self.use_csv = kwargs.get("use_csv")
        

        # Set default values
        if self.pricedata_folder is None:
            self.pricedata_folder = 'resources/pricedata'
        if self.database_folder is None:
            self.database_folder = 'resources/database'
        if self.database_name is None:
            self.database_name = 'database.db'
        if self.use_database is None:
            self.use_database = True
        if self.use_csv is None:
            self.use_csv = False

        if self.progress is None:
            self.progress = True

        # Initialize objects
        self.scraper = DataDownloader(self.pricedata_folder, self.progress)
        self.db = DatabaseManager(self.database_name, self.database_folder)
    
        # Check parameters
        self._check_params()

        # Delete database if it exists
        self._run_all_with_params()


    '''Methods that shouldnt be called by the user'''
    @Logger
    def _check_params(self):
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

    def _run_all_with_params(self):
        if self._check_database_status()==False:
            if self.db.check_database_exists():
                self.db.delete_database()
                self._download_pricedata()
                if self.use_database:
                    self._create_database()
                    self._insert_data_to_database()
                if self.use_csv == False:
                    self._delete_pricedata()
        

    # A Function that checks if the database is the same as the one that should be created
    def _check_database_status(self):
        if self.db.check_database_exists():
            if self.db.get_tickers() == self.tickers:
                if self.db.get_last_date() == self.end_date:
                    if self.db.get_timestamp_distance() == self.interval:
                        return True
        return False


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
        self.scraper.delete_pricedata()

    def _insert_data_to_database(self):
        self.db.insert_data_to_database(self.pricedata_folder)


    '''Methods that can be called by the user'''    

    def start_sqlite_GUI(self):
        self.db.start_database_app_GUI()

    def get_price_data(self, ticker):
        return self.db.get_price_data(ticker)
    
    def get_tickers(self):
        return self.db.get_tickers()
    
    def get_last_date(self):
        return self.db.get_last_date()
    
    def get_timestamp_distance(self):
        return self.db.get_timestamp_distance()
    
    def insert_tickers(self, tickers):
        self.db.insert_tickers(tickers)
    



pricedatadb = CryptoDB(tickers=['BTCUSDT', 'ETHUSDT'], ndays=10, interval_minutes=60, progress=True, use_database=True, use_csv=True)
pricedatadb.start_sqlite_GUI()