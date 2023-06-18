import json
import os
import threading
from datetime import datetime

from binance_historcial_data import download_historical_price_data


#FUNCTION: set_tickers(ticker) -> @params ticker: a list of ticker is given its sets the config/ticker_list.json the list of ticker that where given

def set_tickers(tickers):
    ticker_dict = {"ticker": tickers}

    # Pfad zum Ordner "config"
    config_folder = "config"

    # Erstellen des Ordners, wenn er noch nicht existiert
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    # Pfad zur JSON-Datei
    json_file_path = os.path.join(config_folder, "tickerlist.json")

    # Speichern des JSON-Objekts in der Datei
    with open(json_file_path, "w") as json_file:
        json.dump(ticker_dict, json_file)


def get_tickers():
    # Pfad zur JSON-Datei
    json_file_path = os.path.join("config", "tickerlist.json")

    # Überprüfen, ob die JSON-Datei existiert
    if os.path.exists(json_file_path):
        # Öffnen der JSON-Datei und Laden des Inhalts in eine Python-Liste
        with open(json_file_path, "r") as json_file:
            ticker_dict = json.load(json_file)
            tickers = ticker_dict["ticker"]

            return tickers
    else:
        print("Die JSON-Datei existiert nicht.")
    
    
def download_data_for_dates(ticker_list, start_date, end_date, interval_minutes):
    for ticker in ticker_list:
        download_historical_price_data(ticker, start_date, end_date, interval_minutes)


def download_data_for_ndays(tickers, ndays, interval_minutes):

    pass



tickers_list = ["BTC", "ETH", "LTC", "XRP", "ADA", "DOGE"]
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 6, 30)
interval_minutes = 30

download_data_for_dates(tickers_list, start_date, end_date, interval_minutes)