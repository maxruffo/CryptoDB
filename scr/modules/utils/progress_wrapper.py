import threading
import time

def animate(function_name):
    while thread.is_alive():
        animation = "|/-\\"
        for i in range(len(animation)):
            time.sleep(0.1) 
            print(f"\r{function_name} {animation[i]}", end='', flush=True)

def time_wrapper(func):
    def wrapper(*args, **kwargs):
        global thread

        def run_func():
            func(*args, **kwargs)

        thread = threading.Thread(target=run_func)
        thread.start()
        animate(func.__name__)
        thread.join()
        
    return wrapper


