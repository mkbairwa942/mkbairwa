#import yfinance as yf
#import ta
#from ta import add_all_ta_features
#from ta.utils import dropna
# import pandas_ta as pta
#from finta import TA
# import talib
# import pandas as pd
# import copy
# import numpy as np
# import xlwings as xw
# from five_paisa import *
# from datetime import datetime,timedelta
# from numpy import log as nplog
# from numpy import NaN as npNaN
# from pandas import DataFrame, Series
# from pandas_ta.overlap import ema, hl2
# from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
# from io import BytesIO
# import os
# from zipfile import ZipFile
# import requests
# import itertools

from telethon.sync import TelegramClient
import datetime
import pandas as pd
import requests
import time

first_name = "mkbairwa"
username = "mkbairwa_bot"
id = ":758543600"

print("hi")
resp = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getMe")
resp1 = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates")
resp2 = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates?offset=6432816471")

basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates"



parameters = {
    "offset" : ":758543600",
    #"limit" : "2"
}

resp = requests.get(basr_url, data=parameters)
#print(resp.text)

basr_url1 = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage"

jokes = ["I Invented a New Bot","jokes1","jokes2","jokes3"]
for joke in jokes:
    time.sleep(2)
    parameters1 = {
        "chat_id" : "6143172607",
        "text" : joke
    }

    resp = requests.get(basr_url1, data=parameters1)
    print(resp.text)

print("hi_all")
