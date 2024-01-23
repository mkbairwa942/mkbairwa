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
from five_paisa import *
import threading
from dateutil.parser import parse
import plotly.graph_objects as go
from datetime import datetime
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc 
# import matplotlib.dates as mpl_dates 



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
#     from five_paisa import *

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
trading_dayss1 = ['2024-01-23', '2024-01-20','2024-01-19']
trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[1]
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

price_limit = 300
Available_Cash = 12000
Exposer = 2

print("---- Data Process Started ----")

if not os.path.exists("Trendline_trading.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Trendline_trading.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Trendline_trading.xlsx')
for i in ["Exchange","Filt_Exc","Bhavcopy","FO_Bhavcopy","Five_data","Delv_data","Five_Delv","Final_Data","Position","Strategy1","Strategy2","Strategy3","Buy","Sale",
           "Expiry","stats","Stat","Stat1","Stat2","Stat3","Stat4"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Filt_Exc")
bhv = wb.sheets("Bhavcopy")
bhv_fo = wb.sheets("FO_Bhavcopy")
Fiv_dt = wb.sheets("Five_data")
delv_dt = wb.sheets("Delv_data")
five_delv = wb.sheets("Five_Delv")
fl_data = wb.sheets("Final_Data")
pos = wb.sheets("Position")
strategy1 = wb.sheets("Strategy1")
strategy2 = wb.sheets("Strategy2")
strategy3 = wb.sheets("Strategy3")

exc.range("a:u").value = None
#flt_exc.range("a:u").value = None
bhv.range("a:u").value = None
#bhv_fo.range("a:u").value = None
#Fiv_dt.range("a:u").value = None
#delv_dt.range("a:u").value = None
#five_delv.range("a:u").value = None
#fl_data.range("a:u").value = None
#pos.range("a:u").value = None
strategy1.range("a:u").value = None
strategy2.range("a:u").value = None
strategy3.range("a:u").value = None

st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
st.range("a:u").value = None
st1.range("a:u").value = None
st2.range("a:u").value = None
st3.range("a:u").value = None
st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")


print("Excel : Started")
exchange = None

start_time = time.time()

df_len = 1021

rsi_up_lvll = 60
rsi_dn_lvll = 40

dfpl = client.historical_data('N', 'D', 55790, '1m',last_trading_day,current_trading_day) 
dfpl["RSI_14"] = np.round((pta.rsi(dfpl["Close"], length=14)),2)
dfpl.sort_values(['Datetime'], ascending=[False], inplace=True)
dfpl['Rsi_OK'] = np.where((dfpl["RSI_14"].shift(-1)) > rsi_up_lvll-2,"Rsi_Up_OK",np.where((dfpl["RSI_14"].shift(-1)) < rsi_dn_lvll+2,"Rsi_Dn_OK",""))
strategy1.range("a1").options(index=False).value = dfpl
df_len = (dfpl.shape[0])
print(df_len)
df = dfpl#[0:df_len]
df=df[df['Volume']!=0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()
print(df.tail(7))
print(df.shape[0])

def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.Low[i]>df1.Low[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.Low[i]<df1.Low[i-1]):
            return 0
    return 1

def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.High[i]<df1.High[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.High[i]>df1.High[i-1]):
            return 0
    return 1

def support1(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.Low[i]<df1.Low[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.Low[i]<df1.Low[i+1]):
            return 0
    return 1

def resistance1(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.High[i]>df1.High[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.High[i]>df1.High[i+1]):
            return 0
    return 1
    
#print(resistance(df, 11, 3, 3))

# sr = []
# n1=3
# n2=3
# for row in range(3, df_len): #len(df)-n2
#     if support(df, row, n1, n2):
#         sr.append((df.Datetime[row],df.Low[row],1))
#     if resistance(df, row, n1, n2):
#         sr.append((df.Datetime[row],df.High[row],2))
# print(sr)

# plotlist1 = [x[1] for x in sr if x[2]==1]
# plotlist2 = [x[1] for x in sr if x[2]==2]
# plotlist1.sort()
# plotlist2.sort()

# for i in range(1,len(plotlist1)):
#     if(i>=len(plotlist1)):
#         break
#     if abs(plotlist1[i]-plotlist1[i-1])<=0.005:
#         plotlist1.pop(i)

# for i in range(1,len(plotlist2)):
#     if(i>=len(plotlist2)):
#         break
#     if abs(plotlist2[i]-plotlist2[i-1])<=0.005:
#         plotlist2.pop(i)
# print(plotlist2)
#plt.hist(plotlist, bins=10, alpha=0.5)

ss = []
rr = []
n1=2
n2=2
for row in range(n1, df_len-n2): #len(df)-n2
    if support(df, row, n1, n2):
        ss.append((df.Datetime[row],df.Low[row]))
    if resistance(df, row, n1, n2):
        rr.append((df.Datetime[row],df.High[row]))

# print(ss)
# print(rr)


low_df = pd.DataFrame(ss)
low_df.columns =['Datetime', 'Low_N']
#strategy2.range("a1").options(index=False).value = low_df

high_df = pd.DataFrame(rr)
high_df.columns =['Datetime', 'High_N']

#strategy2.range("a10").options(index=False).value = high_df

df_merged = pd.concat([low_df, high_df])

#strategy2.range("a20").options(index=False).value = df_merged

dfg1 = pd.merge(df_merged, df, on=['Datetime'], how='outer').fillna(npNaN)
dfg1.fillna(method='ffill')
dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)
strategy2.range("a1").options(index=False).value = dfg1