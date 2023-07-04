# Cryptocurrencies-Data

Wie soll der Code Funktionieren:

- Nutzer gibt diese daten an:
- Ticker -> Liste von Strings mit Ticker
- Intervall -> Intervall in Minuten also abstände der Daten
- Start_date -> Datetime wann daten anfangen sollen
- End_date -> bis wann die Daten gehen sollen
   ODER:
- Ndays: rücklaufend wie viele Tage heruntergeladen werden sollen

Dann:

- Falls es eine Datenbank datei schon gibt soll er sich mit dieser Datenbank anbinden und verwenden, dann schaut er ob die Nötigen Daten also Ticker und PriceData vorhanden sind, falls nicht updated er die Daten um  die Api Calls zu minimieren

This Repository is updated daily with new Cryptoccurencies Data

## To - Do Open

- GROßES PROBLEM: download_historical_price_data das wenn falsche ticker angegeben Exception
- so machen das wenn man CryptoDB objekt erstellt man auch mit einer Datenbank verbinden kann anstatt das sie direkt erstellt wird
- methide erstellen welche daten von gestern uodated mit workflow

## To - Do Done

- aktuelles datum -1tag werden die daten auch für akutellen tag abgespeichert sollte nicht so sein
- datenbank namen ändern
- interface hinzufügen sodass für einen bestimmten ticker die Preis daten als datafram zurück gegeben werden
- so machen das ab 00 bis 23:59 heruntergeladen wird
- pricedata übergabe mit parameter include true oder false ob enddatum mit einzuschließen oder nicht
