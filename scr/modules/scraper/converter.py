import csv
import json

def convert_csv_to_json(csv_file, json_file):
    # Daten aus der CSV-Datei lesen
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # JSON-Datei erstellen und Daten schreiben
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Beispielaufruf
csv_file = 'resources/index-list/~index_cryptocurrencies_list.csv'
json_file = 'resources/index-list/~index_cryptocurrencies_list.json'
convert_csv_to_json(csv_file, json_file)
