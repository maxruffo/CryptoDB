import json
from converter import *
from binance_historcial_data import *




def process_tickers_from_json(json_file,num_days,intervall):
    with open(json_file, 'r') as file:
        data = json.load(file)
        ticker_list = data['ticker']

        start_date, end_date = calculate_start_end_dates(num_days)

        for ticker in ticker_list:
            # Hier kannst du den Methodenaufruf für jeden Ticker machen
            download_historical_price_data(ticker+"USDT", start_date, end_date, interval_minutes=intervall)

file = "config/ticker_list.json"
process_tickers_from_json(file,num_days=30, intervall= 1)


"""# Beispielaufruf
json_file = 'path/to/your/json/file.json'
process_tickers_from_json(json_file)


def process_ticker_list(json_file):
    # JSON-Datei einlesen
    with open(json_file, 'r') as file:
        ticker_list = json.load(file)

    # Suffix "USDT" zu jedem Element der Liste hinzufügen
    print(ticker_list)
    


    # Aufruf der Methode download_historical_price_data mit der modifizierten Liste
    start_date, end_date = calculate_start_end_dates(num_days)
    interval_minutes = interval
    for ticker in ticker_list:
        print(ticker)
        download_historical_price_data(ticker+"USDT", start_date, end_date, interval_minutes)



num_days = 30
file = "config/ticker_list.json"
start_date, end_date = process_ticker_list(file)


"""