import sqlite3
import pandas as pd
from .create_database import create_database,insert_data_to_database, insert_data_to_database_for_one_ticker
from .database_app import SQLiteQueryTool
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, database_name='database.db', database_path='resources/database',pricedata_folder='resources/pricedata', progress=True):
        self.database_name = database_name
        self.database_path = database_path
        self.connection = None
        self.progress = progress

        self.pricedata_folder = pricedata_folder

        if self.pricedata_folder is None:
            self.pricedata_folder = 'resources/pricedata'
        
        if self.check_database_exists():
            self.connect_to_existing_database()
        


    def check_database_exists(self):
        return os.path.exists(os.path.join(self.database_path, self.database_name))
    
    def connect_to_existing_database(self):
        self.connection = sqlite3.connect(os.path.join(self.database_path, self.database_name))


    def create_and_fill_database(self, pricedata_folder='resources/pricedata', progress=True):
        create_database(self.database_name, self.database_path, progress)
        insert_data_to_database(self.database_name, self.database_path, pricedata_folder, progress)


    def create_database(self):
        create_database(self.database_name, self.database_path, self.progress)
    

    def insert_data_to_database(self, pricedata_folder='resources/pricedata', progress=True):
        insert_data_to_database(self.database_name, self.database_path, pricedata_folder, progress)

    def insert_data_for_ticker(self, ticker, pricedata_folder='resources/pricedata', progress=True):
        insert_data_to_database_for_one_ticker(self.database_name, self.database_path, ticker, pricedata_folder, progress)
    

    def delete_database(self):
        if self.check_database_exists():
            os.remove(os.path.join(self.database_path, self.database_name))
            
            print(f"Database {self.database_name} deleted")
        else:
            print(f"Database {self.database_name} does not exist")


    def start_database_app_GUI(self):
        direct_database_path = os.path.join(self.database_path, self.database_name)
        database_app = SQLiteQueryTool(direct_database_path)
        database_app.run()


    def get_price_data(self, ticker):
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


    def insert_tickers(self, tickers):
        if isinstance(tickers, str):
            tickers = [tickers]

        if self.connection is None:
            self.connect_to_existing_database()

        cursor = self.connection.cursor()
        for ticker in tickers:
            query = f"INSERT INTO Tickers (Ticker) VALUES ('{ticker}')"
            cursor.execute(query)

        self.connection.commit()

    
    def get_last_date(self):
        if self.connection is None:
            self.connect_to_existing_database()

        cursor = self.connection.cursor()
        query = "SELECT Ticker, MAX(Timestamp) FROM PriceData GROUP BY Ticker"
        cursor.execute(query)
        data = cursor.fetchall()

        last_dates = {item[0]: item[1] for item in data} if data else {}

        oldest_date = None
        for ticker, date_str in last_dates.items():
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            if oldest_date is None or date < oldest_date:
                oldest_date = date

        return oldest_date


    def get_timestamp_distance(self):
        '''
        Function that calculates the distance in minutes between Timestamp field and the next entry for the last 10 entries of each ticker
        '''

        if self.connection is None:
            self.connect_to_existing_database()

        cursor = self.connection.cursor()

        query = """
        SELECT pd1.Ticker, pd1.Timestamp, MIN(pd2.Timestamp) AS NextTimestamp
        FROM PriceData AS pd1
        LEFT JOIN PriceData AS pd2 ON pd2.Ticker = pd1.Ticker AND pd2.Timestamp > pd1.Timestamp
        WHERE pd1.Timestamp IN (
            SELECT Timestamp
            FROM PriceData
            WHERE Ticker = pd1.Ticker
            ORDER BY Timestamp DESC
            LIMIT 10
        )
        GROUP BY pd1.Ticker, pd1.Timestamp
        """

        cursor.execute(query)
        data = cursor.fetchall()

        distances = []

        for ticker, timestamp, next_timestamp in data:
            if next_timestamp:
                distance = int((datetime.strptime(next_timestamp, '%Y-%m-%d %H:%M:%S') - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).total_seconds() / 60)
                distances.append(distance)

        unique_distances = list(set(distances))
        if len(unique_distances) == 1:
            return unique_distances[0]
        else:
            return None
        

    
