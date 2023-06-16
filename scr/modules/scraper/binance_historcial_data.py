import os
import requests
import csv
from datetime import datetime, timedelta
from exceptions.InvalidDateException import InvalidDateComparisonError
from exceptions.InvalidIntervallException import InvalidIntervallError

'''
@params ticker:"ticker" + USDT -> "BTCUSDT
@params start_data: datetime(2022, 12, 20)
@params end_date: datetime(2022, 12, 20)
@interval_minutes: 
'''

def download_historical_price_data(ticker, start_date, end_date, interval_minutes):
    #Exception Kontrolle

    if start_date > end_date:
        raise InvalidDateComparisonError("Start date is after the End date")
    

    valid_intervals = [1, 3, 5, 15, 30]
    if interval_minutes not in valid_intervals:
        raise InvalidIntervallError("This is intervall isnt available, please use: [1, 3, 5, 15, 30]")



    # Binance API-URL für historische Kursdaten
    url = "https://api.binance.com/api/v3/klines"

    # Ordner für Preisdaten erstellen, falls nicht vorhanden
    output_folder = f"resources/pricedata/{ticker}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Schleife über den definierten Zeitraum
    current_date = start_date
    while current_date <= end_date:
        # Start- und Endzeit für den aktuellen Tag
        start_timestamp = int(current_date.timestamp() * 1000)
        next_date = current_date + timedelta(days=1)
        end_timestamp = int(next_date.timestamp() * 1000)

        # Parameter für die API-Anfrage
        parameters = {
            "symbol": ticker,
            "interval": f"{interval_minutes}m",
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": 1000  # Maximale Anzahl von Datensätzen pro Anfrage
        }

        try:
            # API-Anfrage senden
            response = requests.get(url, params=parameters)

            # Überprüfen, ob die API-Anfrage erfolgreich war
            if response.status_code == 200:
                data = response.json()

                # Dateiname für die CSV-Datei
                date_str = current_date.strftime('%Y-%m-%d')
                filename = f"{ticker}_{date_str}.csv"
                filepath = os.path.join(output_folder, filename)

                # Daten in die CSV-Datei schreiben
                with open(filepath, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for row in data:
                        timestamp = datetime.fromtimestamp(row[0] / 1000)  # Umwandlung des Unix-Zeitstempels in datetime
                        writer.writerow([timestamp] + row[1:])  # Schreiben der Zeile mit dem angepassten Datum

                print(f"Historische Preisdaten für {ticker} am {date_str} wurden gespeichert.")

        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der API-Anfrage für {ticker} am {current_date.strftime('%Y-%m-%d')}: {e}")


        # Zum nächsten Tag wechseln
        current_date = next_date

# Beispielaufruf für Bitcoin (BTC) vom 1. Januar 2022 bis 31. Dezember 2022 mit einem Intervall von 30 Minuten
start_date = datetime(2022, 12, 20)
end_date = datetime(2022, 12, 31)
interval_minutes = 30
download_historical_price_data("BTCUSDT", start_date, end_date, interval_minutes)
