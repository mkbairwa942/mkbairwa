#i#import yfinance as yf
#import ta
#from ta import add_all_ta_features
#from ta.utils import dropna
from collections import namedtuple
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

current_trading_day = trading_dayss[1]
last_trading_day = trading_dayss[2]
second_last_trading_day = trading_days[3]

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

print("Excel Starting....")

if not os.path.exists("haresh_hakin_adx.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("haresh_hakin_adx.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('haresh_hakin_adx.xlsx')
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

pos.range("a:u").value = None
strategy1.range("a:u").value = None
strategy2.range("a:u").value = None
strategy3.range("a:u").value = None

st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
st.range("a:u").value = None
# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

symbol1 = '999920005'

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

# fisher_transform = (fisher1(high=df['High'],low=df['Low'],length=10))
# df['stochrsi_k'] = np.round((ta.momentum.stochrsi_k(df.Close)),2)
# df['stochrsi_d'] = np.round((ta.momentum.stochrsi_d(df.Close)),2)
# stochrsi = pta.stochrsi(df['Close'])
# df['stochrsi_k'] = np.round((stochrsi[stochrsi.columns[0]]),2)
# df['stochrsi_d'] = np.round((stochrsi[stochrsi.columns[1]]),2)
# df['DMP_14'] = np.round((ADX[ADX.columns[1]]),2)
# df['DMN_14'] = np.round((ADX[ADX.columns[2]]),2)
# df['stochrsi_k'] = np.round((pta.stochrsi(df['Close'])),2)
# df['FISHERT_WH'] = np.round((fisher_transform[fisher_transform.columns[0]]),2)
# df['FISHERTs_RED'] = np.round((fisher_transform[fisher_transform.columns[1]]),2)
# df['El_Fis_diff'] = np.round(abs((df['FISHERT_WH']-df['FISHERTs_RED'])),2)
# df['stk_50'] = np.where(((df['stochrsi_k'] > 50) & (df['stochrsi_k'] < 80)),"ok","")
# df['sk_above'] = np.where((df['stochrsi_k'] > df['stochrsi_d']),"ok","")
# df['fis_above'] = np.where((df['FISHERT_WH'] > df['FISHERTs_RED']),"ok","")

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

exchange = None
while True:    
    if exchange is None: 
        try:
            exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
            exch.sort_values(['Root'], ascending=[True], inplace=True)
            
            root_list = np.unique(exch['Root']).tolist()

            
            root_list = ["BANKNIFTY"]

            exc_new = exch['Root'].isin(root_list)
            
            exc_new1 = exch[exc_new]
            eq_exc = exc_new1[(exc_new1["Exch"] == "N") & (exc_new1["ExchType"] == "C") & (exc_new1["CpType"] == "EQ")]
            exc.range("a1").options(index=False).value = eq_exc
            Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
            Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
            exc_new2 = Expiry
            exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

            break
        except:
            print("Exchange Download Error....")
            time.sleep(5)

exc_fut = exc_new2
exc_fut1 = exc_fut[exc_fut["CpType"] == "XX"]
Expiry = (np.unique(exc_fut1['Expiry']).tolist())
# print(Expiry)
exc_fut1_Expiryy = (np.unique(exc_fut1['Expiry']).tolist())[0]            
print(exc_fut1_Expiryy)
exc_fut = exc_fut1[exc_fut1['Expiry'] == exc_fut1_Expiryy] 
#exc_fut.sort_values(['Name'], ascending=[True], inplace=True)
exc_fut = exc_fut[['ExchType','Name', 'ISIN', 'FullName','Root','StrikeRate', 'CO BO Allowed','CpType','Scripcode','Expiry','LotSize','Watchlist']]

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = exc_fut

exc_opt = exc_new2
exc_opt1 = exc_opt[exc_opt["CpType"] != "XX"]
Expiry = (np.unique(exc_opt1['Expiry']).tolist())
# print(Expiry)
exc_opt1_Expiryy = (np.unique(exc_opt1['Expiry']).tolist())[0]            
print(exc_opt1_Expiryy)
exc_opt = exc_opt1[exc_opt1['Expiry'] == exc_opt1_Expiryy] 
#exc_opt.sort_values(['Name'], ascending=[True], inplace=True)
exc_opt = exc_opt[['ExchType','Name', 'ISIN', 'FullName','Root','StrikeRate', 'CO BO Allowed','CpType','Scripcode','Expiry','LotSize','Watchlist']]
flt_exc.range("o1").options(index=False).value = exc_opt

telegram_msg = "no"
orders = "no"

def order_book_func():
    try:
        ordbook = pd.DataFrame(client.order_book())
        ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
        #ordbook[['Root']] = ordbook['ScripName'].str.split(' ',expand=True)
        #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
        pos.range("r1").options(index=False).value = ordbook
        
    except Exception as e:
                print(e)

    try:
        if ordbook is not None:
            ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
            #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
            #print("Order Book not Empty")        
            ordbook1 = ordbook[ordbook['OrderStatus'] != "Rejected By 5P"]   
            ordbook1 = ordbook           
            Datetimeee = []
            for i in range(len(ordbook1)):
                datee = ordbook1['BrokerOrderTime'][i]
                timestamp = pd.to_datetime(datee[6:19], unit='ms')
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
                d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
                d2 = d1 + timedelta(hours = 5.5)
                Datetimeee.append(d2)
            ordbook1['Datetimeee'] = Datetimeee
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','Root','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            pos.range("a1").options(index=False).value = ordbook1
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,namee):
    dfg3 = df.tail(1)
    price_of_stock = float(dfg3['Close']) 
    timee = str((dfg3['Datetime'].values)[0])[0:19] 
    timee1= timee.replace("T", " " )
    list_append_on.append(list_to_append)

    if orders.upper() == "YES" or orders.upper() == "":                
        order = client.place_order(OrderType=order_side,Exchange='N',ExchangeType='D', ScripCode = scrip_code, Qty=qtyy,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
    else:
        print(f"Real {CALL_PUT} Order are OFF")
    print(f"1 Minute {CALL_PUT} Data Selected of "+str(namee)+" ("+str(scrip_code)+")")
    print(f"{CALL_PUT} {BUY_EXIT} Order Executed of "+str(namee)+" at : Rs "+str(price_of_stock)+" and Quantity is "+str(qtyy)+" on "+str(timee1))

    print("SYMBOL : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timee1))
    if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
        parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timee1)}
        resp = requests.get(telegram_basr_url, data=parameters1)
    else:
        print("Telegram Message are OFF")
    print("----------------------------------------")



