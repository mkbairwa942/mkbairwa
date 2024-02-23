
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
credi_har = credentials("HARESH")
credi_ash = credentials("ASHWIN")
cred = [credi_har,credi_ash]
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

if not os.path.exists("haresh_trending.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("haresh_trending.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('haresh_trending.xlsx')
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
# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

exchange = None
while True:    
    if exchange is None: 
        try:
            exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
            exch.sort_values(['Root'], ascending=[True], inplace=True)
            
            root_list = np.unique(exch['Root']).tolist()

            
            root_list = ["BANKNIFTY"]

            exc_new = exch['Root'].isin(root_list)
            
            exc_new1 = exch[exc_new]
            eq_exc = exc_new1[(exc_new1["Exch"] == "N") & (exc_new1["ExchType"] == "C") & (exc_new1["CpType"] == "EQ")]
            exc.range("a1").options(index=False).value = eq_exc
            Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
            Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
            exc_new2 = Expiry
            exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

            break
        except:
            print("Exchange Download Error....")
            time.sleep(5)

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = exc_new2

#symbol1 = '999920005'
stk_list = [999920005]


telegram_msg = "YES"
orders = "YES"
Capital = 20000
StockPriceLessThan = 1000
Buy_price_buffer = 0.1
Vol_per = 15
UP_Rsi_lvl = 60
DN_Rsi_lvl = 40
SLL = 1
TSL = 1
tsl1 = 1-(TSL/100)
print(tsl1)


def order_book_func():
    try:
        ordbook = pd.DataFrame(credi_har.order_book())
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
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M')
                d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]))
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

def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,namee):
    timees = list_to_append
    dfg3 = df
    dfg3 = dfg3.astype({"Datetime": "datetime64"})   
    
    dfg3['Entry_Date'] = timees
    dfg3['OK_DF'] = np.where(dfg3['Entry_Date'] == dfg3['Datetime'],"OK","")
    dfg4 = dfg3[(dfg3["OK_DF"] == "OK")]
    print(timees)
    print(dfg4)
    if dfg4.empty:
        print("No Data")
    else:
        price_of_stock = float(dfg4['Close']) 
        # timee = str((dfg3['Datetime'].values)[0])[0:19] 
        # timee1= timee.replace("T", " " )
        print("1")
        list_append_on.append(list_to_append)

        if orders.upper() == "YES" or orders.upper() == "":  
            for credi in cred:
                #postt = pd.DataFrame(credi.margin())['Ledgerbalance'][0]
                #print(f"Ledger Balance is : {postt}") 
                order = credi.place_order(OrderType=order_side,Exchange='N',ExchangeType='D', ScripCode = scrip_code, Qty=qtyy,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        else:
            print(f"Real {CALL_PUT} Order are OFF")
        print(f"1 Minute {CALL_PUT} Data Selected of "+str(namee)+" ("+str(scrip_code)+")")
        print(f"{CALL_PUT} {BUY_EXIT} Order Executed of "+str(namee)+" at : Rs "+str(price_of_stock)+" and Quantity is "+str(qtyy)+" on "+str(timees))

        print("SYMBOL : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timees))
        if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
            parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timees)}
            resp = requests.get(telegram_basr_url, data=parameters1)
        else:
            print("Telegram Message are OFF")
        print("----------------------------------------")

