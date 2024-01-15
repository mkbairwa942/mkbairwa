#import yfinance as yf
#import ta
#from ta import add_all_ta_features
#from ta.utils import dropna
import pandas_ta as pta
#from finta import TA
# import talib
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import datetime,timedelta
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from io import BytesIO
import os
import sys
from zipfile import ZipFile
import requests
import itertools
import math 
from telethon.sync import TelegramClient
#from notifypy import Notify
#from plyer import notification
import inspect
import time
from five_paisa1 import *
#from Breakout_opt_vol_pri_mix_new_TRIAL import stk_list

telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

# operate = input("Do you want to go with TOTP (yes/no): ")
# #notifi = input("Do you want to send Notification on Desktop (yes/no): ")
# telegram_msg = input("Do you want to send TELEGRAM Message (yes/no): ")
# orders = input("Do you want to Place Real Orders (yes/no): ")
# if operate.upper() == "YES":
#     from five_paisa1 import *
#     username = input("Enter Username : ")
#     username1 = str(username)
#     print("Hii "+str(username1)+" have a Good Day")
#     client = credentials(username1)
# else:
from five_paisa import *

# operate = "YES"
# telegram_msg = "no"
# orders = "no"
# username = "ASHWIN"
# username1 = str(username)
# client = credentials(username1)

from_d = (date.today() - timedelta(days=15))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

days_365 = (date.today() - timedelta(days=365))
print(days_365)

holida = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
holida["Date"] = holida["Date1"].dt.date
holida1 = np.unique(holida['Date'])

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holida1)
trading_dayss = trading_days_reverse[::-1]
trading_days = trading_dayss[1:]
# trading_days = trading_dayss[2:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[0]
second_last_trading_day = trading_days[1]

# current_trading_day = trading_dayss[1]
# last_trading_day = trading_dayss[2]
# second_last_trading_day = trading_days[3]

print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last 365 Day is :- "+str(days_365))

days_count = len(trading_days)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

import csv
import os
#import yfinance as yf
import pandas as pd
import threading
from threading import Thread



# stk_list = ['55319',	'55320',	'55321',	'55323',	'55324',	'55325',	'55326',	'55327',	'55328',	'55329',	'55330',	'55332',	'55333',	'55334',	'55335',	'55336',	'55337',	'55338',	'55339',	'55340',	'55341',	'55342',	'55343',	'55344',	'55345',	'55347',	'55348',	'55349',	'55351',	'55352',	'55353',	'55354',	'55355',	'55356',	'55357',	'55358',	'55359',	'55360',	'55361',	'55362',	'55363',	'55364',	'55365',	'55366',	'55368',	'55369',	'55370',	'55371',	'55372',	'55373',	'55374',	'55375',	'55376',	'55377',	'55378',	'55379',	'55381',	'55382',	'55384',	'55385',	'55386',	'55387',	'55388',	'55389',	'55390',	'55391',	'55392',	'55393',	'55394',	'55395',	'55396',	'55397',	'55399',	'55400',	'55401',	'55402',	'55404',	'55409',	'55412',	'55413',	'55414',	'55415',	'55416',	'55417',	'55418',	'55419',	'55421',	'55422',	'55423',	'55424',	'55425',	'55426',	'55427',	'55428',	'55429',	'55430',	'55431',	'55432',	'55433',	'55434',	'55435',	'55436',	'55437',	'55438',	'55440',	'55441',	'55442',	'55443',	'55444',	'55445',	'55446',	'55449',	'55450',	'55451',	'55454',	'55457',	'55458',	'55459',	'55460',	'55461',	'55462',	'55463',	'55464',	'55465',	'55467',	'55468',	'55469',	'55470',	'55471',	'55473',	'55474',	'55476',	'55477',	'55478',	'55479',	'55480',	'55482',	'55483',	'55486',	'55487',	'55488',	'55489',	'55490',	'55493',	'55494',	'55495',	'55496',	'55497',	'55498',	'55499',	'55500',	'55504',	'55505',	'55506',	'55508',	'55510',	'55511',	'55512',	'55513',	'55514',	'55515',	'55516',	'55519',	'55520',	'55521',]

