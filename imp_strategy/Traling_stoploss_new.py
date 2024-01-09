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


if not os.path.exists("Traling_stoploss_new.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Traling_stoploss_new.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Traling_stoploss_new.xlsx')
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
ash.range("a1:t1").color = (54,226,0)
ash.range("a1:t1").font.bold = True
ash.range("a1:t1").api.WrapText = True

har.range("a1:t1").color = (54,226,0)
har.range("a1:t1").font.bold = True
har.range("a1:t1").api.WrapText = True

users = ["ashwin"]#,"haresh","alpesh"]
stoploss = 2

TGTT_SLL = "TSL"    
for credi in users:
    if credi == "ashwin":
        credi_ash = credentials("ASHWIN")
        postt = pd.DataFrame(credi_ash.margin())['Ledgerbalance'][0]
        print(f"Ledger Balance is : {postt}")
    if credi == "haresh":
        credi_har = credentials("HARESH")
        postt = pd.DataFrame(credi_har.margin())['Ledgerbalance'][0]
        print(f"Ledger Balance is : {postt}")
    if credi == "alpesh":
        credi_alp = credentials("ALPESH")
        postt = pd.DataFrame(credi_alp.margin())['Ledgerbalance'][0]
        print(f"Ledger Balance is : {postt}")

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

print("----option chain----")

# df_empty_ash = pd.DataFrame()
# df_empty_har = pd.DataFrame()

def ordef_func(client):
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
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M')
                d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]))
                d2 = d1 + timedelta(hours = 5.5)
                Datetimeee.append(d2)
            ordbook1['Datetimeee'] = Datetimeee
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','AveragePrice','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType','ExchOrderID', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            pos.range("a1").options(index=False).value = ordbook1
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

st4.range("a1").value = pd.DataFrame(credi_ash.order_book())

