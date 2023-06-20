import os
import sqlite3
import csv
import threading

def insert_data(database_name='database.db', database_path='resources/database'):
    database_path = os.path.join(database_path, database_name)
    pricedata_folder = 'resources/pricedata'

    # Funktion, um Daten in die Datenbank einzufügen
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

        # Änderungen speichern und Verbindung zur Datenbank schließen
        conn.commit()
        conn.close()

    # Durchsuche den pricedata-Ordner
    threads = []
    for folder_name in os.listdir(pricedata_folder):
        folder_path = os.path.join(pricedata_folder, folder_name)
        if os.path.isdir(folder_path):
            ticker_name = folder_name  # Verwende den Namen des Ordners als Ticker

            # Füge den Ordner-Namen als Ticker in die Assets-Tabelle ein, falls er noch nicht vorhanden ist
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO Assets (ticker) VALUES (?)", (ticker_name,))
            conn.commit()
            conn.close()

            # Erstelle und starte einen Thread für jeden Ordner
            thread = threading.Thread(target=insert_data_to_db, args=(database_path, folder_path, ticker_name))
            thread.start()
            threads.append(thread)

    # Warte auf Beendigung aller Threads
    for thread in threads:
        thread.join()

    print('Daten wurden erfolgreich in die Datenbank eingefügt.')


