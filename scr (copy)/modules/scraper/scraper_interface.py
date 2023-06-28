import json
import os
import threading
from datetime import datetime, timedelta
import shutil
from .binance_historcial_data import download_historical_price_data

__all__ = ['download_historical_price_data', 'binance_historcial_data','download_data_for_dates', 'download_data_for_ndays', 'update_data_for_yesterday', 'delete_pricedata_folder']


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

'''
FUNCTION: Takes a ticker_list, start and enddate and a given intervall time, downloads the price data for the given days and stores'''
def download_data_for_dates(ticker_list, start_date, end_date, interval_minutes):
    if isinstance(ticker_list, str):
        ticker_list = [ticker_list]

    num_threads = min(len(ticker_list), threading.active_count())

    def download_data(ticker):
        download_historical_price_data(ticker, start_date, end_date, interval_minutes)

    threads = []
    for ticker in ticker_list:
        thread = threading.Thread(target=download_data, args=(ticker,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def download_data_for_ndays(ticker_list, num_days, interval_minutes):
    if isinstance(ticker_list, str):
        ticker_list = [ticker_list]

    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=num_days)

    num_threads = min(len(ticker_list), threading.active_count())

    def download_data(ticker):
        download_historical_price_data(ticker, start_date, end_date, interval_minutes)

    threads = []
    for ticker in ticker_list:
        thread = threading.Thread(target=download_data, args=(ticker,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def update_data_for_yesterday(ticker_list, interval_minutes):
    #Überprüfen falls nur ein Ticker wird es in eine Liste umgewandelt
    if isinstance(ticker_list, str):
            ticker_list = [ticker_list]

    yesterday = datetime.now() - timedelta(days=1)
    start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)

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

  
def delete_pricedata_folder():
    folder_path = "resources/pricedata"

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting folder '{folder_path}': {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")





