import os
import requests
import json
from datetime import datetime, timedelta

def download_historical_bitcoin_data():
    # API-URL für historische Preisdaten
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical"

    # Datum für den Zeitraum festlegen (letztes Jahr)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    # Formatierung der Datumsangaben
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Parameter für die API-Anfrage
    parameters = {
        "symbol": "bitcoin",
        "time_start": start_date_str,
        "time_end": end_date_str,
        "interval": "1m"
    }

    # API-Anfrage senden
    response = requests.get(url, params=parameters)

    # Überprüfen, ob die API-Anfrage erfolgreich war
    if response.status_code == 200:
        data = response.json()
        # Ausgabedatei erstellen
        output_folder = "bitcoin_historical_data"
        output_file = os.path.join(output_folder, "bitcoin_historical_data.json")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Daten in die JSON-Datei schreiben
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Historische Preisdaten für Bitcoin wurden in '{output_file}' gespeichert.")
    else:
        print("Fehler beim Abrufen der Daten von der API.")
        print(response)

# Beispielaufruf
download_historical_bitcoin_data()
