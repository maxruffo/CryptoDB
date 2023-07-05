#*imports*#
import sqlite3
import os
import csv
import threading



def create_database(database_name='database.db', database_path='resources/database', progress = True):
    '''
    Function that creates the SQL Database and Tables Assets and PriceData
    '''

    #Look if database folder exists
    database_file = os.path.join(database_path, database_name)
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    #Look if Database Folder already exists
    if not os.path.isfile(database_file):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Assets (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                type TEXT
            )
        ''')

       
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PriceData (
                ticker TEXT NOT NULL,
                timestamp DATE NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                close_time timestamp,
                quote_asset_volume REAL,
                number_of_trades INTEGER,
                taker_buy_base_asset_volume REAL,
                taker_buy_quote_asset_volume REAL,
                PRIMARY KEY (ticker, timestamp),
                FOREIGN KEY (ticker) REFERENCES Assets (ticker)
            )
        ''')

    
        conn.commit()
        conn.close()


        if progress == True:
            print(f'Datenbankdatei {database_name} wurde erstellt.')
    else:
        if progress == True:
            print(f'Datenbankdatei {database_name} existiert bereits.')



def insert_data_to_database(database_name='database.db', database_path='resources/database', pricedata_folder = 'resources/pricedata', progress = True):
    '''
    Function that inserts the downloaded csv data in a SQL Database
    '''
    
    database_path = os.path.join(database_path, database_name)

    def insert_data_to_db(db_path, folder_path, ticker_name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Überspringe den Header

                    for row in reader:
                        data_row = [ticker_name] + row
                        cursor.execute("INSERT OR IGNORE INTO PriceData VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       data_row)

        conn.commit()
        conn.close()

    threads = []
    for folder_name in os.listdir(pricedata_folder):
        folder_path = os.path.join(pricedata_folder, folder_name)
        if os.path.isdir(folder_path):
            ticker_name = folder_name 
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO Assets (ticker) VALUES (?)", (ticker_name,))

            conn.commit()
            conn.close()

            thread = threading.Thread(target=insert_data_to_db, args=(database_path, folder_path, ticker_name))
            thread.start()
            threads.append(thread)

    
    for thread in threads:
        thread.join()

    if progress == True:
        print('Daten wurden erfolgreich in die Datenbank eingefügt.')




def insert_data_to_database_for_one_ticker(ticker_name, database_name='database.db', database_path='resources/database', pricedata_folder='resources/pricedata', progress=True):
    '''
    Function that inserts the downloaded csv data for a specific ticker in a SQL Database
    '''

    database_path = os.path.join(database_path, database_name)

    def insert_data_to_db(db_path, folder_path, ticker_name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Überspringe den Header

                    for row in reader:
                        data_row = [ticker_name] + row
                        cursor.execute("INSERT OR IGNORE INTO PriceData VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       data_row)

        conn.commit()
        conn.close()

    folder_path = os.path.join(pricedata_folder, ticker_name)
    if os.path.isdir(folder_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Assets (ticker) VALUES (?)", (ticker_name,))

        conn.commit()
        conn.close()

        insert_data_to_db(database_path, folder_path, ticker_name)

    if progress:
        print('Daten wurden erfolgreich für Ticker', ticker_name, 'in die Datenbank eingefügt.')