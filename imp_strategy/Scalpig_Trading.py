import logging
import time
from jugaad_data.nse import *
from sqlalchemy import create_engine
import urllib.parse
import urllib
from io import BytesIO
from zipfile import ZipFile
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
from dateutil.parser import parse
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega


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

#credi_ash = credentials("ASHWIN")
credi_har = credentials("HARESH")

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
# trading_dayss1 = ['2024-01-20', '2024-01-19','2024-01-18']
# trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
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

days_count = len(trading_days)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

# from_date = date(2022, 7, 9)
# to_date = date(2022, 12, 28)

con = urllib.parse.quote_plus(
    'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=Stock_data;trusted_connection=yes')
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))

if not os.path.exists("Scalping_Trading.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Scalping_Trading.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Scalping_Trading.xlsx')
for i in ["stats","Exchange","Expiry","Position","OrderBook","OrderBook_New","Option","Data","Buy","Sale","Final",
            "Stat","Stat1","Stat2","Stat3","Stat4"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
by = wb.sheets("Buy")
sl = wb.sheets("Sale")
fl = wb.sheets("Final")
st = wb.sheets("stats")
exc = wb.sheets("Exchange")
exp = wb.sheets("Expiry")
pos = wb.sheets("Position")
ob = wb.sheets("OrderBook")
ob1 = wb.sheets("OrderBook_New")
oc = wb.sheets("Option")
st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
#dt.range("a:x").value = None
# by.range("a:x").value = None
# sl.range("a:ab").value = None
# fl.range("a:az").value = None
#exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:aj").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

#exc.range("a1").value = script_code_5paisa

exchange = None
while True:
    if exchange is None: 
        try:
            exchange = pd.DataFrame(script_code_5paisa)
            exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
            exchange1 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['Series'].isin(['XX']))]
            exchange1["Watchlist"] = exchange1["Exch"] + ":" + exchange1["ExchType"] + ":" + exchange1["Name"]
            exchange1.sort_values(['Name'], ascending=[True], inplace=True)
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

