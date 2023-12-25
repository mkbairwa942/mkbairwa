import os


import time,json,datetime,sys
import xlwings as xw
import pandas as pd
import copy
import numpy as np
import time
import requests 
import dateutil.parser
import threading
from datetime import datetime,timedelta
import pandas_ta as pta
import math 
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from numpy import log as nplog
from numpy import NaN as npNaN
import pywhatkit as pwk
import dateutil.parser
import threading
import pyotp
from five_paisa1 import *
from datetime import datetime,timedelta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega
telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

# operate = input("Do you want to go with TOTP (yes/no): ")
# TGTT_SLL = input("Do you want to go with FIXED or TRALING STOPLOSS (FSL/TSL): ")
# if operate.upper() == "YES":
#     from five_paisa1 import *
#     # p=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
#     # print(p)
#     username = input("Enter Username : ")
#     username1 = str(username)
#     username2 = username1.upper()
#     print("HII "+str(username2)+" HAVE A GOOD DAY")
#     # username_totp = input("Enter TOTP : ")
#     # username_totp1 = str(username_totp)
#     # print("Hii "+str(username1)+" you enter TOTP is "+str(username_totp1))
#     client = credentials(username1)
# else:
#     from five_paisa import *
#     # from five_paisa1 import *
    
TGTT_SLL = "TSL"    
client = credentials("ASHWIN")

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

users = ["ashwin","haresh"]
stoploss = 2
# for usew in users:
#     usew = credentials(str(usew))

# ashwin = credentials(str(ashwin))
# haresh = credentials(haresh)
# mukesh = credentials(mukesh)


current_time = (datetime.now()).strftime("%H:%M")

def get_live_data(Exchange,ExchangeType,Symbol):

    try:
        live_data
    except:
        live_data = {}
    try:
        live_data = client.fetch_market_depth_by_symbol([{"Exchange":Exchange,"ExchangeType":ExchangeType,"Symbol":Symbol}])
    except Exception as e:
        pass
    return live_data

def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
    t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
    S = asset_price
    K = strike_price
    r = interest_rate
    if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
        raise Exception
    flag = instrument_type[0].lower()
    imp_v = implied_volatility(premium, S, K, t, r, flag)
    return [imp_v,
            delta(flag,S,K,t,r,imp_v),
            gamma(flag,S,K,t,r,imp_v),
            rho(flag,S,K,t,r,imp_v),
            theta(flag,S,K,t,r,imp_v),
            vega(flag,S,K,t,r,imp_v)]