stk_list = ['AARTIIND 25 Jan 2024',	'ABB 25 Jan 2024',	'ABBOTINDIA 25 Jan 2024',	'ABFRL 25 Jan 2024',	'ACC 25 Jan 2024',	'ADANIENT 25 Jan 2024',	'ADANIPORTS 25 Jan 2024',	'ALKEM 25 Jan 2024',	'AMBUJACEM 25 Jan 2024',	'APOLLOHOSP 25 Jan 2024',	'APOLLOTYRE 25 Jan 2024',	'ASIANPAINT 25 Jan 2024',	'ASTRAL 25 Jan 2024',	'ATUL 25 Jan 2024',	'AUBANK 25 Jan 2024',	'AUROPHARMA 25 Jan 2024',	'AXISBANK 25 Jan 2024',	'BAJAJ-AUTO 25 Jan 2024',	'BAJAJFINSV 25 Jan 2024',	'BAJFINANCE 25 Jan 2024',	'BALKRISIND 25 Jan 2024',	'BALRAMCHIN 25 Jan 2024',	'BANDHANBNK 25 Jan 2024',	'BANKBARODA 25 Jan 2024',	'BATAINDIA 25 Jan 2024',	'BERGEPAINT 25 Jan 2024',	'BHARATFORG 25 Jan 2024',	'BHARTIARTL 25 Jan 2024',	'BIOCON 25 Jan 2024',	'BOSCHLTD 25 Jan 2024',	'BPCL 25 Jan 2024',	'BRITANNIA 25 Jan 2024',	'BSOFT 25 Jan 2024',	'CANBK 25 Jan 2024',	'CANFINHOME 25 Jan 2024',	'CHAMBLFERT 25 Jan 2024',	'CHOLAFIN 25 Jan 2024',	'CIPLA 25 Jan 2024',	'COALINDIA 25 Jan 2024',	'COFORGE 25 Jan 2024',	'COLPAL 25 Jan 2024',	'CONCOR 25 Jan 2024',	'COROMANDEL 25 Jan 2024',	'CROMPTON 25 Jan 2024',	'CUMMINSIND 25 Jan 2024',	'DABUR 25 Jan 2024',	'DALBHARAT 25 Jan 2024',	'DEEPAKNTR 25 Jan 2024',	'DELTACORP 25 Jan 2024',	'DIVISLAB 25 Jan 2024',	'DIXON 25 Jan 2024',	'DLF 25 Jan 2024',	'DRREDDY 25 Jan 2024',	'EICHERMOT 25 Jan 2024',	'ESCORTS 25 Jan 2024',	'EXIDEIND 25 Jan 2024',	'GAIL 25 Jan 2024',	'GLENMARK 25 Jan 2024',	'GNFC 25 Jan 2024',	'GODREJCP 25 Jan 2024',	'GODREJPROP 25 Jan 2024',	'GRANULES 25 Jan 2024',	'GRASIM 25 Jan 2024',	'GUJGASLTD 25 Jan 2024',	'HAL 25 Jan 2024',	'HAVELLS 25 Jan 2024',	'HCLTECH 25 Jan 2024',	'HDFCAMC 25 Jan 2024',	'HDFCBANK 25 Jan 2024',	'HDFCLIFE 25 Jan 2024',	'HEROMOTOCO 25 Jan 2024',	'HINDALCO 25 Jan 2024',	'HINDPETRO 25 Jan 2024',	'HINDUNILVR 25 Jan 2024',	'ICICIBANK 25 Jan 2024',	'ICICIGI 25 Jan 2024',	'ICICIPRULI 25 Jan 2024',	'IEX 25 Jan 2024',	'IGL 25 Jan 2024',	'INDHOTEL 25 Jan 2024',	'INDIACEM 25 Jan 2024',	'INDIAMART 25 Jan 2024',	'INDIGO 25 Jan 2024',	'INDUSINDBK 25 Jan 2024',	'INDUSTOWER 25 Jan 2024',	'INFY 25 Jan 2024',	'IPCALAB 25 Jan 2024',	'IRCTC 25 Jan 2024',	'ITC 25 Jan 2024',	'JINDALSTEL 25 Jan 2024',	'JKCEMENT 25 Jan 2024',	'JSWSTEEL 25 Jan 2024',	'JUBLFOOD 25 Jan 2024',	'KOTAKBANK 25 Jan 2024',	'L&TFH 25 Jan 2024',	'LALPATHLAB 25 Jan 2024',	'LAURUSLABS 25 Jan 2024',	'LICHSGFIN 25 Jan 2024',	'LT 25 Jan 2024',	'LTIM 25 Jan 2024',	'LTTS 25 Jan 2024',	'LUPIN 25 Jan 2024',	'M&M 25 Jan 2024',	'M&MFIN 25 Jan 2024',	'MARICO 25 Jan 2024',	'MARUTI 25 Jan 2024',	'MCDOWELL-N 25 Jan 2024',	'MCX 25 Jan 2024',	'METROPOLIS 25 Jan 2024',	'MFSL 25 Jan 2024',	'MGL 25 Jan 2024',	'MPHASIS 25 Jan 2024',	'MRF 25 Jan 2024',	'MUTHOOTFIN 25 Jan 2024',	'NAUKRI 25 Jan 2024',	'NAVINFLUOR 25 Jan 2024',	'NESTLEIND 25 Jan 2024',	'NMDC 25 Jan 2024',	'NTPC 25 Jan 2024',	'OBEROIRLTY 25 Jan 2024',	'OFSS 25 Jan 2024',	'ONGC 25 Jan 2024',	'PAGEIND 25 Jan 2024',	'PEL 25 Jan 2024',	'PERSISTENT 25 Jan 2024',	'PETRONET 25 Jan 2024',	'PFC 25 Jan 2024',	'PIDILITIND 25 Jan 2024',	'PIIND 25 Jan 2024',	'POLYCAB 25 Jan 2024',	'POWERGRID 25 Jan 2024',	'PVRINOX 25 Jan 2024',	'RAMCOCEM 25 Jan 2024',	'RBLBANK 25 Jan 2024',	'RECLTD 25 Jan 2024',	'RELIANCE 25 Jan 2024',	'SBICARD 25 Jan 2024',	'SBILIFE 25 Jan 2024',	'SBIN 25 Jan 2024',	'SHREECEM 25 Jan 2024',	'SHRIRAMFIN 25 Jan 2024',	'SIEMENS 25 Jan 2024',	'SRF 25 Jan 2024',	'SUNPHARMA 25 Jan 2024',	'SUNTV 25 Jan 2024',	'SYNGENE 25 Jan 2024',	'TATACHEM 25 Jan 2024',	'TATACOMM 25 Jan 2024',	'TATACONSUM 25 Jan 2024',	'TATAMOTORS 25 Jan 2024',	'TATAPOWER 25 Jan 2024',	'TCS 25 Jan 2024',	'TECHM 25 Jan 2024',	'TITAN 25 Jan 2024',	'TORNTPHARM 25 Jan 2024',	'TRENT 25 Jan 2024',	'TVSMOTOR 25 Jan 2024',	'UBL 25 Jan 2024',	'ULTRACEMCO 25 Jan 2024',	'UPL 25 Jan 2024',	'VEDL 25 Jan 2024',	'VOLTAS 25 Jan 2024',	'WIPRO 25 Jan 2024',	'ZEEL 25 Jan 2024',	'ZYDUSLIFE 25 Jan 2024',]
start = time.time()

