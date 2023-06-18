import csv
import json
import os
from datetime import datetime,timedelta
def convert_csv_to_json(csv_file, json_file):
    # Daten aus der CSV-Datei lesen
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # JSON-Datei erstellen und Daten schreiben
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

'''# Beispielaufruf
csv_file = 'resources/index-list/~index_cryptocurrencies_list.csv'
json_file = 'resources/index-list/~index_cryptocurrencies_list.json'
convert_csv_to_json(csv_file, json_file)
'''

'''tickers = ["BTC", "ETH", "XRP", "LTC", "ADA"]

set_ticker_list_config_json(tickers)
'''

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







def extract_tickers_from_json(input_file, output_file):
    # Lade die Daten aus der Eingabe-JSON-Datei
    with open(input_file, 'r') as file:
        data = json.load(file)


    # Extrahiere die "Ticker" Werte aus den Datensätzen
    ticker_list = [item['Ticker'] for item in data]
    modified_data = {"ticker": ticker_list}

    # Speichere die "Ticker" Liste in der Ausgabe-JSON-Datei
    with open(output_file, 'w') as file:
        json.dump(modified_data, file)

    print('Ticker wurden erfolgreich in die Datei gespeichert.')



"""
input_file = 'resources/index-list/~index_cryptocurrencies_list.json'
output_file = 'config/ticker_list.json'



extract_tickers_from_json(input_file, output_file)"""




def calculate_start_end_dates(num_days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)
    print(end_date)
    print(type(end_date))
    print(start_date)
    print(type(start_date))
    if(type(start_date)==datetime):
        print("gunt")
    return start_date, end_date



calculate_start_end_dates(10)