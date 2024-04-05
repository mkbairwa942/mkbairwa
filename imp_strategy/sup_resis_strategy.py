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


# username = "HARESH"
# username1 = str(username)
# client = credentials(username1)
users = ["HARESH","MUKESH"]#,"ALPESH"]
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
                if us == "MUKESH":
                    credi_muk = credentials("MUKESH")
                    if credi_muk.request_token is None:
                        credi_muk = credentials("MUKESH")
                        print(credi_muk.request_token)
                # if us == "ALPESH":
                #     credi_alp = credentials("ALPESH")
                #     if credi_alp.request_token is None:
                #         credi_alp = credentials("ALPESH")
                #         print(credi_alp.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_har,credi_muk]#,credi_alp]
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
second_last_trading_day = trading_days[2]
time_change = timedelta(minutes=870) 
new_current_trading_day = current_trading_day + time_change
print(new_current_trading_day)

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

if not os.path.exists("sup_resis_strategy.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("sup_resis_strategy.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('sup_resis_strategy.xlsx')
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
st.range("a:w").value = None

# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

# start = datetime.time(9, 30, 0)
# end = datetime.time(14, 45, 0)
# current = datetime.datetime.now().time()
# print(start, end, current)


# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)
# #script_code_5paisa1 = script_code_5paisa[(script_code_5paisa["Exch"] == "N") & (script_code_5paisa["Series"] == "XX")]
# #exc.range("a1").options(index=False).value = script_code_5paisa1

# exchange = None
# while True:    
#     if exchange is None: 
#         try:
#             exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
#             exch.sort_values(['Root'], ascending=[True], inplace=True)
            
#             root_list = np.unique(exch['Root']).tolist()
            
#             root_list = ["BANKNIFTY","NIFTY"]

#             exc_new = exch['Root'].isin(root_list)
            
#             exc_new1 = exch[exc_new]
#             eq_exc = exc_new1[(exc_new1["Exch"] == "N") & (exc_new1["ExchType"] == "C") & (exc_new1["CpType"] == "EQ")]
#             #exc.range("a1").options(index=False).value = eq_exc
#             Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
#             Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
#             exc_new2 = Expiry
#             exc_new2.rename(columns={'Scripcode': 'ScripCode' },inplace=True)
#             exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(5)

# flt_exc.range("a:az").value = None
# flt_exc.range("a1").options(index=False).value = exc_new2

#symbol1 = '999920005'
stk_list = [999920005,999920000]

# telegram_msg = "yes"
# orders = "yes"
Capital = 20000
StockPriceLessThan = 1000
Buy_price_buffer = 2
Vol_per = 15
UP_Rsi_lvl = 60
DN_Rsi_lvl = 40
adx_parameter = 0.40
adx_parameter_opt = 0.1
sam_21_slop = 1.5
dema_21_slope = 2
slll = -900
tgtt = 3000
lotsize = 2

SLL = 5
TSL = 5
tsl1 = 1-(TSL/100)
print(tsl1)

# st.range("ac1").value = "Orders"
# st.range("ae1").value = "Tele_Msg"
# st.range("ad1").value = "YES"
# st.range("af1").value = "YES"
st.range("ac3").value = "NIFTY"
st.range("ad3").value = "BANKNIFTY"

while True:
    orders,telegram_msg = st.range("ad1").value,st.range("af1").value
    nft_rng_1 = st.range("ac5").options(numbers = lambda x : float(x)).value
    #nft_rng_1 = st.range("ac5").value
    nft_rng_2 = st["ac6"].value
    nft_rng_3 = st.range("ac7").value
    nft_rng_4 = st.range("ac8").value
    nft_rng_5 = st.range("ac9").value
    bk_nft_rng_1 = st.range("ad5").value
    bk_nft_rng_2 = st.range("ad6").value
    bk_nft_rng_3 = st.range("ad7").value
    bk_nft_rng_4 = st.range("ad8").value
    bk_nft_rng_5 = st.range("ad9").value

    # if orders is None:
    #     orders = "yes"
    # if telegram_msg is None:
    #     telegram_msg = "yes"

    print(orders,telegram_msg)
    print(nft_rng_1,nft_rng_2,nft_rng_3,nft_rng_4,nft_rng_5)
    print(bk_nft_rng_1,bk_nft_rng_2,bk_nft_rng_3,bk_nft_rng_4,bk_nft_rng_5)