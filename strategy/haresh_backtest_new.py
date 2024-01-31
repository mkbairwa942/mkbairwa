#i#import yfinance as yf
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
import threading


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

operate = "YES"
telegram_msg = "no"
orders = "no"
username = "HARESH"
username1 = str(username)
client = credentials(username1)

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

# current_trading_day = trading_dayss[0]
# last_trading_day = trading_dayss[2]
# second_last_trading_day = trading_days[3]

print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last 365 Day is :- "+str(days_365))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

symbol1 = '999920005'

df = client.historical_data('N', 'C', symbol1, '5m', last_trading_day,current_trading_day)
#print(df.head(1))
# df = df.astype({"Datetime": "datetime64"})    
# df["Date"] = df["Datetime"].dt.date
df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
df.set_index('Datetime',inplace=True)
#df3 = df         

def fisher(high, low, length=None, signal=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    hl2_ = hl2(high, low)
    highest_hl2 = hl2_.rolling(length).max()
    lowest_hl2 = hl2_.rolling(length).min()

    hlr = high_low_range(highest_hl2, lowest_hl2)
    hlr[hlr < 0.001] = 0.001

    position = ((hl2_ - lowest_hl2) / hlr) - 0.5
    v = 0
    m = high.size
    result = [npNaN for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        v = 0.66 * position[i] + 0.67 * v
        if v < -0.99: v = -0.999
        if v >  0.99: v =  0.999
        result.append(0.5 * (nplog((1 + v) / (1 - v)) + result[i - 1]))
    fisher = Series(result, index=high.index)
    signalma = fisher.shift(signal)

    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    props = f"{length}_{signal}"
    fisher.name = f"FISHERT{props}"
    signalma.name = f"FISHERTs{props}"
    fisher.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {fisher.name: fisher, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"FISHERT{props}"
    df.category = fisher.category

    return df

def fisher1(high, low, length=None, signal=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    hl2_ = hl2(high, low)
    highest_hl2 = hl2_.rolling(length).max()
    lowest_hl2 = hl2_.rolling(length).min()

    #hlr = high_low_range(highest_hl2, lowest_hl2)
    hlr  = highest_hl2-lowest_hl2
    hlr[hlr < 0.001] = 0.001

    position = ((hl2_ - lowest_hl2) / hlr) - 0.5
    v = 0
    m = high.size
    result = [npNaN for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        v = 0.66 * position[i] + 0.67 * v
        if v < -0.99: v = -0.999
        if v >  0.99: v =  0.999
        result.append(0.5 * (nplog((1 + v) / (1 - v)) + result[i - 1]))
    fisher = Series(result, index=high.index)
    signalma = fisher.shift(signal)


    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    props = f"{length}_{signal}"
    fisher.name = f"FISHERT{props}"
    signalma.name = f"FISHERTs{props}"
    fisher.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {fisher.name: fisher, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"FISHERT{props}"
    df.category = fisher.category
    return df

fisher_transform = (fisher1(high=df['High'],low=df['Low'],length=10))

# df['stochrsi_k'] = np.round((ta.momentum.stochrsi_k(df.Close)),2)
# df['stochrsi_d'] = np.round((ta.momentum.stochrsi_d(df.Close)),2)
stochrsi = pta.stochrsi(df['Close'])
ADX = pta.adx(high=df['High'],low=df['Low'],close=df['High'])
df['stochrsi_k'] = np.round((stochrsi[stochrsi.columns[0]]),2)
df['stochrsi_d'] = np.round((stochrsi[stochrsi.columns[1]]),2)
df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)
df['DMP_14'] = np.round((ADX[ADX.columns[1]]),2)
df['DMN_14'] = np.round((ADX[ADX.columns[2]]),2)

# print(stochrsi.head(5))
#df['stochrsi_k'] = np.round((pta.stochrsi(df['Close'])),2)
df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
df['FISHERT_WH'] = np.round((fisher_transform[fisher_transform.columns[0]]),2)
df['FISHERTs_RED'] = np.round((fisher_transform[fisher_transform.columns[1]]),2)
df['El_Fis_diff'] = np.round(abs((df['FISHERT_WH']-df['FISHERTs_RED'])),2)
df['stk_50'] = np.where(((df['stochrsi_k'] > 50) & (df['stochrsi_k'] < 80)),"ok","")
df['sk_above'] = np.where((df['stochrsi_k'] > df['stochrsi_d']),"ok","")
df['fis_above'] = np.where((df['FISHERT_WH'] > df['FISHERTs_RED']),"ok","")
df['Adx_diff'] = df['ADX_14'].shift(-1) - df['ADX_14']
df['Adx_ok'] = np.where(df['Adx_diff'] > 1,"ok","")
#print(df.head(5))
# for i in (5,10,13):
#     df['EMA_'+str(i)] = np.round((ta.trend.ema_indicator(df.Close, window=i)),2)
# df['atr'] = np.round((ta.volatility.average_true_range(df.High,df.Low,df.Close)),2)


# def checkcross(df):
#     series = df['stochrsi_k'] > df['stochrsi_d']
#     return series.diff()

# df['cross'] = checkcross(df).astype(bool)

SLL = 20
TGG = 50
LOTSIZE = 25
Brokerage = 50

# BuySl = SL*-1
# SellSl = SL*1
# print(BuySl,SellSl)
df['TP'] = df.Close + TGG
df['SL'] = df.Close - SLL

# df['TP'] = df.Close + (df.atr * 2)
# df['SL'] = df.Close - (df.atr * 3)

# df['Buysignal'] = np.where((df.cross) & (df.Close > df.EMA_10) & (df.EMA_10 > df.EMA_13) & (df.EMA_13 > df.EMA_200),1,0)

 #df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E",""))
#df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["RSI_14"] > 50),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["RSI_14"] < 50),"S_E",""))
# df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["El_Fis_diff"] > 0.25),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["El_Fis_diff"] > 0.25),"S_E",""))            
# df['Entry1'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(1) != "B_E"),"B_E",np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E",""))
# df['Ent_A'] = (np.where(df['Entry1'] == "B_E",df['Close'],(np.where(df['Entry1'] == "S_E",df['Close'],npNaN))))
# df['Ent_A'] = df['Ent_A'].ffill()
# df['Ent_B'] = df['Close']-df['Ent_A']
# df['Ent_B'] = np.where(df['Entry'] == "B_E",(df['Close']-df['Ent_A']),np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0))
# df['Ent_C'] = np.where(((df['Entry'] == "B_E") & (df['Ent_B'] <= - SLL)),"B_SL",np.where(((df['Entry'] == "B_E") & (df['Ent_B'] >= TGG)),"B_TP",
#               np.where(((df['Entry'] == "S_E") & (df['Ent_B'] <= - SLL)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_B'] >= TGG)),"S_TP",""))))
# #df['Ent_D'] = np.where((df.FISHERT_WH < df.FISHERTs_RED),"B_Ex",np.where((df.FISHERT_WH > df.FISHERTs_RED),"S_Ex",""))
# df['Ent_E'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(-1) != "B_E"),"B_Ex",
#               np.where((df['Entry'] == "S_E") & (df['Entry'].shift(-1) != "S_E"),"S_Ex",""))
# df['Ent_C'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(-1) != "B_E"),"B_Ex",
#               np.where((df['Entry'] == "S_E") & (df['Entry'].shift(-1) != "S_E"),"S_Ex",
#               np.where(((df['Entry'] == "B_E") & (df['Ent_B'] <= - SLL)),"B_SL",np.where(((df['Entry'] == "B_E") & (df['Ent_B'] >= TGG)),"B_TP",
#               np.where(((df['Entry'] == "S_E") & (df['Ent_B'] <= - SLL)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_B'] >= TGG)),"S_TP",""))))))


# df['Entry'] = np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E","")
# df['Entry1'] = np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E","")
# df['Ent_A'] = (np.where(df['Entry1'] == "S_E",df['Close'],npNaN))
# df['Ent_A'] = df['Ent_A'].ffill()
# df['Ent_Bb'] = np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0)
# df['Ent_Cb'] = np.where(((df['Entry'] == "S_E") & (df['Ent_Bb'] <= - SLL)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_Bb'] >= TGG)),"S_TP",""))

# df.dropna(inplace=True)

# length = len(df)-1

# Buying = pd.DataFrame()
# Selling = pd.DataFrame()
# new_df1 = pd.DataFrame()    

# for i in range(len(df)):
#     if [i+1][0] <= length:
#         if df['Entry1'].iloc[i + 1] == "B_E":
#             bay = (df['Ent_A'].iloc[i + 1])
#             buyy = df[i+1:i+2]
#             Buying = pd.concat([buyy, Buying])
#             sal = df[df['Ent_A'] == bay]
#             sal1 = (sal[(sal['Ent_C'] == "B_SL") | (sal['Ent_C'] == "B_TP") | (sal['Ent_C'] == "B_Ex")])
#             sal1['Sell_Date'] = (df.Date.iloc[i + 1])
#             sal1['Sell_Time'] = (df.Time.iloc[i + 1])
#             Selling = pd.concat([sal1[:1], Selling])

#         if df['Entry1'].iloc[i + 1] == "S_E":
#             bay1 = (df['Ent_A'].iloc[i + 1])
#             buyy1 = df[i+1:i+2]
#             Buying = pd.concat([buyy1, Buying])
#             sal1 = df[df['Ent_A'] == bay1]
#             sal11 = (sal1[(sal1['Ent_C'] == "S_SL") | (sal1['Ent_C'] == "S_TP") | (sal1['Ent_C'] == "S_Ex")])
#             sal11['Sell_Date'] = (df.Date.iloc[i + 1])
#             sal11['Sell_Time'] = (df.Time.iloc[i + 1])
#             Selling = pd.concat([sal11[:1], Selling])

# Buying.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True) 
# Buying.rename(columns={'Date': 'Datee', 'Time': 'Timee'}, inplace=True)
# Selling.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True)  
# Selling.rename(columns={'Sell_Date': 'Datee', 'Sell_Time': 'Timee'}, inplace=True)
# new_df1 = pd.merge(Buying, Selling,on=["Datee", "Timee"])

# new_df1['P&L'] = np.where((new_df1['Ent_C_y'] == "B_Ex") | (new_df1['Ent_C_y'] == "S_Ex"),Brokerage*-1,
#                   np.where((new_df1['Ent_C_y'] == "B_TP") | (new_df1['Ent_C_y'] == "S_TP"),(TGG*LOTSIZE)-Brokerage,
#                   np.where((new_df1['Ent_C_y'] == "B_SL") | (new_df1['Ent_C_y'] == "S_SL"),(SLL*LOTSIZE+Brokerage)*-1,0)))

# selldates = []
# outcome = []

# for i in range(length):
#     if df.Buysignal.iloc[i]:
#         k = 1
#         SL = df.SL.iloc[i]     
#         TP = df.TP.iloc[i]
#         in_position = True
#         while in_position:
#             if [i+k][0] <= length:
#                 looping_close = df.Close.iloc[i + k]
#                 if looping_close >= TP:
#                     selldates.append(df.iloc[i+k].name)
#                     outcome.append('TP')
#                     in_position = False
#                 elif looping_close <= SL:
#                     selldates.append(df.iloc[i+k].name)
#                     outcome.append('SL')                         
#                 k += 1
#                 in_position = False           

# df.loc[selldates, "Sellsignal"] = 1
# df.Sellsignal = df.Sellsignal.fillna(0).astype(int)
# df['Sellsignal1'] = np.where((df['Sellsignal'] == 1) & (df['Sellsignal'].shift(1) == 0),1,0)
# df.loc[selldates, "outcome"] = outcome
# buyyy = df[(df.Buysignal1 == 1)]
# mask2 = df[(df.Sellsignal1 == 1)]
# print(mask2.outcome.value_counts().sum())
# print(mask2.outcome.value_counts())

print("Excel Starting....")
if not os.path.exists("haresh_backtest_new.xlsx"):
    try:
        wb = xw.Book()
        wb.save("haresh_backtest_new.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('haresh_backtest_new.xlsx')
for i in ["Data","Buy","Sale","Final","Extra"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
by = wb.sheets("Buy")
sl = wb.sheets("Sale")
fl = wb.sheets("Final")
ex = wb.sheets("Extra")
dt.range("a:z").value = None
by.range("a:z").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
ex.range("a:g").value = None

try:
    time.sleep(0.5)
    dt.range("a1").value = df
    # by.range("a1").value = Buying
    # sl.range("a1").value = Selling
    # fl.range("a1").value = new_df1
    # ex.range("a1").value = dfg
except Exception as e:
    print(e)
