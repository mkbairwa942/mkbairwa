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

if not os.path.exists("Mssql_Trading_Data.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Mssql_Trading_Data.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Mssql_Trading_Data.xlsx')
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
print(exc_new['Name'])
print(exc_new.shape[0])
stock_df = pd.DataFrame({"FNO Symbol": list(exchange1["Root"].unique())})
stock_df = stock_df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = stock_df


# delete_table = "drop table dbo.tick_data"
# del_df = pd.read_sql(sql=delete_table, con=engine)
start_time = time.time()
for i in stk_list:    
    print(i)
    df = credi_ash.historical_data('N', 'C', i, '1m',last_trading_day,current_trading_day)
    df1 = df.tail(1)
end4 = time.time() - start_time

print(f"Total Data Analysis Completed Time: {end4:.2f}s")



#     sqlquery = "select * from dbo.tick_data"
#     dff = pd.read_sql(sql=sqlquery, con=engine)
#     dff.sort_values(['ScripCode','TimeNow'], ascending=[False, False], inplace=True)
#     dff1 = pd.DataFrame(dff)
    
    #print(dff1.tail(1))

    # dff1 = dff1[['ScripCode','TimeNow','Open','High','Low','Close','LastTradedPrice','AverageTradePrice','Volume','LowerCircuitLimit','UpperCircuitLimit','OpenInterest','NetChange']]
    # dff1.rename(columns={'LastTradedPrice': 'LTP','AverageTradePrice': 'ATP','LowerCircuitLimit': 'Lo_Cir','UpperCircuitLimit': 'Up_Cir','OpenInterest': 'OI' },inplace=True)
    # dt.range("a:az").value = None
    # dt.range("a1").options(index=False).value = dff1


# stocks = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
# # stocks = pd.read_csv('E:\STOCK\eq_stock.csv')
# # stocks = pd.read_csv('E:\STOCK\patterns\datasets\companies.csv')
# stocks = stocks.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
# stocks = stocks['SYMBOL']

# def bhavcopy(date):
#     dmyformat = datetime.strftime(date, '%d%m%Y')
#     url = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_' + dmyformat + '.csv'
#     bhav_eq1 = pd.read_csv(url)
#     bhav_eq1 = pd.DataFrame(bhav_eq1)
#     bhav_eq1.columns = bhav_eq1.columns.str.strip()
#     bhav_eq1 = bhav_eq1.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
#     bhav_eq1['DATE1'] = pd.to_datetime(bhav_eq1['DATE1'])
#     bhav_eq = bhav_eq1[bhav_eq1['SERIES'] == 'EQ']
#     bhav_eq['LAST_PRICE'] = bhav_eq['LAST_PRICE'].astype(float)
#     bhav_eq['DELIV_QTY'] = bhav_eq['DELIV_QTY'].astype(float)
#     bhav_eq['DELIV_PER'] = bhav_eq['DELIV_PER'].astype(float)

#     return bhav_eq

# # bh_df = bhavcopy(to_date)
# # print(bh_df.head())
# # print(bh_df.info())

# def bhavcopy_fno(date):
#     dmyformat = datetime.strftime(date, '%d%b%Y').upper()
#     MMM = datetime.strftime(date, '%b').upper()
#     yyyy = datetime.strftime(date, '%Y')
#     url1 = 'https://archives.nseindia.com/content/historical/DERIVATIVES/' + yyyy + '/' + MMM + '/fo' + dmyformat + 'bhav.csv.zip'
#     content = requests.get(url1)
#     zf = ZipFile(BytesIO(content.content))
#     match = [s for s in zf.namelist() if ".csv" in s][0]
#     bhav_fo = pd.read_csv(zf.open(match), low_memory=False)
#     bhav_fo.columns = bhav_fo.columns.str.strip()
#     bhav_fo = bhav_fo.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
#     bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT'])
#     bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
#     bhav_fo = bhav_fo.drop(["Unnamed: 15"], axis=1)
#     return bhav_fo

# for i in dates:
#     try:
#         print(i)
#         bh_df = bhavcopy(i)
#         bh_df = pd.DataFrame(bh_df)
#         bh_df.to_sql(name="full_bhavcopy", con=engine, if_exists="append", index=False)
#         print(bh_df.head(2))
#
#     except:
#         pass

# for i in dates:
#     try:
#         print(i)
#         fo_df = bhavcopy_fno(i)
#         fo_df = pd.DataFrame(fo_df)
#         fo_df.to_sql(name="FO_bhavcopy", con=engine, if_exists="append", index=False)
#         # print(fo_df.head(2))
#
#     except:
#         pass

# for stock in stocks:
#     try:
#         print(stock)
#         st_df = get_history(symbol=stock, start=from_date, end=to_date)
#         st_df = pd.DataFrame(st_df)
#         st_df.reset_index(inplace=True)
#         st_df['Date'] = pd.to_datetime(st_df['Date'])
#         for column in st_df.columns[3:9]:
#             st_df[column] = st_df[column].astype(str).str.replace(',', '').replace('-', '0').astype(float)
#         st_df['%Deliverble'] = st_df['%Deliverble'] * 100
#         st_df.rename(columns={'Deliverable Volume': 'Del_Vol', '%Deliverble': 'Del_Per'}, inplace=True)
#         st_df.to_sql(name="eq_stock_new", con=engine, if_exists="append", index=False)
#         print(st_df.head(2))
#         # print(st_df.info())
#
#     except:
#         pass

# for day in dates:
#     try:
#         print(day)
#         dmyformat = datetime.strftime(day, '%d%m%Y')
#         url = 'https://archives.nseindia.com/content/nsccl/fao_participant_oi_' + dmyformat + '.csv'
#         # tablename = 'fii_dii_open_int'
#         fii_op_int = pd.read_csv(url, skiprows=1)
#         fii_op_int = fii_op_int.drop(fii_op_int.index[4])
#         fii_op_int.insert(0, 'Date', day)
#         fii_op_int['Date'] = pd.to_datetime(fii_op_int['Date'])
#         fii_op_int.columns = [c.strip() for c in fii_op_int.columns.values.tolist()]
#         fii_op_int.to_sql(name="FII_DII_Open_Int", con=engine, if_exists="append", index=False)
#         print(fii_op_int.head(1))
#         print("Data Successfully updated for " + day)
#
#     except:
#         pass

# for day in dates:
#     try:
#         dmyformat = datetime.strftime(day, '%d%m%Y')
#         url = 'https://archives.nseindia.com/content/nsccl/fao_participant_vol_' + dmyformat + '.csv'
#         # tablename = 'fii_dii_volume'
#         fii_op_vol = pd.read_csv(url, skiprows=1)
#         fii_op_vol = fii_op_vol.drop(fii_op_vol.index[4])
#         fii_op_vol.insert(0, 'Date', day)
#         fii_op_vol['Date'] = pd.to_datetime(fii_op_vol['Date'])
#         fii_op_vol.columns = [c.strip() for c in fii_op_vol.columns.values.tolist()]
#         fii_op_vol.to_sql(name="FII_DII_Volume", con=engine, if_exists="append", index=False)
#         print(fii_op_vol.head(1))
#         print("Data Successfully updated for " + day)
#     except:
#         pass


