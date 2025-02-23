
from collections import namedtuple

#from finta import TA
# import talib
import pandas as pd
import pandas_ta as pta
import copy
import numpy as np
import xlwings as xw
from datetime import datetime,timedelta,timezone
# from numpy import log as nplog
# from numpy import NaN as npNaN
from pandas import DataFrame, Series
# from pandas_ta.overlap import ema, hl2
# from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
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
from datetime import datetime
import time
from calendar import timegm


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

# username = "HARESH"
# username1 = str(username)
# client = credentials(username1)
users = ["HARESH"]#,"ASHWIN","ALPESH"]
credi_har = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_har is None:# and credi_ash is None and credi_alp is None:
        try:
            for us in users:
                print("1")
                if us == "HARESH":
                    credi_har = credentials("HARESH")
                    if credi_har.request_token is None:
                        credi_har = credentials("HARESH")
                        print(credi_har.request_token)
                # if us == "ASHWIN":
                #     credi_ash = credentials("ASHWIN")
                #     if credi_ash.request_token is None:
                #         credi_ash = credentials("ASHWIN")
                #         print(credi_ash.request_token)
                # if us == "ALPESH":
                #     credi_alp = credentials("ALPESH")
                #     if credi_alp.request_token is None:
                #         credi_alp = credentials("ALPESH")
                #         print(credi_alp.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_har]#,credi_ash,credi_alp]
print(cred) 
for credi in cred:
    postt = pd.DataFrame(credi.margin())['Ledgerbalance'][0]
    print(f"Ledger Balance is : {postt}")

from_d = (date.today() - timedelta(days=15))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

days_365 = (date.today() - timedelta(days=365)) 
print("1")
holida = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
print("2")
holida["Date"] = holida["Date1"].dt.date
holida1 = np.unique(holida['Date'])
print(holida1)

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holida1)
trading_dayss = trading_days_reverse[::-1]
# trading_dayss1 = ['2024-01-20', '2024-01-19','2024-01-18']
# trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[0]
second_last_trading_day = trading_days[-1]
time_change = timedelta(minutes=870) 
upto_df = timedelta(minutes=930) 
new_current_trading_day = current_trading_day + time_change
df_upto_datetime = current_trading_day + upto_df
print(new_current_trading_day)
print(df_upto_datetime)

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

print("Excel Starting....")

