import csv
import json
import os

def convert_csv_to_json(csv_file, json_file):
    # Daten aus der CSV-Datei lesen
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # JSON-Datei erstellen und Daten schreiben
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

"""# Beispielaufruf
csv_file = 'resources/index-list/~index_cryptocurrencies_list.csv'
json_file = 'resources/index-list/~index_cryptocurrencies_list.json'
convert_csv_to_json(csv_file, json_file)
"""



def set_ticker_list_config_json(tickers):
    output_folder = "config"
    output_file = os.path.join(output_folder, "ticker_list.json")

    # Überprüfen, ob der Ausgabeordner existiert, andernfalls erstellen
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ticker_list = {"tickers": tickers}

    with open(output_file, 'w') as file:
        json.dump(ticker_list, file)

    print(f"Die Ticker-Liste wurde in '{output_file}' gespeichert.")


tickers = ["BTC", "ETH", "XRP", "LTC", "ADA"]
output_file = "ticker_list.json"

set_ticker_list_config_json(tickers)
