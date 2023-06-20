import json
import os
from datetime import datetime, date
import sys
from .scraper.scraper_interface import download_data_for_dates,download_data_for_ndays,delete_pricedata_folder
from .database.database_interface import DatabaseManager
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
        self.update_config(**kwargs)
        self.load_config()
        self.run_jobs()

    def update_config(self, **kwargs):
        config_file = 'config/cryptodbconfig.json'

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {
                "tickers": [
                    "BTCUSDT",
                    "ETHUSDT",
                    "BNBUSDT"
                ],
                "database": True,
                "csv": True,
                "ndays": 30,
                "interval": 1,
                "start_date": "2023-05-20",
                "end_date": "2023-06-19",
                "databasefolder": "resources/database",
                "databasename": "database.db",
                "pricedatafolder": "resource/pricedata"
            }

            with open(config_file, 'w') as f:
                json.dump(config, f)

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        ndays = kwargs.get('ndays')

        if (start_date or end_date) and ndays:
            raise ValueError("Both start_date/end_date and ndays cannot be specified simultaneously.")
        elif start_date and end_date:
            config["start_date"] = start_date.strftime("%Y-%m-%d")
            config["end_date"] = end_date.strftime("%Y-%m-%d")
            config["ndays"] = None
        elif start_date and end_date == None:
            config["start_date"] = start_date.strftime("%Y-%m-%d")
            config["end_date"] = date.today()
        elif ndays:
            config["ndays"] = ndays
            config["start_date"] = None
            config["end_date"] = None
        

        database = kwargs.get('database')
        csv = kwargs.get('csv')
        interval = kwargs.get('interval')
        databasefolder = kwargs.get('databasefolder')
        databasename = kwargs.get('databasename')
        pricedatafolder = kwargs.get('pricedatafolder')

        if database is not None:
            config["database"] = bool(database)
        if csv is not None:
            config["csv"] = bool(csv)
        if interval is not None:
            config["interval"] = int(interval)
        if databasefolder is not None:
            config["databasefolder"] = str(databasefolder)
        if databasename is not None:
            config["databasename"] = str(databasename)
        if pricedatafolder is not None:
            config["pricedatafolder"] = str(pricedatafolder)

        with open(config_file, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        config_file = 'config/cryptodbconfig.json'

        with open(config_file, 'r') as f:
            config = json.load(f)

        self.tickers = config["tickers"]
        self.database = config["database"]
        self.csv = config["csv"]
        self.ndays = config["ndays"]
        self.interval = config["interval"]
        self.start_date = datetime.strptime(config["start_date"], "%Y-%m-%d") if config["start_date"] else None
        self.end_date = datetime.strptime(config["end_date"], "%Y-%m-%d") if config["end_date"] else None
        self.databasefolder = config["databasefolder"]
        self.databasename = config["databasename"]
        self.pricedatafolder = config["pricedatafolder"]

    
    def run_jobs(self):

        if self.ndays:
            download_data_for_ndays(ticker_list=self.tickers, num_days=self.ndays, interval_minutes=self.interval)

        elif self.ndays == None and (self.start_date and self.end_date):
            download_data_for_dates(ticker_list=self.tickers, start_date=self.start_date, end_date=self.end_date, interval_minutes=self.interval)
        

        if self.database == True:
            self.db = DatabaseManager()
            if self.csv == False:
                delete_pricedata_folder()

    def run_app(self):
        db = self.db
        db.start_database_app()

        


            
            