posit = pd.DataFrame(client.positions()) 
if posit.empty:
    print("Position is Empty")
    buy_order_list_dummy = []
    sell_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order = order_book_func()
    buy_order_li = buy_order[buy_order['BuySell'] == 'B']
    exit_order_li = buy_order[buy_order['BuySell'] == 'S']
    buy_order_list_dummy = (np.unique([str(i) for i in buy_order_li['Datetimeee']])).tolist()
    sell_order_list_dummy = (np.unique([str(i) for i in exit_order_li['Datetimeee']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()

def HakinAshi_func(df):
    df = df.copy()
    df['HA_Close']=(df.Open + df.High + df.Low + df.Close)/4
    df.reset_index(inplace=True)
    ha_open = [ (df.Open[0] + df.Close[0]) / 2 ]
    [ ha_open.append((ha_open[i] + df.HA_Close.values[i]) / 2) \
    for i in range(0, len(df)-1) ]
    df['HA_Open'] = ha_open
    df.set_index('index', inplace=True)
    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df

while True:
    print(buy_order_list_dummy)
    print(sell_order_list_dummy)
    df = client.historical_data('N', 'C', symbol1, '1m', from_d,to_d)
    df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
    df = df.astype({"Datetime": "datetime64"})
    df['Scripcode'] = int(symbol1)
    df = pd.merge(df, eq_exc, on=['Scripcode'], how='inner') 

    hakin_ashi = HakinAshi_func(df)

    df = hakin_ashi.copy()
    df = df[['Scripcode','Root','Name','Datetime','Open','High','Low','Close','HA_Open','HA_High','HA_Low','HA_Close','Volume']]
    df['Spot'] = round(df['Close']/100,0)*100
    df["Date"] = df["Datetime"].dt.date   

    df['SMA_14'] = np.round((pta.sma(df['Close'],length=14)),2)
    df['SMA_29'] = np.round((pta.sma(df['Close'],length=29)),2)
    df['SMA_60'] = np.round((pta.sma(df['Close'],length=60)),2)
    ADX = pta.adx(high=df['High'],low=df['Low'],close=df['Close'])
    df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)
    df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
    df['Adx_diff'] = df['ADX_14'] - df['ADX_14'].shift(1)
    df['Adx_ok'] = np.where(df['Adx_diff'] > 1,"ok","")
    df['Sma_cross_up'] = np.where((df['Close'] >= df['SMA_14']) & (df['SMA_14'] >= df['SMA_29']) & (df['SMA_29'] >= df['SMA_60']),"ok","")
    df['Sma_cross_dn'] = np.where((df['Close'] <= df['SMA_14']) & (df['SMA_14'] <= df['SMA_29']) & (df['SMA_29'] <= df['SMA_60']),"ok","")
    df['Exit'] = np.where((df['Sma_cross_up'].shift(1) == "ok") & (df['Close'] < df['SMA_14']) | 
                          (df['Adx_ok'].shift(1) == "ok") & (df['Adx_diff'] < 0 ),"Call_Buy_Exit",
                          np.where((df['Sma_cross_dn'].shift(1) == "ok") & (df['Close'] > df['SMA_14']) |
                                   (df['Adx_ok'].shift(1) == "ok") & (df['Adx_diff'] < 0 ),"Put_Buy_Exit",""))
    #df['Exit'] = np.where(df['Low'] < df['HA_Low'].shift(1),"Call_Buy_Exit","")


    df1_up = df[(df["Adx_ok"] == "ok") & (df["Sma_cross_up"] == "ok") & (df['RSI_14'] > 70)]
    df1_dn = df[(df["Adx_ok"] == "ok") & (df["Sma_cross_dn"] == "ok") & (df['RSI_14'] < 30)]
    # df1_up = df[(df["Adx_ok"] == "ok") & (df["Sma_cross_up"] == "ok") & (df['HA_Open'] == df['HA_Low']) & (df['Close'] > df['SMA_29']) & (df['RSI_14'] > 70) & (df['ADX_14'] > 20)]
    # df1_dn = df[(df['HA_Open'] == df['HA_High'])]

    df1_up['Date_Dif'] = abs((df1_up["Datetime"] -df1_up["Datetime"].shift(1)).astype('timedelta64[m]')) 
    df1_dn['Date_Dif'] = abs((df1_dn["Datetime"] -df1_dn["Datetime"].shift(1)).astype('timedelta64[m]')) 
    
    df1_up['Entry'] = np.where(df1_up['Date_Dif'] > 1, "Buy","")
    df1_dn['Entry'] = np.where(df1_dn['Date_Dif'] > 1, "Buy","")
    
    buy_df = df1_up#[df1_up['Entry'] == "Buy"]
    sell_df = df1_dn#[df1_dn['Entry'] == "Buy"]
    
    buy_exit_call_df = df[df['Exit'] == 'Call_Buy_Exit']
    buy_exit_put_df = df[df['Exit'] == 'Put_Buy_Exit']
    
    final_call = pd.concat([buy_df, buy_exit_call_df])
    final_put = pd.concat([sell_df, buy_exit_put_df])    
    
    listo_call = np.unique(final_call['Datetime'])
    listo_put = np.unique(final_put['Datetime'])

    final_df_call = pd.DataFrame()
    final_df_put = pd.DataFrame()

    position_Call = 0
    position_put = 0

    for i in listo_call:
        f_df_call = final_call[final_call['Datetime'] == i]
        if list(f_df_call['Entry'])[0] == 'Buy' and position_Call == 0:
            final_df_call = pd.concat([f_df_call, final_df_call])
            position_Call = 1

        if list(f_df_call['Exit'])[0] == 'Call_Buy_Exit' and position_Call == 1:
            final_df_call = pd.concat([f_df_call, final_df_call])
            position_Call = 0

    for i in listo_put:
        f_df_put = final_put[final_put['Datetime'] == i]
        if list(f_df_put['Entry'])[0] == 'Buy' and position_put == 0:
            final_df_put = pd.concat([f_df_put, final_df_put])
            position_put = 1

        if list(f_df_put['Exit'])[0] == 'Put_Buy_Exit' and position_put == 1:
            final_df_put = pd.concat([f_df_put, final_df_put])
            position_put = 0    
    
    dfgg_call_buy_fut = final_df_call[(final_df_call["Entry"] == "Buy") & (final_df_call["Date"] == current_trading_day.date())]# & (final_df_call["Minutes"] < 2 )]
    dfgg_call_Exit_fut = final_df_call[(final_df_call["Exit"] == "Call_Buy_Exit") & (final_df_call["Date"] == current_trading_day.date())]# & (final_df_call["Minutes"] < 2 )]

    dfgg_put_buy_fut = final_df_put[(final_df_put["Entry"] == "Buy") & (final_df_put["Date"] == current_trading_day.date())]# & (final_df_call["Minutes"] < 2 )]
    dfgg_put_Exit_fut = final_df_put[(final_df_put["Exit"] == "Put_Buy_Exit") & (final_df_put["Date"] == current_trading_day.date())]# & (final_df_call["Minutes"] < 2 )]

    # dfgg_call_buy_fut.sort_values(['Datetime'], ascending=[True], inplace=True)
    # dfgg_call_Exit_fut.sort_values(['Datetime'], ascending=[True], inplace=True)
       
    # dfgg_put_buy_fut.sort_values(['Datetime'], ascending=[True], inplace=True)
    # dfgg_put_Exit_fut.sort_values(['Datetime'], ascending=[True], inplace=True)

    # dfgg_call_buy_fut1 = dfgg_call_buy_fut.tail(1)
    # dfgg_call_Exit_fut1 = dfgg_call_Exit_fut.tail(1)

    # dfgg_put_buy_fut1 = dfgg_put_buy_fut.tail(1)
    # dfgg_put_Exit_fut1 = dfgg_put_Exit_fut.tail(1)

    # Fut_Closee_call = (np.unique([float(i) for i in dfgg_call_buy_fut1['Close']])).tolist()[0] #float(dfgg_call_buy_fut1['Close'])
    # Root_call = (np.unique([str(i) for i in dfgg_call_buy_fut1['Root']])).tolist()[0] 

    # Fut_Closee_put = (np.unique([float(i) for i in dfgg_put_buy_fut1['Close']])).tolist()[0] #float(dfgg_put_buy_fut1['Close'])
    # Root_put = (np.unique([str(i) for i in dfgg_put_buy_fut1['Root']])).tolist()[0] 

    # Buy_call_timee_fut = list(dfgg_call_buy_fut1['Datetime'])[0]
    # Buy_call_timee_fut1 = str(Buy_call_timee_fut).replace(' ','T') 
    # Buy_call_exit_timee_fut = list(dfgg_call_Exit_fut1['Datetime'])[0]
    # Buy_call_exit_timee_fut1 = str(Buy_call_exit_timee_fut).replace(' ','T') 
    # print("Call")
    # print(Fut_Closee_call,Root_call,Buy_call_timee_fut1,Buy_call_exit_timee_fut1)

    # Buy_put_timee_fut = list(dfgg_put_buy_fut1['Datetime'])[0]
    # Buy_put_timee_fut1 = str(Buy_put_timee_fut).replace(' ','T') 
    # Buy_put_exit_timee_fut = list(dfgg_put_Exit_fut1['Datetime'])[0]
    # Buy_put_exit_timee_fut1 = str(Buy_put_exit_timee_fut).replace(' ','T') 
    # print("Put")
    # print(Fut_Closee_put,Root_put,Buy_put_timee_fut1,Buy_put_exit_timee_fut1)

    # Excchhh_up_call = exc_opt[(exc_opt["CpType"] == 'CE')]
    # Excchh_up_call = Excchhh_up_call[Excchhh_up_call['Root'] == Root_call]
    # Excchh2_up_call = Excchh_up_call[(Excchh_up_call['StrikeRate'] > Fut_Closee_call)]
    # Excchh2_up_call.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)

    # Excchhh_up_put = exc_opt[(exc_opt["CpType"] == 'PE')]
    # Excchh_up_put = Excchhh_up_put[Excchhh_up_put['Root'] == Root_put]
    # Excchh2_up_put = Excchh_up_put[(Excchh_up_put['StrikeRate'] < Fut_Closee_put)]
    # Excchh2_up_put.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)

    # Excchh3_up_call = Excchh2_up_call.head(1)
    # Buy_call_quantity_of_stock = int(np.unique(Excchh3_up_call['LotSize']))
    # Buy_call_Scriptcodee = int(np.unique(Excchh3_up_call['Scripcode'])[0])
    # stk_call_name1_up = (np.unique([str(i) for i in Excchh3_up_call['Name']])).tolist()[0]
    # print("Call")
    # print(Buy_call_Scriptcodee,stk_call_name1_up,Buy_call_quantity_of_stock)

    # Excchh3_up_put = Excchh2_up_put.tail(1)
    # Buy_put_quantity_of_stock = int(np.unique(Excchh3_up_put['LotSize']))
    # Buy_put_Scriptcodee = int(np.unique(Excchh3_up_put['Scripcode'])[0])
    # stk_put_name1_up = (np.unique([str(i) for i in Excchh3_up_put['Name']])).tolist()[0]
    # print("Put")
    # print(Buy_put_Scriptcodee,stk_put_name1_up,Buy_put_quantity_of_stock)

    # dfgg_buy_call_op = client.historical_data('N', 'D', Buy_call_Scriptcodee, '1m', from_d,to_d)
    # dfgg_buy_call_op.sort_values(['Datetime'], ascending=[True], inplace=True)
    # dfgg_buy_call_op['Scriptcode'] = Buy_call_Scriptcodee
    # dfgg_buy_call_op['Name'] = stk_call_name1_up
    # dfgg_buy_call_op['Entry_Date'] = Buy_call_timee_fut1
    # dfgg_buy_call_op['Exit_Date'] = Buy_call_exit_timee_fut1
    # dfgg_buy_call_op['Entry_OK_DF'] = np.where(dfgg_buy_call_op['Entry_Date'] == dfgg_buy_call_op['Datetime'],"OK","")
    # dfgg_buy_call_op['Exit_OK_DF'] = np.where(dfgg_buy_call_op['Exit_Date'] == dfgg_buy_call_op['Datetime'],"OK","")
    # dfgg_buy_call_opt = dfgg_buy_call_op[dfgg_buy_call_op['Entry_OK_DF'] == "OK"]
    # dfgg_buy_call_Exit_opt = dfgg_buy_call_op[dfgg_buy_call_op['Exit_OK_DF'] == "OK"]

    # dfgg_buy_put_op = client.historical_data('N', 'D', Buy_put_Scriptcodee, '1m', from_d,to_d)
    # dfgg_buy_put_op.sort_values(['Datetime'], ascending=[True], inplace=True)
    # dfgg_buy_put_op['Scriptcode'] = Buy_put_Scriptcodee
    # dfgg_buy_put_op['Name'] = stk_put_name1_up
    # dfgg_buy_put_op['Entry_Date'] = Buy_put_timee_fut1
    # dfgg_buy_put_op['Exit_Date'] = Buy_put_exit_timee_fut1
    # dfgg_buy_put_op['Entry_OK_DF'] = np.where(dfgg_buy_put_op['Entry_Date'] == dfgg_buy_put_op['Datetime'],"OK","")
    # dfgg_buy_put_op['Exit_OK_DF'] = np.where(dfgg_buy_put_op['Exit_Date'] == dfgg_buy_put_op['Datetime'],"OK","")
    # dfgg_buy_put_opt = dfgg_buy_put_op[dfgg_buy_put_op['Entry_OK_DF'] == "OK"]
    # dfgg_buy_put_Exit_opt = dfgg_buy_put_op[dfgg_buy_put_op['Exit_OK_DF'] == "OK"]

    # final_df_call_opt = pd.concat([dfgg_buy_call_opt, dfgg_buy_call_Exit_opt])
    # final_df_put_opt = pd.concat([dfgg_buy_put_opt, dfgg_buy_put_Exit_opt])

    # if not dfgg_buy_call_opt.empty:
    #     print("Buy Call")
    #     if Buy_call_timee_fut in buy_order_list_dummy: 
    #         print(str(stk_call_name1_up)+" is Already Buy")
    #         print("----------------------------------------")
    #     else:
    #         rde_exec = order_execution(dfgg_buy_call_opt,buy_order_list_dummy,Buy_call_timee_fut,telegram_msg,orders,"Call","BUY","B",Buy_call_Scriptcodee,Buy_call_quantity_of_stock,stk_call_name1_up)

    # if not dfgg_buy_call_Exit_opt.empty:
    #     print("Exit Call")
    #     if Buy_call_exit_timee_fut in sell_order_list_dummy: 
    #         print(str(stk_call_name1_up)+" is Already Exited")
    #     else:
    #         rde_exec = order_execution(dfgg_buy_call_Exit_opt,sell_order_list_dummy,Buy_call_exit_timee_fut,telegram_msg,orders,"Call","Exit","S",Buy_call_Scriptcodee,Buy_call_quantity_of_stock,stk_call_name1_up)

    # if not dfgg_buy_put_opt.empty:
    #     print("Buy Put")
    #     if Buy_put_timee_fut in buy_order_list_dummy: 
    #         print(str(stk_put_name1_up)+" is Already Buy")
    #         print("----------------------------------------")
    #     else:
    #         rde_exec = order_execution(dfgg_buy_put_opt,buy_order_list_dummy,Buy_put_timee_fut,telegram_msg,orders,"Put","BUY","B",Buy_put_Scriptcodee,Buy_put_quantity_of_stock,stk_put_name1_up)

    # if not dfgg_buy_put_Exit_opt.empty:
    #     print("Exit Put")
    #     if Buy_put_exit_timee_fut in sell_order_list_dummy: 
    #         print(str(stk_put_name1_up)+" is Already Exited")
    #     else:
    #         rde_exec = order_execution(dfgg_buy_put_Exit_opt,sell_order_list_dummy,Buy_put_exit_timee_fut,telegram_msg,orders,"Put","Exit","S",Buy_put_Scriptcodee,Buy_put_quantity_of_stock,stk_put_name1_up)
                    
    if df.empty:
        pass
    else:
        #df = df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        #df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        Fiv_dt.range("a:az").value = None
        Fiv_dt.range("a1").options(index=False).value = df 

    if df1_up.empty:
        pass
    else:
        #df1_up = df1_up[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        #df1_up.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        by.range("a:az").value = None
        by.range("a1").options(index=False).value = buy_df

    if df1_dn.empty:
        pass
    else:
        #df1_dn = df1_dn[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        #df1_dn.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        #by.range("a:az").value = None
        by.range("a1000").options(index=False).value = sell_df

    if buy_exit_call_df.empty:
        pass
    else:
        #buy_exit_call_df = buy_exit_call_df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        #buy_exit_call_df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        sl.range("a:az").value = None
        sl.range("a1").options(index=False).value = buy_exit_call_df

    if buy_exit_put_df.empty:
        pass
    else:
        #buy_exit_put_df = buy_exit_put_df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        #buy_exit_put_df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        #sl.range("a:az").value = None
        sl.range("a1000").options(index=False).value = buy_exit_put_df

    if final_df_call.empty:
        pass
    else:
        #final_df_call = final_df_call[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        final_df_call.sort_values(['Datetime'], ascending=[True], inplace=True)
        final_df_call['P&L'] = np.where(final_df_call['Exit'] == 'Call_Buy_Exit',final_df_call['Close']-final_df_call['Close'].shift(1),0)
        fl_data.range("a:az").value = None
        fl_data.range("a1").options(index=False).value = final_df_call

    if final_df_put.empty:
        pass
    else:
        #final_df_put = final_df_put[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        final_df_put.sort_values(['Datetime'], ascending=[True], inplace=True)
        final_df_put['P&L'] = np.where(final_df_put['Exit'] == 'Put_Buy_Exit',final_df_put['Close'].shift(1)-final_df_put['Close'],0)
        #fl_data.range("a:az").value = None
        fl_data.range("a1000").options(index=False).value = final_df_put





    # if dfgg_buy_call_op.empty:
    #     pass
    # else:
    #     #dfgg_buy_call_op = dfgg_buy_call_op[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_call_op.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     st1.range("a:az").value = None
    #     st1.range("a1").options(index=False).value = dfgg_buy_call_op

    # if dfgg_buy_put_op.empty:
    #     pass
    # else:
    #     #dfgg_buy_put_op = dfgg_buy_put_op[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_put_op.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     #st1.range("a:az").value = None
    #     st1.range("a1000").options(index=False).value = dfgg_buy_put_op
    
    # if dfgg_buy_call_opt.empty:
    #     pass
    # else:
    #     #dfgg_buy_call_opt = dfgg_buy_call_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_call_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     st2.range("a:az").value = None
    #     st2.range("a1").options(index=False).value = dfgg_buy_call_opt
    
    # if dfgg_buy_put_opt.empty:
    #     pass
    # else:
    #     #dfgg_buy_put_opt = dfgg_buy_put_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_put_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     #st2.range("a:az").value = None
    #     st2.range("a200").options(index=False).value = dfgg_buy_put_opt
    
    # if dfgg_buy_call_Exit_opt.empty:
    #     pass
    # else:
    #     #dfgg_buy_call_Exit_opt = dfgg_buy_call_Exit_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_call_Exit_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     st3.range("a:az").value = None
    #     st3.range("a1").options(index=False).value = dfgg_buy_call_Exit_opt
    
    # if dfgg_buy_put_Exit_opt.empty:
    #     pass
    # else:
    #     #dfgg_buy_put_Exit_opt = dfgg_buy_put_Exit_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #dfgg_buy_put_Exit_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     #st3.range("a:az").value = None
    #     st3.range("a200").options(index=False).value = dfgg_buy_put_Exit_opt
    
    # if final_df_call_opt.empty:
    #     pass
    # else:
    #     #final_df_call_opt = final_df_call_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #final_df_call_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     final_df_call_opt.sort_values(['Datetime'], ascending=[True], inplace=True)
    #     final_df_call_opt['P&L'] = np.where(final_df_call_opt['Exit_OK_DF'] == 'OK',final_df_call_opt['Close']-final_df_call_opt['Close'].shift(1),0)
    #     st4.range("a:az").value = None
    #     st4.range("a1").options(index=False).value = final_df_call_opt
    
    # if final_df_put_opt.empty:
    #     pass
    # else:
    #     #final_df_put_opt = final_df_put_opt[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
    #     #final_df_put_opt.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
    #     #st4.range("a:az").value = None
    #     final_df_put_opt.sort_values(['Datetime'], ascending=[True], inplace=True)
    #     final_df_put_opt['P&L'] = np.where(final_df_put_opt['Exit_OK_DF'] == 'OK',final_df_put_opt['Close'].shift(1)-final_df_put_opt['Close'],0)
    #     st4.range("a200").options(index=False).value = final_df_put_opt