while True: 
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # start_time = '09:15:00'
    # end_time = '15:15:20'
    # if current_time > start_time and current_time < end_time:
    #     print("Market Hours Open")
    #     market_status = pd.DataFrame(credi_ash.get_market_status())#[1]['MarketStatus']
    #     market_status1 = market_status[market_status['ExchDescription'] == 'Nse Derivative']
    #     market_status2 = list(market_status1['MarketStatus'])[0]
    #     if market_status2 == "Open":
    #         print(f"Market {market_status2}")
    for sh_na in users:
        if sh_na == "ashwin":
            posit = pd.DataFrame(credi_ash.positions()) 
            if posit.empty:
                print("Ashwin's Position is Empty")
                print("--------------------------")
                pass
            else: 
                try:      
                    buy_order_li = ordef_func(credi_ash)         
                    ash.range("ad1").value = pd.DataFrame(credi_ash.margin())
                    ash.range("ad10").value = pd.DataFrame(credi_ash.holdings())
                    ash.range("ad20").value = pd.DataFrame(credi_ash.positions()) 
                    ash.range("ad30").value = buy_order_li
                
                
                    posit = pd.DataFrame(credi_ash.positions()) 
                    posit1 = posit #posit[(posit['MTOM'] != 0)]             
                    posit3 = np.unique([int(i) for i in posit1['ScripCode']])
                #print(posit3)
                except Exception as e:
                    print(e)

                five_df3 = pd.DataFrame()
                five_df4 = pd.DataFrame()

                for ord in posit3:
                    try: 
                        #time.sleep(0.5)
                        #timee = datetime.now()
                        buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B') & (buy_order_li['AveragePrice'] != 0)]
                        buy_order_liiist = buy_order_liiist[['Datetimeee','ScripCode']] 
                        #print(buy_order_liiist)
                        new_df11 = posit1[(posit1['ScripCode'] == ord)]
                        #print(new_df11)
                        new_df1 = pd.merge(buy_order_liiist, new_df11, on=['ScripCode'], how='inner')
                        #print(new_df1)
                        Buy_Name = list(new_df1['ScripName'])[0]
                        Buy_price = float(new_df1['BuyAvgRate'])                 
                        Buy_Stop_Loss = float(round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*stoploss)/100),1))
                        Buy_Target = float(round((((new_df1['BuyAvgRate']*stoploss)/100) + new_df1['BuyAvgRate']),1))
                        Buy_Exc = list(new_df1['Exch'])[0]
                        Buy_Exc_Type = list(new_df1['ExchType'])[0]
                        Buy_Qty = int(new_df1['BuyQty'])    
                        Buy_timee = list(new_df1['Datetimeee'])[0]
                        Buy_timee1 = str(Buy_timee).replace(' ','T')     

                        #Buy_timee = Buy_timee - timedelta(minutes=1)

                        # if Buy_Name == 'DELTACORP 25 Jan 2024 CE 155.00':                            
                        #     Buy_timee = '2024-01-01 14:03:12'
                        # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 485.00':                            
                        #     Buy_timee = '2024-01-01 14:15:18'
                        # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 500.00':                            
                        #     Buy_timee = '2024-01-01 14:33:30'

                        Buy_timee1 = str(Buy_timee).replace(' ','T')
                        
                        dfg1 = credi_ash.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
                        #print(dfg1.head(1))
                        dfg1['ScripCode'] = ord
                        dfg1['ScripName'] = Buy_Name
                        dfg1['Entry_Date'] = Buy_timee1
                        dfg1['Entry_Price'] = Buy_price

                        dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                        dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                        
                        #dfg1['TimeNow'] = datetime.now()
                        
                        dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                        dfg2['StopLoss'] = round((dfg2['Entry_Price'] - (dfg2['Entry_Price']*stoploss)/100),1)
                        dfg2['Benchmark'] = dfg2['High'].cummax()
                        dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98                             
                        dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < Buy_Stop_Loss,"SL",""))
                        dfg2['P&L_TSL'] = np.where(dfg2['Status'] == "SL",(dfg2['StopLoss'] - dfg2['Entry_Price'])*Buy_Qty,np.where(dfg2['Status'] == "TSL",(dfg2['TStopLoss'] - dfg2['Entry_Price'])*Buy_Qty,"" ))
                        five_df3 = pd.concat([dfg2, five_df3])
                        #print(dfg2.head(1))
                        dfg3 = dfg2[(dfg2["Status"] == "TSL") | (dfg2["Status"] == "SL")]
                        dfg22 = dfg3.head(1)
                        final_df = pd.merge(posit1,dfg22, on=['ScripCode'], how='inner')  
                        final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                        final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TSL")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                        #print(final_df)                         
                        final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                        final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                        final_df.sort_values(['Entry_Date'], ascending=[True], inplace=True)
                        five_df4 = pd.concat([final_df, five_df4])

                        order_dff = final_df[(final_df['Exit'] == 'SELL')]

                        if order_dff.empty:
                            print("No Open Position of Ashwin")
                        else:
                            try: 
                                buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B') & (buy_order_li['AveragePrice'] != 0)]
                                order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])
                                for ordd in order_dff_Scpt:
                                    order_df = order_dff[(order_dff['ScripCode'] == ordd)]
                                    order = credi_ash.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Sell order Executed") 
                            except Exception as e:
                                print(e)

                    except Exception as e:
                        print(e)

                # #df_empty_ash.sort_values(['ScripName','Entry_Date',], ascending=[True,True], inplace=True)   

                # for ord in posit3:
                #     #print(ord)
                        #dataframe_new = df_empty_ash[(df_empty_ash['ScripCode'] == ord)]                                      
                #         dataframe_new['StopLoss'] = round((dataframe_new['Entry_Price'] - (dataframe_new['Entry_Price']*stoploss)/100),1)
                #         dataframe_new['Benchmark'] = dataframe_new['High'].cummax()
                #         dataframe_new['TStopLoss'] = dataframe_new['Benchmark'] * 0.98                             
                #         dataframe_new['Status'] = np.where(dataframe_new['Close'] < dataframe_new['TStopLoss'],"TSL",np.where(dataframe_new['Close'] < Buy_Stop_Loss,"SL",""))
                #         dataframe_new['P&L_TSL'] = np.where(dataframe_new['Status'] == "SL",(dataframe_new['StopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,np.where(dataframe_new['Status'] == "TSL",(dataframe_new['TStopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,"" ))
                        
                #         first_row = dataframe_new.head(1)
                #         last_row = dataframe_new.tail(1)
                #         last_row['Entry_Date'] = first_row['Entry_Date']
                #         five_df3 = pd.concat([last_row, five_df3])

                # final_df = pd.merge(posit1,five_df3, on=['ScripCode'], how='inner')  
                # final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                # final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TSL")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                # #print(final_df)                         
                # final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                # final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                # final_df.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True)

                if five_df4.empty:
                    pass
                else:
                    try:
                        #fo_bhav = fo_bhav[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
                        #df_empty_ash.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
                        #st2.range("a:az").value = None
                        ash.range("a1").options(index=False).value = five_df4
                    except Exception as e:
                        print(e)

                if five_df3.empty:
                    pass
                else:
                    try:
                        #fo_bhav = fo_bhav[['Name','Scripcode','Datetime','Date','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
                        #final_df.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
                        #har.range("a:az").value = None
                        st3.range("a1").options(index=False).value = five_df3
                        #st3.range("a1").options(index=False).value = final_df
                        # st4.range("a1").options(index=False).value = df_empty_ash
                        # ash.range("a1").options(index=False).value = final_df
                    except Exception as e:
                        print(e)
                
                # buy_order_liiist1 = buy_order_li[(buy_order_li['AveragePrice'] != 0) & (buy_order_li['BuySell'] == 'S') ]
                # print(buy_order_liiist1)
                # order_dff_Scpt2 = np.unique([int(i) for i in buy_order_liiist1['ScripCode']])
                # print(order_dff_Scpt2)
                # for ui in order_dff_Scpt2:
                #     order_df1 = buy_order_liiist1[(buy_order_liiist1['ScripCode'] == ui)]
                #     order = credi_ash.cancel_order(exch_order_id=int(order_df1['ExchOrderID']))

                #     print(buy_order_liiist1['ExchOrderID'],buy_order_liiist1['ScripCode'],buy_order_liiist1['ScripName'])
                
                
                order_dff = final_df[(final_df['Exit'] == 'SELL')]
                #order_dff = final_df
                if order_dff.empty:
                    print("No Open Position of Ashwin")
                else:
                    try: 
                        order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])
                        buy_order_liiist1 = buy_order_li[(buy_order_li['AveragePrice'] != 0) & (buy_order_li['BuySell'] == 'S')]
                        for ordd1 in order_dff_Scpt:
                            order_df1 = buy_order_liiist1[(buy_order_liiist1['ScripCode'] == ordd1)]                            
                            order = credi_ash.cancel_order(exch_order_id=int(order_df1['ScripCode']))
                        for ordd in order_dff_Scpt:
                            order_df = order_dff[(order_dff['ScripCode'] == ordd)]
                            order = credi_ash.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                            print("Sell order Executed") 
                    except Exception as e:
                        print(e)
                        
            print("Data Analysis Complete for Ashwin")
            print("---------------------------------")

        