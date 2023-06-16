import os
import requests
import pandas as pd

def get_50cryptocurrencies_by_marketcap_csv():
    # Pfad für die Ausgabedatei
    output_folder = "resources/index-list"
    output_file = os.path.join(output_folder, "~index_cryptocurrencies_list.csv")

    # Überprüfen, ob der Ausgabeordner existiert, andernfalls erstellen
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # API-URL für die Top-Kryptowährungen
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",  # Währung für die Preise (USD)
        "order": "market_cap_desc",  # Sortierreihenfolge nach Marktkapitalisierung
        "per_page": 50,  # Anzahl der Ergebnisse (50)
        "page": 1,  # Seite der Ergebnisse (1)
    }

    # API-Anfrage senden
    response = requests.get(url, params=params)
    data = response.json()

    # Überprüfen, ob die API-Anfrage erfolgreich war
    if response.status_code == 200:
        # Liste der Kryptowährungen und deren Daten extrahieren
        cryptocurrencies = []
        for item in data:
            crypto = {
                "Rank": item["market_cap_rank"],
                "Ticker": item["symbol"].upper(),
                "Name": item["name"],
                "Price": item["current_price"],
                "Market Cap": item["market_cap"],
                "Volume": item["total_volume"],
                "Change (24h)": item["price_change_percentage_24h"],
            }
            cryptocurrencies.append(crypto)

        # DataFrame erstellen und in CSV-Datei speichern
        df = pd.DataFrame(cryptocurrencies)
        df.to_csv(output_file, index=False)
        print(f"Die Top 50 Kryptowährungen wurden in '{output_file}' gespeichert.")
    else:
        print("Fehler beim Abrufen der Daten von der API.")

get_50cryptocurrencies_by_marketcap_csv()