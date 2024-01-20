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

operate = input("Do you want to go with TOTP (yes/no): ")
#notifi = input("Do you want to send Notification on Desktop (yes/no): ")
telegram_msg = input("Do you want to send TELEGRAM Message (yes/no): ")
orders = input("Do you want to Place Real Orders (yes/no): ")
if operate.upper() == "YES":
    from five_paisa1 import *
    username = input("Enter Username : ")
    username1 = str(username)
    print("Hii "+str(username1)+" have a Good Day")
    client = credentials(username1)
else:
    from five_paisa import *

# operate = "YES"
# telegram_msg = "no"
# orders = "no"
# username = "ASHWIN"
# username1 = str(username)
# client = credentials(username1)

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
trading_dayss = ['2024-01-20', '2024-01-19','2024-01-18']
trading_days = trading_dayss[1:]

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

price_limit = 300
Available_Cash = 12000
Exposer = 2

print("---- Data Process Started ----")

if not os.path.exists("Index_trading.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Index_trading.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Index_trading.xlsx')
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
            exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N") & (script_code_5paisa["ExchType"] == "D")]
            exch.sort_values(['Root'], ascending=[True], inplace=True)
            
            root_list = np.unique(exch['Root']).tolist()

            
            root_list = ["BANKNIFTY"]

            exc_new = exch['Root'].isin(root_list)
            
            exc_new1 = exch[exc_new]
            #print(exc_new1.head(1))
            #Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
            #Expiry = (np.unique(Expiry1['Expiry']).tolist())
            Expiry = exc_new1
            Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)
            #print(Expiry)
            # exc_new1 = exc_new1[exc_new1["LotSize"] < 5000]
            # Expiry = (np.unique(exc_new1['Expiry']).tolist())
            # print(Expiry)
            # Expiryy = (np.unique(exc_new1['Expiry']).tolist())[1]            
            # print(Expiryy)
            #exc_new2 = exc_new1[exc_new1['Expiry'] == Expiryy]     
            exc_new2 = Expiry
            #print(exc_new2)
            #exc_new2.sort_values(['Root'], ascending=[True], inplace=True)
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

print("Exchange Data Download")

stop_thread = False

#stk_list = ['BAJAJ-AUTO',	'BPCL',	'BSOFT',	'CANFINHOME',	'DLF',	'FEDERALBNK',	'GODREJPROP',	'GRANULES',	'HEROMOTOCO',	'HINDALCO',	'HINDPETRO',	'IDEA',	'IGL',	'INDHOTEL',	'INDUSTOWER',	'IOC',	'LT',	'MARICO',	'MCX',	'MPHASIS',	'NAUKRI',	'NAVINFLUOR',	'OBEROIRLTY',	'OFSS',	'ONGC',	'PFC',	'PNB',	'RECLTD',	'AARTIIND',	'ABCAPITAL',	'ACC',	'ADANIENT',	'ADANIPORTS',	'ASHOKLEY',	'ASIANPAINT',	'ASTRAL',	'ATUL',	'AUROPHARMA',	'BAJAJFINSV',	'BALRAMCHIN',	'BANKNIFTY',	'BATAINDIA',	'BERGEPAINT',	'BHARTIARTL',	'CANBK',	'CHAMBLFERT',	'COALINDIA',	'CONCOR',	'CROMPTON',	'DABUR',	'DEEPAKNTR',	'DIVISLAB',	'DRREDDY',	'EICHERMOT',	'ESCORTS',	'GMRINFRA',	'GNFC',	'HAVELLS',	'HCLTECH',	'HINDCOPPER',	'ICICIGI',	'IDFC',	'IDFCFIRSTB',	'IEX',	'INDIACEM',	'INDIAMART',	'INDUSINDBK',	'INFY',	'IPCALAB',	'JINDALSTEL',	'JSWSTEEL',	'LTIM',	'LTTS',	'MARUTI',	'MFSL',	'MGL',	'NESTLEIND',	'NIFTY',	'NMDC',	'PETRONET',	'RAMCOCEM',	'RELIANCE',	'SBILIFE',	'SYNGENE',	'TATAPOWER',	'TATASTEEL',	'TCS',	'TECHM',	'TVSMOTOR',	'UBL',	'WIPRO',]

stk_list = np.unique(exc_fut['Root'])
print("Total Stock : "+str(len(stk_list)))

