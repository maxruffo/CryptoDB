import json
import os
from datetime import datetime, date,timedelta
import sys
import sqlite3
import pandas as pd
from .scraper.scraper_interface import DataDownloader
from .database.database_interface import DatabaseManager
from .utils.progress_wrapper import time_wrapper

# Jetzt können Sie die Methoden und Klassen aus "scraper_interface" verwenden

'''
@param ticker: List of String for the Ticker 
@param database: Boolean indicating whether to use a database (True or False)
@param csv: Boolean indicating whether to use CSV files (True or False)
@param ndays: Number of days of data to consider (integer)
@param interval: Interval in minutes for data retrieval (integer)
@param start_date: Start date for data retrieval (YYYY-MM-DD format)
@param end_date: End date for data retrieval (YYYY-MM-DD format)
@param databasefolder: Folder path for the database (string)
@param databasename: Name of the database file (string)
@param pricedatafolder: Folder path for the price data (string)
'''



class CryptoDB:
    def __init__(self, **kwargs):
        self.update_parameters(**kwargs)
        self.update_parameters()
        try:
            self.connect_database()
        except Exception as e:
            self.create_database()

    def update_parameters(self, **kwargs):
        parameters = {
            "tickers": kwargs.get("tickers"),
            "use_database": kwargs.get("use_database"),
            "use_csv": kwargs.get("use_csv"),
            "ndays": kwargs.get("ndays"),
            "interval": kwargs.get("interval"),
            "start_date": kwargs.get("start_date"),
            "end_date": kwargs.get("end_date"),
            "database_folder": kwargs.get("database_folder"),
            "database_name": kwargs.get("database_name"),
            "pricedata_folder": kwargs.get("pricedata_folder")
        }
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

        self.scraper = DataDownloader(kwargs.get(self.pricedata_folder))

        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        ndays = kwargs.get("ndays")

        if (start_date or end_date) and ndays:
            raise ValueError("Both start_date/end_date and ndays cannot be specified simultaneously.")
        
        elif start_date and end_date:
            parameters["start_date"] = start_date.strftime("%Y-%m-%d")
            parameters["end_date"] = end_date.strftime("%Y-%m-%d")
            parameters["ndays"] = None
        elif start_date and end_date is None:
            parameters["start_date"] = start_date.strftime("%Y-%m-%d")
            parameters["end_date"] = date.today()
        elif ndays:
            parameters["ndays"] = ndays
            parameters["start_date"] = None
            parameters["end_date"] = None

        








   
    def create_database(self):
        if self.tickers is None:
            print("Eine Liste von Tickers wird benötigt.")

        if self.ndays:
            self.scraper.download_data_for_ndays(ticker_list=self.tickers, num_days=self.ndays, interval_minutes=self.interval)

        elif self.ndays is None and (self.start_date and self.end_date):
            self.scraper.download_data_for_dates(ticker_list=self.tickers, start_date=self.start_date, end_date=self.end_date, interval_minutes=self.interval)
        
            
        
        db = DatabaseManager()
        db.create_and_fill_database()
        self.db = db

            
   
    def connect_database(self, database_folder=None, database_name=None):
        if database_folder is None:
            database_folder = 'resources/database'
        if database_name is None:
            database_name = 'database.db'

        db = DatabaseManager()
        db.connect_to_existing_database()
        self.db = db

        # Überprüfen, ob die Datenbank veraltet oder unvollständig ist
        if self.check_database_status():
            self.update_database()

    
    def check_database_status(self):
        # Überprüfen, ob alle Ticker in der Datenbank vorhanden sind
        missing_tickers = self.get_missing_tickers()
        if missing_tickers:
            print(f"Die folgenden Ticker fehlen in der Datenbank: {missing_tickers}")
            return True

        # Überprüfen, ob die Preisdaten bis zum aktuellen Tag vorhanden sind
        end_date = date.today()
        missing_days = self.get_missing_days(end_date)
        if missing_days:
            print(f"Die Preisdaten sind nicht vollständig bis zum aktuellen Tag für die folgenden Tage: {missing_days}")
            return True

        return False

    
    def get_missing_tickers(self):
        available_tickers = self.db.get_tickers()
        missing_tickers = [ticker for ticker in self.tickers if ticker not in available_tickers]
        
        return missing_tickers
    
   
    def get_missing_days(self):
        end_date = datetime.now().date()
        missing_days = []

        for ticker in self.tickers:
            last_available_date = self.db.get_last_available_date(ticker)
            if last_available_date is not None:
                start_date = last_available_date + timedelta(days=1)
                missing_range = pd.date_range(start=start_date, end=end_date)
                missing_days.extend(missing_range)

        missing_days = list(set(missing_days)) 
        return missing_days

   
    def update_database(self):

        interval = self.db.get_timestamp_distance()
        if interval == None:
            self.create_databse() # <- fals einzelne daten fehlen soll einfach die Datenbank gerestet werden
        
        missing_tickers = self.get_missing_tickers()
        if missing_tickers:
            print(f"Fehlende Ticker werden heruntergeladen: {missing_tickers}")
            self.scraper.download_data_for_ndays(ticker_list=missing_tickers, num_days=self.ndays, interval_minutes=self.interval)

        end_date = date.today()
        missing_days = self.get_missing_days()
        if missing_days:
            print(f"Fehlende Preisdaten werden heruntergeladen: {missing_days}")
            self.scraper.download_data_for_dates(ticker_list=self.tickers, start_date=missing_days[0], end_date=end_date, interval_minutes=self.interval)

        self.db.update_database()

    def run_app(self):
        db = self.db
        db.start_database_app()

    def get_price_data(self, ticker_list=None):
        if ticker_list is None:
            ticker_list = self.tickers
        elif isinstance(ticker_list, str):
            ticker_list = [ticker_list]

        dataframes = self.db.get_price_data(ticker_list=ticker_list)
        return dataframes










'''
@param ticker: List of String for the Ticker 
@param database: Boolean indicating whether to use a database (True or False)
@param csv: Boolean indicating whether to use CSV files (True or False)
@param ndays: Number of days of data to consider (integer)
@param interval: Interval in minutes for data retrieval (integer)
@param start_date: Start date for data retrieval (YYYY-MM-DD format)
@param end_date: End date for data retrieval (YYYY-MM-DD format)
@param databasefolder: Folder path for the database (string)
@param databasename: Name of the database file (string)
@param pricedatafolder: Folder path for the price data (string)
'''




tickers = ["BTCUSDT", "ETHUSDT", "BNBUSDT",]
database = True
csv = True
ndays = 30
interval = 15


crypto = CryptoDB(tickers=tickers,database=database,csv=True,ndays=30,interval=15)














