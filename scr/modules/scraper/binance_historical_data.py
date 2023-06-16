import os
import requests
import json
from datetime import datetime, timedelta

def download_historical_bitcoin_data():
    # Binance API-URL für historische Kursdaten
    url = "https://api.binance.com/api/v3/klines"

    # Datum für den Zeitraum festlegen (letztes Jahr)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Formatierung der Datumsangaben
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)

    # Parameter für die API-Anfrage
    parameters = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "startTime": start_timestamp,
        "endTime": end_timestamp,
        "limit": 1000  # Maximale Anzahl von Datensätzen pro Anfrage
    }

    # API-Anfrage senden
    response = requests.get(url, params=parameters)

    # Überprüfen, ob die API-Anfrage erfolgreich war
    if response.status_code == 200:
        data = response.json()

        # Konvertierung der Unix-Zeitstempel in Datumsformat
        converted_data = []
        for entry in data:
            timestamp = entry[0] / 1000  # Unix-Zeitstempel in Sekunden
            date = datetime.fromtimestamp(timestamp)
            entry[0] = date.strftime('%Y-%m-%d %H:%M:%S')
            converted_data.append(entry)

        # Ausgabedatei erstellen
        output_folder = "bitcoin_historical_data"
        output_file = os.path.join(output_folder, "bitcoin_historical_data.json")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Daten in die JSON-Datei schreiben
        with open(output_file, 'w') as file:
            json.dump(converted_data, file, indent=4)
        print(f"Historische Preisdaten für Bitcoin wurden in '{output_file}' gespeichert.")
    else:
        print("Fehler beim Abrufen der Daten von der API.")

# Beispielaufruf
download_historical_bitcoin_data()
