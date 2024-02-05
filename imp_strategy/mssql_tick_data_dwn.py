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

operate = "YES"
telegram_msg = "yes"
orders = "yes"
# username = "ASHWIN"
# username1 = str(username)
# client = credentials(username1)

credi_ash = credentials("ASHWIN")
# credi_har = credentials("HARESH")

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

if not os.path.exists("mssql_tick_data_dwn.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("mssql_tick_data_dwn.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('mssql_tick_data_dwn.xlsx')
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
by.range("a:x").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
#exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:aj").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

exc.range("a1").value = script_code_5paisa

exchange = None
while True:
    if exchange is None: 
        try:
            exchange = pd.DataFrame(script_code_5paisa)
            exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
            exchange1 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['CpType'].isin(['EQ', 'XX']))]
            exchange2 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['C'])) & (exchange['Series'].isin(['EQ']))]
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

name_df = pd.DataFrame({"FNO Symbol": list(exchange1["Root"].unique())})
scpt_df = pd.DataFrame({"FNO Symbol": list(exchange1["Scripcode"].unique())})
# print(name_df)
# print(scpt_df)
fo_stk_list = np.unique(exchange1['Root'])

print(len(fo_stk_list))

#exc_new = exchange2['Root'].isin(fo_stk_list)
exc_new = exchange2[(exchange2['Root'].isin(fo_stk_list))]
stk_list = np.unique(exc_new['Scripcode'])
#print(exc_new['Name'])
print(exc_new.shape[0])
stock_df = pd.DataFrame({"FNO Symbol": list(exchange1["Root"].unique())})
stock_df = stock_df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = stock_df


# delete_table = "drop table dbo.Live_Data"
# del_df = pd.read_sql(sql=delete_table, con=engine)

# start_time = time.time()
# for i in stk_list:    
#     print(i)
#     df = credi_ash.historical_data('N', 'C', i, '1m',last_trading_day,current_trading_day)
#     df['Scripcode'] = i
#     df.to_sql(name="Live_Data", con=engine, if_exists="append", index=False)
# end4 = time.time() - start_time

# print(f"Total Data Analysis Completed Time: {end4:.2f}s")


while True:
    start_time = time.time()
    for i in stk_list:    
        print(i)
        df = credi_ash.historical_data('N', 'C', i, '1m',last_trading_day,current_trading_day)
        df['Scripcode'] = i
        df1 = df.tail(1)
        df1.to_sql(name="Live_Data", con=engine, if_exists="append", index=False)
        #print(df1.tail(1))
    end4 = time.time() - start_time

    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

print("Data Process Completed")