if not os.path.exists("nifty_strategy.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("nifty_strategy.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('nifty_strategy.xlsx')
for i in ["Exchange","Filt_Exc","Position","Strategy1","Strategy2","Strategy3"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Filt_Exc")
pos = wb.sheets("Position")
strategy1 = wb.sheets("Strategy1")
strategy2 = wb.sheets("Strategy2")
strategy3 = wb.sheets("Strategy3")

exc.range("a:u").value = None
pos.range("a:u").value = None
strategy1.range("a:u").value = None
strategy2.range("a:u").value = None
strategy3.range("a:u").value = None

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)
# #script_code_5paisa1 = script_code_5paisa[(script_code_5paisa["Exch"] == "N") & (script_code_5paisa["Series"] == "XX")]
# #exc.range("a1").options(index=False).value = script_code_5paisa1

# segment = "nse_fo"
# '''
# all - scrips across all segments
# bse_eq - BSE Equity
# nse_eq - NSE Equity
# nse_fo - NSE Derivatives
# bse_fo - BSE Derivatives
# ncd_fo - NSE Currecny
# mcx_fo - MCX
# '''

# script_code_5paisa_url1 = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment}"
# script_code_5paisa1 = pd.read_csv(script_code_5paisa_url1,low_memory=False)

# exchange = None
# while True:    
#     if exchange is None: 
#         try:   
#             #root_list = np.unique(exch['Root']).tolist()      
#             root_list = ["BANKNIFTY","NIFTY"]

#             exch1 = script_code_5paisa1[(script_code_5paisa1["Exch"] == "N") & (script_code_5paisa1["ScripType"] != "XX")]            
#             exch1.rename(columns={'ScripType': 'CpType','SymbolRoot': 'Root','BOCOAllowed': 'CO BO Allowed'},inplace=True)
#             exch1.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)
#             exc_new = exch1['Root'].isin(root_list)            
#             exc_new1 = exch1[exc_new]

#             exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
#             exch.sort_values(['Root'], ascending=[True], inplace=True)            
#             excc = exch['Root'].isin(root_list)            
#             excc1 = exch[excc]

#             Expiry = excc1[(excc1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
#             Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
#             exc_new2 = Expiry
#             exc_new2.rename(columns={'Scripcode': 'ScripCode' },inplace=True)
#             exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

#             # eq_exc = excc1[(excc1["Exch"] == "N") & (excc1["ExchType"] == "C") & (excc1["CpType"] == "EQ")]
#             # exc.range("a1").options(index=False).value = eq_exc
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(5)

# exc.range("a:az").value = None
# exc.range("a1").options(index=False).value = exc_new2

# flt_exc.range("a:az").value = None
# flt_exc.range("a1").options(index=False).value = exc_new1

# stk_list = [999920000,999920005] # NIFTY & BANKNIFTY BOTH
# stk_list = [999920005]#,999920000] # BANKNIFTY
stk_list = [999920000]#,999920005] # NIFTY

def data_download_day(stk_nm):
    df = credi_har.historical_data('N', 'C', stk_nm, '1d', second_last_trading_day,current_trading_day)
    df = df.astype({"Datetime": "datetime64[ns]"})    
    df["Date"] = df["Datetime"].dt.date
    return df

def data_download_min(stk_nm):
    df = credi_har.historical_data('N', 'C', stk_nm, '5m', second_last_trading_day,current_trading_day)
    df = df.astype({"Datetime": "datetime64[ns]"})    
    df["Date"] = df["Datetime"].dt.date
    return df
#while True:
five_df1 = pd.DataFrame()
five_df2 = pd.DataFrame()

for sc in stk_list:
    for dt in trading_days_reverse:
        try:
            dfg1 = data_download_day(sc) 
            dfg1['Cand_Col'] = np.where(dfg1['Close'] > dfg1['Open'],"Green",np.where(dfg1['Close'] < dfg1['Open'],"Red","") ) 
            dfg1['Trade'] = np.where(dfg1['Cand_Col'].shift(1) == 'Green','Call',np.where(dfg1['Cand_Col'].shift(1) == 'Red','Put',''))
            

            dfg2 = data_download_min(sc) 
            

            new_day = dfg1[(dfg1["Date"] == dt.date())]
            five_df1 = pd.concat([new_day, five_df1])
            trad = list(new_day['Trade'])[0]
            # print(trad)
            # print(new_day.tail(1))
            new_min = dfg2[(dfg2["Date"] == dt.date())]
            new_min['Trade'] = trad
            new_min['Cand_Col'] = np.where(new_min['Close'] > new_min['Open'],"Green",np.where(new_min['Close'] < new_min['Open'],"Red","") ) 
            new_min['point'] = np.round((np.where(new_min['Close'] > new_min['Open'],new_min['Close'] - new_min['Open'],np.where(new_min['Close'] < new_min['Open'],new_min['Open'] - new_min['Close'],0))),2)
            new_min['active'] = np.where((new_min['Trade'] == 'Call') & (new_min['Cand_Col'] == 'Red'),"Call_Trade",np.where((new_min['Trade'] == 'Put') & (new_min['Cand_Col'] == 'Green'),"Put_Trade",""))
            
            timelist = new_min['Datetime'].tolist()
            #timelisttt = timelist[::-1]
            #print(timelist)
            for tim in timelist:
                print(tim)
                #print(new_min.tail(1))
                new_min_df = new_min[(new_min["Datetime"] == tim)]
                tradee = list(new_min_df['active'])[0]
                #tradee_side = list(new_min_df['active'])[0]
                if tradee == "Call_Trade":
                    print("yes")
                    Buy_price = (np.unique([float(i) for i in new_min_df['Open']])).tolist()[0]
                    print(Buy_price)
                    break
                if tradee == "Put_Trade":
                    print("yess")
                    Buy_price = (np.unique([float(i) for i in new_min_df['Open']])).tolist()[0]
                    print(Buy_price)
                    break
            new_min['Benchmark'] = Buy_price
            # new_min['Benchmark'] = np.where(new_min['Trade'] == 'Put',new_min['Open'].cummax(),np.where(new_min['Trade'] == 'Call',new_min['Open'].cummin(),0))
            new_min['Buy'] = np.where((new_min['Trade'] == 'Put') & (new_min['Close'] < new_min['Benchmark']),"Put_buy",np.where((new_min['Trade'] == 'Call') & (new_min['Close'] > new_min['Benchmark']),"Call_buy",""))
            five_df2 = pd.concat([new_min, five_df2])

            print(new_min.tail(1))
        except Exception as e:
            print(e) 

try:
    if five_df1.empty:
        pass
    else:
        try:
            five_df1.sort_values(['Datetime'], ascending=[True], inplace=True)
            strategy1.range("a1").options(index=False).value = five_df1 
        except Exception as e:
            print(e)

    if five_df2.empty:
        pass
    else:
        try:
            five_df2.sort_values(['Datetime'], ascending=[True], inplace=True)
            strategy2.range("a1").options(index=False).value = five_df2
        except Exception as e:
            print(e)

except Exception as e:
    print(e) 