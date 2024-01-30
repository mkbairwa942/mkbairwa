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

current_trading_day = trading_dayss[0]
last_trading_day = trading_dayss[2]
second_last_trading_day = trading_days[3]

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

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a1").value = script_code_5paisa

# exchange = None
# while True:
#     if exchange is None: 
#         try:
#             exchange = pd.DataFrame(script_code_5paisa)
#             exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
#             exchange1 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['CpType'].isin(['EQ', 'XX']))]
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(10)
# df = pd.DataFrame({"FNO Symbol": list(exchange1["Root"].unique())})
# df = df.set_index("FNO Symbol",drop=True)
# oc.range("a1").value = df

while True:
    # a=[{"Exchange":"M","ExchangeType":"D","Symbol":"SILVER 05 Mar 2024                                "},
    #    {"Exchange":"M","ExchangeType":"D","Symbol":"GOLD 05 Feb 2024                            "}]
    a=[        
        {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MIDCPNIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"FINNIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"AARTIIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ABB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ABBOTINDIA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ABCAPITAL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ABFRL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ACC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ADANIENT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ADANIPORTS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ALKEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"AMBUJACEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"APOLLOHOSP"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"APOLLOTYRE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ASHOKLEY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ASIANPAINT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ASTRAL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ATUL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"AUBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"AUROPHARMA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"AXISBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BAJAJ-AUTO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BAJAJFINSV"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BAJFINANCE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BALKRISIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BALRAMCHIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BANDHANBNK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BANKBARODA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BATAINDIA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BERGEPAINT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BHARATFORG"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BHARTIARTL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BHEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BIOCON"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BOSCHLTD"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BPCL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BRITANNIA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BSOFT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CANBK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CANFINHOME"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CHAMBLFERT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CHOLAFIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CIPLA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"COALINDIA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"COFORGE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"COLPAL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CONCOR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"COROMANDEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CROMPTON"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CUB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"CUMMINSIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DABUR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DALBHARAT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DEEPAKNTR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DIVISLAB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DIXON"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DLF"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DRREDDY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"EICHERMOT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ESCORTS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"EXIDEIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"FEDERALBNK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GAIL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GLENMARK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GMRINFRA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GNFC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GODREJCP"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GODREJPROP"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GRANULES"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GRASIM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"GUJGASLTD"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HAL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HAVELLS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HCLTECH"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HDFCAMC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HDFCBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HDFCLIFE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HEROMOTOCO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HINDALCO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HINDCOPPER"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HINDPETRO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"HINDUNILVR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ICICIBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ICICIGI"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ICICIPRULI"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IDEA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IDFC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IDFCFIRSTB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IEX"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IGL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDHOTEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDIACEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDIAMART"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDIGO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDUSINDBK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INDUSTOWER"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"INFY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IOC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IPCALAB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"IRCTC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ITC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"JINDALSTEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"JKCEMENT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"JSWSTEEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"JUBLFOOD"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"KOTAKBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"L&TFH"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LALPATHLAB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LAURUSLABS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LICHSGFIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LTIM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LTTS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"LUPIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"M&M"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"M&MFIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MANAPPURAM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MARICO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MARUTI"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MCDOWELL-N"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MCX"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"METROPOLIS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MFSL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MGL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MOTHERSON"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MPHASIS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MRF"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"MUTHOOTFIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NATIONALUM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NAUKRI"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NAVINFLUOR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NESTLEIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NMDC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"NTPC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"OBEROIRLTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"OFSS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ONGC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PAGEIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PERSISTENT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PETRONET"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PFC"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PIDILITIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PIIND"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PNB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"POLYCAB"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"POWERGRID"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"PVRINOX"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"RAMCOCEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"RBLBANK"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"RECLTD"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"RELIANCE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SAIL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SBICARD"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SBILIFE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SBIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SHREECEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SHRIRAMFIN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SIEMENS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SRF"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SUNPHARMA"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SUNTV"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"SYNGENE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATACHEM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATACOMM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATACONSUM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATAMOTORS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATAPOWER"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TATASTEEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TCS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TECHM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TITAN"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TORNTPHARM"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TRENT"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"TVSMOTOR"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"UBL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ULTRACEMCO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"UPL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"VEDL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"VOLTAS"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"WIPRO"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ZEEL"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"ZYDUSLIFE"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"DELTACORP"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"India"}]

    dfg1 = credi_ash.fetch_market_depth_by_symbol(a)
    dfg2 = dfg1['Data']
    dfg3 = pd.DataFrame(dfg2)
    dfg3['TimeNow'] = datetime.now()
    dfg3.to_sql(name="tick_data", con=engine, if_exists="append", index=False)
    #print(dfg3.tail(1))



    sqlquery = "select * from dbo.tick_data"
    dff = pd.read_sql(sql=sqlquery, con=engine)
    dff.sort_values(['ScripCode','TimeNow'], ascending=[False, False], inplace=True)
    dff1 = pd.DataFrame(dff)
    print(dff1.tail(1))

    dff1 = dff1[['ScripCode','TimeNow','Open','High','Low','Close','LastTradedPrice','AverageTradePrice','Volume','LowerCircuitLimit','UpperCircuitLimit','OpenInterest','NetChange']]
    dff1.rename(columns={'LastTradedPrice': 'LTP','AverageTradePrice': 'ATP','LowerCircuitLimit': 'Lo_Cir','UpperCircuitLimit': 'Up_Cir','OpenInterest': 'OI' },inplace=True)
    dt.range("a:az").value = None
    dt.range("a1").options(index=False).value = dff1


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


