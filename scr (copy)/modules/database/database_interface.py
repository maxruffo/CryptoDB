import sqlite3
import pandas as pd
from .create_database_structure import init_database
from .insert_data_in_database import insert_data
from .database_app import SQLiteQueryTool
import time
import os


class DatabaseManager:
    def __init__(self, database_path='resources/database/database.db'):
        self.database_path = database_path
        

    def create_and_fill_database(self):
        init_database()
        time.sleep(1)
        insert_data()

    def connect_to_existing_database(self, databasefolder = None, databasename = None):
        if databasefolder is not None and databasename is not None:
            self.database_path = os.path.join(databasefolder, databasename)

    def start_database_app(self):
        database_app = SQLiteQueryTool(self.database_path)
        database_app.run()



    def get_price_data(self, ticker_list):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        data_frames = []

        for ticker in ticker_list:
            query = "SELECT * FROM PriceData WHERE Ticker = ?"
            cursor.execute(query, (ticker,))
            data = cursor.fetchall()

            # If data is found for the ticker, create a DataFrame and append it to the list
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

        conn.close()
        return data_frames

    
                        


