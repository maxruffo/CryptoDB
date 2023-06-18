import sqlite3
import os

#from insert_assets.insert_crypto_into_assets import _insert_crypto
#from insert_assets.insert_stocks_into_assets import _insert_stocks
#from insert_pricedata.insert_data_into_pricedata import _insert_pricedata


def init_database(database_path = 'resources/database', database_name = 'database.db'):
    database_folder = 'resources/database'
    database_file = 'database.db'
    database_path = os.path.join(database_folder, database_file)

    # Überprüfen, ob der Ordner bereits existiert, andernfalls erstellen
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)

    # Überprüfen, ob die Datenbankdatei bereits existiert
    if not os.path.exists(database_path):
        # Verbindung zur Datenbank herstellen oder eine neue Datenbank erstellen
        conn = sqlite3.connect(database_path)

        # Ein Cursor-Objekt erstellen, um SQL-Abfragen auszuführen
        cursor = conn.cursor()

        # Erste Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Assets (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                type TEXT
            )
        ''')

        # Zweite Tabelle erstellen
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



        # Änderungen speichern und die Verbindung zur Datenbank schließen
        conn.commit()
        conn.close()
        print(f'Datenbankdatei {database_file} wurde erstellt.')
    else:
        print(f'Datenbankdatei {database_file} existiert bereits.')


'''
Für die erstellung der Big Database wo sich alle Ticker und Price Daten befinden
'''



