import numpy as np
import talib

# Generate random data
np.random.seed(123)
close = np.random.random(100)
high = np.random.random(100)
low = np.random.random(100)
opem = np.random.random(100)

# Overlap Studies Functions
upper, middle, lower = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
print("BBANDS:", upper, middle, lower)

# Momentum Indicator Functions
output = talib.MOM(close, timeperiod=5)
print("MOM:", output)

# Volume Indicator Functions
volumes = np.random.random(100)
output = talib.OBV(close, volumes)
print("OBV:", output)

# Volatility Indicator Functions
output = talib.ATR(high, low, close, timeperiod=14)
print("ATR:", output)

# Price Transform Functions
output = talib.AVGPRICE(open, high, low, close)
print("AVGPRICE:", output)

# Cycle Indicator Functions
output = talib.HT_DCPERIOD(close)
print("HT_DCPERIOD:", output)

# Pattern Recognition Functions
output = talib.CDL3BLACKCROWS(open, high, low, close)
print("CDL3BLACKCROWS:", output)

# Statistic Functions
output = talib.BETA(high, low, timeperiod=5)
print("BETA:", output)

# Math Transform Functions
output = talib.ACOS(close)
print("ACOS:", output)

# Math Operator Functions
output = talib.ADD(high, low)
print("ADD:", output)
