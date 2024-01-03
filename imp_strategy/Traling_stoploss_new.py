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

users = ["ashwin","haresh"]#,"alpesh"]
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



# def place_trade(User,Exche,ExchTypee,OrderFor,symbol,scripte,quantity,price,direction):
#     try:
#         order = User.place_order(OrderType=direction,
#                         Exchange=Exche,
#                         ExchangeType=ExchTypee,
#                         ScripCode = scripte,
#                         Qty=int(quantity),
#                         Price=price,
#                         IsIntraday=True if OrderFor == "I" else False,)
#                         #IsIntraday=True,
#                         #IsStopLossOrder=True
#                         #StopLossPrice=StopLossPrice)
#         print("CALL PLACE TRADE")
#         print(f"order for {User} :Exche {Exche},ExchTypee {ExchTypee},scripte {scripte}, Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
#         return order
#     except Exception as e:
#         return f"{e}"

# Exchange = None
# prev_info = {"Symbol": None, "Expiry": None}
# instruments_dict = {}
# option_data = {}
 

print("----option chain----")

df_empty_ash = pd.DataFrame()
df_empty_har = pd.DataFrame()

while True: 
    for sh_na in users:
        if sh_na == "ashwin":
            posit = pd.DataFrame(credi_ash.positions()) 
            if posit.empty:
                print("Ashwin's Position is Empty")
                print("--------------------------")
                pass
            else:                
                ash.range("ad1").value = pd.DataFrame(credi_ash.margin())
                ash.range("ad10").value = pd.DataFrame(credi_ash.holdings())
                ash.range("ad20").value = pd.DataFrame(credi_ash.positions()) 

                posit = pd.DataFrame(credi_ash.positions()) 
                posit1 = posit #posit[(posit['MTOM'] != 0)]             
                posit3 = np.unique([int(i) for i in posit1['ScripCode']])
                #print(posit3)

                five_df3 = pd.DataFrame()
                five_df4 = pd.DataFrame()

                for ord in posit3:
                    #time.sleep(0.5)
                    timee = datetime.now()
                    #print(timee)
                    new_df1 = posit1[(posit1['ScripCode'] == ord)]
                    Buy_Name = list(new_df1['ScripName'])[0]
                    Buy_price = float(new_df1['BuyAvgRate'])                 
                    Buy_Stop_Loss = float(round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*stoploss)/100),1))
                    Buy_Target = float(round((((new_df1['BuyAvgRate']*stoploss)/100) + new_df1['BuyAvgRate']),1))
                    Buy_Exc = list(new_df1['Exch'])[0]
                    Buy_Exc_Type = list(new_df1['ExchType'])[0]
                    Buy_Qty = int(new_df1['BuyQty'])    
                    Buy_timee = datetime.now()     

                    Buy_timee = Buy_timee - timedelta(minutes=1)

                    # if Buy_Name == 'DELTACORP 25 Jan 2024 CE 155.00':                            
                    #     Buy_timee = '2024-01-01 14:03:12'
                    # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 485.00':                            
                    #     Buy_timee = '2024-01-01 14:15:18'
                    # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 500.00':                            
                    #     Buy_timee = '2024-01-01 14:33:30'

                    Buy_timee1 = str(Buy_timee).replace(' ','T')
                    
                    dfg1 = credi_ash.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
               
                    dfg1['ScripCode'] = ord
                    dfg1['ScripName'] = Buy_Name
                    dfg1['Entry_Date'] = Buy_timee1
                    dfg1['Entry_Price'] = Buy_price
             
                    dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                    dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                    dfg1['TimeNow'] = datetime.now()
                    
                    dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                    # dfg2['StopLoss'] = Buy_Stop_Loss
                    # dfg2['Benchmark'] = dfg2['High'].cummax()
                    # dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98                             
                    # dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < Buy_Stop_Loss,"SL",""))
                    # dfg2['P&L_TSL'] = np.where(dfg2['Status'] == "SL",(dfg2['StopLoss'] - dfg2['Entry_Price'])*Buy_Qty,np.where(dfg2['Status'] == "TSL",(dfg2['TStopLoss'] - dfg2['Entry_Price'])*Buy_Qty,"" ))

                    # final_df = pd.merge(posit1,dfg2, on=['ScripCode'], how='inner') 

                    # final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                    # final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TGT")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                    # final_df = final_df[['ScripName_x','Exch','ExchType','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','TStopLoss','Status','Benchmark','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]
                    # five_df4 = pd.concat([final_df, five_df4])
  
                    dfg22 = dfg2.tail(1)
                    df_empty_ash = pd.concat([dfg22, df_empty_ash])

                #df_empty_ash.sort_values(['ScripName','Entry_Date',], ascending=[True,True], inplace=True)   

                for ord in posit3:
                    #print(ord)
                    dataframe_new = df_empty_ash[(df_empty_ash['ScripCode'] == ord)]                                      
                    dataframe_new['StopLoss'] = round((dataframe_new['Entry_Price'] - (dataframe_new['Entry_Price']*stoploss)/100),1)
                    dataframe_new['Benchmark'] = dataframe_new['High'].cummax()
                    dataframe_new['TStopLoss'] = dataframe_new['Benchmark'] * 0.98                             
                    dataframe_new['Status'] = np.where(dataframe_new['Close'] < dataframe_new['TStopLoss'],"TSL",np.where(dataframe_new['Close'] < Buy_Stop_Loss,"SL",""))
                    dataframe_new['P&L_TSL'] = np.where(dataframe_new['Status'] == "SL",(dataframe_new['StopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,np.where(dataframe_new['Status'] == "TSL",(dataframe_new['TStopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,"" ))
                    
                    first_row = dataframe_new.head(1)
                    last_row = dataframe_new.tail(1)
                    last_row['Entry_Date'] = first_row['Entry_Date']
                    five_df3 = pd.concat([last_row, five_df3])

                final_df = pd.merge(posit1,five_df3, on=['ScripCode'], how='inner')  
                final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TGT")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                #print(final_df)                         
                final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                final_df.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True)

                #st3.range("a1").options(index=False).value = final_df
                st4.range("a1").options(index=False).value = df_empty_ash
                ash.range("a1").options(index=False).value = final_df


                order_dff = final_df[(final_df['Exit'] == 'SELL')]
                #order_dff = final_df
                if order_dff.empty:
                    print("No Open Position of Ashwin")
                else:
                    order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])
                    for ordd in order_dff_Scpt:
                        order_df = order_dff[(order_dff['ScripCode'] == ordd)]
                        order = credi_ash.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                        print("Sell order Executed") 
                        
            print("Data Analysis Complete for Ashwin")
            print("---------------------------------")

        if sh_na == "haresh":
            posit = pd.DataFrame(credi_har.positions()) 
            if posit.empty:
                print("Haresh's Position is Empty")
                print("--------------------------")
                pass
            else:                
                har.range("ad1").value = pd.DataFrame(credi_har.margin())
                har.range("ad10").value = pd.DataFrame(credi_har.holdings())
                har.range("ad20").value = pd.DataFrame(credi_har.positions()) 

                posit = pd.DataFrame(credi_har.positions()) 
                posit1 = posit #posit[(posit['MTOM'] != 0)]             
                posit3 = np.unique([int(i) for i in posit1['ScripCode']])
                #print(posit3)

                five_df3 = pd.DataFrame()
                five_df4 = pd.DataFrame()

                for ord in posit3:
                    #time.sleep(0.5)
                    timee = datetime.now()
                    #print(timee)
                    new_df1 = posit1[(posit1['ScripCode'] == ord)]
                    Buy_Name = list(new_df1['ScripName'])[0]
                    Buy_price = float(new_df1['BuyAvgRate'])                 
                    Buy_Stop_Loss = float(round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*stoploss)/100),1))
                    Buy_Target = float(round((((new_df1['BuyAvgRate']*stoploss)/100) + new_df1['BuyAvgRate']),1))
                    Buy_Exc = list(new_df1['Exch'])[0]
                    Buy_Exc_Type = list(new_df1['ExchType'])[0]
                    Buy_Qty = int(new_df1['BuyQty'])    
                    Buy_timee = datetime.now()     

                    Buy_timee = Buy_timee - timedelta(minutes=1)

                    # if Buy_Name == 'DELTACORP 25 Jan 2024 CE 155.00':                            
                    #     Buy_timee = '2024-01-01 14:03:12'
                    # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 485.00':                            
                    #     Buy_timee = '2024-01-01 14:15:18'
                    # if Buy_Name == 'GUJGASLTD 25 Jan 2024 CE 500.00':                            
                    #     Buy_timee = '2024-01-01 14:33:30'

                    Buy_timee1 = str(Buy_timee).replace(' ','T')
                    
                    dfg1 = credi_har.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
               
                    dfg1['ScripCode'] = ord
                    dfg1['ScripName'] = Buy_Name
                    dfg1['Entry_Date'] = Buy_timee1
                    dfg1['Entry_Price'] = Buy_price
             
                    dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
                    dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                    dfg1['TimeNow'] = datetime.now()
                    
                    dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
                    # dfg2['StopLoss'] = Buy_Stop_Loss
                    # dfg2['Benchmark'] = dfg2['High'].cummax()
                    # dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98                             
                    # dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < Buy_Stop_Loss,"SL",""))
                    # dfg2['P&L_TSL'] = np.where(dfg2['Status'] == "SL",(dfg2['StopLoss'] - dfg2['Entry_Price'])*Buy_Qty,np.where(dfg2['Status'] == "TSL",(dfg2['TStopLoss'] - dfg2['Entry_Price'])*Buy_Qty,"" ))

                    # final_df = pd.merge(posit1,dfg2, on=['ScripCode'], how='inner') 

                    # final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                    # final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TGT")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                    # final_df = final_df[['ScripName_x','Exch','ExchType','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','TStopLoss','Status','Benchmark','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]
                    # five_df4 = pd.concat([final_df, five_df4])
  
                    dfg22 = dfg2.tail(1)
                    df_empty_har = pd.concat([dfg22, df_empty_har])

                #df_empty_ash.sort_values(['ScripName','Entry_Date',], ascending=[True,True], inplace=True)   

                for ord in posit3:
                    #print(ord)
                    dataframe_new = df_empty_har[(df_empty_har['ScripCode'] == ord)]                                      
                    dataframe_new['StopLoss'] = round((dataframe_new['Entry_Price'] - (dataframe_new['Entry_Price']*stoploss)/100),1)
                    dataframe_new['Benchmark'] = dataframe_new['High'].cummax()
                    dataframe_new['TStopLoss'] = dataframe_new['Benchmark'] * 0.98                             
                    dataframe_new['Status'] = np.where(dataframe_new['Close'] < dataframe_new['TStopLoss'],"TSL",np.where(dataframe_new['Close'] < Buy_Stop_Loss,"SL",""))
                    dataframe_new['P&L_TSL'] = np.where(dataframe_new['Status'] == "SL",(dataframe_new['StopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,np.where(dataframe_new['Status'] == "TSL",(dataframe_new['TStopLoss'] - dataframe_new['Entry_Price'])*Buy_Qty,"" ))
                    
                    first_row = dataframe_new.head(1)
                    last_row = dataframe_new.tail(1)
                    last_row['Entry_Date'] = first_row['Entry_Date']
                    five_df3 = pd.concat([last_row, five_df3])

                final_df = pd.merge(posit1,five_df3, on=['ScripCode'], how='inner')  
                final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
                final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TGT")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
                #print(final_df)                         
                final_df = final_df[['ScripName_x','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
                final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
                final_df.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True)

                #st3.range("a1").options(index=False).value = final_df
                st4.range("a1").options(index=False).value = df_empty_har
                har.range("a1").options(index=False).value = final_df


                order_dff = final_df[(final_df['Exit'] == 'SELL')]
                #order_dff = final_df
                if order_dff.empty:
                    print("No Open Position of Ashwin")
                else:
                    order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])
                    for ordd in order_dff_Scpt:
                        order_df = order_dff[(order_dff['ScripCode'] == ordd)]
                        order = credi_har.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                        print("Sell order Executed") 
                        
            print("Data Analysis Complete for Ashwin")
            print("---------------------------------")