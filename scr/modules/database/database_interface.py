import sqlite3
import pandas as pd
from create_databse.create_database_structure import init_database
from create_databse.insert_data_in_database import insert_data
from database_app import SQLiteQueryTool
import time


class DatabaseManager:
    def __init__(self, database_path='resources/database/database.db'):
        self.database_path = database_path

    def create_and_fill_database(self):
        init_database()
        time.sleep(1)
        insert_data()

    def start_database_app(self):
        database_app = SQLiteQueryTool(self.database_path)
        database_app.run()

    def get_pricedata_for_ticker(self, ticker):
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM PriceData WHERE ticker='{ticker}'"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data

    def get_pricedata_for_date_range(self, start_date, end_date):
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM PriceData WHERE timestamp >= '{start_date}' AND timestamp <= '{end_date}'"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data

    def get_assets_by_sector(self, sector):
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM Assets WHERE sector='{sector}'"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data

    def get_assets_by_type(self, asset_type):
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM Assets WHERE type='{asset_type}'"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
