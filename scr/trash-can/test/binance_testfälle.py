import requests
import pandas as pd

def download_klines(symbol, interval, start_time, end_time):
    base_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Anzahl der zurückgegebenen Klines pro Anfrage
    }

    response = requests.get(base_url, params=params)
    klines = response.json()

    # Konvertiere die Klines in ein DataFrame
    
    df = pd.DataFrame(klines)

    return df

# Beispielaufruf
symbol = 'BTC'
interval = '1m'
start_time = 1625000000000  # Unix-Zeitstempel im Millisekundenformat
end_time = 1625096400000

klines_df = download_klines(symbol, interval, start_time, end_time)
print(klines_df)