a = [{'Exchange':'N','ExchangeType':'D','Symbol':'AARTIIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ABB 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ABBOTINDIA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ABFRL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ACC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ADANIENT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ADANIPORTS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ALKEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'AMBUJACEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'APOLLOHOSP 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'APOLLOTYRE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ASIANPAINT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ASTRAL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ATUL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'AUBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'AUROPHARMA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'AXISBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BAJAJ-AUTO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BAJAJFINSV 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BAJFINANCE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BALKRISIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BALRAMCHIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BANDHANBNK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BANKBARODA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BATAINDIA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BERGEPAINT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BHARATFORG 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BHARTIARTL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BIOCON 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BOSCHLTD 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BPCL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BRITANNIA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'BSOFT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CANBK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CANFINHOME 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CHAMBLFERT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CHOLAFIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CIPLA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'COALINDIA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'COFORGE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'COLPAL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CONCOR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'COROMANDEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CROMPTON 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'CUMMINSIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DABUR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DALBHARAT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DEEPAKNTR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DELTACORP 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DIVISLAB 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DIXON 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DLF 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'DRREDDY 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'EICHERMOT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ESCORTS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'EXIDEIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GAIL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GLENMARK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GNFC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GODREJCP 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GODREJPROP 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GRANULES 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GRASIM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'GUJGASLTD 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HAL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HAVELLS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HCLTECH 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HDFCAMC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HDFCBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HDFCLIFE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HEROMOTOCO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HINDALCO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HINDPETRO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'HINDUNILVR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ICICIBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ICICIGI 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ICICIPRULI 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'IEX 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'IGL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDHOTEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDIACEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDIAMART 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDIGO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDUSINDBK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INDUSTOWER 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'INFY 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'IPCALAB 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'IRCTC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ITC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'JINDALSTEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'JKCEMENT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'JSWSTEEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'JUBLFOOD 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'KOTAKBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'L&TFH 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LALPATHLAB 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LAURUSLABS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LICHSGFIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LTIM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LTTS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'LUPIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'M&M 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'M&MFIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MARICO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MARUTI 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MCDOWELL-N 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MCX 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'METROPOLIS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MFSL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MGL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MPHASIS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MRF 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'MUTHOOTFIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'NAUKRI 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'NAVINFLUOR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'NESTLEIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'NMDC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'NTPC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'OBEROIRLTY 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'OFSS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ONGC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PAGEIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PERSISTENT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PETRONET 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PFC 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PIDILITIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PIIND 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'POLYCAB 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'POWERGRID 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'PVRINOX 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'RAMCOCEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'RBLBANK 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'RECLTD 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'RELIANCE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SBICARD 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SBILIFE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SBIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SHREECEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SHRIRAMFIN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SIEMENS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SRF 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SUNPHARMA 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SUNTV 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'SYNGENE 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TATACHEM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TATACOMM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TATACONSUM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TATAMOTORS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TATAPOWER 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TCS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TECHM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TITAN 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TORNTPHARM 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TRENT 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'TVSMOTOR 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'UBL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ULTRACEMCO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'UPL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'VEDL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'VOLTAS 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'WIPRO 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ZEEL 25 Jan 2024'},
{'Exchange':'N','ExchangeType':'D','Symbol':'ZYDUSLIFE 25 Jan 2024'},]
ltp = client.fetch_market_depth_by_symbol(a)['Data']
#print(ltp)
neww = pd.DataFrame.from_dict(ltp)#['Data']#[0]['LastTradedPrice']
#new1 = pd.DataFrame.from_dict(new)
###ltp1 = [i[['ScripCode','LastTradedPrice']] for i in new['Data']]
print(neww.head(1))
# new = new[['AverageTradePrice','BuyQuantity','Close','High','Low','LastTradedPrice''LowerCircuitLimit',]]
# print(new.head(3))
#ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":index}])['Data'][0]['LastTradedPrice'])
# for stk in stk_list:
#     #print(stk)
#     ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"D","Symbol":stk}])['Data'][0]['LastTradedPrice'])
#     print(stk,ltp)
# with open('tickers.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     name = None
#     for row in reader:
#         if row[0]:
#             ticker_list.append(row[0])