#order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 3045, Qty=10,Price=25)

def ordef_func():
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

#buy_order_li = ordef_func()


posit = pd.DataFrame(client.positions()) 
if posit.empty:
    print("Position is Empty")
    buy_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order_li = ordef_func()
    buy_order_list_dummy = (np.unique([int(i) for i in buy_order_li['ScripCode']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()
    #print(buy_order_list_dummy)

def data_download(stk_nm,Qty,start_dt,end_dt,vol_pr,rsi_up_lvll,rsi_dn_lvll):
        #print(stk_nm)
        # scpt1 = exc_fut[exc_fut['Root'] == stk_nm]
        
        # aaa = int(scpt1['Scripcode'])

        dfg1 = client.historical_data('N', 'D', stk_nm, '1m',start_dt,end_dt) 
        dfg1['Scripcode'] = stk_nm
        #print(dfg1.head(1))
        dfg1 = pd.merge(exc_opt, dfg1, on=['Scripcode'], how='inner') 
        dfg1 = dfg1[['Scripcode','Root','Name','Datetime','Open','High','Low','Close','Volume']]
        dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)

        dfg1["RSI_14"] = np.round((pta.rsi(dfg1["Close"], length=14)),2) 

        dfg1.sort_values(['Datetime'], ascending=[False], inplace=True)
        dfg1['TimeNow'] = datetime.now()
        dfg1['Price_Chg'] = round(((dfg1['Close'] * 100) / (dfg1['Close'].shift(-1)) - 100), 2).fillna(0)      

        dfg1['Vol_Chg'] = round(((dfg1['Volume'] * 100) / (dfg1['Volume'].shift(-1)) - 100), 2).fillna(0)

        dfg1['Price_break'] = np.where((dfg1['Close'] > (dfg1.High.rolling(5).max()).shift(-5)),
                                            'Pri_Up_brk',
                                            (np.where((dfg1['Close'] < (dfg1.Low.rolling(5).min()).shift(-5)),
                                                        'Pri_Dwn_brk', "")))
        dfg1['Vol_break'] = np.where(dfg1['Volume'] > (dfg1.Volume.rolling(5).mean() * vol_pr).shift(-5),
                                            "Vol_brk","")       
                                                                                                            
        dfg1['Vol_Price_break'] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"), "Vol_Pri_Up_break",np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Dwn_brk"), "Vol_Pri_Dn_break", ""))
        dfg1["Buy/Sell"] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"),
                                            "BUY", np.where((dfg1['Vol_break'] == "Vol_brk")
                                                & (dfg1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
        dfg1['Rsi_OK'] = np.where((dfg1["RSI_14"].shift(-1)) > rsi_up_lvll-2,"Rsi_Up_OK",np.where((dfg1["RSI_14"].shift(-1)) < rsi_dn_lvll+2,"Rsi_Dn_OK",""))
        dfg1['Price_OK'] = np.where((dfg1["Price_break"].shift(-1)) == "Pri_Up_brk","Price_Up_OK",np.where((dfg1["Price_break"].shift(-1)) == "Pri_Dwn_brk","Price_Dn_OK",""))
        dfg1['Cand_Col'] = np.where(dfg1['Close'] > dfg1['Open'],"Green",np.where(dfg1['Close'] < dfg1['Open'],"Red","") ) 
        dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)
        dfg1 = dfg1.astype({"Datetime": "datetime64"}) 
        
        dfg1["Date"] = dfg1["Datetime"].dt.date
        dfg1['Minutes'] = dfg1['TimeNow']-dfg1["Datetime"]
        dfg1['Minutes'] = round((dfg1['Minutes']/np.timedelta64(1,'m')),2)
        dfg1['LotSize'] = Qty
        dfg1['Buy_At'] = round((dfg1['Close']),2)
        dfg1['Add_Till'] = round((dfg1['Buy_At']-10),1)
        dfg1['StopLoss'] = round((dfg1['Buy_At']-20),1)               
        dfg1['Target'] = round((dfg1['Buy_At']+20),2) 
        #print(dfg1.head(1))   
        dfg1['Benchmark'] = dfg1['High'].cummax()
        dfg1['TStopLoss'] = dfg1['Benchmark'] - 20                         
        dfg1['Status'] = np.where(dfg1['Close'] < dfg1['TStopLoss'],"TSL",np.where(dfg1['Close'] < dfg1['StopLoss'],"SL",""))
        dfg1['P&L_TSL'] = np.where(dfg1['Status'] == "SL",(dfg1['StopLoss'] - dfg1['Buy_At'])*dfg1['LotSize'],np.where(dfg1['Status'] == "TSL",(dfg1['TStopLoss'] - dfg1['Buy_At'])*dfg1['LotSize'],"" ))
        dfg1['Buy/Sell1'] = np.where((dfg1['Close'] > dfg1['High'].shift(-1)),"Buy_new",np.where((dfg1['Close'] < dfg1['Low'].shift(-1)),"Sell_new",""))#np.where((dfg1['Close'] < dfg1['Low'].shift(-1)),"Sell_new",""))       
        #print(dfg1.head(1))  
       
        # pdb = dfg1[(dfg1["Date"] == last_trading_day.date())]
        # pdhb1 = pdb['High'].cummax()[0]
        # pdlb1 = pdb['Low'].cummin()[0]

        # dfg1['PDB'] = np.where(dfg1['Open'] > pdhb1,"PDHB",np.where(dfg1['Open'] < pdlb1,"PDLB",""))   
        
        return dfg1

while True:

    print("buy_order_list_dummy")
    print(buy_order_list_dummy)
    print(buy_root_list_dummy)
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()
    five_df7 = pd.DataFrame()
    fo_bhav = pd.DataFrame()

    Vol_per = 15
    UP_Rsi_lvl = 60
    DN_Rsi_lvl = 40

    #stk_list = (np.unique([str(i) for i in dfg1['Scripcode']])).tolist()

    for sc in stk_list:
        try:
            scpt1 = exc_fut[exc_fut['Root'] == sc]
            aaa = int(scpt1['Scripcode'])
            #print(scpt1,aaa)
            stk_name = (np.unique([str(i) for i in scpt1['Name']])).tolist()[0]
            Root = (np.unique([str(i) for i in scpt1['Root']])).tolist()[0]
            fut_cls = client.historical_data('N', 'D', aaa, '1m',last_trading_day,current_trading_day)
            fut_cls['Scripcode'] = sc
            fut_cls['Name'] = stk_name
            fut_cls1 = fut_cls.tail(1)
            Fut_Closee = int(float(fut_cls1['Close']))           
            print(Fut_Closee)
            Excchhh_up = exc_opt[(exc_opt["CpType"] == 'CE')]
            Excchh_up = Excchhh_up[Excchhh_up['Root'] == Root]
            Excchh2_up = Excchh_up[(Excchh_up['StrikeRate'] > Fut_Closee)]
            Excchh2_up.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
            
            Excchh3_up = Excchh2_up.head(1)
            Buy_quantity_of_stock = int(np.unique(Excchh3_up['LotSize']))
            Buy_Scriptcodee = int(np.unique(Excchh3_up['Scripcode'])[0])
            stk_name1_up = (np.unique([str(i) for i in Excchh3_up['Name']])).tolist()[0]

            dfg1_up = data_download(Buy_Scriptcodee,Buy_quantity_of_stock,last_trading_day,current_trading_day,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl)   
            dfg1_up = dfg1_up.tail(397)
           
            five_df1 = pd.concat([dfg1_up, five_df1])

            dfgg_up11 = dfg1_up[(dfg1_up["RSI_14"] > UP_Rsi_lvl ) & (dfg1_up["Rsi_OK"] == "Rsi_Up_OK" ) & (dfg1_up["Price_OK"] == "Price_Up_OK" ) & (dfg1_up["Cand_Col"] == "Green" )]
            dfgg_up11['Date_Dif'] = (dfgg_up11["Datetime"].shift(-1) -dfgg_up11["Datetime"]).astype('timedelta64[m]') 
            dfgg_up11 = dfgg_up11[(dfgg_up11["Date"] == current_trading_day)]# & ((dfgg_up11['Date_Dif'].shift(1)) > 10)]
            five_df2 = pd.concat([dfgg_up11, five_df2])

            dfgg_up = dfgg_up11[(dfgg_up11["Date"] == current_trading_day) & (dfgg_up11["Minutes"] < 5 )]# & (dfg1['PDB'] == "PDHB")]

            print("5 Min Option Call Data Download and Scan "+str(stk_name1_up)+" ("+str(Buy_Scriptcodee)+")")                                  

            if not dfgg_up.empty:
                print("up")
                if Buy_Scriptcodee in buy_order_list_dummy: 
                    print(str(Buy_Scriptcodee)+" is Already Buy")
                else:
                    dfg3 = dfgg_up.tail(1)
                    Buy_price_of_stock = float(dfg3['Buy_At'])  
                    Buy_Add_Till = float(dfg3['Add_Till'])                
                    Buy_Stop_Loss = float(dfg3['StopLoss'])    
                    Buy_Target = float(dfg3['Target'])                                  
                    Buy_timee = str((dfg3['Datetime'].values)[0])[0:19] 
                    Buy_timee1= Buy_timee.replace("T", " " )
                    buy_order_list_dummy.append(Buy_Scriptcodee)
                    buy_root_list_dummy.append(Root)
                    
                    if orders.upper() == "YES" or orders.upper() == "":
                        #order =  client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, Price=Buy_price_of_stock)
                        order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock,Price=Buy_price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                        #order = client.bo_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,TargetPrice=345,StopLossPrice=320,LimitPriceForSL=319,TrailingSL=1.5)
                        #order = client.cover_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Stop_Loss-0.5,TrailingSL=0.5)
                        #order = client.bo_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,TargetPrice=Buy_Target1,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Stop_Loss-1,TrailingSL=0.5)
                    else:
                        print("Real Call Order are OFF")
                    print("5 Minute Data Call Selected "+str(stk_name1_up)+" ("+str(Buy_Scriptcodee)+")")
                    print("Call Buy Order of "+str(stk_name1_up)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock)+" on "+str(Buy_timee1))
                
                    print("SYMBOL : "+str(stk_name1_up)+"\n Call BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1))
                    if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                        parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(stk_name1_up)+"\n Call BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1)}
                        resp = requests.get(telegram_basr_url, data=parameters1)
                    else:
                        print("Telegram Message are OFF")

            Excchhh_dn = exc_opt[(exc_opt["CpType"] == 'PE')]
            Excchh_dn = Excchhh_dn[Excchhh_dn['Root'] == Root]
            Excchh2_dn = Excchh_dn[(Excchh_dn['StrikeRate'] < Fut_Closee)]
            Excchh2_dn.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
            
            Excchh3_dn = Excchh2_dn.tail(1)
            Sell_quantity_of_stock = int(np.unique(Excchh3_dn['LotSize']))
            Sell_Scriptcodee = int(np.unique(Excchh3_dn['Scripcode'])[0])
            stk_name1_dn = (np.unique([str(i) for i in Excchh3_dn['Name']])).tolist()[0]

            dfg1_dn = data_download(Sell_Scriptcodee,Sell_quantity_of_stock,last_trading_day,current_trading_day,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl)   
            dfg1_dn = dfg1_dn.tail(397)

            five_df3 = pd.concat([dfg1_dn, five_df3])

            dfgg_dn11 = dfg1_dn[(dfg1_dn["RSI_14"] > UP_Rsi_lvl ) & (dfg1_dn["Rsi_OK"] == "Rsi_Up_OK" ) & (dfg1_dn["Price_OK"] == "Price_Up_OK" ) & (dfg1_dn["Cand_Col"] == "Green" )]
            dfgg_dn11['Date_Dif'] = (dfgg_dn11["Datetime"].shift(-1) -dfgg_dn11["Datetime"]).astype('timedelta64[m]') 
            dfgg_dn11 = dfgg_dn11[(dfgg_dn11["Date"] == current_trading_day) & ((dfgg_dn11['Date_Dif'].shift(1)) > 10)]
            five_df4 = pd.concat([dfgg_dn11, five_df4])

            dfgg_dn = dfgg_dn11[(dfgg_dn11["Date"] == current_trading_day) & (dfgg_dn11["Minutes"] < 5 )]
           
            print("5 Min Option Data Put Download and Scan "+str(stk_name1_dn)+" ("+str(Sell_Scriptcodee)+")")                                  

            if not dfgg_dn.empty:
                print("dn")
                if Sell_Scriptcodee in buy_order_list_dummy: 
                    print(str(stk_name1_dn)+" is Already Buy")
                else:
                    dfg3_dn = dfgg_dn.tail(1)
                    Sell_price_of_stock = float(dfg3_dn['Buy_At'])  
                    Sell_Add_Till = float(dfg3_dn['Add_Till'])                
                    Sell_Stop_Loss = float(dfg3_dn['StopLoss'])    
                    Sell_Target = float(dfg3_dn['Target'])                                  
                    Sell_timee = str((dfg3_dn['Datetime'].values)[0])[0:19] 
                    Sell_timee1= Sell_timee.replace("T", " " )
                    buy_order_list_dummy.append(Sell_Scriptcodee)
                    buy_root_list_dummy.append(Root)
                    
                    if orders.upper() == "YES" or orders.upper() == "":
                        #order =  client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, Price=Buy_price_of_stock)
                        order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Sell_Scriptcodee, Qty=Sell_quantity_of_stock,Price=Sell_price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                        #order = client.bo_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,TargetPrice=345,StopLossPrice=320,LimitPriceForSL=319,TrailingSL=1.5)
                        #order = client.cover_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Stop_Loss-0.5,TrailingSL=0.5)
                        #order = client.bo_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock, LimitPrice=Buy_price_of_stock,TargetPrice=Buy_Target1,StopLossPrice=Buy_Stop_Loss,LimitPriceForSL=Buy_Stop_Loss-1,TrailingSL=0.5)
                    else:
                        print("Real Put Order are OFF")
                    print("5 Minute Data Put Selected "+str(stk_name1_dn)+" ("+str(Sell_Scriptcodee)+")")
                    print("Put Buy Order of "+str(stk_name1_dn)+" at : Rs "+str(Sell_price_of_stock)+" and Quantity is "+str(Sell_quantity_of_stock)+" on "+str(Sell_timee1))
                
                    print("SYMBOL : "+str(stk_name1_dn)+"\n Put BUY AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1))
                    if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
                        parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(stk_name1_dn)+"\n Put BUY AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1)}
                        resp = requests.get(telegram_basr_url, data=parameters1)
                    else:
                        print("Telegram Message are OFF")


                
            else:
                pass
                
                print("5 Minute Option Data Scan But Not Selected "+str(stk_name)+" ("+str(aaa)+")")

        except Exception as e:
                    print(e) 

        print("------------------------------------------------") 

    if fo_bhav.empty:
        pass
    else:
        #fo_bhav = fo_bhav[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        #fo_bhav.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        bhv_fo.range("a:az").value = None
        bhv_fo.range("a1").options(index=False).value = fo_bhav


    if five_df1.empty:
        pass
    else:
        five_df1 = five_df1[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Rsi_OK','Price_OK','Cand_Col','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','Buy/Sell','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df1.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        Fiv_dt.range("a:az").value = None
        Fiv_dt.range("a1").options(index=False).value = five_df1

    if five_df3.empty:
        pass
    else:
        five_df3 = five_df3[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Rsi_OK','Price_OK','Cand_Col','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','Buy/Sell','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df3.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        Fiv_dt.range("a400").options(index=False).value = five_df3

    if five_df2.empty:
        pass
    else:
        five_df2 = five_df2[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df2.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        delv_dt.range("a:az").value = None
        delv_dt.range("a1").options(index=False).value = five_df2

    if five_df4.empty:
        pass
    else:
        five_df4 = five_df4[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df4.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
        delv_dt.range("a25").options(index=False).value = five_df4

    # if five_df4.empty:
    #     pass
    # else:
    #     #five_df4 = five_df4[['Name','Scripcode','StopLoss','Add_Till','Buy_At','Target','Term','Datetime','LotSize','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    #     five_delv.range("a:az").value = None
    #     five_delv.range("a1").options(index=False).value = five_df4

    # if five_df5.empty:
    #     pass
    # else:
    #     #five_df5 = five_df5[['Name','Scripcode','StopLoss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     five_df5.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    #     fl_data.range("a:az").value = None
    #     fl_data.range("a1").options(index=False).value = five_df5

    # if five_df6.empty:
    #     pass
    # else:
    #     #five_df6 = five_df6[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     five_df6.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    #     bhv_fo.range("a:az").value = None
    #     bhv_fo.range("a1").options(index=False).value = five_df6

    # if five_df7.empty:
    #     pass
    # else:
    #     #five_df7 = five_df7[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     five_df7.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    #     #bhv_fo.range("a:az").value = None
    #     bhv_fo.range("a50").options(index=False).value = five_df7

    end = time.time() - start_time

    print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    # print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")








































































































           