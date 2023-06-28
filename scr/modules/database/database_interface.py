import sqlite3
import pandas as pd
from create_database import create_database,insert_data_to_database
from database_app import SQLiteQueryTool
import os

class DatabaseManager:
    def __init__(self, database_name='database.db', database_path='resources/database'):
        self.database_name = database_name
        self.database_path = database_path
        self.connection = None

        if not self.check_database_exists():
            self.create_and_fill_database()



    def check_database_exists(self):
        return os.path.exists(os.path.join(self.database_path, self.database_name))



    def create_and_fill_database(self, pricedata_folder='resources/pricedata', progress=True):
        '''
        Function that connects to a SQL Database and inserts the data from csv files located in 'resources/pricedata'
        '''

        create_database(self.database_name, self.database_path, progress)
        insert_data_to_database(self.database_name, self.database_path, pricedata_folder, progress)



    def connect_to_existing_database(self):
        '''
        Function that with a given database_name and database_path returns a sqlite3.Connection Object
        '''
        
        self.connection = sqlite3.connect(os.path.join(self.database_path, self.database_name))



    def start_database_app_GUI(self):
        '''
        Function that starts the GUI for the SQL Database
        '''

        direct_database_path = os.path.join(self.database_path, self.database_name)
        database_app = SQLiteQueryTool(direct_database_path)
        database_app.run()



    def get_price_data(self, ticker):
        '''
        Function that with a given ticker or list of tickers return a list of dataframes for the Pricedata
        '''

        if self.connection is None:
            self.connect_to_existing_database()

        cursor = self.connection.cursor()
        data_frames = []

        if isinstance(ticker, str):
            ticker = [ticker]

        for ticker_item in ticker:
            query = "SELECT * FROM PriceData WHERE Ticker = ?"
            cursor.execute(query, (ticker_item,))
            data = cursor.fetchall()

            if data:
                df = pd.DataFrame(
                    data,
                    columns=[
                        'Ticker', 'Timestamp', 'Open', 'High', 'Low', 'Close',
                        'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades',
                        'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume'
                    ]
                )
                data_frames.append(df)
                print(f"Price Data found for {ticker_item}\n")
            else:
                print(f"Price data NOT found for {ticker_item}\n")

        return data_frames



    def get_tickers(self):
        if self.connection is None:
            self.connect_to_existing_database()

        cursor = self.connection.cursor()
        query = "SELECT ticker FROM Assets"
        cursor.execute(query)
        data = cursor.fetchall()

        tickers = [item[0] for item in data] if data else []

        return tickers