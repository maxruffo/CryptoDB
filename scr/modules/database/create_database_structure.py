import sqlite3
import os

def init_database(database_name='database.db', database_path='resources/database'):
    database_file = os.path.join(database_path, database_name)

    # Überprüfen, ob der Ordner bereits existiert, andernfalls erstellen
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Überprüfen, ob die Datenbankdatei bereits existiert
    if not os.path.isfile(database_file):
        # Verbindung zur Datenbank herstellen oder eine neue Datenbank erstellen
        conn = sqlite3.connect(database_file)

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
        print(f'Datenbankdatei {database_name} wurde erstellt.')
    else:
        print(f'Datenbankdatei {database_name} existiert bereits.')


