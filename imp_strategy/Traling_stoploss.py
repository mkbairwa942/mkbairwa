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


def place_trade(Exche,ExchTypee,OrderFor,symbol,scripte,quantity,price,direction):
    try:
        order = client.place_order(OrderType=direction,
                        Exchange=Exche,
                        ExchangeType=ExchTypee,
                        ScripCode = scripte,
                        Qty=int(quantity),
                        Price=price,
                        IsIntraday=True if OrderFor == "I" else False,)
                        #IsIntraday=True,
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

if not os.path.exists("Traling_stoploss.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Traling_stoploss.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Traling_stoploss.xlsx')
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



# def ordef_func():
#     try:
#         ordbook = pd.DataFrame(client.order_book())
#         #print(ordbook.tail(2))
#         ob.range("a1").options(index=False).value = ordbook
#     except Exception as e:
#                 print(e)

#     try:
#         if ordbook is not None:
#             #print("Order Book not Empty")        
#             #ordbook1 = ordbook[ordbook['AveragePrice'] != 0]   
#             ordbook1 = ordbook           
#             Datetimeee = []
#             for i in range(len(ordbook1)):
#                 datee = ordbook1['BrokerOrderTime'][i]
#                 timestamp = pd.to_datetime(datee[6:19], unit='ms')
#                 ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
#                 d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
#                 d2 = d1 + timedelta(hours = 5.5)
#                 Datetimeee.append(d2)
#             ordbook1['Datetimeee'] = Datetimeee
#             ordbook1 = ordbook1[['Datetimeee', 'ScripName','BuySell','AveragePrice', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason','Exch','ExchType', 'MarketLot', 'OrderValidUpto','AtMarket']]
#             ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
#             #ordbook1['Datetimeee1'] = ordbook1['Datetimeee'] - timedelta(days=3)
#             # ordbook2 = pd.DataFrame(ordbook1)
#             # print(ordbook2.dtypes())
            
#         else:
#             print("Order Book Empty")
#     except Exception as e:
#                 print(e)
#     return ordbook1

# posit = pd.DataFrame(client.positions()) 
# if posit.empty:
#     print("Position is Empty")
# else:
#     buy_order_li = ordef_func()

#print(buy_order_li['AveragePrice'].dtypes())


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

dataframe_empty = pd.DataFrame()

SLL = 1
TSL = 1


tsl1 = 1-(TSL/100)
print(tsl1)

while True: 
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # start_time = '09:15:00'
    # end_time = '15:15:20'
    # if current_time > start_time and current_time < end_time:
    #     print("Market Hours Open")
    #     market_status = pd.DataFrame(client.get_market_status())#[1]['MarketStatus']
    #     market_status1 = market_status[market_status['ExchDescription'] == 'Nse Derivative']
    #     market_status2 = list(market_status1['MarketStatus'])[0]
    #     if market_status2 == "Open":
    #         print(f"Market {market_status2}")
    for sh_na in users:
        if sh_na == "ashwin":
            posit = pd.DataFrame(client.positions()) 
            #print(posit.head(1))
            if posit.empty:
                print("Position is Empty")
                print("------------------")
                pass
            else:   
                try:             
                    ash.range("ad1").value = pd.DataFrame(client.margin())
                    ash.range("ad10").value = pd.DataFrame(client.holdings())
                    ash.range("ad20").value = pd.DataFrame(client.positions()) 


                    posit = pd.DataFrame(client.positions()) 
                    posit1 = posit #posit[(posit['MTOM'] != 0)]             
                    posit3 = np.unique([int(i) for i in posit1['ScripCode']])

                except Exception as e:
                    print(e)

                five_df3 = pd.DataFrame()
                five_df4 = pd.DataFrame()

                for ord in posit3:
                    try:
                        #print(ord)
                        #time.sleep(0.5)
                        timee = datetime.now()
                        #print(timee)
                        new_df1 = posit1[(posit1['ScripCode'] == ord)]
                        Buy_Name = list(new_df1['ScripName'])[0]
                        Buy_price = float(new_df1['BuyAvgRate'])                 
                        Buy_Stop_Loss = float(round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*SLL)/100),1))
                        Buy_Target = float(round((((new_df1['BuyAvgRate']*SLL)/100) + new_df1['BuyAvgRate']),1))
                        Buy_Exc = list(new_df1['Exch'])[0]
                        Buy_Exc_Type = list(new_df1['ExchType'])[0]
                        Buy_Qty = int(new_df1['BuyQty'])    
                        Buy_timee = datetime.now()     

                        Buy_timee = Buy_timee - timedelta(minutes=1)
                        
                        # if Buy_Name == 'TATACONSUM 25 Jan 2024 CE 1080.00':                            
                        #     Buy_timee = '2023-12-29 10:34:12'
                        # if Buy_Name == 'TATACONSUM 25 Jan 2024 CE 1090.00':                            
                        #     Buy_timee = '2023-12-29 14:31:18'
                        # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 470.00':                            
                        #     Buy_timee = '2023-12-29 15:04:30'
                        # if Buy_Name == 'GMRINFRA':                            
                        #     Buy_timee = '2023-12-29 15:28:08'
                        # if Buy_Name == 'NATURALGAS 23 Jan 2024 CE 210.00':                            
                        #     Buy_timee = '2023-12-29 16:48:08'
                        Buy_timee1 = str(Buy_timee).replace(' ','T')
                        #print(Buy_Name,Buy_price,Buy_Stop_Loss,Buy_Target,Buy_Exc,Buy_Exc_Type,Buy_Qty,Buy_timee,Buy_timee1)

                        dfg1 = client.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
                        #print(dfg1.head(2))
                        
                        # dataframe_empty['Buy_timee'] = Buy_timee1
                        # dataframe_empty['Close'] = dfg1.iloc['Close'][-1]
                        # print(dataframe_empty)
                        # dataframe_empty = pd.concat([dataframe_empty, dataframe_empty])
                        # print(dataframe_empty)
                        dfg1['ScripCode'] = ord
                        dfg1['ScripName'] = Buy_Name
                        dfg1['Entry_Date'] = Buy_timee1
                        dfg1['Entry_Price'] = Buy_price
                        #print(dfg1.head(2))
                        dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                        dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                        dfg1['TimeNow'] = datetime.now()
                        #print(dfg1.head(1))
                        # dfg1['Minutes'] = pd.to_datetime(dfg1['TimeNow'])-Buy_timee1
                        # dfg1['Minutes'] = round((dfg1['Minutes']/np.timedelta64(1,'m')),2)
                        
                        dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                        #print(dfg2.head(1))
                        # dfg2['StopLoss'] = Buy_Stop_Loss
                        # dfg2['Benchmark'] = dfg2['High'].cummax()
                        # dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98                             
                        # dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < Buy_Stop_Loss,"SL",""))
                        # dfg2['P&L_TSL'] = np.where(dfg2['Status'] == "SL",(dfg2['StopLoss'] - dfg2['Entry_Price'])*Buy_Qty,np.where(dfg2['Status'] == "TSL",(dfg2['TStopLoss'] - dfg2['Entry_Price'])*Buy_Qty,"" ))
                        # #print(dfg2)
                        # final_df = pd.merge(posit1,dfg2, on=['ScripCode'], how='inner')  
                        # final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                        # final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TGT")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                        # final_df = final_df[['ScripName_x','Exch','ExchType','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]
                        # five_df4 = pd.concat([final_df, five_df4])
                        dfg22 = dfg2.tail(1)
                        #print(dfg22)
                        dataframe_empty = pd.concat([dfg22, dataframe_empty])

                        # st4.range("a:q").value = None
                        # st4.range("a1").options(index=False).value = dfg22
                        # #print(dfg2.head(2))
                        # #print(dfg2.iloc[[-1]])
                        # #five_df4 = pd.concat([dfg2, five_df4])
                        # dfg3 = dfg2[(dfg2['Status'] != '')] 

                        # if dfg3.empty:
                        #     dfg4 = dfg2.iloc[[-1]]
                        # else:  
                        #     dfg4 = dfg3.iloc[0:1]
                        # five_df3 = pd.concat([dfg4, five_df3])
                    except Exception as e:
                        print(e)

                #print(five_df3)
                try:
                    dataframe_empty.sort_values(['ScripName','Entry_Date',], ascending=[True,True], inplace=True)   
                    dataframe_Scpt = np.unique([int(i) for i in dataframe_empty['ScripCode']])
                    for ord in posit3:
                        dataframe_new = dataframe_empty[(dataframe_empty['ScripCode'] == ord)]
                        dataframe_new['StopLoss'] = round((dataframe_new['Entry_Price'] - (dataframe_new['Entry_Price']*SLL)/100),1)
                        dataframe_new['Benchmark'] = dataframe_new['High'].cummax()
                        dataframe_new['TStopLoss'] = dataframe_new['Benchmark'] * tsl1                            
                        dataframe_new['Status'] = np.where(dataframe_new['Close'] < dataframe_new['TStopLoss'],"TSL",np.where(dataframe_new['Close'] < Buy_Stop_Loss,"SL",""))
                        dataframe_new['P&L_TSL'] = np.where(dataframe_new['Status'] == "SL",(dataframe_new['StopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,np.where(dataframe_new['Status'] == "TSL",(dataframe_new['TStopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,"" ))
                        first_row = dataframe_new.head(1)                    

                        last_row = dataframe_new.tail(1)
                        last_row['Entry_Date'] = first_row['Entry_Date']

                        five_df3 = pd.concat([last_row, five_df3])

                    final_df = pd.merge(posit1,five_df3, on=['ScripCode'], how='inner')  
                    final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                    final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TSL")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                                                                
                    #final_df = final_df[['ScripName_x','Exch','ExchType','ScripCode','Entry_Date','Datetime','Minutes','BuyAvgRate','SellAvgRate','StopLoss','TStopLoss','Status','Benchmark','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	 
                    final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                    final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                    final_df.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True)
                except Exception as e:
                    print(e)
                #st3.range("a1").options(index=False).value = five_df4
                try:
                    st4.range("a1").options(index=False).value = dataframe_empty
                    ash.range("a1").options(index=False).value = final_df

                    # ash.range("t2").options(index=False).value = '=IF(AND(S2="BUY",M2="TSL"),"SELL",IF(AND(S2="BUY",M2="SL"),"SELL",""))'
                    # ash.range("t3").options(index=False).value = '=IF(AND(S3="BUY",M3="TSL"),"SELL",IF(AND(S3="BUY",M3="SL"),"SELL",""))'
                    # ash.range("t4").options(index=False).value = '=IF(AND(S4="BUY",M4="TSL"),"SELL",IF(AND(S4="BUY",M4="SL"),"SELL",""))'
                    # ash.range("t5").options(index=False).value = '=IF(AND(S5="BUY",M5="TSL"),"SELL",IF(AND(S5="BUY",M5="SL"),"SELL",""))'
                    # ash.range("t6").options(index=False).value = '=IF(AND(S6="BUY",M6="TSL"),"SELL",IF(AND(S6="BUY",M6="SL"),"SELL",""))'
                    # ash.range("t7").options(index=False).value = '=IF(AND(S7="BUY",M7="TSL"),"SELL",IF(AND(S7="BUY",M7="SL"),"SELL",""))'
                    # ash.range("t8").options(index=False).value = '=IF(AND(S8="BUY",M8="TSL"),"SELL",IF(AND(S8="BUY",M8="SL"),"SELL",""))'
                    # ash.range("t9").options(index=False).value = '=IF(AND(S9="BUY",M9="TSL"),"SELL",IF(AND(S9="BUY",M9="SL"),"SELL",""))'
                    # ash.range("t10").options(index=False).value = '=IF(AND(S10="BUY",M10="TSL"),"SELL",IF(AND(S10="BUY",M10="SL"),"SELL",""))'
                    # ash.range("t11").options(index=False).value = '=IF(AND(S11="BUY",M11="TSL"),"SELL",IF(AND(S11="BUY",M11="SL"),"SELL",""))'
                
                except Exception as e:
                    print(e)
                    
                trading_info = ash.range(f"a{2}:t{19}").value
                sym = ash.range(f"a{2}:a{19}").value
                symbols = list(filter(lambda item: item is not None, sym))
                idx = 0
                for i in symbols:
                    if i:
                        trade_info = trading_info[idx]
                        
                        #place_trade(Exche,ExchTypee,OrderFor,symbol,scripte,quantity,price,direction)
                        print(trade_info[1],trade_info[2],trade_info[3],trade_info[0],trade_info[4],trade_info[17],trade_info[14],trade_info[18],trade_info[19])

                        if trade_info[17] is not None and trade_info[18] is not None:

                            if trade_info[18] == "BUY" and trade_info[19] is None:  
                                print("Buy order")   
                                #dt.range(f"t{idx + 2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[8]),"B")

                            if trade_info[18] == "BUY" and trade_info[19] == "SELL":
                                print("Sell order") 
                                #squareoff = client.squareoff_all() place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction)
                                dt.range(f"u{idx +2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[3]),str(trade_info[0]),int(trade_info[4]),int(trade_info[17]),int(trade_info[14]),"S")
                                                            #place_trade(     Exche,              ExchTypee,       OrderFor,          symbol,            scripte,            quantity,       price,         direction)
                                
                                
                            if trade_info[18] == "SELL" and trade_info[19] is None:  
                                print("Sell order")   
                                #squareoff = client.squareoff_all()                                  
                                #dt.range(f"t{idx +2 }").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[8]),"S")

                            if trade_info[18] == "SELL" and trade_info[19] == "BUY":   
                                print("Buy order")                                   
                                #dt.range(f"u{idx + 2}").value = place_trade(str(trade_info[1]),str(trade_info[2]),str(trade_info[0]),int(trade_info[3]),int(trade_info[16]),float(trade_info[8]),"B")

                    idx +=1
        

                print("Data Analysis Complete for Ashwin")
            
    # else:
    #     print("Market Hours Closed")
    #     market_status = pd.DataFrame(client.get_market_status())#[1]['MarketStatus']
    #     market_status1 = market_status[market_status['ExchDescription'] == 'Nse Derivative']
    #     market_status2 = list(market_status1['MarketStatus'])[0]
    #     if market_status2 == "Closed":
    #         print(f"Market {market_status2}")