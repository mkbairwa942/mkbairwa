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
from five_paisa import *
import threading
from dateutil.parser import parse
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega


telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

from_d = (date.today() - timedelta(days=15))
from_d = date(2023, 1, 1)

to_d = (date.today())
to_d = date(2023, 12, 31)

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

if not os.path.exists("Chart_Pat_Ana.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Chart_Pat_Ana.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Chart_Pat_Ana.xlsx')
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

#credi_ash = credentials("ashwin")

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# #exc.range("a1").value = script_code_5paisa

# exchange = None
# while True:
#     if exchange is None: 
#         try:
#             exchange = pd.DataFrame(script_code_5paisa)      
#             exchange3 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['C'])) & (exchange['Series'].isin(['EQ']))]
#             exchange2 = exchange3[1044:]
#             #df = df[0:299]
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(10)
# exc.range("a1").value = exchange2

# stk_list = np.unique(exchange2['Scripcode'])

start_time = time.time()
# for i in stk_list:    
#     try:
#         print(i)
#         df = credi_ash.historical_data('N', 'C', i, '5m',from_d,to_d)
#         df['Scripcode'] = i
#         df = df.astype({"Datetime": "datetime64"})    
#         df["Date"] = df["Datetime"].dt.date
#         df['Prev_Close'] = df['Close'].shift(1)
#         dfg1 = pd.merge(exchange2, df, on=['Scripcode'], how='inner') 
#         dfg1 = dfg1[['Scripcode','Name','Datetime','Date','Open','High','Low','Close','Prev_Close','Volume']]
#         dfg1['Open_P'] = round(((((100*dfg1['Open'])/dfg1['Prev_Close']))-100),1)
#         dfg1['High_P'] = round(((((100*dfg1['High'])/dfg1['Prev_Close']))-100),1)
#         dfg1['Low_P'] = round(((((100*dfg1['Low'])/dfg1['Prev_Close']))-100),1)
#         dfg1['Close_P'] = round(((((100*dfg1['Close'])/dfg1['Prev_Close']))-100),1)
#         by.range("a1").value = dfg1
#         dfg1.to_sql(name="Hist_Data", con=engine, if_exists="append")
#         print(dfg1['Name'].head(1))
#         #print(dfg1.tail(5))
#     except Exception as e:
#         print(f"Error : {e}")

stockName = 'SBIN'
sbinquery = f"select * from dbo.Hist_Data where Name = '{stockName}'"
#select * from dbo.Hist_Data where Name = 'SBIN'
sbin_df = pd.read_sql(sql=sbinquery, con=engine)
sbin_df = sbin_df[120:150]
sbin_len = sbin_df.shape[0]
print("SBIN length is "+str(sbin_len))
by.range("a1").value = sbin_df

allquery = "select TOP 10000 * from dbo.Hist_Data"
#select * from dbo.Hist_Data where Name = 'SBIN'
all_df = pd.read_sql(sql=allquery, con=engine)
all_len = all_df.shape[0]
print("All length is "+str(all_len))
#all_df = all_df[0:100]

ss = []

sbi_idx = 0
all_idx = 0

for ind in range(120, 150-4):
    print("SBIN idx is "+str(ind))
    for ind1 in range(0, all_len-4):
        #print(ind1)
        if sbin_df['Open_P'][ind] == all_df['Open_P'][ind1] and sbin_df['High_P'][ind] == all_df['High_P'][ind1] and sbin_df['Low_P'][ind] == all_df['Low_P'][ind1] and sbin_df['Close_P'][ind] == all_df['Close_P'][ind1]:# and sbin_df.shape[0] <= sbin_len and all_df.shape[0] <= all_len:
            if sbin_df['Open_P'][ind+1] == all_df['Open_P'][ind1+1] and sbin_df['High_P'][ind+1] == all_df['High_P'][ind1+1] and sbin_df['Low_P'][ind+1] == all_df['Low_P'][ind1+1] and sbin_df['Close_P'][ind+1] == all_df['Close_P'][ind1+1]:# and sbin_df.shape[0] <= sbin_len and all_df.shape[0] <= all_len:
                if sbin_df['Open_P'][ind+2] == all_df['Open_P'][ind1+2] and sbin_df['High_P'][ind+2] == all_df['High_P'][ind1+2] and sbin_df['Low_P'][ind+2] == all_df['Low_P'][ind1+2] and sbin_df['Close_P'][ind+2] == all_df['Close_P'][ind1+2]:# and sbin_df.shape[0] < sbin_len and all_df.shape[0] < all_len:
                    if sbin_df['Open_P'][ind+3] == all_df['Open_P'][ind1+3] and sbin_df['High_P'][ind+3] == all_df['High_P'][ind1+3] and sbin_df['Low_P'][ind+3] == all_df['Low_P'][ind1+3] and sbin_df['Close_P'][ind+3] == all_df['Close_P'][ind1+3]:# and sbin_df.shape[0] < sbin_len and all_df.shape[0] < all_len:
                        if sbin_df['Open_P'][ind+4] == all_df['Open_P'][ind1+4] and sbin_df['High_P'][ind+4] == all_df['High_P'][ind1+4] and sbin_df['Low_P'][ind+4] == all_df['Low_P'][ind1+4] and sbin_df['Close_P'][ind+4] == all_df['Close_P'][ind1+4]:# and sbin_df.shape[0] < sbin_len and all_df.shape[0] < all_len:
                            
                            ids = 0
                            for ui in range(0,5):
                                print(ui,ids)
                                print(sbin_df['Name'][ind+ids],sbin_df['Datetime'][ind+ids],sbin_df['Open_P'][ind+ids],sbin_df['High_P'][ind+ids],sbin_df['Low_P'][ind+ids],sbin_df['Close_P'][ind]+ids)
                                print(all_df['Name'][ind1+ids],all_df['Datetime'][ind1+ids],all_df['Open_P'][ind1+ids],all_df['High_P'][ind1+ids],all_df['Low_P'][ind1+ids],all_df['Close_P'][ind1]+ids)
                                # print(sbin_df['Name'][ind+1],sbin_df['Datetime'][ind+1],sbin_df['Open_P'][ind+1],sbin_df['High_P'][ind+1],sbin_df['Low_P'][ind+1],sbin_df['Close_P'][ind+1])
                                # print(all_df['Name'][ind1+1],all_df['Datetime'][ind1+1],all_df['Open_P'][ind1+1],all_df['High_P'][ind1+1],all_df['Low_P'][ind1+1],all_df['Close_P'][ind1+1])
                                # print(sbin_df['Name'][ind+2],sbin_df['Datetime'][ind+2],sbin_df['Open_P'][ind+2],sbin_df['High_P'][ind+2],sbin_df['Low_P'][ind+2],sbin_df['Close_P'][ind+2])
                                # print(all_df['Name'][ind1+2],all_df['Datetime'][ind1+2],all_df['Open_P'][ind1+2],all_df['High_P'][ind1+2],all_df['Low_P'][ind1+2],all_df['Close_P'][ind1+2]) 
                                # print(sbin_df['Name'][ind+3],sbin_df['Datetime'][ind+3],sbin_df['Open_P'][ind+3],sbin_df['High_P'][ind+3],sbin_df['Low_P'][ind+3],sbin_df['Close_P'][ind+3])
                                # print(all_df['Name'][ind1+3],all_df['Datetime'][ind1+3],all_df['Open_P'][ind1+3],all_df['High_P'][ind1+3],all_df['Low_P'][ind1+3],all_df['Close_P'][ind1+3])  
                                # print(sbin_df['Name'][ind+4],sbin_df['Datetime'][ind+4],sbin_df['Open_P'][ind+4],sbin_df['High_P'][ind+4],sbin_df['Low_P'][ind+4],sbin_df['Close_P'][ind+4])
                                # print(all_df['Name'][ind1+4],all_df['Datetime'][ind1+4],all_df['Open_P'][ind1+4],all_df['High_P'][ind1+4],all_df['Low_P'][ind1+4],all_df['Close_P'][ind1+4])
                                ss.append([sbin_df['Name'][ind+ids],sbin_df['Datetime'][ind+ids],sbin_df['Open_P'][ind+ids],sbin_df['High_P'][ind+ids],sbin_df['Low_P'][ind+ids],sbin_df['Close_P'][ind]+ids,
                                            all_df['Name'][ind1+ids],all_df['Datetime'][ind1+ids],all_df['Open_P'][ind1+ids],all_df['High_P'][ind1+ids],all_df['Low_P'][ind1+ids],all_df['Close_P'][ind1]+ids])         
                                ids +=1
                            print("All idx is "+str(ind1+4))

                            # ss.append([sbin_df['Name'][ind],sbin_df['Datetime'][ind],sbin_df['Open_P'][ind],sbin_df['High_P'][ind],sbin_df['Low_P'][ind],sbin_df['Close_P'][ind],
                            # all_df['Name'][ind1],all_df['Datetime'][ind1],all_df['Open_P'][ind1],all_df['High_P'][ind1],all_df['Low_P'][ind1],all_df['Close_P'][ind1],
                            # sbin_df['Name'][ind+1],sbin_df['Datetime'][ind+1],sbin_df['Open_P'][ind+1],sbin_df['High_P'][ind+1],sbin_df['Low_P'][ind+1],sbin_df['Close_P'][ind+1],
                            # all_df['Name'][ind1+1],all_df['Datetime'][ind1+1],all_df['Open_P'][ind1+1],all_df['High_P'][ind1+1],all_df['Low_P'][ind1+1],all_df['Close_P'][ind1+1],
                            # sbin_df['Name'][ind+2],sbin_df['Datetime'][ind+2],sbin_df['Open_P'][ind+2],sbin_df['High_P'][ind+2],sbin_df['Low_P'][ind+2],sbin_df['Close_P'][ind+2],
                            # all_df['Name'][ind1+2],all_df['Datetime'][ind1+2],all_df['Open_P'][ind1+2],all_df['High_P'][ind1+2],all_df['Low_P'][ind1+2],all_df['Close_P'][ind1+2], 
                            # sbin_df['Name'][ind+3],sbin_df['Datetime'][ind+3],sbin_df['Open_P'][ind+3],sbin_df['High_P'][ind+3],sbin_df['Low_P'][ind+3],sbin_df['Close_P'][ind+3],
                            # all_df['Name'][ind1+3],all_df['Datetime'][ind1+3],all_df['Open_P'][ind1+3],all_df['High_P'][ind1+3],all_df['Low_P'][ind1+3],all_df['Close_P'][ind1+3],  
                            # sbin_df['Name'][ind+4],sbin_df['Datetime'][ind+4],sbin_df['Open_P'][ind+4],sbin_df['High_P'][ind+4],sbin_df['Low_P'][ind+4],sbin_df['Close_P'][ind+4],
                            # all_df['Name'][ind1+4],all_df['Datetime'][ind1+4],all_df['Open_P'][ind1+4],all_df['High_P'][ind1+4],all_df['Low_P'][ind1+4],all_df['Close_P'][ind1+4]])            

                            #ss.append([sbin_df['Name'][ind],sbin_df['Datetime'][ind],sbin_df['Open_P'][ind],sbin_df['High_P'][ind],sbin_df['Low_P'][ind],sbin_df['Close_P'][ind],all_df['Name'][ind1],all_df['Datetime'][ind1],all_df['Open_P'][ind1],all_df['High_P'][ind1],all_df['Low_P'][ind1],all_df['Close_P'][ind1]])
print(ss)
df1 = pd.DataFrame(ss, columns=['Name', 'Datetime', 'Open_P','High_P','Low_P','Close_P','Name', 'Datetime', 'Open_P','High_P','Low_P','Close_P'])
print(df1)
fl.range("a1").value = df1
end4 = time.time() - start_time