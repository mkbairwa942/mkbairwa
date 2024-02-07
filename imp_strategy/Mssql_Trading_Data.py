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

# operate = "YES"
# telegram_msg = "no"
# orders = "no"
# username = "ASHWIN"
# username1 = str(username)
# client = credentials(username1)

#credi_ash = credentials("ASHWIN")
credi_har = credentials("HARESH")

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
# by.range("a:x").value = None
# sl.range("a:ab").value = None
# fl.range("a:az").value = None
#exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:aj").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None


script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

#exc.range("a1").value = script_code_5paisa

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
print("Exchange Download Completed")

#exc_new = exchange2['Root'].isin(fo_stk_list)
exc_new = exchange2[(exchange2['Root'].isin(fo_stk_list))]
stk_list = np.unique(exc_new['Scripcode'])
#print(exc_new['Name'])
print(exc_new.shape[0])
stock_df = pd.DataFrame({"FNO Symbol": list(exchange1["Root"].unique())})
stock_df = stock_df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = stock_df





#buy_order_li = ordef_func()
operate = "YES"
telegram_msg = "no"
orders = "yes"
Capital = 20000
StockPriceLessThan = 1000
Vol_per = 15
UP_Rsi_lvl = 60
DN_Rsi_lvl = 40
SLL = 1
TSL = 1
tsl1 = 1-(TSL/100)
print(tsl1)

def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.Low[i]>df1.Low[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.Low[i]<df1.Low[i-1]):
            return 0
    return 1

def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.High[i]<df1.High[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.High[i]>df1.High[i-1]):
            return 0
    return 1

def ordef_func():
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

def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee):
    dfg3 = df.tail(1)
    price_of_stock = Buy_At
    timee = str((dfg3['Datetime'].values)[0])[0:19] 
    timee1= timee.replace("T", " " )
    list_append_on.append(list_to_append)
    print(order_side,scrip_code,qtyy,price_of_stock)
    if orders.upper() == "YES" or orders.upper() == "":
        if price_of_stock < StockPriceLessThan:  
            order = credi_har.place_order(OrderType=order_side,Exchange='N',ExchangeType='C', ScripCode = scrip_code, Qty=qtyy,Price=Buy_At, IsIntraday=True)
        else:
            print(f"Stock Price is Greater than {StockPriceLessThan}")
    else:
        print(f"Real {CALL_PUT} Order are OFF")
    print(f"1 Minute {CALL_PUT} Data Selected of "+str(namee)+" ("+str(scrip_code)+")")
    print(f"{CALL_PUT} {BUY_EXIT} Order Executed of "+str(namee)+" at : Rs "+str(price_of_stock)+" and Quantity is "+str(qtyy)+" on "+str(timee1))

    print("SYMBOL : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timee1))
    if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
        parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timee1)}
        resp = requests.get(telegram_basr_url, data=parameters1)
    else:
        print("Telegram Message are OFF")
    print("----------------------------------------")

