import os
import requests
import csv
from datetime import datetime, timedelta

'''
@param ticker:
@param start_date:
@param end_date: [2023-06-16]
@param intervall: ["1s", "1m", "3m", "5m", "15m.", "30m"]
'''

def download_historical_price_data(ticker, start_date, end_date, intervall):
    #convert string to datetyp
    start_date = datetime.strptime(start_date,"%Y-%m-%d")
    end_date = datetime.strptime(end_date,"%Y-%m-%d")

    # Binance API-URL für historische Kursdaten
    url = "https://api.binance.com/api/v3/klines"

    # Datum für den Zeitraum festlegen (letztes Jahr)

    # Ordner für Preisdaten erstellen, falls nicht vorhanden
    output_folder = f"resources/pricedata/{ticker}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Schleife über jeden Tag im Zeitraum
    current_date = start_date
    while current_date <= end_date:
        # Formatierung des Datums
        start_timestamp = int(current_date.timestamp() * 1000)
        next_date = current_date + timedelta(days=1)
        end_timestamp = int(next_date.timestamp() * 1000)

        # Parameter für die API-Anfrage
        parameters = {
            "symbol": ticker,
            "interval": f"{intervall}m",
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": 1000  # Maximale Anzahl von Datensätzen pro Anfrage
        }

        # API-Anfrage senden
        response = requests.get(url, params=parameters)

        # Überprüfen, ob die API-Anfrage erfolgreich war
        if response.status_code == 200:
            data = response.json()

            # Dateiname für die CSV-Datei
            filename = current_date.strftime('%Y-%m-%d') + ".csv"
            filepath = os.path.join(output_folder, filename)

            # Daten in die CSV-Datei schreiben
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            print(f"Historische Preisdaten für {ticker} am {current_date.strftime('%Y-%m-%d')} wurden gespeichert.")

        # Zum nächsten Tag wechseln
        current_date = next_date

# Beispielaufruf für Bitcoin (BTC)
download_historical_price_data("BTC",start_date="2023-06-10",end_date="2023-06-12",intervall=1)
