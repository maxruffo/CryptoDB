'''
@author: Max Ruff
@version: v1.0.0
'''
from datetime import datetime


from exceptions.NormalExceptions import *


def check_param_type(param, type):
    return isinstance(param, type)

def check_intervall(intervall):
    allowed_intervall = [1, 3, 5, 15, 30]

    if intervall in allowed_intervall:
        return True
    else:
        return False

def check_ticker(ticker):
    if not ticker == None or len(ticker) == 0:
        return True
    else:
        return False 
    



def get_data_with_dates(ticker, start_date = None, end_date = None, intervall = 30):

    # Check if intervall is in the range of allowed interavalls
    print(intervall)
    if not check_intervall(intervall):
        raise IntervallError(f"Wrong Intervall: {intervall}, allowed Intervalls: [1, 3, 5, 15, 30]")

    # Check if ticker was given or ticker list length is lover than 0
    if not check_ticker(ticker):
        raise TickerError("Ticker can not be None or less than 0")

    # Check if start and end date are datetime datatypes
    if not check_param_type(start_date,datetime) or check_param_type(end_date, datetime):
        raise DateTypeError(f"Start date or End date habe the wrong DataType: start_date: {type(start_date)}, end_date: {end_date}")






def get_data_with_days(self, ticker, days, intervall = 30):
    print()
    
    
  





get_data_with_dates("BTCUSDT", datetime(2002, 2, 2), datetime(2002, 2, 2), 15)
