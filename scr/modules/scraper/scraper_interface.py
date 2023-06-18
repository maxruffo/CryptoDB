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
    num_threads = min(len(ticker_list), threading.active_count() + 1)

    def download_data(tickers):
        for ticker in tickers:
            download_historical_price_data(ticker, start_date, end_date, interval_minutes)

    # Liste der Aufgaben für jeden Thread aufteilen
    task_list = []
    chunk_size = len(ticker_list) // num_threads

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = start_index + chunk_size if i < num_threads - 1 else None
        task_list.append(ticker_list[start_index:end_index])

    # Threads erstellen und ausführen
    threads = []
    for task in task_list:
        thread = threading.Thread(target=download_data, args=(task,))
        thread.start()
        threads.append(thread)

    # Warten, bis alle Threads ihre Aufgaben abgeschlossen haben
    for thread in threads:
        thread.join()



def download_data_for_ndays(tickers, ndays, interval_minutes):

    pass



tickers_list = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"]
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 1, 30)
interval_minutes = 30

download_data_for_dates(tickers_list, start_date, end_date, interval_minutes)