def data_download(stk_nm,vol_pr,rsi_up_lvll,rsi_dn_lvll):
    # sqlquery = f"select * from dbo.Live_Data where Scripcode = {stk_nm}"
    # #print(sqlquery)
    # dfg = pd.read_sql(sql=sqlquery, con=engine)
    # dfg1 = pd.DataFrame(dfg) 
    dfg1 = credi_har.historical_data('N', 'C', stk_nm, '1m',last_trading_day,current_trading_day)
    dfg1['Scripcode'] = stk_nm
    dfg1 = pd.merge(exchange2, dfg1, on=['Scripcode'], how='inner') 
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
    #print(dfg1.head(10))                                                                                       
    dfg1['Vol_Price_break'] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"), "Vol_Pri_Up_break",np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Dwn_brk"), "Vol_Pri_Dn_break", ""))
    dfg1["Buy/Sell"] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"),
                                        "BUY", np.where((dfg1['Vol_break'] == "Vol_brk")
                                            & (dfg1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
    dfg1['Rsi_OK'] = np.where((dfg1["RSI_14"].shift(-1)) > rsi_up_lvll,"Rsi_Up_OK",np.where((dfg1["RSI_14"].shift(-1)) < rsi_dn_lvll,"Rsi_Dn_OK",""))
    dfg1['Cand_Col'] = np.where(dfg1['Close'] > dfg1['Open'],"Green",np.where(dfg1['Close'] < dfg1['Open'],"Red","") ) 
    dfg1 = dfg1.astype({"Datetime": "datetime64"})    
    dfg1["Date"] = dfg1["Datetime"].dt.date
    dfg1['Minutes'] = dfg1['TimeNow']-dfg1["Datetime"]
    dfg1['Minutes'] = round((dfg1['Minutes']/np.timedelta64(1,'m')),2)  
    dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)    
    
    
    return dfg1
    #print(dfg1.dtypes)
    # print(dfg1.head(1))


posit = pd.DataFrame(credi_har.positions()) 
if posit.empty:
    print("Position is Empty")
    buy_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order_li = ordef_func()
    buy_order_list_dummy = (np.unique([int(i) for i in buy_order_li['ScripCode']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()
    print(buy_order_list_dummy)

start_time = time.time()

# Buy_Scriptcodee = 10604
while True:
    print(buy_order_list_dummy)
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()
    five_df7 = pd.DataFrame()
    final_df = pd.DataFrame()

    for sc in stk_list:
        try:
            dfg1 = data_download(sc,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl)  
            stk_name = (np.unique([str(i) for i in dfg1['Name']])).tolist()[0]
            #print(stk_name)
            five_df1 = pd.concat([dfg1, five_df1])
            by_df = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_Up_break") & (dfg1["Buy/Sell"] == "BUY") & (dfg1["RSI_14"] > UP_Rsi_lvl ) & (dfg1["Rsi_OK"] == "Rsi_Up_OK" ) & (dfg1["Cand_Col"] == "Green" )]# & (dfg1["Date"] == current_trading_day.date())]
            five_df4 = pd.concat([by_df, five_df4])
            
            #print(len(by_df))
            dfg3 = by_df.tail(1)

            if not dfg3.empty:       
                Namee = (np.unique([str(i) for i in dfg3['Name']])).tolist()[0]
                Scripcodee = int(float(dfg3['Scripcode'])) 
                Buy_At = float(dfg3['Open'])
                Qtyy = round((Capital/Buy_At),0)                
                Buy_Stop_Loss = float(round((Buy_At - (Buy_At*SLL)/100),1))
                Buy_Target = float(round((((Buy_At*SLL)/100) + Buy_At),1))   
                Buy_date = list(dfg3['Date'])[0]         
                Buy_timee = list(dfg3['Datetime'])[0]
                Buy_timee1 = str(Buy_timee).replace(' ','T')    

                print(Namee,Scripcodee,Qtyy,Buy_At,Buy_date,Buy_timee1)     
                dfg1['Buy_At'] = Buy_At
                dfg1['Name'] = Namee
                dfg1['Entry_Date'] = Buy_timee1
                dfg1['Entry_Price'] = Buy_At
                dfg1.sort_values(['Name', 'Datetime'], ascending=[True, True], inplace=True)
                dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                dfg1['Qty'] = Qtyy
                
                five_df2 = pd.concat([dfg1, five_df2])

                dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                dfg2['StopLoss'] = round((dfg2['Entry_Price'] - (dfg2['Entry_Price']*SLL)/100),1)
                #print(dfg2.head(10))
                dfg2['Benchmark'] = dfg2['High'].cummax()
                dfg2['TStopLoss'] = dfg2['Benchmark'] * tsl1                            
                dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < Buy_Stop_Loss,"SL",""))
                dfg2['P&L_TSL'] = np.where(dfg2['Status'] == "SL",(dfg2['StopLoss'] - dfg2['Entry_Price'])*Qtyy,np.where(dfg2['Status'] == "TSL",(dfg2['TStopLoss'] - dfg2['Entry_Price'])*Qtyy,"" ))
                five_df3 = pd.concat([dfg2, five_df3])
                 
                sl_d = dfg2[(dfg2['Date'] == Buy_date) & (dfg2['Status'] == 'TSL')]
                if sl_d.empty:
                    sl_df = dfg2[(dfg2['Date'] == Buy_date)]
                    sl_df1 = sl_df.tail(1)
                else:
                    sl_df = sl_d = dfg2[(dfg2['Status'] == 'TSL')]
                    sl_df1 = sl_d.head(1)
                final_d = pd.merge(by_df, sl_df1, on=['Name'], how='inner')
                final_d['P&LL'] = (final_d['Close_y']-final_d['Buy_At'])*(Qtyy)
                final_df = pd.concat([final_d,final_df],ignore_index=True)
                dfgg_up = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_Up_break") & (dfg1["Buy/Sell"] == "BUY") & (dfg1["RSI_14"] > UP_Rsi_lvl ) & (dfg1["Rsi_OK"] == "Rsi_Up_OK" ) & (dfg1["Cand_Col"] == "Green" ) & (dfg1["Date"] == current_trading_day.date()) & (dfg1["Minutes"] < 5 )]# & (dfg1['PDB'] == "PDHB")]
                
                if not dfgg_up.empty:
                    #Buy_call_quantity_of_stock = int(np.unique(dfgg_up['Qty']))
                    print("Buy Stock")
                    if sc in buy_order_list_dummy: 
                        print(str(stk_name)+" is Already Buy")
                        print("----------------------------------------")
                    else:
                        rde_exec = order_execution(dfgg_up,buy_order_list_dummy,sc,telegram_msg,orders,"Stock","BUY","B",Scripcodee,Qtyy,Buy_At,stk_name)
            
            print("1 Min Cash Data Download and Scan "+str(stk_name)+" ("+str(sc)+")") 

        except Exception as e:
            print(e) 

        print("------------------------------------------------") 

    if five_df1.empty:
        pass
    else:
        #five_df1 = five_df1[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Rsi_OK','Cand_Col','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df1.sort_values(['Name', 'Datetime'], ascending=[True, True], inplace=True)
        # st1.range("a:az").value = None
        # st1.range("a1").options(index=False).value = five_df1

    if five_df2.empty:
        pass
    else:
        #five_df2 = five_df2[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df2.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
        # st2.range("a:az").value = None
        # st2.range("a1").options(index=False).value = five_df2

    if five_df3.empty:
        pass
    else:
        #five_df3 = five_df3[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df3.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
        # st3.range("a:az").value = None
        # st3.range("a1").options(index=False).value = five_df3

    
    if five_df3.empty:
        pass
    else:
        five_df3 = five_df3[five_df3['Status'] == 'TSL']
        #five_df3 = five_df3[['Name','Scripcode','Datetime','Date','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','LotSize','Buy_At','Add_Till','StopLoss','Target','Benchmark','TStopLoss','Status','P&L_TSL']]
        five_df3.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
        sl.range("a:az").value = None
        sl.range("a1").options(index=False).value = five_df3

    if five_df4.empty:
        pass
    else:
        #five_df4 = five_df4[['Name','Scripcode','StopLoss','Add_Till','Buy_At','Target','Term','Datetime','LotSize','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Datetime','Name'], ascending=[False, True], inplace=True)
        st4.range("a:az").value = None
        st4.range("a1").options(index=False).value = five_df4

    if five_df4.empty:
        pass
    else:
        #five_df4 = five_df4[['Name','Scripcode','StopLoss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Datetime','Name'], ascending=[False, True], inplace=True)
        by.range("a:az").value = None
        by.range("a1").options(index=False).value = five_df4

    if final_df.empty:
        pass
    else:
        #final_df = final_df[['Name','Scripcode','StopLoss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        final_df.sort_values(['Datetime_x','Name'], ascending=[False, True], inplace=True)
        fl.range("a:az").value = None
        fl.range("a1").options(index=False).value = final_df

    print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    print(f"Five Paisa Data Download Time: {end4:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    # print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")








































































































           