def place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction):
    try:
        order = client.place_order(OrderType=direction,
                        Exchange=Exche,
                        ExchangeType=ExchTypee,
                        ScripCode = scripte,
                        Qty=int(quantity),
                        Price=0.0,
                        IsIntraday=True,)
                        #IsStopLossOrder=True
                        #StopLossPrice=StopLossPrice)
        print("CALL PLACE TRADE")
        print(f"order :Exche {Exche},ExchTypee {ExchTypee},scripte {scripte}, Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
        return order
    except Exception as e:
        return f"{e}"

Exchange = None
prev_info = {"Symbol": None, "Expiry": None}
instruments_dict = {}
option_data = {}
 

print("----option chain----")

if not os.path.exists("Terminal_multiple.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Terminal_multiple.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Terminal_multiple.xlsx')
for i in ["stats","Exchange","Expiry","Position","OrderBook","OrderBook_New","Option","Data","Buy","Sale","Final",
            "Stat","Stat1","Stat2","Stat3","Stat4","mukesh","ashwin","haresh"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

muk = wb.sheets("mukesh")  
ash = wb.sheets("ashwin")      
har = wb.sheets("haresh")           

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
dt.range("a:x").value = None
by.range("a:x").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:aj").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None
# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None
#oc.range("a:z").value = None
dt.range(f"a1:d1").value = ["Namee","Scriptcodee","Stop_Loss","Add_Till","Buy_At","Target" ,"Term","Datetime", "","","","","","","","","","","","","","Quantity","Entry","Exit","SL","Status"]
oc.range("a:b").value = oc.range("d8:e30").value = oc.range("g1:v4000").value = None

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a1").value = script_code_5paisa
# # exc.range("a1").value = exchange

# exchange = None
# while True:
#     if exchange is None: 
#         try:
#             exchange = pd.DataFrame(script_code_5paisa)
#             #exchange = exchange[exchange["Exch"] == "N"]
#             #exchange = exchange[exchange["ExchType"] == "D"]
#             exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
#             exchange1 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['CpType'].isin(['EQ', 'XX']))]
#             # exchange1 = exchange[(exchange['ExchType'].isin(['C', 'D']))]
#             # exchange1 = exchange1[(exchange1['Series'].isin(['EQ', 'XX']))]
#             # exchange2 = exchange[exchange["Series"] == "EQ"]
#             #exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]
            
#             # print(exchange.tail(20))
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(10)

def ordef_func():
    try:
        ordbook = pd.DataFrame(client.order_book())
        #print(ordbook.tail(2))
        ob.range("a1").options(index=False).value = ordbook
    except Exception as e:
                print(e)

    try:
        if ordbook is not None:
            #print("Order Book not Empty")        
            #ordbook1 = ordbook[ordbook['AveragePrice'] != 0]   
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
            ordbook1 = ordbook1[['Datetimeee', 'ScripName','BuySell','AveragePrice', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason','Exch','ExchType', 'MarketLot', 'OrderValidUpto','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            #ordbook1['Datetimeee1'] = ordbook1['Datetimeee'] - timedelta(days=3)
            # ordbook2 = pd.DataFrame(ordbook1)
            # print(ordbook2.dtypes())
            
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

posit = pd.DataFrame(client.positions()) 
if posit.empty:
    print("Position is Empty")
else:
    buy_order_li = ordef_func()

#print(buy_order_li['AveragePrice'].dtypes())

def get_oi(data):
    global prev_day_oi,kite,stop_thread
    for symbol, v in data.items():
        if stop_thread:
            break
        while True:
            try:
                prev_day_oi[symbol]
                break
            except:
                try:
                    prev_day_data = kite.historical_data(v["token"],(datetime.now() - timedelta(days=5)).date(),
                                                         (datetime.now()-timedelta(days=1)).date(),"day",oi=True)
                    try:
                        prev_day_oi[symbol] = prev_day_data[-1]["oi"]
                    except:
                        prev_day_oi[symbol] = 0
                    break
                except Exception as e:
                    time.sleep(0.5)
print("Excel : Started")

ash.range("a1:t1").color = (54,226,0)
ash.range("a1:t1").font.bold = True
ash.range("a1:t1").api.WrapText = True

har.range("a1:t1").color = (54,226,0)
har.range("a1:t1").font.bold = True
har.range("a1:t1").api.WrapText = True

# Dummy_positionss = buy_order_li.copy()
# print("11")
# print(Dummy_positionss.head(1))
# Dummy_positionss.rename(columns={'Qty': 'BuyQty','Rate':'BuyAvgRate'}, inplace=True)
# Dummy_positionss['BookedPL'] = 10
# Dummy_positionss['MTOM'] = 0
# Dummy_positionss['LTP'] = Dummy_positionss['BuyAvgRate']
# Dummy_positionss = Dummy_positionss[['Exch','ExchType','ScripCode','ScripName','BuyAvgRate','BuyQty','LTP','BookedPL','MTOM',]]
# print("22")
# print(Dummy_positionss.head(1))

while True: 
    for sh_na in users:
        if sh_na == "ashwin":
            posit = pd.DataFrame(client.positions()) 
            if posit.empty:
                print("Position is Empty")
                pass
            else:
                #client = credentials(sh_na)
                ash.range("ad1").value = pd.DataFrame(client.margin())
                ash.range("ad10").value = pd.DataFrame(client.holdings())
                ash.range("ad20").value = pd.DataFrame(client.positions()) 

                buy_order_li = ordef_func()
                buy_order_liii = buy_order_li[(buy_order_li['AveragePrice'] != 0)]
                ash.range("ad40").options(index=False).value = buy_order_liii                   
        
                buy_order_liiist = buy_order_liii[buy_order_liii['BuySell'] == 'B']
                buy_order_list = np.unique([int(i) for i in buy_order_liiist['ScripCode']])

                buy_ord_new = pd.DataFrame()
                five_df = pd.DataFrame()
                five_dff = pd.DataFrame()

                for ord in buy_order_list:
                    new_df = buy_order_liii[(buy_order_liii['ScripCode'] == ord) & (buy_order_liii['BuySell'] == 'B')]
                    
                    new_df.sort_values(['Datetimeee','Rate'], ascending=[True,True], inplace=True)
                    new_df1 = new_df.iloc[[0]]
                    
                    buy_ord_new = pd.concat([new_df1, buy_ord_new]) 
                    #Buy_Scriptcodee = int(new_df1['ScripCode'])
                    Buy_Name = list(new_df1['ScripName'])[0]
                    Buy_price = float(new_df1['Rate'])                 
                    Buy_Stop_Loss = float(round((new_df1['Rate'] - (new_df1['Rate']*stoploss)/100),1))
                    Buy_Target = float(round((((new_df1['Rate']*stoploss)/100) + new_df1['Rate']),1))
                    Buy_Exc = list(new_df1['Exch'])[0]
                    Buy_Exc_Type = list(new_df1['ExchType'])[0]
                    Buy_Qty = int(new_df1['Qty'])                
                    Buy_timee = list(new_df1['Datetimeee'])[0]
                    Buy_timee1 = str(Buy_timee).replace(' ','T')
  
                    dfg1 = client.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
                    dfg1['ScripCode'] = ord
                    dfg1['ScripName'] = Buy_Name
                    dfg1['Entry_Date'] = Buy_timee1
                    dfg1['Entry_Price'] = Buy_price
            
                    dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                    #st.range("a1").options(index=False).value = dfg1
                    dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                    dfg1['StopLoss'] = Buy_Stop_Loss
                    dfg1['Target'] = Buy_Target
                    dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                    dfg2['Benchmark'] = dfg2['High'].cummax()
                    dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98 
                    five_dff = pd.concat([dfg2, five_dff])

                    dfg3 = dfg2.iloc[[-1]] 

                    five_df = pd.concat([dfg3, five_df])
                #st.range("a1").options(index=False).value = five_dff 

                posit = pd.DataFrame(client.positions()) 
                if posit.empty:
                    print("Position is Empty")
                    pass
                else:
                    final_df = pd.merge(posit,buy_ord_new, on=['ScripCode'], how='inner')
                    final_df['TimeNow'] = datetime.now()
                    final_df['Minutes'] = pd.to_datetime(final_df['TimeNow'])-pd.to_datetime(final_df["Datetimeee"])
                    final_df['Minutes'] = round((final_df['Minutes']/np.timedelta64(1,'m')),2)

                    final_df1 = pd.merge(final_df,five_df, on=['ScripCode'], how='inner')

                    if TGTT_SLL.upper() == "FSL":                    
                        final_df1['Status'] = np.where(final_df1['LTP'] > final_df1['BuyAvgRate'],"TGT",np.where(final_df1['LTP'] < final_df1['StopLoss'],"SL",""))  

                    if TGTT_SLL.upper() == "TSL" or TGTT_SLL.upper() == "": 
                        final_df1['Status'] = np.where(final_df1['LTP'] < final_df1['TStopLoss'],"TSL",np.where(final_df1['LTP'] < final_df1['StopLoss'],"SL",""))
    
                    final_df1['New_LTP'] = final_df1['LTP']-0.10
                    final_df1['Entry'] = np.where((final_df1['MTOM'] != 0) & (final_df1['BuyQty'] != 0) & (final_df1['MTOM'] != "") & (final_df1['BuyQty'] != ""),"BUY","")
                    final_df1['Exit'] = np.where(((final_df1['Entry'] == "BUY") & (final_df1['Status'] == "TGT")) | ((final_df1['Entry'] == "BUY") & (final_df1['Status'] == "TSL")) | ((final_df1['Entry'] == "BUY") & (final_df1['Status'] == "SL")),"SELL","")
                    
                    final_df1 = final_df1[['ScripName_x','Exch_x','ExchType_x','ScripCode','Datetimeee','Datetime','Minutes','BuyAvgRate','LTP','StopLoss','Target','Benchmark','TStopLoss','Status','BookedPL','MTOM','BuyQty','New_LTP','Entry','Exit']]	

                    ash.range("a1").options(index=False).value = final_df1
                    ash.range("t2").options(index=False).value = '=IF(AND(S2="BUY",N2="TSL"),"SELL",IF(AND(S2="BUY",N2="SL"),"SELL",""))'
                    ash.range("t3").options(index=False).value = '=IF(AND(S3="BUY",N3="TSL"),"SELL",IF(AND(S3="BUY",N3="SL"),"SELL",""))'
                    ash.range("t4").options(index=False).value = '=IF(AND(S4="BUY",N4="TSL"),"SELL",IF(AND(S4="BUY",N4="SL"),"SELL",""))'
                    ash.range("t5").options(index=False).value = '=IF(AND(S5="BUY",N5="TSL"),"SELL",IF(AND(S5="BUY",N5="SL"),"SELL",""))'
                    ash.range("t6").options(index=False).value = '=IF(AND(S6="BUY",N6="TSL"),"SELL",IF(AND(S6="BUY",N6="SL"),"SELL",""))'
                    ash.range("t7").options(index=False).value = '=IF(AND(S7="BUY",N7="TSL"),"SELL",IF(AND(S7="BUY",N7="SL"),"SELL",""))'
                    ash.range("t8").options(index=False).value = '=IF(AND(S8="BUY",N8="TSL"),"SELL",IF(AND(S8="BUY",N8="SL"),"SELL",""))'
                    ash.range("t9").options(index=False).value = '=IF(AND(S9="BUY",N9="TSL"),"SELL",IF(AND(S9="BUY",N9="SL"),"SELL",""))'
                    ash.range("t10").options(index=False).value = '=IF(AND(S10="BUY",N10="TSL"),"SELL",IF(AND(S10="BUY",N10="SL"),"SELL",""))'
                    ash.range("t11").options(index=False).value = '=IF(AND(S11="BUY",N11="TSL"),"SELL",IF(AND(S11="BUY",N11="SL"),"SELL",""))'
                    
                    trading_info = ash.range(f"a{2}:t{19}").value
                    sym = ash.range(f"a{2}:a{19}").value
                    symbols = list(filter(lambda item: item is not None, sym))
                    idx = 0
                    for i in symbols:
                        if i:
                            trade_info = trading_info[idx]
                            #place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction)
                            print(trade_info[1],trade_info[2],trade_info[0],trade_info[3],trade_info[16],trade_info[17],trade_info[18],trade_info[19])

                            if trade_info[16] is not None and trade_info[18] is not None:

                                if trade_info[18] == "BUY" and trade_info[19] is None:  
                                    print("Buy order")   
                                    #dt.range(f"t{idx + 2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[17]),"B")

                                if trade_info[18] == "BUY" and trade_info[19] == "SELL":
                                    print("Sell order") 
                                    #squareoff = client.squareoff_all() 
                                    dt.range(f"u{idx +2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[17]),"S")

                                if trade_info[18] == "SELL" and trade_info[19] is None:  
                                    print("Sell order")   
                                    #squareoff = client.squareoff_all()                                  
                                    #dt.range(f"t{idx +2 }").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[17]),"S")

                                if trade_info[18] == "SELL" and trade_info[19] == "BUY":   
                                    print("Buy order")                                   
                                    #dt.range(f"u{idx + 2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[17]),"B")

                        idx +=1
            

            print("Data Analysis Complete for Ashwin")
        
