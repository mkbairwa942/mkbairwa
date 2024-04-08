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
import inspect
from five_paisa1 import *

telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

operate = input("Do you want to go with TOTP (yes/no): ")
telegram_msg = input("Do you want to send TELEGRAM Message (yes/no): ")
orders = input("Do you want to Place Real Orders (yes/no): ")

# operate = 'YES'
# telegram_msg = 'NO'
# orders = 'YES'
# client = credentials("ASHWIN")

if operate.upper() == "YES":
    from five_paisa1 import *
    # p=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
    # print(p)
    username = input("Enter Username : ")
    username1 = str(username)
    print("Hii "+str(username1)+" have a Good Day")
    # username_totp = input("Enter TOTP : ")
    # username_totp1 = str(username_totp)
    # print("Hii "+str(username1)+" you enter TOTP is "+str(username_totp1))
    client = credentials(username1)
else:
    from five_paisa import *

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

#nse = NSELive()

price_limit = 300
Available_Cash = 12000
Exposer = 2


print("---- Data Process Started ----")

if not os.path.exists("Breakout_Nifty_Banknifty.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Breakout_Nifty_Banknifty.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Breakout_Nifty_Banknifty.xlsx')
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
flt_exc.range("a:u").value = None
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
st1.range("a:u").value = None
st2.range("a:u").value = None
st3.range("a:u").value = None
st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

# st.range("a:z").value = None
# exp.range("a:z").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a:s").value = None
# exc.range("a1").options(index=False).value = script_code_5paisa
print("Excel : Started")
exchange = None

def round_up(n, decimals = 0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier



while True:    
    if exchange is None: 
        try:
            exc_fut = pd.DataFrame(script_code_5paisa)
            exc_fut = exc_fut[(exc_fut["Exch"] == "N") & (exc_fut["ExchType"] == "D")]
            exc_fut = exc_fut[exc_fut["CpType"] == "XX"]
            exc_fut = exc_fut[exc_fut["LotSize"] < 5000]
            exc_fut["Watchlist"] = exc_fut["Exch"] + ":" + exc_fut["ExchType"] + ":" + exc_fut["Name"]
            exc_fut.sort_values(['Name'], ascending=[True], inplace=True)
 
            exc_opt = pd.DataFrame(script_code_5paisa)
            exc_opt = exc_opt[(exc_opt["Exch"] == "N") & (exc_opt["ExchType"] == "D")]
            exc_opt = exc_opt[exc_opt["CpType"] != "XX"]
            exc_opt["Watchlist"] = exc_opt["Exch"] + ":" + exc_opt["ExchType"] + ":" + exc_opt["Name"]
            exc_opt.sort_values(['Name'], ascending=[True], inplace=True)
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)


exc_fut.sort_values(['Name'], ascending=[True], inplace=True)
exc_fut = exc_fut[['ExchType','Name', 'ISIN', 'FullName','Root','StrikeRate', 'CO BO Allowed','CpType','Scripcode','Expiry','LotSize','Watchlist']]

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = exc_fut

exc_opt.sort_values(['Name'], ascending=[True], inplace=True)
exc_opt = exc_opt[['ExchType','Name', 'ISIN', 'FullName','Root','StrikeRate', 'CO BO Allowed','CpType','Scripcode','Expiry','LotSize','Watchlist']]
flt_exc.range("o1").options(index=False).value = exc_opt

print("Exchange Data Download")

stop_thread = False

# stk_list = ['BAJAJ-AUTO',	'BPCL',	'BSOFT',	'CANFINHOME',	'DLF',	'FEDERALBNK',	'GODREJPROP',	'GRANULES',	'HEROMOTOCO',	'HINDALCO',	'HINDPETRO',	'IDEA',	'IGL',	'INDHOTEL',	'INDUSTOWER',	'IOC',	'LT',	'MARICO',	'MCX',	'MPHASIS',	'NAUKRI',	'NAVINFLUOR',	'OBEROIRLTY',	'OFSS',	'ONGC',	'PFC',	'PNB',	'RECLTD',	'AARTIIND',	'ABCAPITAL',	'ACC',	'ADANIENT',	'ADANIPORTS',	'ASHOKLEY',	'ASIANPAINT',	'ASTRAL',	'ATUL',	'AUROPHARMA',	'BAJAJFINSV',	'BALRAMCHIN',	'BANKNIFTY',	'BATAINDIA',	'BERGEPAINT',	'BHARTIARTL',	'CANBK',	'CHAMBLFERT',	'COALINDIA',	'CONCOR',	'CROMPTON',	'DABUR',	'DEEPAKNTR',	'DIVISLAB',	'DRREDDY',	'EICHERMOT',	'ESCORTS',	'GMRINFRA',	'GNFC',	'HAVELLS',	'HCLTECH',	'HINDCOPPER',	'ICICIGI',	'IDFC',	'IDFCFIRSTB',	'IEX',	'INDIACEM',	'INDIAMART',	'INDUSINDBK',	'INFY',	'IPCALAB',	'JINDALSTEL',	'JSWSTEEL',	'LTIM',	'LTTS',	'MARUTI',	'MFSL',	'MGL',	'NESTLEIND',	'NIFTY',	'NMDC',	'PETRONET',	'RAMCOCEM',	'RELIANCE',	'SBILIFE',	'SYNGENE',	'TATAPOWER',	'TATASTEEL',	'TCS',	'TECHM',	'TVSMOTOR',	'UBL',	'WIPRO',]

# dfg1 = client.historical_data('N', 'D', 57923, '5m',last_trading_day,current_trading_day) 
# print(dfg1)

# stk_list = np.unique(exc_fut['Root'])
# print("Total Stock : "+str(len(stk_list)))

stk_list = {'NIFTY':999920000,'BANKNIFTY':999920005}

# df = client.historical_data('N', 'C', 999920000, '5m', '2023-12-21','2023-12-22')
# print(df)



#order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 3045, Qty=10,Price=25)

def ordef_func():
    try:
        ordbook = pd.DataFrame(client.order_book())
        #print(ordbook.tail(2))
        pos.range("q1").options(index=False).value = ordbook
    except Exception as e:
                print(e)

    try:
        if ordbook is not None:
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
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            pos.range("a1").options(index=False).value = ordbook1
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

posit = pd.DataFrame(client.positions()) 
if posit.empty:
    print("Position is Empty")
    buy_order_list_dummy = []
else:
    buy_order_li = ordef_func()
    buy_order_list_dummy = (np.unique([int(i) for i in buy_order_li['ScripCode']])).tolist()
    print(buy_order_list_dummy)

while True:
    #time.sleep(60)
    print("buy_order_list_dummy")
    print(buy_order_list_dummy)
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()
    fo_bhav = pd.DataFrame()

    for k, v in stk_list.items():    
        try:
            scpt1 = exc_fut[exc_fut['Root'] == k]
            scpt1.sort_values(['Expiry'], ascending=[False], inplace=True)
            scpt2 = (np.unique(scpt1['Expiry']).tolist())[1]
            scpt3 = scpt1[scpt1['Expiry'] == scpt2]
            aa = int(scpt3['Scripcode'])
            dfg1 = client.historical_data('N', 'D', aa, '5m',last_trading_day,current_trading_day) 
            dfg1['Scripcode'] = aa
            dfg1['Name'] = k
             
            dfg1 = dfg1[['Scripcode','Name','Datetime','Open','High','Low','Close','Volume']]
            dfg1['Date'] = current_trading_day 
            dfg1["RSI_14"] = np.round((pta.rsi(dfg1["Close"], length=14)),2) 

            dfg1.sort_values(['Datetime'], ascending=[False], inplace=True)
            dfg1['TimeNow'] = datetime.now()
            dfg1['Price_Chg'] = round(((dfg1['Close'] * 100) / (dfg1['Close'].shift(-1)) - 100), 2).fillna(0)      

            dfg1['Vol_Chg'] = round(((dfg1['Volume'] * 100) / (dfg1['Volume'].shift(-1)) - 100), 2).fillna(0)

            dfg1['Price_break'] = np.where((dfg1['Close'] > (dfg1.High.rolling(5).max()).shift(-5)),
                                                'Pri_Up_brk',
                                                (np.where((dfg1['Close'] < (dfg1.Low.rolling(5).min()).shift(-5)),
                                                            'Pri_Dwn_brk', "")))
            dfg1['Vol_break'] = np.where(dfg1['Volume'] > (dfg1.Volume.rolling(5).mean() * 2.5).shift(-5),
                                                "Vol_brk","")       
                                                                                                                
            dfg1['Vol_Price_break'] = np.where((dfg1['Vol_break'] == "Vol_brk") &
                                                        (dfg1['Price_break'] != ""), "Vol_Pri_break", "")
            
            dfg1['O=H=L'] = np.where((dfg1['Open'] == dfg1['High']), 'Open_High',
                                            (np.where((dfg1['Open'] == dfg1['Low']), 'Open_Low', "")))
            dfg1['Pattern'] = np.where((dfg1['High'] < dfg1['High'].shift(-1)) &
                                            (dfg1['Low'] > dfg1['Low'].shift(-1)), 'Inside_Bar',
                                            (np.where((dfg1['Low'] < dfg1['Low'].shift(-1)) &
                                                        (dfg1['Close'] > dfg1['High'].shift(-1)), 'Bullish',
                                                        (np.where((dfg1['High'] > dfg1['High'].shift(-1)) &
                                                                (dfg1['Close'] < dfg1['Low'].shift(-1)), 'Bearish',
                                                                "")))))
            dfg1["Buy/Sell"] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"),
                                            "BUY", np.where((dfg1['Vol_break'] == "Vol_brk")
                                                & (dfg1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                        
            dfg1['R3'] = round(dfg1['High'] + (
                    2 * (((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) - dfg1['Low'])), 2).fillna(0)
            dfg1['R2'] = round((((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) + dfg1['High']) - \
                                    dfg1['Low'], 2).fillna(0)
            dfg1['R1'] = round(
                (2 * ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3)) - dfg1['Low'], 2).fillna(0)
            dfg1['Pivot'] = round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3), 2).fillna(0)
            dfg1['S1'] = round(
                (2 * ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3)) - dfg1['High'], 2).fillna(0)
            dfg1['S2'] = round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) - (dfg1['High'] -
                                                                                                    dfg1['Low']),2).fillna(0)
                                
            dfg1['S3'] = round(dfg1['Low'] - (
                    2 * (dfg1['High'] - ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3))), 2)
            dfg1['Mid_point'] = round(((dfg1['High'] + dfg1['Low']) / 2), 2).fillna(0)
            dfg1['CPR'] = round(
                abs((round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3), 2)) - dfg1['Mid_point']),
                2).fillna(0)
            dfg1['CPR_SCAN'] = np.where((dfg1['CPR'] < ((dfg1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                            "")
            dfg1['Candle'] = np.where(abs(dfg1['Open'] - dfg1['Close']) <
                                            abs(dfg1['High'] - dfg1['Low']) * 0.2, "DOZI",
                                            np.where(abs(dfg1['Open'] - dfg1['Close']) >
                                                    abs(dfg1['High'] - dfg1['Low']) * 0.7, "s", ""))
            
            # dfg1 = dfg1[0:25]
            dfg1 = dfg1.astype({"Datetime": "datetime64"})    
            dfg1["Date"] = dfg1["Datetime"].dt.date

            five_df1 = pd.concat([dfg1, five_df1])

            dfgg_up = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_break") & (dfg1["Buy/Sell"] != "") & (dfg1["RSI_14"] > 55 ) & (dfg1["Date"] == current_trading_day.date())]
            dfgg_dn = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_break") & (dfg1["Buy/Sell"] != "") & (dfg1["RSI_14"] < 45 ) & (dfg1["Date"] == current_trading_day.date())]


            dfgg_up1 = dfgg_up.iloc[:2]
            dfgg_dn1 = dfgg_dn.iloc[:2]

            five_df2 = pd.concat([dfgg_up1, five_df2])            
            five_df3 = pd.concat([dfgg_dn1, five_df3])

            stk_name = dfg1['Name'][0]
            print("5 Min Future Data Download and Scan "+str(stk_name)+" ("+str(aa)+")")                            

            if len(dfgg_up) == 0:
                print("111")
            else:
                stk_name1 = k
                dfgg_up_sc = dfgg_up.iloc[:1]
                dfgg_up_scpt = int(dfgg_up_sc['Close'])
                dfgg_up_scpt1 = exc_opt[(exc_opt["CpType"] == 'CE')]
                dfgg_up_scpt2 = dfgg_up_scpt1[dfgg_up_scpt1['Root'] == stk_name1]
                dfgg_up_scpt3 = dfgg_up_scpt2[(dfgg_up_scpt2['StrikeRate'] > dfgg_up_scpt)]
                dfgg_up_scpt3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                
                dfgg_up_scpt4 = dfgg_up_scpt3.iloc[2:3]
                dfgg_up_scpt5 = int(np.unique(dfgg_up_scpt4['Scripcode']))
                dfg2 = client.historical_data('N', 'D', dfgg_up_scpt5, '5m',last_trading_day,current_trading_day) 
                dfg2['Scripcode'] = dfgg_up_scpt5
                dfg2 = pd.merge(exc_opt, dfg2, on=['Scripcode'], how='inner') 
                dfg2 = dfg2[['Scripcode','Root','Name','Datetime','Open','High','Low','Close','Volume','LotSize']]
                dfg2['Date'] = current_trading_day 
                dfg2["RSI_14"] = np.round((pta.rsi(dfg2["Close"], length=14)),2) 

                dfg2.sort_values(['Datetime'], ascending=[False], inplace=True)
                dfg2['TimeNow'] = datetime.now()
                dfg2['Price_Chg'] = round(((dfg2['Close'] * 100) / (dfg2['Close'].shift(-1)) - 100), 2).fillna(0)      
                
                dfg2['Vol_Chg'] = round(((dfg2['Volume'] * 100) / (dfg2['Volume'].shift(-1)) - 100), 2).fillna(0)

                dfg2['Price_break'] = np.where((dfg2['Close'] > (dfg2.High.rolling(5).max()).shift(-5)),
                                                    'Pri_Up_brk',
                                                    (np.where((dfg2['Close'] < (dfg2.Low.rolling(5).min()).shift(-5)),
                                                                'Pri_Dwn_brk', "")))
                dfg2['Vol_break'] = np.where(dfg2['Volume'] > (dfg2.Volume.rolling(5).mean() * 2.5).shift(-5),
                                                    "Vol_brk","")       
                                                                                                                    
                dfg2['Vol_Price_break'] = np.where((dfg2['Vol_break'] == "Vol_brk") &
                                                            (dfg2['Price_break'] != ""), "Vol_Pri_break", "")
                
                dfg2['O=H=L'] = np.where((dfg2['Open'] == dfg2['High']), 'Open_High',
                                                (np.where((dfg2['Open'] == dfg2['Low']), 'Open_Low', "")))
                dfg2['Pattern'] = np.where((dfg2['High'] < dfg2['High'].shift(-1)) &
                                                (dfg2['Low'] > dfg2['Low'].shift(-1)), 'Inside_Bar',
                                                (np.where((dfg2['Low'] < dfg2['Low'].shift(-1)) &
                                                            (dfg2['Close'] > dfg2['High'].shift(-1)), 'Bullish',
                                                            (np.where((dfg2['High'] > dfg2['High'].shift(-1)) &
                                                                    (dfg2['Close'] < dfg2['Low'].shift(-1)), 'Bearish',
                                                                    "")))))
                dfg2["Buy/Sell"] = np.where((dfg2['Vol_break'] == "Vol_brk") & (dfg2['Price_break'] == "Pri_Up_brk"),
                                                "BUY", np.where((dfg2['Vol_break'] == "Vol_brk")
                                                    & (dfg2['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                            
                dfg2['R3'] = round(dfg2['High'] + (
                        2 * (((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3) - dfg2['Low'])), 2).fillna(0)
                dfg2['R2'] = round((((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3) + dfg2['High']) - \
                                        dfg2['Low'], 2).fillna(0)
                dfg2['R1'] = round(
                    (2 * ((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3)) - dfg2['Low'], 2).fillna(0)
                dfg2['Pivot'] = round(((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3), 2).fillna(0)
                dfg2['S1'] = round(
                    (2 * ((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3)) - dfg2['High'], 2).fillna(0)
                dfg2['S2'] = round(((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3) - (dfg2['High'] -
                                                                                                        dfg2['Low']),2).fillna(0)
                                    
                dfg2['S3'] = round(dfg2['Low'] - (
                        2 * (dfg2['High'] - ((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3))), 2)
                dfg2['Mid_point'] = round(((dfg2['High'] + dfg2['Low']) / 2), 2).fillna(0)
                dfg2['CPR'] = round(
                    abs((round(((dfg2['High'] + dfg2['Low'] + dfg2['Close']) / 3), 2)) - dfg2['Mid_point']),
                    2).fillna(0)
                dfg2['CPR_SCAN'] = np.where((dfg2['CPR'] < ((dfg2.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                                "")
                dfg2['Candle'] = np.where(abs(dfg2['Open'] - dfg2['Close']) <
                                                abs(dfg2['High'] - dfg2['Low']) * 0.2, "DOZI",
                                                np.where(abs(dfg2['Open'] - dfg2['Close']) >
                                                        abs(dfg2['High'] - dfg2['Low']) * 0.7, "s", ""))

                dfg2 = dfg2.astype({"Datetime": "datetime64"})    
                dfg2["Date"] = dfg2["Datetime"].dt.date

                dfg2['Minutes'] = dfg2['TimeNow']-dfg2["Datetime"]
                dfg2['Minutes'] = round((dfg2['Minutes']/np.timedelta64(1,'m')),2)
                dfg2['Buy/Sell1'] = np.where(dfg2['Close'] > (dfg2['High']).shift(-1),"Buy_new",np.where(dfg2['Close'] < (dfg2['Low']).shift(-1),"Sell_new",""))
                dfg2['Buy_At'] = round((dfg2['Close']),1)
                dfg2['Stop_Loss'] = np.where(dfg2['Buy/Sell1'] == "Buy_new",round((dfg2['Buy_At'] - (dfg2['Buy_At']*2)/100),1),np.where(dfg2['Buy/Sell1'] == "Sell_new",round((((dfg2['Buy_At']*2)/100) + dfg2['Buy_At']),1),""))
                dfg2['Add_Till'] = round((dfg2['Buy_At']-((dfg2['Buy_At']*0.5)/100)),1)         
                dfg2['Target'] = np.where(dfg2['Buy/Sell1'] == "Buy_new",round((((dfg2['Buy_At']*2)/100) + dfg2['Buy_At']),2),np.where(dfg2['Buy/Sell1'] == "Sell_new",round((dfg2['Buy_At'] - (dfg2['Buy_At']*2)/100),1),""))
                dfg2['Term'] = "SFT"
                five_df4 = pd.concat([dfg2, five_df4])

                stk_name2 = dfg2['Name'][0]
                print("5 Minute Option Data Download and Scan "+str(stk_name2)+" ("+str(dfgg_up_scpt5)+")")               

                

                dfgg_up_11 = dfg2[(dfg2["Vol_Price_break"] == "Vol_Pri_break") & (dfg2["Buy/Sell1"] == "Buy_new") & (dfg2["RSI_14"] > 55 ) & (dfg2["Date"] == current_trading_day.date()) & (dfg2["Minutes"] < 5 )]
                dfgg_dn_11 = dfg2[(dfg2["Vol_Price_break"] == "Vol_Pri_break") & (dfg2["Buy/Sell1"] == "Sell_new") & (dfg2["RSI_14"] < 45 ) & (dfg2["Date"] == current_trading_day.date()) & (dfg2["Minutes"] < 5 )]

                #dfgg1 = dfgg1.iloc[[1]]
                #dfgg1 = dfgg1.iloc[1:2]
                if len(dfgg_up_11) == 0:
                    print("5 Minute Option Data Scan But Not Selected "+str(stk_name2)+" ("+str(dfgg_up_scpt5)+")")                            
                else:
                    print("5 Minute Option Data Scan and Selected "+str(stk_name2)+" ("+str(dfgg_up_scpt5)+")")
                    dfgg_up_1 = dfgg_up_11.iloc[[0]]
                    Buy_Scriptcodee = int(dfgg_up_1['Scripcode'])
                    five_df5 = pd.concat([dfgg_up_1, five_df5])        

                    if dfgg_up_1.empty:
                        
                        if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                            parameters = {"chat_id" : "6143172607","text" : "Stock Selected but more than '5 MINUTE' ago : "+str(stk_name1)}
                            resp = requests.get(telegram_basr_url, data=parameters)
                            #print(resp.text)
                            print("Stock Selected for Buy but more than '5 MINUTE' ago : "+str(stk_name2))
                        else:
                            print("Telegram Message are OFF")

                    else:    
                        # buy_order_li = ordef_func()                            
                        # buy_order_list = (np.unique([int(i) for i in buy_order_li['ScripCode']])).tolist()
                        # print(aa,buy_order_list,Buy_Scriptcodee)
                        # Buy_Scriptcodee = int(dfgg_up_1['Scripcode'])
                        # if Buy_Scriptcodee in buy_order_list:                                     
                        #     print(str(Buy_Scriptcodee)+" is Already Buy")
                        # else:
                        if Buy_Scriptcodee in buy_order_list_dummy: 
                            print(str(Buy_Scriptcodee)+" is Already Buy")
                        else:
                            Buy_Scriptcodee = int(dfgg_up_1['Scripcode'])
                            Buy_price_of_stock = float(dfgg_up_1['Buy_At'])  
                            Buy_Add_Till = float(dfgg_up_1['Add_Till'])                       
                            Buy_Stop_Loss = float(dfgg_up_1['Stop_Loss']) 
                            Buy_Limt_Stop_Loss = float(dfgg_up_1['Stop_Loss']) - 0.5  
                            Buy_Target = float(dfgg_up_1['Target']) 
                            Buy_Target1 = round((((dfgg_up_1['Buy_At']*4)/100) + dfgg_up_1['Buy_At']),2)                                    
                            Buy_timee = str((dfgg_up_1['Datetime'].values)[0])[0:19] 
                            Buy_timee1= Buy_timee.replace("T", " " )
                            Buy_Lotsize = int(dfgg_up_1['LotSize'])
                            buy_order_list_dummy.append(Buy_Scriptcodee)
                            Buy_traling = round(((dfgg_up_1['Buy_At']*2)/100),2)
                            print(Buy_price_of_stock,Buy_traling)
                            # print(Buy_timee1)

                            # if Buy_price_of_stock < 100:
                            #     Buy_quantity_of_stock = 200
                            # if Buy_price_of_stock > 100 and Buy_price_of_stock < 200:
                            #     Buy_quantity_of_stock = 100                        
                            # if Buy_price_of_stock > 200 and Buy_price_of_stock < 300:
                            #     Buy_quantity_of_stock = 80
                            # if Buy_price_of_stock > 300:
                            #     Buy_quantity_of_stock = 50
                            # Req_Amount = Buy_quantity_of_stock*Buy_price_of_stock   

                            Buy_quantity_of_stock = Buy_Lotsize
                            if orders.upper() == "YES" or orders.upper() == "":
                                #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock,Price=Buy_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                order = client.cover_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Limt_Stop_Loss,TrailingSL=0.5)
                                #order = client.bo_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,TargetPrice=Buy_Target1,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Stop_Loss-1,TrailingSL=0.5)
                                #print("orders")                            
                            else:
                                pass
                            print("5 Minute Data Selected "+str(stk_name2)+" ("+str(Buy_Scriptcodee)+")")
                            print("Buy Order of "+str(stk_name2)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock)+" on "+str(Buy_timee1))
                        
                            print("SYMBOL : "+str(stk_name2)+"\n BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1))
                            if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                                parameters1 = {"chat_id" : "6143172607","text" : "STOCK : "+str(stk_name2)+"\n BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1)}
                                resp = requests.get(telegram_basr_url, data=parameters1)
                            else:
                                print("Telegram Message are OFF")
                            # print(resp.text)

                        # buy_order_list.append(aa)

                if len(dfgg_dn_11) == 0:
                    print("222")
                else:
                    print("22")
                    dfgg_dn_1 = dfgg_dn_11.iloc[[0]]
                    five_df6 = pd.concat([dfgg_dn_1, five_df6])

                    if dfgg_dn_1.empty:
                        if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                            parameters = {"chat_id" : "6143172607","text" : "Stock Selected but more than '5 MINUTE' ago : "+str(stk_name2)}
                            resp = requests.get(telegram_basr_url, data=parameters)
                        else:
                            print("Telegram Message are OFF")
                        print("Stock Selected for Sell but more than '5 MINUTE' ago : "+str(stk_name2))

                    else:
                        buy_order_list = buy_order_list_dummy
                        Sell_Scriptcodee = int(dfgg_dn_1['Scripcode'])
                        if Sell_Scriptcodee in buy_order_list: 
                            print(str(Sell_Scriptcodee)+" is Already Buy")
                        else:
                            if Buy_Scriptcodee in buy_order_list_dummy: 
                                print(str(Buy_Scriptcodee)+" is Already Buy")
                            else:
                                Sell_Scriptcodee = int(dfgg_dn_1['Scripcode'])
                                Sell_price_of_stock = float(dfgg_dn_1['Buy_At'])  
                                Sell_Add_Till = float(dfgg_dn_1['Add_Till'])                       
                                Sell_Stop_Loss = float(dfgg_dn_1['Stop_Loss'])    
                                Sell_Target = float(dfgg_dn_1['Target']) 
                                Sell_timee = str((dfgg_dn_1['Datetime'].values)[0])[0:19] 
                                Sell_timee1= Sell_timee.replace("T", " " )
                                Sell_Lotsize = int(dfgg_dn_1['LotSize'])
                                Sell_quantity_of_stock = Sell_Lotsize

                                if orders.upper() == "YES" or orders.upper() == "":
                                    buy_order_list_dummy.append(Sell_Scriptcodee)
                                    #order = client.place_order(OrderType='S',Exchange='N',ExchangeType='D', ScripCode = Sell_Scriptcodee, Qty=Sell_quantity_of_stock,Price=Sell_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Sell_Stop_Loss)
                                else:
                                    pass
                                print("5 Minute Data Selected "+str(stk_name2)+" ("+str(Sell_Scriptcodee)+")")
                                print("Sell Order of "+str(stk_name2)+" at : Rs "+str(Sell_price_of_stock)+" and Quantity is "+str(Sell_quantity_of_stock)+" on"+str(Sell_timee1))
                                
                                print("SYMBOL : "+str(stk_name2)+"\n SELL AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1))
                                if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                                    parameters1 = {"chat_id" : "6143172607","text" : "STOCK : "+str(stk_name2)+"\n SELL AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1)}
                                    resp = requests.get(telegram_basr_url, data=parameters1)
                                else:
                                    print("Telegram Message are OFF")
        
        except Exception as e:
                    print(e) 

        print("------------------------------------------------") 

    if fo_bhav.empty:
        pass
    else:
        #fo_bhav = fo_bhav[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        fo_bhav.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        bhv_fo.range("a:az").value = None
        bhv_fo.range("a1").options(index=False).value = fo_bhav


    if five_df1.empty:
        pass
    else:
        five_df1 = five_df1[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df1.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        Fiv_dt.range("a:az").value = None
        Fiv_dt.range("a1").options(index=False).value = five_df1

    if five_df2.empty:
        pass
    else:
        five_df2 = five_df2[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df2.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        delv_dt.range("a:az").value = None
        delv_dt.range("a1").options(index=False).value = five_df2
    
    # if five_df3.empty:
    #     pass
    # else:
    #     five_df3 = five_df3[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     five_df3.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    #     delv_dt.range("a50").options(index=False).value = five_df3

    if five_df4.empty:
        pass
    else:
        five_df4 = five_df4[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','LotSize','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        five_delv.range("a:az").value = None
        five_delv.range("a1").options(index=False).value = five_df4
    
    if five_df5.empty:
        pass
    else:
        # five_df14 = pd.merge(flt_exc_eq, five_df5, on=['Scripcode'], how='inner') 
        five_df5 = five_df5[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df5.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        fl_data.range("a:az").value = None
        fl_data.range("a1").options(index=False).value = five_df5

    if five_df6.empty:
        pass
    else:
        # five_df12 = pd.merge(flt_exc_eq, five_df6, on=['Scripcode'], how='inner') 
        five_df6 = five_df6[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df6.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        #fl_data.range("a:az").value = None
        #fl_data.range("a30").options(index=False).value = five_df6

    if five_df4.empty:
        pass
    else:
        # five_df13 = pd.merge(flt_exc_eq, five_df4, on=['Scripcode'], how='inner') 
        five_df4 = five_df4[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        
        not_selected_up = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Buy_new") & (five_df4["RSI_14"] > 55 ) & (five_df4["Date"] == current_trading_day.date())]
        not_selected_dn = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Sell_new") & (five_df4["RSI_14"] < 45 ) & (five_df4["Date"] == current_trading_day.date())]
        
    end = time.time() - start_time
 
    print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    # print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Breakout_Nifty_Banknifty.xlsx")


