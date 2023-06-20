import sqlite3
import pandas as pd
from .create_database_structure import init_database
from .insert_data_in_database import insert_data
from .database_app import SQLiteQueryTool
import time


class DatabaseManager:
    def __init__(self, database_path='resources/database/database.db'):
        self.database_path = database_path
        self.create_and_fill_database()

    def create_and_fill_database(self):
        init_database()
        time.sleep(1)
        insert_data()

    def start_database_app(self):
        database_app = SQLiteQueryTool(self.database_path)
        database_app.run()