exchange1 = exchange1[(exchange1['Root'].isin(['NIFTY','BANKNIFTY']))]
exchange1.sort_values(['Expiry'], ascending=[True], inplace=True)
exchange1 = exchange1[['ExchType','Name', 'ISIN', 'FullName','Root','StrikeRate', 'CO BO Allowed','CpType','Scripcode','Expiry','LotSize','Watchlist']]
exchange1 = exchange1[(exchange1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
exc_fut1_Expiryy = (np.unique(exchange1['Expiry']).tolist())[:2]         
print(exc_fut1_Expiryy)
exchange1 = exchange1[(exchange1['Expiry'].isin(exc_fut1_Expiryy))] 
exc.range("a1").options(index=False).value = exchange1

print("Exchange Download Completed")

while True:
    a=[
        {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"}]        
        
    #print(credi_har.fetch_market_depth_by_symbol(a))
    dfg1 = credi_har.fetch_market_depth_by_symbol(a)
    dfg2 = dfg1['Data']
    dfg3 = pd.DataFrame(dfg2)
    dfg3['TimeNow'] = datetime.now()
    dfg3['Spot'] = round(dfg3['LastTradedPrice']/100,0)*100
    dfg3['Root'] = np.where(dfg3['ScripCode'] == 999920000,"NIFTY",np.where(dfg3['ScripCode'] == 999920005,"BANKNIFTY",""))
    dfg3 = dfg3[['ScripCode','Root','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow']]
    #dt.range("a22").options(index=False).value = dfg3

    listo = (np.unique(dfg3['Root']).tolist())
    scpt_list = []

    for i in listo: 
        print(i)
        dfg4 = dfg3[dfg3['Root'] == i]
        Spot = int(dfg4['Spot'])   
        print(Spot) 
        stk_name = i
        dfgg = exchange1[exchange1['Root'] == stk_name]
        dfgg.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
        
        dfgg_CE1 = dfgg[(dfgg["CpType"] == 'CE')]        
        dfgg_CE2 = dfgg_CE1[(dfgg_CE1['StrikeRate'] >= Spot)]                        
        dfgg_CE3 = dfgg_CE2.head(1)
        dfgg_CE_scpt = int(np.unique(dfgg_CE3['Scripcode']))
        scpt_list.append(dfgg_CE_scpt)
        #dfg1 = credi_har.fetch_market_depth_by_symbol(a)
        # print(dfgg_CE_scpt)

        dfgg_PE1 = dfgg[(dfgg["CpType"] == 'PE')]        
        dfgg_PE2 = dfgg_PE1[(dfgg_PE1['StrikeRate'] <= Spot)]                        
        dfgg_PE3 = dfgg_PE2.tail(1)
        dfgg_PE_scpt = int(np.unique(dfgg_PE3['Scripcode']))
        scpt_list.append(dfgg_PE_scpt)
        # print(dfgg_PE_scpt)

    print(scpt_list)

    a=[{"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{scpt_list[0]}"},
    {"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{scpt_list[1]}"},
    {"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{scpt_list[2]}"},
    {"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{scpt_list[3]}"}]
    
    dfgg = credi_har.fetch_market_depth(a)
    dfgg1 = dfgg['Data']
    dfgg2 = pd.DataFrame(dfgg1)
    exc = exchange1[['Scripcode','Root','Name','CpType','LotSize']]
    exc.rename(columns={'Scripcode': 'ScripCode'}, inplace=True)
    dfgg3 = pd.merge(dfgg2, exc, on=['ScripCode'], how='inner')
    dfgg3 = dfgg3[['Root','Name','ScripCode','CpType','Open','High','Low','Close','LastTradedPrice','LotSize','OpenInterest','Volume','TotalBuyQuantity','TotalSellQuantity']]
    #dt.range("a8").options(index=False).value = dfgg3

    dfgg4 = pd.merge(dfgg3, dfg3, on=['Root'], how='inner')
    dfgg4.rename(columns={'ScripCode_x': 'ScripCode','CpType':'Type','LotSize':'Lot','Open_x': 'Open_OPT','High_x': 'High_OPT','Low_x': 'Low_OPT','Close_x': 'Close_OPT','LastTradedPrice_x': 'LTP_OPT',
                          'ScripCode_y': 'ScpCode_SPOT','Open_y': 'Open_SPOT','High_y': 'High_SPOT','Low_y': 'Low_SPOT','Close_y': 'Close_SPOT','LastTradedPrice_y': 'LTP_SPOT',}, inplace=True)
    dfgg4['Diff_QTY'] = dfgg4['TotalSellQuantity'] - dfgg4['TotalBuyQuantity']
    #dt.range("a15").options(index=False).value = dfgg4
    
    dfgg5 = dfgg4[['Name','Root','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
                    
    posi = pd.DataFrame(credi_har.positions())
    
    if posi.empty:
        print("First Position is Empty")
        dfgg5 =dfgg5[['Name','Root','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
        dt.range(f"k1:v1").value = ['LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM','Buy_lvl','TGT','SLL','BUY','SELL']
        dt.range("a1").options(index=False).value = dfgg5
    else:
        posit = posi #posit[(posit['MTOM'] != 0)]
        posit3 = (np.unique([int(i) for i in posit['ScripCode']])).tolist()     
        dfgg6 = pd.merge(dfgg5, posi, on=['ScripCode'], how='outer')
        dfgg6 =dfgg6[['Name','Root','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot',
                    'LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM']]
        dt.range(f"r1:v1").value = ["Buy_lvl","TGT","SLL","BUY","SELL"]
        dt.range("a1").options(index=False).value = dfgg6




    scpt = dt.range(f"a{1}:v{5}").value            
    sym = dt.range(f"a{2}:a{500}").value
    symbols = list(filter(lambda item: item is not None, sym))

    scpts = pd.DataFrame(scpt[1:],columns=scpt[0])
    scpts['Name'] = scpts['Name'].apply(lambda x : str(x))

    order_dff_buy = scpts[(scpts['BUY'] >= 1)]
    
    #print(order_dff_buy)
    if order_dff_buy.empty:
        print("No Open Position of Haresh Buy")
    else:
        try: 
            print(order_dff_buy)
            #buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B') & (buy_order_li['AveragePrice'] != 0)]
            order_dff_Scpt = np.unique([int(i) for i in order_dff_buy['ScripCode']])
            for ordd in order_dff_Scpt:
                order_df = order_dff_buy[(order_dff_buy['ScripCode'] == ordd)]
                order = credi_har.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BUY'])*int(order_df['Lot']),Price=float(order_df['LTP_OPT']),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                print("Buy order Executed") 
        except Exception as e:
            print(e)

    order_dff_sell = scpts[(scpts['SELL'] >= 1)]
    #print(order_dff_sell)
    if order_dff_sell.empty:# and order_dff['MTOM'] == 0:
        print("No Open Position of Haresh Sell")
    else:
        if posi.empty:
            print("Position is Empty You Can't Sell")
        else:
            # if order_dff_sell['MTOM'] == 0:
            #     print("There is no Buy Position")
            # else:
            try: 
                print(order_dff_sell)
                #buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B') & (buy_order_li['AveragePrice'] != 0)]
                order_dff_Scpt = np.unique([int(i) for i in order_dff_sell['ScripCode']])
                for ordd in order_dff_Scpt:
                    order_df = order_dff_sell[(order_dff_sell['ScripCode'] == ordd)]
                    order = credi_har.place_order(OrderType='S',Exchange='N',ExchangeType='D', ScripCode = int(order_df['ScripCode']), Qty=int(order_df['SELL'])*int(order_df['Lot']),Price=float(order_df['LTP_OPT']),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    print("Buy order Executed") 
            except Exception as e:
                print(e)
        
    dt.range(f"u2:u5").value = ''
    dt.range(f"v2:v5").value = ''
    dt.range("a10").options(index=False).value = scpts
        
    scpt_list = []
    print(scpt_list)