def data_download(stk_nm,vol_pr,rsi_up_lvll,rsi_dn_lvll):
    df = credi_har.historical_data('N', 'C', stk_nm, '5m', second_last_trading_day,current_trading_day)
    #print(df.head(1))
    df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
    df = df.astype({"Datetime": "datetime64"})
    #df['Scripcode'] = int(symbol1)
    df['Name'] = 'BANKNIFTY'
    df['Price_break'] = np.where((df['Close'] > (df.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((df['Close'] < (df.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    df['Vol_break'] = np.where(df['Volume'] > (df.Volume.rolling(5).mean() * vol_pr).shift(-5),
                                        "Vol_brk","") 
    df['SMA_21'] = np.round((pta.sma(df['Close'],length=21)),2)
    df['DEMA_21'] = np.round((pta.dema(df['Close'],length=21)),2)
    ADX = pta.adx(high=df['High'],low=df['Low'],close=df['High'],length=14)
    df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)
    df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
    df['Rsi_OK'] = np.where((df["RSI_14"].shift(-1)) > rsi_up_lvll,"Rsi_Up_OK",np.where((df["RSI_14"].shift(-1)) < rsi_dn_lvll,"Rsi_Dn_OK",""))
    df['Adx_diff'] = df['ADX_14'] - df['ADX_14'].shift(1)
    df['Adx_ok'] = np.where(df['Adx_diff'] > adx_parameter,"ok","")
    df['SMA_21_diff'] = df['SMA_21'] - df['SMA_21'].shift(1)
    df['DEMA_21_diff'] = df['DEMA_21'] - df['DEMA_21'].shift(1)
    df['SMA_21_ok'] = np.where(df['SMA_21_diff'] > 2,"up_ok",np.where(df['SMA_21_diff'] < -2,"dn_ok",""))
    df['DEMA_21_ok'] = np.where(df['DEMA_21_diff'] > 2,"up_ok",np.where(df['DEMA_21_diff'] < -2,"dn_ok",""))
    #df['SMA_21_ok1'] = np.where((df['SMA_21']) > (df['SMA_21'].shift(1)),"up_ok",np.where((df['SMA_21']) < (df['SMA_21'].shift(1)),"dn_ok",""))
    #df['DEMA_21_ok1'] = np.where((df['DEMA_21']) > (df['DEMA_21'].shift(1)),"up_ok",np.where((df['DEMA_21']) < (df['DEMA_21'].shift(1)),"dn_ok",""))
    df['CROSS'] = np.where(df['DEMA_21'] > df['SMA_21'],"up_ok",np.where(df['DEMA_21'] < df['SMA_21'],"dn_ok",""))
    df['Signal'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "up_ok") & (df['DEMA_21_ok'] == "up_ok") & (df['CROSS'] == "up_ok"),"Call_Buy","Call_Exit")
    df['Signal1'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "dn_ok") & (df['DEMA_21_ok'] == "dn_ok") & (df['CROSS'] == "dn_ok"),"Put_Buy","Put_Exit")
    df['Cand_Col'] = np.where(df['Close'] > df['Open'],"Green",np.where(df['Close'] < df['Open'],"Red","") ) 
    df['TimeNow'] = datetime.now()
    df = df.astype({"Datetime": "datetime64[ns]"})    
    df["Date"] = df["Datetime"].dt.date
    df['Minutes'] = df['TimeNow']-df["Datetime"]
    df['Minutes'] = round((df['Minutes']/np.timedelta64(1,'m')),2) 
    df.sort_values(['Datetime'], ascending=[True], inplace=True)
    return df

posit = pd.DataFrame(credi_har.positions()) 
if posit.empty:
    print("Position is Empty")
    buy_order_list_dummy = []
    sell_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order = order_book_func()
    buy_order_li = buy_order[buy_order['BuySell'] == 'B']
    exit_order_li = buy_order[buy_order['BuySell'] == 'S']
    buy_order_list_dummy = (np.unique([str(i) for i in buy_order_li['Datetimeee']])).tolist()
    sell_order_list_dummy = (np.unique([str(i) for i in exit_order_li['Datetimeee']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()

adx_parameter = 0.60
sll = -300
while True:
    if posit.empty:
        print("Position is Empty")
    else:
        positt = posit[(posit['MTOM'] != 0)]
        stop_loss = posit[(posit['MTOM'] <= sll)]
        if orders.upper() == "YES" or orders.upper() == "": 
            if stop_loss.empty:
                print("NO Loss Less than -300")
            else:
                scrip_code1 = int(float(stop_loss['ScripCode'])) 
                qtyy1 = int(np.unique(stop_loss['BuyQty']))
                price_of_stock1 = float(stop_loss['LTP'])  
                for credi in cred:
                    # postt = pd.DataFrame(credi.margin())['Ledgerbalance'][0]
                    # print(f"Ledger Balance is : {postt}")            
                    order = credi.place_order(OrderType="S",Exchange='N',ExchangeType='D', ScripCode = scrip_code1, Qty=qtyy1,Price=price_of_stock1, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
    print(buy_order_list_dummy)
    print(sell_order_list_dummy)
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()
    five_df7 = pd.DataFrame()
    five_df8 = pd.DataFrame()
    five_df9 = pd.DataFrame()
    five_df10 = pd.DataFrame()
    final_df_call = pd.DataFrame()
    final_df_Put = pd.DataFrame()
    
    for sc in stk_list:
        try:
            print(sc)
            dfg1 = data_download(sc,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl) 
            stk_name = (np.unique([str(i) for i in dfg1['Name']])).tolist()[0] 
            dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)
            five_df1 = pd.concat([dfg1, five_df1]) 

            Call_by_df = dfg1[(dfg1["Signal"] == "Call_Buy")]
            Call_by_df['Date_Dif'] = abs((Call_by_df["Datetime"] - Call_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Call_by_df['Entry'] = np.where(Call_by_df['Date_Dif'] > 5, "Call_Buy","")
            Call_by_df1 = Call_by_df[(Call_by_df['Entry'] == "Call_Buy")]
            Call_by_df1.sort_values(['Datetime'], ascending=[True], inplace=True)            
            five_df2 = pd.concat([Call_by_df1, five_df2])
            
            Call_by_df2 = Call_by_df1[(Call_by_df1["Date"] == current_trading_day.date()) & (Call_by_df1["Minutes"] < 5 )]          
 
            if Call_by_df2.empty:
                print("Call Buy DF Empty")
            else:                  
                Call_by_ord = Call_by_df2.tail(1)
                Call_by_Closee = (float(Call_by_ord['Close']))
                Call_by_Spot = round(Call_by_Closee/100,0)*100
                Call_by_time = str(list(Call_by_ord['Datetime'])[0])
                Call_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Call_by_ord2 = Call_by_ord1[(Call_by_ord1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
                Expiryyy_Call_by = (np.unique(Call_by_ord2['Expiry']).tolist())[0]      
                Call_by_ord3 = Call_by_ord2[Call_by_ord2['Expiry'] == Expiryyy_Call_by]
                Call_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Call_by_ord4 = Call_by_ord3[(Call_by_ord3["CpType"] == 'CE')] 
                Call_by_ord5 = Call_by_ord4[(Call_by_ord4['StrikeRate'] < Call_by_Spot)] 
                Call_by_ord6 = Call_by_ord5.tail(1)
                Call_by_Scripcodee = int(float(Call_by_ord6['Scripcode']))
                Call_by_Qtyy = int(np.unique(Call_by_ord6['LotSize']))

                print(Call_by_Scripcodee,Call_by_Qtyy,Call_by_time)
                #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
                if not Call_by_ord6.empty:                    
                    dfg1_Call_by = credi_har.historical_data('N', 'D', Call_by_Scripcodee, '1m', second_last_trading_day,current_trading_day)
                    if Call_by_time in buy_order_list_dummy: 
                        print(str(stk_name)+" Call is Already Buy")
                        print("----------------------------------------")
                    else:
                        print("Call Buy")                        
                        rde_exec = order_execution(dfg1_Call_by,buy_order_list_dummy,Call_by_time,telegram_msg,orders,"IDX OPT","CALL BUY","B",Call_by_Scripcodee,Call_by_Qtyy,stk_name)
                       
            Put_by_df = dfg1[(dfg1["Signal1"] == "Put_Buy")]
            Put_by_df['Date_Dif'] = abs((Put_by_df["Datetime"] - Put_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Put_by_df['Entry'] = np.where(Put_by_df['Date_Dif'] > 5, "Put_Buy","")
            Put_by_df1 = Put_by_df[Put_by_df['Entry'] == "Put_Buy"]
            Put_by_df1.sort_values(['Datetime'], ascending=[True], inplace=True)
            five_df3 = pd.concat([Put_by_df1, five_df3]) 

            Put_by_df2 = Put_by_df1[(Put_by_df1["Date"] == current_trading_day.date()) & (Put_by_df1["Minutes"] < 5 )]          

            if Put_by_df2.empty:
                print("Put Buy DF Empty")
            else:                
                Put_by_ord = Put_by_df2.tail(1)
                Put_by_Closee = (float(Put_by_ord['Close']))
                Put_by_Spot = round(Put_by_Closee/100,0)*100
                Put_by_time = str(list(Put_by_ord['Datetime'])[0])
                Put_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Put_by_ord2 = Put_by_ord1[(Put_by_ord1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
                Expiryyy_Put_by = (np.unique(Put_by_ord2['Expiry']).tolist())[0]  
                Put_by_ord3 = Put_by_ord2[Put_by_ord2['Expiry'] == Expiryyy_Put_by]
                Put_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Put_by_ord4 = Put_by_ord3[(Put_by_ord3["CpType"] == 'PE')] 
                Put_by_ord5 = Put_by_ord4[(Put_by_ord4['StrikeRate'] > Put_by_Spot)] 
                Put_by_ord6 = Put_by_ord5.head(1)      
                Put_by_Scripcodee = int(float(Put_by_ord6['Scripcode']))
                Put_by_Qtyy = int(np.unique(Put_by_ord6['LotSize']))
                
                print(Put_by_Scripcodee,Put_by_Qtyy,Put_by_time)
                #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
                if not Put_by_ord6.empty:
                    dfg1_Put_by = credi_har.historical_data('N', 'D', Put_by_Scripcodee, '1m', second_last_trading_day,current_trading_day)
                    if Put_by_time in buy_order_list_dummy: 
                        print(str(stk_name)+" Put is Already Buy")
                        print("----------------------------------------")
                    else:
                        print("Put Buy")                        
                        rde_exec = order_execution(dfg1_Put_by,buy_order_list_dummy,Put_by_time,telegram_msg,orders,"IDX OPT","PUT BUY","B",Put_by_Scripcodee,Put_by_Qtyy,stk_name)

            Call_sl_df = dfg1[(dfg1["Signal"] == "Call_Exit")]
            Call_sl_df['Date_Dif'] = abs((Call_sl_df["Datetime"] - Call_sl_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Call_sl_df['Entry'] = np.where(Call_sl_df['Date_Dif'] > 5, "Call_Exit","")
            Call_sl_df1 = Call_sl_df[Call_sl_df['Entry'] == "Call_Exit"]
            Call_sl_df1.sort_values(['Datetime'], ascending=[True], inplace=True)
            five_df4 = pd.concat([Call_sl_df1, five_df4]) 

            Call_sl_df2 = Call_sl_df1[(Call_sl_df1["Date"] == current_trading_day.date()) & (Call_sl_df1["Minutes"] < 5 )]          
 
            if Call_sl_df2.empty:
                print("Call DF Empty")
            else:                  
                Call_sl_ord = Call_sl_df2.tail(1)
                Call_sl_Closee = (float(Call_sl_ord['Close']))
                Call_sl_Spot = round(Call_sl_Closee/100,0)*100
                Call_sl_time = str(list(Call_sl_ord['Datetime'])[0])
                Call_sl_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Call_sl_ord2 = Call_sl_ord1[(Call_sl_ord1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
                Expiryyy_Call_sl = (np.unique(Call_sl_ord2['Expiry']).tolist())[0]      
                Call_sl_ord3 = Call_sl_ord2[Call_sl_ord2['Expiry'] == Expiryyy_Call_sl]
                Call_sl_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Call_sl_ord4 = Call_sl_ord3[(Call_sl_ord3["CpType"] == 'CE')] 
                Call_sl_ord5 = Call_sl_ord4[(Call_sl_ord4['StrikeRate'] < Call_sl_Spot)] 
                Call_sl_ord6 = Call_sl_ord5.tail(1)
                
                #Call_sl_Scripcodee = int(float(Call_sl_ord6['Scripcode']))
                Call_sl_Scripcodee = int(float(positt['ScripCode']))
                Call_sl_Qtyy = int(np.unique(Call_sl_ord6['LotSize']))
                
                

                print(Call_sl_Scripcodee,Call_sl_Qtyy,Call_sl_time)
                #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
                if not Call_sl_ord6.empty:                    
                    dfg1_Call_sl = credi_har.historical_data('N', 'D', Call_sl_Scripcodee, '1m', second_last_trading_day,current_trading_day)
                    if Call_sl_time in sell_order_list_dummy: 
                        print(str(stk_name)+" Call is Already Exit")
                        print("----------------------------------------")
                    else:
                        print("Call Exit")                        
                        rde_exec = order_execution(dfg1_Call_sl,sell_order_list_dummy,Call_sl_time,telegram_msg,orders,"IDX OPT","CALL EXIT","S",Call_sl_Scripcodee,Call_sl_Qtyy,stk_name)
                       
            Put_sl_df = dfg1[(dfg1["Signal1"] == "Put_Exit")]
            Put_sl_df['Date_Dif'] = abs((Put_sl_df["Datetime"] - Put_sl_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Put_sl_df['Entry'] = np.where(Put_sl_df['Date_Dif'] > 5, "Put_Exit","")
            Put_sl_df1 = Put_sl_df[Put_sl_df['Entry'] == "Put_Exit"]
            Put_sl_df1.sort_values(['Datetime'], ascending=[True], inplace=True)
            five_df5 = pd.concat([Put_sl_df1, five_df5]) 

            Put_sl_df2 = Put_sl_df1[(Put_sl_df1["Date"] == current_trading_day.date()) & (Put_sl_df1["Minutes"] < 5 )]          
 
            if Put_sl_df2.empty:
                print("Put DF Empty")
            else:                  
                Put_sl_ord = Put_sl_df2.tail(1)
                Put_sl_Closee = (float(Put_sl_ord['Close']))
                Put_sl_Spot = round(Put_sl_Closee/100,0)*100
                Put_sl_time = str(list(Put_sl_ord['Datetime'])[0])
                Put_sl_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Put_sl_ord2 = Put_sl_ord1[(Put_sl_ord1['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
                Expiryyy_Put_sl = (np.unique(Put_sl_ord2['Expiry']).tolist())[0]      
                Put_sl_ord3 = Put_sl_ord2[Put_sl_ord2['Expiry'] == Expiryyy_Put_sl]
                Put_sl_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Put_sl_ord4 = Put_sl_ord3[(Put_sl_ord3["CpType"] == 'PE')] 
                Put_sl_ord5 = Put_sl_ord4[(Put_sl_ord4['StrikeRate'] > Put_sl_Spot)] 
                Put_sl_ord6 = Put_sl_ord5.head(1)
                #Put_sl_Scripcodee = int(float(Put_sl_ord6['Scripcode']))
                Put_sl_Scripcodee = int(float(positt['ScripCode']))
                Put_sl_Qtyy = int(np.unique(Put_sl_ord6['LotSize']))

                print(Put_sl_Scripcodee,Put_sl_Qtyy,Put_sl_time)
                #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
                if not Put_sl_ord6.empty:
                    dfg1_Put_sl = credi_har.historical_data('N', 'D', Put_sl_Scripcodee, '1m', second_last_trading_day,current_trading_day)
                    if Put_sl_time in sell_order_list_dummy: 
                        print(str(stk_name)+" Put is Already Exit")
                        print("----------------------------------------")
                    else:
                        print("Put Exit")                        
                        rde_exec = order_execution(dfg1_Put_sl,sell_order_list_dummy,Put_sl_time,telegram_msg,orders,"IDX OPT","PUT EXIT","S",Put_sl_Scripcodee,Put_sl_Qtyy,stk_name)

            try:
                final_call = pd.concat([Call_by_df1, Call_sl_df1])
                final_call.sort_values(['Datetime'], ascending=[True], inplace=True)
                five_df6 = pd.concat([final_call, five_df6]) 

                final_Put = pd.concat([Put_by_df1, Put_sl_df1])
                final_Put.sort_values(['Datetime'], ascending=[True], inplace=True)
                five_df7 = pd.concat([final_Put, five_df7]) 

                listo_call = np.unique(final_call['Datetime'])
                listo_Put = np.unique(final_Put['Datetime'])

                position_Call = 0
                position_Put = 0

                for i in listo_call:
                    f_df_call = final_call[final_call['Datetime'] == i]
                    if list(f_df_call['Entry'])[0] == 'Call_Buy' and position_Call == 0:
                        final_df_call = pd.concat([f_df_call, final_df_call])
                        position_Call = 1

                    if list(f_df_call['Entry'])[0] == 'Call_Exit' and position_Call == 1:
                        final_df_call = pd.concat([f_df_call, final_df_call])
                        position_Call = 0

                for i in listo_Put:
                    f_df_put = final_Put[final_Put['Datetime'] == i]
                    if list(f_df_put['Entry'])[0] == 'Put_Buy' and position_Put == 0:
                        final_df_Put = pd.concat([f_df_put, final_df_Put])
                        position_Put = 1

                    if list(f_df_put['Entry'])[0] == 'Put_Exit' and position_Put == 1:
                        final_df_Put = pd.concat([f_df_put, final_df_Put])
                        position_Put = 0  
            except Exception as e:
                print(e)   
        
        except Exception as e:
            print(e) 

        print("------------------------------------------------") 

    try:
        if five_df1.empty:
            pass
        else:
            #df = df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            #df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
            #st.range("a:az").value = None
            st.range("a1").options(index=False).value = five_df1 

        if five_df2.empty:
            pass
        else:
            #df1_up = df1_up[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            #df1_up.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
            #by.range("a:az").value = None
            by.range("a1").options(index=False).value = five_df2

        if five_df3.empty:
            pass
        else:
            #df1_dn = df1_dn[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            #df1_dn.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
            #by.range("a:az").value = None
            by.range("a15").options(index=False).value = five_df3

        if five_df4.empty:
            pass
        else:
            #buy_exit_call_df = buy_exit_call_df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            #buy_exit_call_df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
            #sl.range("a:az").value = None
            sl.range("a1").options(index=False).value = five_df4

        if five_df5.empty:
            pass
        else:
            #buy_exit_put_df = buy_exit_put_df[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            #buy_exit_put_df.sort_values(['Datetime','Name'], ascending=[False,True], inplace=True)
            #sl.range("a:az").value = None
            sl.range("a15").options(index=False).value = five_df5

        if five_df6.empty:
            pass
        else:
            #final_df_call = final_df_call[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            # final_df_call.sort_values(['Datetime'], ascending=[True], inplace=True)
            # final_df_call['P&L'] = np.where(final_df_call['Exit'] == 'Call_Buy_Exit',final_df_call['Close']-final_df_call['Close'].shift(1),0)
            #fl_data.range("a:az").value = None
            fl_data.range("a1").options(index=False).value = five_df6

        if five_df7.empty:
            pass
        else:
            # final_df_put = final_df_put[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Date_Dif','Price_Chg','Vol_Chg','Price_break','Vol_break','Vol_Price_break','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
            # final_df_put.sort_values(['Datetime'], ascending=[True], inplace=True)
            # final_df_put['P&L'] = np.where(final_df_put['Exit'] == 'Put_Buy_Exit',final_df_put['Close'].shift(1)-final_df_put['Close'],0)
            # fl_data.range("a:az").value = None
            fl_data.range("a15").options(index=False).value = five_df7

        if final_df_call.empty:
            pass
        else:
            final_df_call.sort_values(['Datetime'], ascending=[True], inplace=True)
            final_df_call['P&L'] = np.where(final_df_call['Entry'] == 'Call_Exit',final_df_call['Close']-final_df_call['Close'].shift(1),0)
            exp.range("a1").options(index=False).value = final_df_call

        if final_df_Put.empty:
            pass
        else:
            final_df_Put.sort_values(['Datetime'], ascending=[True], inplace=True)
            final_df_Put['P&L'] = np.where(final_df_Put['Entry'] == 'Put_Exit',final_df_Put['Close'].shift(1)-final_df_Put['Close'],0)
            exp.range("a15").options(index=False).value = final_df_Put

    except Exception as e:
        print(e) 
