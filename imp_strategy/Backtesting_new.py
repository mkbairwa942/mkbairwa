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
from five_paisa1 import *

telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

# operate = input("Do you want to go with TOTP (yes/no): ")
# if operate.upper() == "YES":
#     from five_paisa1 import *
#     # p=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
#     # print(p)
#     username = input("Enter Username : ")
#     username1 = str(username)
#     print("Hii "+str(username1)+" have a Good Day")
#     # username_totp = input("Enter TOTP : ")
#     # username_totp1 = str(username_totp)
#     # print("Hii "+str(username1)+" you enter TOTP is "+str(username_totp1))
#     client = credentials(username1)
# else:
#     from five_paisa import *

operate = "YES"
username = "ASHWIN"
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

nse = NSELive()

price_limit = 300
Available_Cash = 12000
Exposer = 2

print("---- Data Process Started ----")

if not os.path.exists("Backtesting_new.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Backtesting_new.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Backtesting_new.xlsx')
for i in ["Exchange","Filt_Exc","Bhavcopy","FO_Bhavcopy","Five_data","Delv_data","Five_Delv","Final_Data","Position","Strategy1","Strategy2","Strategy3","Buy","Sale",
           "Expiry","stats","Stat","Stat1","Stat2","Stat3","Stat4","OrderBook","OrderBook_New"]:
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
ob = wb.sheets("OrderBook")
ob1 = wb.sheets("OrderBook_New")

exc.range("a:u").value = None
flt_exc.range("a:u").value = None
bhv.range("a:u").value = None
bhv_fo.range("a:u").value = None
# Fiv_dt.range("a:u").value = None
# delv_dt.range("a:u").value = None
# five_delv.range("a:u").value = None
# fl_data.range("a:u").value = None
pos.range("a:u").value = None
# strategy1.range("a:u").value = None
# strategy2.range("a:u").value = None
# strategy3.range("a:u").value = None

st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
# st.range("a:u").value = None
# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

strategy1.range("a1:l1").color = (54,226,0)
strategy1.range("a1:l1").font.bold = True
strategy1.range("a1:l1").api.WrapText = True

strategy2.range("a1:l1").color = (54,226,0)
strategy2.range("a1:l1").font.bold = True
strategy2.range("a1:l1").api.WrapText = True

# st.range("a:z").value = None
# exp.range("a:z").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a:s").value = None
# exc.range("a1").options(index=False).value = script_code_5paisa
print("Excel : Started")
exchange = None

# def round_up(n, decimals = 0): 
#     multiplier = 10 ** decimals 
#     return math.ceil(n * multiplier) / multiplier

# while True:    
#     if exchange is None: 
#         try:
#             exc_equity = pd.DataFrame(script_code_5paisa)
#             # exc_equity = exc_equity[(exc_equity["Exch"] == "N") & (exc_equity["ExchType"] == "C")]
#             # exc_equity = exc_equity[exc_equity["Series"] == "EQ"]
#             # exc_equity = exc_equity[exc_equity["CpType"] == "XX"]
#             exc_equity["Watchlist"] = exc_equity["Exch"] + ":" + exc_equity["ExchType"] + ":" + exc_equity["Name"]
#             exc_equity.sort_values(['Name'], ascending=[True], inplace=True)
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(10)

# symb = pd.DataFrame({"Name": list(exc_equity["Root"].unique())})
# symb = symb.set_index("Name",drop=True)

# flt_exc_eq = pd.merge(symb, exc_equity, on=['Name'], how='inner')
# flt_exc_eq.sort_values(['Name'], ascending=[True], inplace=True)
# flt_exc_eq = flt_exc_eq[['ExchType','Name', 'ISIN', 'FullName', 'CO BO Allowed','Scripcode','Watchlist']]

# flt_exc.range("a:az").value = None
# flt_exc.range("a1").options(index=False).value = exc_equity

print("Exchange Data Download")

stop_thread = False

start_time = time.time()

five_df1 = pd.DataFrame()
five_df2 = pd.DataFrame()
five_df3 = pd.DataFrame()
five_df4 = pd.DataFrame()
five_df5 = pd.DataFrame()
five_df6 = pd.DataFrame()
bhv_fo1 = pd.DataFrame()
one_day = pd.DataFrame()

#buy_order_list = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
buy_order_li = pd.read_excel('D:\STOCK\Capital_vercel_new\Backtesting_new.xlsx',sheet_name='Expiry')
#print(buy_order_li.head(2))
buy_order_list = (np.unique([int(i) for i in buy_order_li['Scripcode']])).tolist()

SLL = 1
TSL = 1


tsl1 = 1-(TSL/100)
print(tsl1)

for a in buy_order_list:
    orderboo = buy_order_li[(buy_order_li['Scripcode'] == a)]# & (buy_order_li['BuySell'] == "B")]
    orderboo.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
    print(orderboo['Name'].head(2))
    dfgg_up_1 = orderboo.iloc[[0]]

    Buy_Scriptcodee = int(dfgg_up_1['Scripcode'])
    Buy_Name = list(dfgg_up_1['Name'])[0]
    Buy_price = float(dfgg_up_1['Buy_At'])                 
    Buy_Stop_Loss = float(round((dfgg_up_1['Buy_At'] - (dfgg_up_1['Buy_At']*SLL)/100),1))  
    Buy_Target = float(round((((dfgg_up_1['Buy_At']*SLL)/100) + dfgg_up_1['Buy_At']),1))
    Buy_Exc = 'N' #list(dfgg_up_1['Exch'])[0]
    Buy_Exc_Type = 'D' #list(dfgg_up_1['ExchType'])[0]
    Buy_Qty = int(dfgg_up_1['LotSize'])
    
    Buy_timee = list(dfgg_up_1['Datetime'])[0]
    Buy_timee1 = str(Buy_timee).replace(' ','T')

    dfg1 = client.historical_data(str(Buy_Exc), str(Buy_Exc_Type), a, '1m',last_trading_day,current_trading_day) 
    # print(dfg1.head(2))
    # print(dfg1.tail(2))
    dfg1['Scripcode'] = a
    dfg1['ScripName'] = Buy_Name
    dfg1['Entry_Date'] = Buy_timee1
    dfg1['Entry_Price'] = Buy_price
    # print(dfg1.head(2))
    dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
    dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
    dfg1['StopLoss'] = Buy_Stop_Loss
    dfg1['Target'] = Buy_Target

    dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
    dfg2['Benchmark'] = dfg2['High'].cummax()
    dfg2['TStopLoss'] = dfg2['Benchmark'] * tsl1
    dfg2['BValue'] = dfg2['Entry_Price']*Buy_Qty
    
    dfg2['TGT_SL'] = np.where(dfg2['High'] > Buy_Target,"TGT",np.where(dfg2['Low'] < Buy_Stop_Loss,"SL",""))
    dfg2['SValue'] = np.where(dfg2['TGT_SL'] == "SL",Buy_Stop_Loss*Buy_Qty,np.where(dfg2['TGT_SL'] == "TGT",Buy_Target*Buy_Qty,""))  
    
    dfg2['P&L_SL'] = pd.to_numeric(dfg2['SValue']) - dfg2['BValue']
    dfg2['Qty'] = Buy_Qty
    dfgg2 = dfg2.copy()
    five_df2 = pd.concat([dfg2, five_df2])
    dfg3 = dfg2[(dfg2['TGT_SL'] != '')]    
    dfg4 = dfg3.iloc[0:1]
    five_df1 = pd.concat([dfg4, five_df1])

    dfgg2['TGT_TSL'] = np.where(dfgg2['Low'] < dfgg2['TStopLoss'],"TSL",np.where(dfgg2['Low'] < Buy_Stop_Loss,"SL",""))
    
    five_df4 = pd.concat([dfgg2, five_df4])
    dfgg3 = dfgg2[(dfgg2['TGT_TSL'] != '')] 
    dfgg4 = dfgg3.iloc[0:1]
    #dfgg4['P&L'] = (dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*Buy_Qty
    dfgg4['P&L_TSL'] = np.where(dfgg4['TGT_TSL'] == "SL",(dfgg4['StopLoss'] - dfgg4['Entry_Price'])*Buy_Qty,np.where(dfgg4['TGT_TSL'] == "TSL",(dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*Buy_Qty,"" ))
    five_df3 = pd.concat([dfgg4, five_df3])
    


if five_df1.empty:
    pass
else:
    five_df1.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
    five_df1 = five_df1[['Scripcode','Entry_Date','Exit_Date','ScripName','Entry_Price','Close',
                         'StopLoss','Target','Qty','TGT_SL','P&L_SL','BValue']]
    five_df1.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True) 
                
    strategy1.range("a:az").value = None
    strategy1.range("a1").options(index=False).value = five_df1

if five_df3.empty:
    pass
else:
    five_df3.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
    five_df3 = five_df3[['Scripcode','Entry_Date','Exit_Date','ScripName','Entry_Price','Close',
                         'Benchmark','TStopLoss','Qty','TGT_TSL','P&L_TSL','BValue']]
    five_df3.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True) 
                
    strategy2.range("a:az").value = None
    strategy2.range("a1").options(index=False).value = five_df3

if five_df2.empty:
    pass
else:
    # five_df1 = five_df1[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
    #                         'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
    #                         'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
    #                         'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    five_df2.sort_values(['ScripName', 'Datetime',], ascending=[True, True], inplace=True) 
                
    Fiv_dt.range("a:az").value = None
    Fiv_dt.range("a1").options(index=False).value = five_df2

if five_df4.empty:
    pass
else:
    # five_df4 = five_df1[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
    #                         'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
    #                         'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
    #                         'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    five_df4.sort_values(['ScripName', 'Datetime',], ascending=[True, True], inplace=True) 
                
    delv_dt.range("a:az").value = None
    delv_dt.range("a1").options(index=False).value = five_df4
  
    end = time.time() - start_time
 
    # print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    # print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    #print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Backtesting_new.xlsx")



