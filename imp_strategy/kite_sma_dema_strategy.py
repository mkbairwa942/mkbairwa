
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
#from five_paisa1 import *
from kite_trade_main import *
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
users = ["MUKESH"]#,"ASHWIN","ALPESH"]
credi_har = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_har is None:# and credi_ash is None and credi_alp is None:
        try:
            for us in users:
                print("1")
                if us == "MUKESH":
                    credi_har = credentials("MUKESH")
                    if credi_har.request_token is None:
                        credi_har = credentials("MUKESH")
                        print(credi_har.request_token)
                # if us == "ASHWIN":
                #     credi_ash = credentials("ASHWIN")
                #     if credi_ash.request_token is None:
                #         credi_ash = credentials("ASHWIN")
                #         print(credi_ash.request_token)
                # if us == "ALPESH":
                #     credi_alp = credentials("ALPESH")
                #     if credi_alp.request_token is None:
                #         credi_alp = credentials("ALPESH")
                #         print(credi_alp.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_har]#,credi_ash,credi_alp]
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

if not os.path.exists("kite_sma_dema_strategy.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("kite_sma_dema_strategy.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('kite_sma_dema_strategy.xlsx')
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
            
            root_list = ["BANKNIFTY","NIFTY"]

            exc_new = exch['Root'].isin(root_list)
            
            exc_new1 = exch[exc_new]
            eq_exc = exc_new1[(exc_new1["Exch"] == "N") & (exc_new1["ExchType"] == "C") & (exc_new1["CpType"] == "EQ")]
            exc.range("a1").options(index=False).value = eq_exc
            Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
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
stk_list = [999920005,999920000]

telegram_msg = "yes"
orders = "yes"
Capital = 20000
StockPriceLessThan = 1000
Buy_price_buffer = 2
Vol_per = 15
UP_Rsi_lvl = 60
DN_Rsi_lvl = 40
adx_parameter = 0.40
sam_21_slop = 1.5
dema_21_slope = 2
slll = -600
tgtt = 1200
lotsize = 2

SLL = 10
TSL = 10
tsl1 = 1-(TSL/100)
print(tsl1)

def order_book_func(cred):
    try:
        ordbook = pd.DataFrame(cred.order_book())
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
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot','ExchOrderID','OrderStatus', 'OrderValidUpto','ScripName','Root','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            pos.range("a1").options(index=False).value = ordbook1
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,namee,stk_name):
    timees = list_to_append
    dfg4 = df.tail(1)
    if stk_name == "BANKNIFTY":
        lotsize = 3
    if stk_name == "NIFTY":
        lotsize = 2
    quantity = (qtyy*lotsize)
    # print(stk_name)
    # print(quantity)
    # dfg3 = df
    # dfg3 = dfg3.astype({"Datetime": "datetime64"})   
    
    # dfg3['Entry_Date'] = timees
    # dfg3['OK_DF'] = np.where(dfg3['Entry_Date'] == dfg3['Datetime'],"OK","")
    # dfg4 = dfg3[(dfg3["OK_DF"] == "OK")]
    # print(timees)
    # print(dfg4)
    if dfg4.empty:
        print("No Data")
    else:
        if order_side == "B":
            price_of_stoc = float(dfg4['Close'])
            # buff = (price_of_stoc*Buy_price_buffer)/100
            # price_of_stock = round((price_of_stoc+buff),1)
            # print(price_of_stoc)
            # print(buff)
            # print(price_of_stock)
            price_of_stock = price_of_stoc
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
                order = credi.place_order(OrderType=order_side,Exchange='N',ExchangeType='D', ScripCode = scrip_code, Qty=quantity,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
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
    df['Name'] = np.where(stk_nm == 999920005,"BANKNIFTY",np.where(stk_nm == 999920000,"NIFTY",""))
    df['Price_break'] = np.where((df['Close'] > (df.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((df['Close'] < (df.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    df['Vol_break'] = np.where(df['Volume'] > (df.Volume.rolling(5).mean() * vol_pr).shift(-5),
                                        "Vol_brk","") 
    df['SMA_21'] = np.round((pta.sma(df['Close'],length=21)),2)
    df['DEMA_21'] = np.round((pta.dema(df['Close'],length=21)),2)
    ADX = pta.adx(high=df['High'],low=df['Low'],close=df['Close'],length=14)
    df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)
    df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
    df['Rsi_OK'] = np.where((df["RSI_14"].shift(-1)) > rsi_up_lvll,"Rsi_Up_OK",np.where((df["RSI_14"].shift(-1)) < rsi_dn_lvll,"Rsi_Dn_OK",""))
    df['Adx_diff'] = df['ADX_14'] - df['ADX_14'].shift(1)
    df['Adx_ok'] = np.where(df['Adx_diff'] > adx_parameter,"ok","")
    df['SMA_21_diff'] = df['SMA_21'] - df['SMA_21'].shift(1)
    df['DEMA_21_diff'] = df['DEMA_21'] - df['DEMA_21'].shift(1)     
    df['SMA_21_ok'] = np.where(df['SMA_21_diff'] > sam_21_slop,"up_ok",np.where(df['SMA_21_diff'] < -sam_21_slop,"dn_ok",""))
    df['DEMA_21_ok'] = np.where(df['DEMA_21_diff'] > dema_21_slope,"up_ok",np.where(df['DEMA_21_diff'] < -dema_21_slope,"dn_ok",""))
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
    #print("Position is Empty")
    buy_order_list_dummy = []
    sell_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order = order_book_func(credi_har)
    buy_order_li = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Fully Executed')]
    exit_order_li = buy_order[(buy_order['BuySell'] == 'S') & (buy_order['OrderStatus'] == 'Fully Executed')]
    buy_order_list_dummy = (np.unique([str(i) for i in buy_order_li['Datetimeee']])).tolist()
    sell_order_list_dummy = (np.unique([str(i) for i in exit_order_li['Datetimeee']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()

while True:
    # print(buy_order_list_dummy)
    # print(sell_order_list_dummy)
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()

    for credi in cred:        
        if posit.empty:
            pass
        else:
            buy_order = order_book_func(credi)
            buy_order_li1 = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Pending')]
            if buy_order_li1.empty:
                pass
            else:
                exc_order_id = (np.unique([int(i) for i in buy_order_li1['ExchOrderID']])).tolist()[0] 
                print(exc_order_id)
                cancel_bulk=[{"ExchOrderID": f"{exc_order_id}"}]
                credi.cancel_bulk_order(cancel_bulk)
                buy_order_list_dummy = []

    try:      
        for sc in stk_list:
            dfg1 = data_download(sc,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl) 
            stk_name = (np.unique([str(i) for i in dfg1['Name']])).tolist()[0] 
            print(stk_name)
            #print(ADX(dfg1))
            dfg1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
            dfg111 = dfg1[(dfg1["Date"] == current_trading_day.date())]
            dfg1112 = dfg111.tail(10)
            five_df1 = pd.concat([dfg1112, five_df1]) 


            Call_by_df = dfg1[(dfg1["Signal"] == "Call_Buy")]
            Call_by_df['Date_Dif'] = abs((Call_by_df["Datetime"] - Call_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Call_by_df['Entry'] = np.where(Call_by_df['Date_Dif'] > 5, "Call_Buy","")
            Call_by_df1 = Call_by_df[(Call_by_df['Entry'] == "Call_Buy")]
            Call_by_df1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)           
            five_df2 = pd.concat([Call_by_df1, five_df2])
            
            Call_by_df2 = Call_by_df1[(Call_by_df1["Date"] == current_trading_day.date()) & (Call_by_df1["Minutes"] < 5 )]   

            if Call_by_df2.empty:
                pass
                #print("Call Buy DF Empty")
            else:
                Call_by_ord = Call_by_df2.tail(1)
                Call_by_Closee = (float(Call_by_ord['Close']))
                Call_by_Spot = round(Call_by_Closee/100,0)*100
                Call_by_time = str(list(Call_by_ord['Datetime'])[0])
                Call_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Call_by_ord2 = Call_by_ord1[(Call_by_ord1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
                Expiryyy_Call_by = (np.unique(Call_by_ord2['Expiry']).tolist())[0]      
                Call_by_ord3 = Call_by_ord2[Call_by_ord2['Expiry'] == Expiryyy_Call_by]
                Call_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Call_by_ord4 = Call_by_ord3[(Call_by_ord3["CpType"] == 'CE')] 
                Call_by_ord5 = Call_by_ord4[(Call_by_ord4['StrikeRate'] < Call_by_Spot)] 
                Call_by_ord6 = Call_by_ord5.tail(1)
                Call_by_Name = np.unique([str(i) for i in Call_by_ord6['Name']]).tolist()[0]
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
                        rde_exec = order_execution(dfg1_Call_by,buy_order_list_dummy,Call_by_time,telegram_msg,orders,"IDX OPT","CALL BUY","B",Call_by_Scripcodee,Call_by_Qtyy,Call_by_Name,stk_name)
                    
            Put_by_df = dfg1[(dfg1["Signal1"] == "Put_Buy")]
            Put_by_df['Date_Dif'] = abs((Put_by_df["Datetime"] - Put_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
            Put_by_df['Entry'] = np.where(Put_by_df['Date_Dif'] > 5, "Put_Buy","")
            Put_by_df1 = Put_by_df[Put_by_df['Entry'] == "Put_Buy"]
            Put_by_df1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True) 
            five_df3 = pd.concat([Put_by_df1, five_df3]) 

            Put_by_df2 = Put_by_df1[(Put_by_df1["Date"] == current_trading_day.date()) & (Put_by_df1["Minutes"] < 5 )]          
            if Put_by_df2.empty:
                pass
                #print("Put Buy DF Empty")
            else:   
                Put_by_ord = Put_by_df2.tail(1)
                Put_by_Closee = (float(Put_by_ord['Close']))
                Put_by_Spot = round(Put_by_Closee/100,0)*100
                Put_by_time = str(list(Put_by_ord['Datetime'])[0])
                Put_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
                Put_by_ord2 = Put_by_ord1[(Put_by_ord1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
                Expiryyy_Put_by = (np.unique(Put_by_ord2['Expiry']).tolist())[0]  
                Put_by_ord3 = Put_by_ord2[Put_by_ord2['Expiry'] == Expiryyy_Put_by]
                Put_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
                Put_by_ord4 = Put_by_ord3[(Put_by_ord3["CpType"] == 'PE')] 
                Put_by_ord5 = Put_by_ord4[(Put_by_ord4['StrikeRate'] > Put_by_Spot)] 
                Put_by_ord6 = Put_by_ord5.head(1)    
                Put_by_Name = np.unique([str(i) for i in Put_by_ord6['Name']]).tolist()[0]  
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
                        rde_exec = order_execution(dfg1_Put_by,buy_order_list_dummy,Put_by_time,telegram_msg,orders,"IDX OPT","PUT BUY","B",Put_by_Scripcodee,Put_by_Qtyy,Put_by_Name,stk_name)

            posi = pd.DataFrame(credi_har.positions()) 
            if posi.empty:            
                print("No Current Running Position")
            else:
                posit = posi[(posi['MTOM'] != 0)]            
                pl = (np.unique([int(i) for i in posit['MTOM']])).tolist()[0]
                if pl < -600 or pl > 1200:
                    Buy_Qty1 = posit['BuyQty'] - posit['SellQty']
                    order = credi_har.place_order(OrderType='S',Exchange=list(posit['Exch'])[0],ExchangeType=list(posit['ExchType'])[0], ScripCode = int(posit['ScripCode']), Qty=int(posit['BuyQty'])-int(posit['SellQty']),Price=float(posit['LTP']),IsIntraday=True if list(posit['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    print("StopLoss is Greater than -600")
                    print("Sell stoplOSS order Executed")
                else:
                    posit3 = (np.unique([int(i) for i in posit['ScripCode']])).tolist()  
                    buy_order_li = order_book_func(credi_har)             
                    for ord in posit3:
                        buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B')]# & (buy_order_li['AveragePrice'] != 0)]
                        buy_order_liiist = buy_order_liiist[['Datetimeee','ScripCode']] 
                        new_df11 = posit[(posit['ScripCode'] == ord)]
                        new_df1 = pd.merge(buy_order_liiist, new_df11, on=['ScripCode'], how='inner')
                        Buy_Name = list(new_df1['ScripName'])[0]
                        Buy_price = (np.unique([float(i) for i in new_df1['BuyAvgRate']])).tolist()[0]    
                        Buy_Stop_Loss = (round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*SLL)/100),1)).astype(float)
                        Buy_Target = (round((((new_df1['BuyAvgRate']*SLL)/100) + new_df1['BuyAvgRate']),1)).astype(float)
                        Buy_Exc = list(new_df1['Exch'])[0]
                        Buy_Exc_Type = list(new_df1['ExchType'])[0]
                        Buy_Qty = new_df1['BuyQty'] - new_df1['SellQty']
                        Buy_timee = list(new_df1['Datetimeee'])[0]
                        Buy_timee1 = str(Buy_timee).replace(' ','T')  
                        
                        dfg1 = credi_har.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
                        #print(dfg1.head(1))
                        dfg1['ScripCode'] = ord
                        dfg1['ScripName'] = Buy_Name
                        dfg1['Entry_Date'] = Buy_timee1
                        dfg1['Entry_Price'] = Buy_price
                        
                        dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                        dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                        
                        dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                        dfg2['StopLoss'] = round((dfg2['Entry_Price'] - (dfg2['Entry_Price']*SLL)/100),1)

                        dfg2['Benchmark'] = dfg2['High'].cummax()
                        dfg2['TStopLoss'] = dfg2['Benchmark'] * tsl1  
                        dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < dfg2['StopLoss'],"SL",""))
    
                        five_df4 = pd.concat([dfg2, five_df4])
                        dfg3 = dfg2[(dfg2["Status"] == "TSL") | (dfg2["Status"] == "SL")]                       

                        if dfg3.empty:
                            dfg3 = dfg2.tail(1)
                            
                        dfg22 = dfg3.head(1)

                        final_df = pd.merge(posit,dfg22, on=['ScripCode'], how='inner')  
                        final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                        final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TSL")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                    
                        final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                        final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                        final_df.sort_values(['Entry_Date'], ascending=[True], inplace=True)
                        five_df5 = pd.concat([final_df, five_df5])
                        
                        order_dff = final_df[(final_df['Exit'] == 'SELL')]

                        if order_dff.empty:
                            print("No Target And Stoploss Hit")
                        else:
                            try: 
                                buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B')]# & (buy_order_li['AveragePrice'] != 0)]
                                #print(buy_order_liiist)
                                order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])
                                for ordd in order_dff_Scpt:
                                    order_df = order_dff[(order_dff['ScripCode'] == ordd)]
                                    order = credi_har.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Sell order Executed") 
                            except Exception as e:
                                print(e)
    except Exception as e:
        print(e) 
    
        print("------------------------------------------------") 

    try:
        if five_df1.empty:
            pass
        else:
            try:
                st.range("a1").options(index=False).value = five_df1 
            except Exception as e:
                print(e)

        if five_df2.empty:
            pass
        else:
            try:
                by.range("a1").options(index=False).value = five_df2
            except Exception as e:
                print(e)

        if five_df3.empty:
            pass
        else:
            try:
                by.range("a50").options(index=False).value = five_df3
            except Exception as e:
                print(e)
        
        if five_df4.empty:
            pass
        else:
            try:
                fl_data.range("a1").options(index=False).value = five_df4
            except Exception as e:
                print(e)
        
        if five_df5.empty:
            pass
        else:
            try:
                st1.range("a1").options(index=False).value = five_df5
            except Exception as e:
                print(e)

    except Exception as e:
        print(e) 
