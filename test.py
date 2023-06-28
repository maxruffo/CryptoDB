from scr.modules import CryptoDB


tickers = ["BTCUSDT", "ETHUSDT", "BNBUSDT",]
database = True
csv = True
ndays = 30
interval = 15


crypto = CryptoDB(tickers=tickers,database=database,csv=True,ndays=30,interval=15)
















"""import threading
import time

def animate(function_name):
    while thread.is_alive():
        animation = "|/-\\"
        for i in range(len(animation)):
            time.sleep(0.1)  # Wartezeit zwischen den Animationsschritten
            print(f"\r{function_name} {animation[i]}", end='', flush=True)

def time_wrapper(func):
    def wrapper(*args, **kwargs):
        global thread

        def run_func():
            func(*args, **kwargs)

        # Erstelle einen Thread für die Methode
        thread = threading.Thread(target=run_func)

        # Starte den Thread
        thread.start()

        # Starte die Animation im Hintergrund
        animate(func.__name__)

        # Warte, bis der Thread abgeschlossen ist
        thread.join()

        # Animation beenden
        print(f"\rDone! {func.__name__}")

    return wrapper

"""
