import os
import sqlite3
import csv

database_folder = 'resources/database'
database_file = 'all_crypto_database.db'
database_path = os.path.join(database_folder, database_file)
pricedata_folder = 'resources/pricedata'

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Durchsuche den pricedata-Ordner
for folder_name in os.listdir(pricedata_folder):
    folder_path = os.path.join(pricedata_folder, folder_name)
    if os.path.isdir(folder_path):
        # Füge den Ordner-Namen als Ticker in die Assets-Tabelle ein, falls er noch nicht vorhanden ist
        cursor.execute("INSERT OR IGNORE INTO Assets (ticker) VALUES (?)", (folder_name,))

        # Durchsuche die CSV-Dateien im Ordner
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Überspringe den Header

                    for row in reader:
                        data_row = [folder_name] + row
                        cursor.execute("INSERT OR IGNORE INTO PriceData VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_row)

# Änderungen speichern und Verbindung zur Datenbank schließen
conn.commit()
conn.close()
print('Daten wurden erfolgreich in die Datenbank eingefügt.')
