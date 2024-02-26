import logging
import time
from datetime import date, timedelta
import calendar
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

users = ["HARESH","ASHWIN","ALPESH"]
credi_har = None
credi_ash = None
credi_alp = None

while True:
    if credi_har is None and credi_ash is None and credi_alp is None:
        try:
            for us in users:
                print("1")
                if us == "HARESH":
                    credi_har = credentials("HARESH")
                    if credi_har.request_token is None:
                        credi_har = credentials("HARESH")
                        print(credi_har.request_token)
                if us == "ASHWIN":
                    credi_ash = credentials("ASHWIN")
                    if credi_ash.request_token is None:
                        credi_ash = credentials("ASHWIN")
                        print(credi_ash.request_token)
                if us == "ALPESH":
                    credi_alp = credentials("ALPESH")
                    if credi_alp.request_token is None:
                        credi_alp = credentials("ALPESH")
                        print(credi_alp.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_har,credi_ash,credi_alp]
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
second_last_trading_day = trading_days[1]
last_day = date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1])
# print(last_day)
# current_trading_day = trading_dayss[0]
# last_trading_day = trading_dayss[2]
# second_last_trading_day = trading_days[3]

print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last Day of Current Month is :- "+str(last_day))
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

if not os.path.exists("Scalping_Trading_new.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Scalping_Trading_new.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Scalping_Trading_new.xlsx')
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
# exp.range("a:z").value = None
# pos.range("a:z").value = None
# ob.range("a:aj").value = None
# ob1.range("a:al").value = None
# st.range("a:u").value = None

def exch_down():
    try:
        script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
        script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)
        df = pd.DataFrame(script_code_5paisa)
        #print(df.head(1))
        df.rename(columns={'Scripcode': 'ScripCode',}, inplace=True)
        df["Watchlist"] = df["Exch"] + ":" + df["ExchType"] + ":" + df["Name"]
        #print(df.head(1))
        exchange_cash = df[(df["Exch"] == "N") & (df['ExchType'].isin(['C'])) & (df["Series"] == "EQ")]
        #print(exchange_cash.head(1))
        exchange_opt = df[(df["Exch"] == "N") & (df['ExchType'].isin(['D'])) & (df['CpType'].isin(['CE','PE']))]
        #print(exchange_opt.head(1))
    except:
        print("Exchange Download Error....")
        time.sleep(10)

    Expiry_exc = (np.unique(exchange_opt['Expiry']).tolist())   
    F_O_List = (np.unique(exchange_opt['Root']).tolist())
    F_O_List_exc = []
    for dttg in F_O_List:
        ag={"Exchange": "N", "ExchangeType": "C", "Symbol": f"{dttg}"}
        F_O_List_exc.append(ag) 

    scpt_listtt_exc = []

    for i in F_O_List:
        print(i)
        Fo_dfg1 = credi_har.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":f"{i}"}])['Data'][0]['LastTradedPrice']
        Spot = round(Fo_dfg1/100,0)*100
        dfc2 = exchange_opt[exchange_opt['Root'] == i]
        dfc3 = dfc2[(dfc2['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
        Expiryyy = (np.unique(dfc3['Expiry']).tolist())[0]        
        dfc = dfc3[dfc3['Expiry'] == Expiryyy]
        dfc.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)

        dfgg_CE1 = dfc[(dfc["CpType"] == 'CE')] 
        dfgg_CE2 = dfgg_CE1[(dfgg_CE1['StrikeRate'] < Spot)] 
        dfgg_PE1 = dfc[(dfc["CpType"] == 'PE')]        
        dfgg_PE2 = dfgg_PE1[(dfgg_PE1['StrikeRate'] > Spot)] 

        if i == 'NIFTY' or i == 'BANKNIFTY':
            dfgg_CE3 = dfgg_CE2.tail(10)
            dfgg_PE3 = dfgg_PE2.head(10)
        else:
            dfgg_CE3 = dfgg_CE2.tail(3)
            dfgg_PE3 = dfgg_PE2.head(3)
        
        dfgg_CE_scpt = (np.unique([int(i) for i in dfgg_CE3['ScripCode']])).tolist()
        scpt_listtt_exc.append(dfgg_CE_scpt)                      
        dfgg_PE_scpt = (np.unique([int(i) for i in dfgg_PE3['ScripCode']])).tolist()
        scpt_listtt_exc.append(dfgg_PE_scpt)


    scpt_listtt2 = []
    for list in scpt_listtt_exc:
        for number in list:
            scpt_listtt2.append(number)

    scpt_listtt2 = np.unique(scpt_listtt2)
    #print(len(scpt_listtt2))

    exchange_opt = exchange_opt[(exchange_opt['ScripCode'].isin(scpt_listtt2))]
    exchange_opt.sort_values(['Name','StrikeRate'], ascending=[True,True], inplace=True)
    exchange_new = pd.concat([exchange_cash, exchange_opt], ignore_index=True, sort=False)
    # print(exchange_new.shape[0])
    # print(exchange_new.head(20))
    return exchange_new

# exchange_new = exch_down()
# exchange_cash = exchange_new[exchange_new['ExchType'] == 'C'] 
# exchange_opt = exchange_new[exchange_new['ExchType'] == 'D'] 

# exc.range("a1").options(index=False).value = exchange_opt
# exc.range("x1").options(index=False).value = exchange_cash

# exchange_cash = exchange_cash[['Exch','ExchType','CpType','LotSize','Root','Name','Expiry','StrikeRate','ScripCode']]
# exchange_opt = exchange_opt[['Exch','ExchType','CpType','LotSize','Root','Name','Expiry','StrikeRate','ScripCode']]

print("Exchange Download Completed")

exchange_opt2 = exc.range(f"a{1}:t{2000}").value
exchange_cash2 = exc.range(f"x{1}:aq{2000}").value
exchange_cash1 = pd.DataFrame(exchange_cash2)
exchange_opt1 = pd.DataFrame(exchange_opt2)
headers_cash = ['Exch','ExchType','ScripCode','Name','Series','Expiry','CpType','StrikeRate','WireCat','ISIN','FullName','LotSize','AllowedToTrade','QtyLimit','Multiplier','Underlyer','Root','TickSize','CO BO Allowed','Watchlist']
headers_opt = ['Exch','ExchType','ScripCode','Name','Series','Expiry','CpType','StrikeRate','WireCat','ISIN','FullName','LotSize','AllowedToTrade','QtyLimit','Multiplier','Underlyer','Root','TickSize','CO BO Allowed','Watchlist']
exchange_cash1.columns = headers_cash
exchange_opt1.columns = headers_opt
exchange_cash = exchange_cash1[1:]
exchange_opt = exchange_opt1[1:]
# exchange_cash['ScripCode'] = exchange_cash['ScripCode'].astype(int)
# exchange_opt['ScripCode'] = exchange_opt['ScripCode'].astype(int)
exchange_cash['ScripCode'] = exchange_cash['ScripCode'].apply(pd.to_numeric, errors='coerce')
exchange_opt['ScripCode'] = exchange_opt['ScripCode' ].apply(pd.to_numeric, errors='coerce')
exp.range("a1").options(index=False).value = exchange_opt
exp.range("x1").options(index=False).value = exchange_cash


buy_lst = []
sell_lst = []
orders = "YES"

while True:

    
    
    scpt = by.range(f"c{2}:c{15}").value
    scpt1 = by.range(f"a{2}:d{15}").value
    symbols = dt.range(f"a{2}:a{15}").value
    trading_info = dt.range(f"a{2}:x{15}").value

    by.range(f"a1:d1").value = ["Exch","ExchType","Name","ScripCode"]
    # print(scpt)
    # print(scpt1)
    # print(symbols)
    # print(trading_info)


    scpt_list = []

    idxex = 0
    for ii in scpt:
        if ii:
            trade1 = scpt1[idxex]
            namew = trade1[0]+":"+trade1[1]+":"+trade1[2]
            aaa={"Exchange": f"{trade1[0]}", "ExchangeType":f"{trade1[1]}", "Symbol": f"{trade1[2]}"}
            scpt_list.append(aaa) 
        idxex += 1

    gg=[
        {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
        {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"}]  

    for tt in gg:
        scpt_list.append(tt) 
        
    #print(scpt_list)
    dfg1 = credi_har.fetch_market_depth_by_symbol(scpt_list)
    dfg2 = dfg1['Data']
    dfg3 = pd.DataFrame(dfg2)
    dfg3['TimeNow'] = datetime.now()
    dfg3['Spot'] = round(dfg3['LastTradedPrice']/100,0)*100
    #dfg3['Root'] = np.where(dfg3['ScripCode'] == 999920000,"NIFTY",np.where(dfg3['ScripCode'] == 999920005,"BANKNIFTY",""))
    dfg3 = dfg3[['ScripCode','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow']]

    #dt.range("a15").options(index=False).value = dfg3

    desire_lst = (np.unique(dfg3['ScripCode']))       
    #exchange_cash.rename(columns={'Scripcode': 'ScripCode'}, inplace=True)
    # print(dfg3.dtypes)
    # print(exchange_cash.dtypes)
    dfg4 = pd.merge(dfg3, exchange_cash, on=['ScripCode'], how='inner')
    #sl.range("a1").options(index=False).value = dfg4


    dfg5 = dfg4[dfg4['ExchType'] == 'C']
    #sl.range("a10").options(index=False).value = dfg5

    listo = (np.unique(dfg5['Root']).tolist())
    
    scpt_listtt = []

    for i in listo: 
        #print(i)
        dfg6 = dfg5[dfg5['Root'] == i]

        #print(dfg6.head(1))
        Spot = int(dfg6['Spot'])   
        print("Spot Price is : "+str(Spot)) 
        stk_name = i
        dfc2 = exchange_opt[exchange_opt['Root'] == stk_name]
        #print(np.unique(dfc2['Root']).tolist())
        dfc3 = dfc2[(dfc2['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
        Expiryyy = (np.unique(dfc3['Expiry']).tolist())[0]        
        #print(Expiryyy)
        dfc = dfc3[dfc3['Expiry'] == Expiryyy]
        dfc.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
        dfgg_CE1 = dfc[(dfc["CpType"] == 'CE')] 
        dfgg_CE2 = dfgg_CE1[(dfgg_CE1['StrikeRate'] < Spot)] 
        dfgg_CE3 = dfgg_CE2.tail(1)
        #print(dfgg_CE3)
        dfgg_CE_scpt = (np.unique([int(i) for i in dfgg_CE3['ScripCode']])).tolist()[0]
        scpt_listtt.append(dfgg_CE_scpt)
        #dfg1 = credi_har.fetch_market_depth_by_symbol(a)
        # print(dfgg_CE_scpt)

        dfgg_PE1 = dfc[(dfc["CpType"] == 'PE')]        
        dfgg_PE2 = dfgg_PE1[(dfgg_PE1['StrikeRate'] > Spot)]                        
        dfgg_PE3 = dfgg_PE2.head(1)
        #print(dfgg_PE3)
        dfgg_PE_scpt = (np.unique([int(i) for i in dfgg_PE3['ScripCode']])).tolist()[0]
        scpt_listtt.append(dfgg_PE_scpt)

    posi = pd.DataFrame(credi_har.positions())
    posi1 = pd.DataFrame(credi_ash.positions())
    if posi.empty:
        print("First Position of Haresh Empty")
    else:
        try:
            pos.range("a1").options(index=False).value = posi
            if posi1.empty:
                print("First Position of Ashwin Empty")
            else:
                pos.range("a10").options(index=False).value = posi1
            #dt.range("a10").options(index=False).value = posi1
            posit3 = (np.unique([int(i) for i in posi['ScripCode']])).tolist()#[0] 
            #print(posit3)
            for t in posit3:
                scpt_listtt.append(t) 
        except Exception as e:
            print(f"Error : {e}")

    
    scpt_listtt1 = np.unique(scpt_listtt)
    #print(scpt_listtt1)
    Data_fr = []

    for dtt in scpt_listtt1:
        #print(dtt)
        a={"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{dtt}"}
        Data_fr.append(a) 

    #print(Data_fr)
    dfggg = credi_har.fetch_market_depth(Data_fr)
    dfggg1 = dfggg['Data']
    dfggg2 = pd.DataFrame(dfggg1)
    dfggg2['TimeNow'] = datetime.now()
    dfggg2['Spot'] = round(dfggg2['LastTradedPrice']/100,0)*100
    dfggg2 = dfggg2[['ScripCode','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow','TotalBuyQuantity','TotalSellQuantity']]
    #sl.range("a20").options(index=False).value = dfggg2

    #print(dfgg2)
    
    # print(exchange_opt.head(2))
    # print(dfggg2.head(2))
    #exchange_opt = exchange_opt[['ScripCode','Root','Name','Exch','ExchType','CpType','LotSize']]
    dfgg3 = pd.merge(dfggg2, exchange_opt, on=['ScripCode'], how='inner')
    dfgg3 = dfgg3[['Root','Name','ScripCode','Exch','ExchType','CpType','Open','High','Low','Close','LastTradedPrice','LotSize','TotalBuyQuantity','TotalSellQuantity']]
    #sl.range("a30").options(index=False).value = dfgg3

    dfgg4 = pd.merge(dfgg3, dfg5, on=['Root'], how='inner')
    dfgg4.rename(columns={'Name_x': 'Name','Exch_x': 'Exch','ExchType_x': 'ExchType','ScripCode_x': 'ScripCode','CpType_x':'Type','LotSize_x':'Lot','Open_x': 'Open_OPT','High_x': 'High_OPT','Low_x': 'Low_OPT','Close_x': 'Close_OPT','LastTradedPrice_x': 'LTP_OPT',
                          'ScripCode_y': 'ScpCode_SPOT','Open_y': 'Open_SPOT','High_y': 'High_SPOT','Low_y': 'Low_SPOT','Close_y': 'Close_SPOT','LastTradedPrice_y': 'LTP_SPOT',}, inplace=True)
    dfgg4['Diff_QTY'] = dfgg4['TotalSellQuantity'] - dfgg4['TotalBuyQuantity']
    
    #sl.range("a40").options(index=False).value = dfgg4
    
    dfgg5 = dfgg4[['Name','Root','Exch','ExchType','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
    
    try:
        if posi.empty:
            print("First Position is Empty")
            dfgg5 =dfgg5[['Name','Root','Exch','ExchType','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
            dt.range(f"m1:x1").value = ['LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM','Buy_lvl','TGT','SLL','BUY','SELL','Status']
            dt.range("a1").options(index=False).value = dfgg5
        else:
            posit = posi #posit[(posit['MTOM'] != 0)]
            #posit3 = (np.unique([int(i) for i in posit['ScripCode']])).tolist()     
            dfgg6 = pd.merge(dfgg5, posi, on=['ScripCode'], how='outer')
            dfgg6 =dfgg6[['Name','Root','Exch_x','ExchType_x','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot',
                        'LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM']]
            dfgg6.sort_values(['Spot','Type'], ascending=[False, True], inplace=True)
            dt.range(f"t1:x1").value = ["Buy_lvl","TGT","SLL","BUY","SELL","Status"]            
            dt.range("a1").options(index=False).value = dfgg6

    except Exception as e:
        print(f"Error : {e}")

    idx = 0
    for i in symbols:
        if i:
            try:
                
                #print("1")
                trade_info = trading_info[idx]
                #print(trade_info)
                Exch = trade_info[2]
                Exc_typ = trade_info[3]
                typee = trade_info[4]
                scpt_code = int(trade_info[5])
                lt_spt = trade_info[7]
                pricee = trade_info[9]
                lotee = trade_info[11]
                mtomm = trade_info[18]
                tgtt = trade_info[20]
                slll = trade_info[21]                
                buyy = trade_info[22]
                selll = trade_info[23]
                by_qty = trade_info[15]
                sl_qty = trade_info[16]
                

                # print(i)
                # print(scpt_code)
                # print(buy_lst)
                # print(sell_lst)     
                if buyy is None:
                    if scpt_code in buy_lst:
                        buy_lst.remove(scpt_code)
                if selll is None:
                    if scpt_code in sell_lst:
                        sell_lst.remove(scpt_code)
                if slll is not None and buyy is not None:
                    var =  ((lt_spt)*0.2)/100                    
                    # print(var)
                    # print(scpt_code)
                    # print(buy_lst)
                    # print("-01")
                    if typee == "CE" and slll < lt_spt and slll > lt_spt-var:  

                        if scpt_code in buy_lst: 
                            print(str(scpt_code)+" Call is Already Buy")
                        else:
                            if orders.upper() == "YES" or orders.upper() == "":  
                                for credi in cred:                            
                                    order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Buy Call Order Executed")
                                    buy_lst.append(scpt_code)

                    if typee == "PE" and slll > lt_spt and slll < lt_spt+var:                        
                        if scpt_code in buy_lst: 
                            print(str(scpt_code)+" Put is Already Buy")
                        else:
                            if orders.upper() == "YES" or orders.upper() == "":  
                                for credi in cred: 
                                    order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Buy Put Order Executed")
                                    buy_lst.append(scpt_code)
                #print("0")        

                if mtomm is not None:
                    #print("01")
                    if selll is not None:
                         #print("02")
                        if float(mtomm) > 0 or float(mtomm) < 0:
                            if scpt_code in sell_lst: 
                                print(str(scpt_code)+" Sell Already Exited")
                            else:
                                if orders.upper() == "YES" or orders.upper() == "":  
                                    for credi in cred:
                                        order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                        print("Sell Order Executed")
                                        sell_lst.append(scpt_code)
                #print("1")  
                if mtomm is not None: 
                    #print("11")
                    if slll is not None:
                        #print("12")
                        if float(mtomm) > 0 or float(mtomm) < 0:
                            #print("13")
                            if typee == "CE" and lt_spt < slll:
                                if scpt_code in sell_lst: 
                                    print(str(scpt_code)+" call Stop Loss Hit Already")
                                else:
                                    if orders.upper() == "YES" or orders.upper() == "":  
                                        for credi in cred:
                                            order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                            print("Call Stop Loss Hit")
                                            sell_lst.append(scpt_code)
                            if typee == "PE" and lt_spt > slll:
                                if scpt_code in sell_lst: 
                                    print(str(scpt_code)+" Put Stop Loss Already")
                                else:
                                    if orders.upper() == "YES" or orders.upper() == "":  
                                        for credi in cred:
                                            order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                            print("Put Stop Loss Hit")
                                            sell_lst.append(scpt_code)
                #print("2")   
                if mtomm is not None:  
                    #print("21")
                    if tgtt is not None:
                        #print("22")
                        if float(mtomm) > 0 or float(mtomm) < 0:
                            #print("23")
                            if typee == "CE" and lt_spt > tgtt:
                                #print("24")
                                if scpt_code in sell_lst: 
                                    #print("25")
                                    print(str(scpt_code)+" Call Target Hit Already ")
                                else:
                                    #print("26")
                                    if orders.upper() == "YES" or orders.upper() == "":  
                                        #print("27")
                                        ide = idx+2
                                        print(ide)
                                            #dt.range(f"a1:d1").value
                                        dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
                                        #for credi in cred:
                                            #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                        print("Call Target Hit")
                                        #print("28")
                                        sell_lst.append(scpt_code)
                                        #print("29")
                            if typee == "PE" and lt_spt < tgtt:
                                #print("30")
                                if scpt_code in sell_lst: 
                                    #print("31")
                                    print(str(scpt_code)+" Put Target Hit Already")
                                else:
                                    #print("32")
                                    if orders.upper() == "YES" or orders.upper() == "":  
                                        #print("33")
                                        #for credi in cred:
                                            # print("34")
                                        
                                        ide = idx+2
                                        print(ide)
                                            #dt.range(f"a1:d1").value
                                        dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
                                            #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                        print("Put Target Hit")
                                        #print("35")
                                        sell_lst.append(scpt_code)
                                        #print("36")

                #print("3")    
            except Exception as e:
                print(e)            
        idx += 1
    # dt.range(f"w2:w15").value = ''
    # dt.range(f"x2:x15").value = ''
    dt.range("y2").value = '=IF(T2="","",IF(AND(E2="CE",H2>T2),"Buy",IF(AND(E2="PE",H2<T2),"Buy","")))'  
    dt.range("v2").value = '=IF(H2="","",IF(E2="CE",(H2-H2*0.2%)+1,IF(E2="PE",(H2+H2*0.2%)-1,"")))'    
    scpt_list = []
    scpt_listtt = []

    