# start_date = '2019-03-03'
# end_date = '2020-03-04'



# stklen = len(stk_list)
# print("Total Stock : "+str(len(stk_list)))
# def y_hist():
#     for stk in stk_list:
#         dfg1 = client.historical_data('N', 'D', stk, '1m',last_trading_day,current_trading_day) 
#         print(stk)
        #print(dfg1.head(1))

        # data = yf.download(ticker, start=start_date, end=end_date, group_by="ticker")
        # data.to_csv('yhist/' + ticker + '.csv', sep=',', encoding='utf-8')

# threads = []

# for i in range(os.cpu_count()):
#     print('registering thread %d' % i)
#     threads.append(Thread(target=y_hist))

# for thread in threads:
#     thread.start()

# for thread in threads:
#     thread.join()
# while True:   
#     number_of_threads = os.cpu_count()   
#     part = int(stklen) / number_of_threads 
#     print(number_of_threads,part)

#     for i in range(number_of_threads): 
#         start = part * i 
#         end = start + part 
    
#         # create a Thread with start and end locations 
#         t = threading.Thread(target=y_hist) 
#         t.setDaemon(True) 
#         t.start() 


#     main_thread = threading.current_thread() 
#     for t in threading.enumerate(): 
#         if t is main_thread: 
#             continue
#         t.join() 

print('It took', time.time()-start, 'seconds.')