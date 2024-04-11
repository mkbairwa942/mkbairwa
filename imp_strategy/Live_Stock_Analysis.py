
from collections import namedtuple
import pandas_ta as pta
#from finta import TA
from jugaad_data import *
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import date, datetime,timedelta
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
from datetime import datetime
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
credi_muk = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_muk is None:# and credi_ash is None and credi_alp is None:
        try:
            for us in users:
                print("1")
                if us == "MUKESH":
                    print(us)
                    credi_muk = KiteApp(mukesh)
                    print("2")

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

cred = [credi_muk]#,credi_ash,credi_alp]
print(cred)

for credi in cred:
    postt = credi
    postt = pd.DataFrame(credi_muk.margins())['equity']['available']['opening_balance']
    print(f"5Paisa Ledger Balance is : {postt}")

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

if not os.path.exists("Live_Stock_Analysis.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Live_Stock_Analysis.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Live_Stock_Analysis.xlsx')
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

#exc.range("a:u").value = None
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


exchange = None
while True:    
    if exchange is None: 
        try:
            exch = master_contract = pd.DataFrame(credi_muk.instruments())
            exch1 = master_contract = pd.DataFrame(credi_muk.instruments("NFO"))
            exch.sort_values(['name'], ascending=[True], inplace=True)
            
            root_list = np.unique(exch1['name']).tolist()
            # print(root_list)
            # print(len(root_list))
            unwanted_num = {"BANKNIFTY","FINNIFTY","MIDCPNIFTY","NIFTY"}
            root_list = [ele for ele in root_list if ele not in unwanted_num]
            #root_list = ["BANKNIFTY","NIFTY"]

            eq_exc = exch['tradingsymbol'].isin(root_list)            
            eq_exc1 = exch[eq_exc]
            eq_exc2 = eq_exc1[(eq_exc1["segment"] == "NSE") & (eq_exc1["exchange"] == "NSE")]# & (exc_new1["instrument_type"] == "EQ")]

            fo_exc = exch['name'].isin(root_list)            
            fo_exc1 = exch[fo_exc]            
            fo_exc2 = fo_exc1[(fo_exc1["segment"] == "NFO-FUT") & (fo_exc1["exchange"] == "NFO")]# & (exc_new1["instrument_type"] == "EQ")]
            Expiry_exc = (np.unique(fo_exc2['expiry']).tolist())[0]
            fo_exc3 = fo_exc2[(fo_exc2["expiry"] == Expiry_exc)]
            fo_exc3.rename(columns={'tradingsymbol': 'name1','name': 'tradingsymbol'},inplace=True) 
            
            new_excc = pd.merge(eq_exc2, fo_exc3, on=['tradingsymbol'], how='inner')

            break
        except:
            print("Exchange Download Error....")
            time.sleep(5)

new_excc['value'] = new_excc.apply(lambda x: (x.tradingsymbol,x.instrument_token_x, x.instrument_token_y), axis=1)
flt_exc.range("a:w").value = None
flt_exc.range("a1").options(index=False).value = new_excc
#new_excc = new_excc.head(5)
inst_dict = new_excc.set_index(['tradingsymbol','instrument_token_x','instrument_token_y'])['value'].to_dict()
#print(insttt)

#inst_token = np.unique(eq_exc2['instrument_token']).tolist()
#print(inst_token)


class NseIndia:

    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple'
                                      'WebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://nseindia.com", headers=self.headers)

    def get_stock_info(self, symbol, trade_info=False):
        if trade_info:
            url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol + "&section=trade_info"
        else:
            url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol
        data = self.session.get(url, headers=self.headers).json()
        return data

nse = NseIndia()

def datastk(symbol):
    # datastk_nse = nse.get_stock_info(symbol.replace("&", "%26"))
    return {symbol.upper(): {"dlv_per":
                                 nse.get_stock_info(symbol.replace("&", "%26"), trade_info=True)['securityWiseDP'][
                                     'deliveryToTradedQuantity']}}


def bhavcopy(lastTradingDay):
    dmyformat = datetime.strftime(lastTradingDay, '%d%m%Y')
    url = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_' + dmyformat + '.csv'
    bhav_eq1 = pd.read_csv(url)
    bhav_eq1 = pd.DataFrame(bhav_eq1)
    bhav_eq1.columns = bhav_eq1.columns.str.strip()
    bhav_eq1 = bhav_eq1.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    bhav_eq1['DATE1'] = pd.to_datetime(bhav_eq1['DATE1'])
    bhav_eq = bhav_eq1[bhav_eq1['SERIES'] == 'EQ']
    bhav_eq['LAST_PRICE'] = bhav_eq['LAST_PRICE'].replace(' -', 0).astype(float)
    bhav_eq['DELIV_QTY'] = bhav_eq['DELIV_QTY'].replace(' -', 0).astype(float)
    bhav_eq['DELIV_PER'] = bhav_eq['DELIV_PER'].replace(' -', 0).astype(float)
    return bhav_eq

# print(bhavcopy(lastTradingDay))

def bhavcopy_fno(lastTradingDay):
    try:
        dmyformat = datetime.strftime(lastTradingDay, '%d%b%Y').upper()
        MMM = datetime.strftime(lastTradingDay, '%b').upper()
        yyyy = datetime.strftime(lastTradingDay, '%Y')
        url1 = 'https://archives.nseindia.com/content/historical/DERIVATIVES/' + yyyy + '/' + MMM + '/fo' + dmyformat + 'bhav.csv.zip'
        content = requests.get(url1)      
        if content.status_code == 200:
            zf = ZipFile(BytesIO(content.content))
            match = [s for s in zf.namelist() if ".csv" in s][0]
            bhav_fo = pd.read_csv(zf.open(match), low_memory=False)
            bhav_fo.columns = bhav_fo.columns.str.strip()
            bhav_fo = bhav_fo.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
            #bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT'])
            bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT']).dt.date
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo = bhav_fo.drop(["Unnamed: 15"], axis=1)
            #print(bhav_fo.head(1))
        else:
            print("No Data Found of Date :- "+str(lastTradingDay))
    except Exception as e:
        print(e)
    return bhav_fo



def bhavcopy_func():
    eq_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            print("Equity Stock Bhavcopy Download od Date :- "+str(i))
            bh_df = bhavcopy(i)
            bh_df = pd.DataFrame(bh_df)
            eq_bhav = pd.concat([bh_df, eq_bhav])
        except Exception as e:
            print(e)

    eq_bhav.sort_values(['SYMBOL', 'DATE1'], ascending=[True, False], inplace=True)
    eq_bhav = eq_bhav[
            ['SYMBOL', 'DATE1', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
            'DELIV_QTY', 'DELIV_PER']]
    eq_bhav.rename(columns={'SYMBOL': 'Name', 'DATE1': 'Date','OPEN_PRICE': 'Open','HIGH_PRICE': 'High', 'LOW_PRICE': 'Low',
                                'CLOSE_PRICE': 'Close','TTL_TRD_QNTY': 'Volume','DELIV_QTY': 'Deliv_qty','DELIV_PER': 'Deliv_per', },inplace=True)
    return eq_bhav

eq_bhav = bhavcopy_func()
strategy1.range("a:i").value = None                          
strategy1.range("a1").options(index=False).value = eq_bhav
#print(str(days_count)+" Days STOCK Data Download")

def bhavcopy_fno_func():
    fo_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            print("F&O Stock Bhavcopy Download od Date :- "+str(i))
            fo_bh_df = bhavcopy_fno(i)
            fo_bh_df = pd.DataFrame(fo_bh_df)             
            fo_bh_df = fo_bh_df[(fo_bh_df["INSTRUMENT"] == "FUTSTK") & (fo_bh_df["EXPIRY_DT"] == Expiry_exc)]
            fo_bhav = pd.concat([fo_bh_df, fo_bhav])
        except Exception as e:
            print(e)
            

    fo_bhav.sort_values(['SYMBOL', 'TIMESTAMP'], ascending=[True, False], inplace=True)
    fo_bhav = fo_bhav[
            ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH',
            'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI','TIMESTAMP']]
    fo_bhav.rename(columns={'SYMBOL': 'Name','TIMESTAMP': 'Date','OPEN_PRICE': 'FO_Open','HIGH_PRICE': 'FO_High', 'LOW_PRICE': 'FO_Low','CLOSE_PRICE': 'FO_Close','TTL_TRD_QNTY': 'FO_Volume','VAL_INLAKH':'Value','OPEN_INT':'OI','CHG_IN_OI':'Chg_OI' },inplace=True)
    return fo_bhav

fo_bhav = bhavcopy_fno_func()
#print(fo_bhav.dtypes)
strategy2.range("a:i").value = None                          
strategy2.range("a1").options(index=False).value = fo_bhav
#print(str(days_count)+" Days F&O Data Download")

delv_data = pd.merge(eq_bhav, fo_bhav, on=['Name','Date'], how='inner')
#delv_data.sort_values(['Date', 'Name'], ascending=[False, True], inplace=True)
delv_data = delv_data[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume','Deliv_qty', 'Deliv_per', 'Value', 'OI', 'Chg_OI']]
#strategy3.range("a1").options(index=False).value = delv_data

juyjyu = pd.DataFrame()
for stkks in inst_dict:
    new_delv_data = delv_data[(delv_data["Name"] == stkks[0])]  
    new_delv_data['Price_Chg'] = round(((new_delv_data['Close'] * 100) / (new_delv_data['Close'].shift(-1)) - 100), 2).fillna(0)      

    new_delv_data['Vol_Chg'] = round(((new_delv_data['Volume'] * 100) / (new_delv_data['Volume'].shift(-1)) - 100), 2).fillna(0) 
    new_delv_data['OI_Chg'] = round(((new_delv_data['OI'] * 100) / (new_delv_data['OI'].shift(-1)) - 100), 2).fillna(0)
    new_delv_data['Price_Break'] = np.where((new_delv_data['Close'] > (new_delv_data.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((new_delv_data['Close'] < (new_delv_data.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    new_delv_data['Vol_Break'] = np.where(new_delv_data['Volume'] > (new_delv_data.Volume.rolling(5).mean() * 1.5).shift(-5),
                                        "Vol_brk","")  
    new_delv_data['Delv_Break'] = np.where(new_delv_data['Deliv_per'] > (new_delv_data.Deliv_per.rolling(5).mean() * 1.5).shift(-5),
                                        "Delv_brk","")  
    new_delv_data['OI_Break'] = np.where(new_delv_data['OI'] > (new_delv_data.OI.rolling(5).mean() * 1.2).shift(-5),
                                        "OI_brk","")  
    juyjyu = pd.concat([new_delv_data, juyjyu])
juyjyu.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
strategy3.range("a1").options(index=False).value = juyjyu
print("EOD DATA &  F&O Data Merged")

def Down_Stock_Data(period,data):    
    data_fram = pd.DataFrame()
    #for inst in inst_dict:      
    try:
        print(data[0])
        df = pd.DataFrame(credi_muk.historical_data(data[1], last_trading_day, to_d, period, continuous=False, oi=True))
        df1 = pd.DataFrame(credi_muk.historical_data(data[2], last_trading_day, to_d, period, continuous=False, oi=True))
        dfgh = pd.merge(df, df1, on=['date'], how='inner')
        data1 = pd.DataFrame(datastk(data[0]))   
        dfgh['TimeNow'] = datetime.now()     
        dfgh['Name'] = data[0]
        dfgh['Del_Per'] = data1[data[0]][0]
        data_fram = pd.concat([dfgh, data_fram])
        #data1 = (data1[['Name','Del_Per']]).reset_index(drop=True)
    except Exception as e:
        print(e)

    data_fram = data_fram[['Name','date','open_x','high_x','low_x','close_x','volume_x','oi_y','Del_Per','TimeNow']]
    data_fram.rename(columns={'date': 'DateTime','open_x': 'Open','high_x': 'High','low_x': 'Low','close_x': 'Close','volume_x': 'Volume','oi_y': 'OI',},inplace=True)
    data_fram.sort_values(['Name','DateTime'], ascending=[True,True], inplace=True)
    return data_fram

while True:
    start_time = time.time()
    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    for inst in inst_dict:      
        try:
            df1 = Down_Stock_Data("5minute",inst)
            five_df1 = pd.concat([df1, five_df1]) 
        except Exception as e:
            print(e)


    try:
        if five_df1.empty:
            pass
        else:
            try:
                st1.range("a:j").value = None
                st1.range("a1").options(index=False).value = five_df1 
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    end = time.time() - start_time
    print(f"Kite Data Download Time: {end:.2f}s")






# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exchange = None
# while True:    
#     if exchange is None: 
#         try:
#             exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
#             exch.sort_values(['Root'], ascending=[True], inplace=True)
            
#             root_list = np.unique(exch['Root']).tolist()
            
#             root_list = ["BANKNIFTY","NIFTY"]

#             exc_new = exch['Root'].isin(root_list)
            
#             exc_new1 = exch[exc_new]
#             eq_exc = exc_new1[(exc_new1["Exch"] == "N") & (exc_new1["ExchType"] == "C") & (exc_new1["CpType"] == "EQ")]
#             exc.range("a1").options(index=False).value = eq_exc
#             Expiry = exc_new1[(exc_new1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
#             Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
#             exc_new2 = Expiry
#             exc_new2.rename(columns={'Scripcode': 'ScripCode' },inplace=True)
#             exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(5)

# flt_exc.range("a:az").value = None
# flt_exc.range("a1").options(index=False).value = exc_new2

# #symbol1 = '999920005'
# stk_list = [999920005,999920000]

# telegram_msg = "yes"
# orders = "yes"
# Capital = 20000
# StockPriceLessThan = 1000
# Buy_price_buffer = 2
# Vol_per = 15
# UP_Rsi_lvl = 60
# DN_Rsi_lvl = 40
# adx_parameter = 0.20
# adx_parameter_opt = 0.60
# sam_21_slop = 1.5
# dema_21_slope = 2
# slll = -900
# tgtt = 3000
# lotsize = 2

# SLL = 10
# TSL = 10
# tsl1 = 1-(TSL/100)
# print(tsl1)

# st.range("ac1").value = "Orders"
# st.range("ae1").value = "Tele_Msg"
# st.range("ad1").value = "YES"
# st.range("af1").value = "YES"




# def order_book_func(cred):
#     try:
#         ordbook = pd.DataFrame(cred.order_book())
#         ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
#         #ordbook[['Root']] = ordbook['ScripName'].str.split(' ',expand=True)
#         #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
#         pos.range("r1").options(index=False).value = ordbook
        
#     except Exception as e:
#                 print(e)

#     try:
#         if ordbook is not None:
#             ordbook['Root'] = [x.split(' ')[-0] for x in ordbook['ScripName']]
#             #ordbook['Root'] = ordbook['ScripName'].tolist()#.str.split(" ")[0]
#             #print("Order Book not Empty")        
#             ordbook1 = ordbook[ordbook['OrderStatus'] != "Rejected By 5P"]   
#             ordbook1 = ordbook           
#             Datetimeee = []
#             for i in range(len(ordbook1)):
#                 datee = ordbook1['BrokerOrderTime'][i]
#                 timestamp = pd.to_datetime(datee[6:19], unit='ms')
#                 ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M')
#                 d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]))
#                 d2 = d1 + timedelta(hours = 5.5)
#                 Datetimeee.append(d2)
#             ordbook1['Datetimeee'] = Datetimeee
#             ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot','ExchOrderID','OrderStatus', 'OrderValidUpto','ScripName','Root','AtMarket']]
#             ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
#             pos.range("a1").options(index=False).value = ordbook1
#         else:
#             print("Order Book Empty")
#     except Exception as e:
#                 print(e)
#     return ordbook1

# def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,namee,stk_name):
#     timees = list_to_append

    
#     dfg4 = df.tail(1)
#     if stk_name == "BANKNIFTY":
#         lotsize = 2
#     if stk_name == "NIFTY":
#         lotsize = 1
#     har_quantity = (qtyy*lotsize)
#     muk_quantity = (qtyy)
#     # print(stk_name)
#     # print(har_quantity)
#     # dfg3 = df
#     # dfg3 = dfg3.astype({"Datetime": "datetime64"})   
    
#     # dfg3['Entry_Date'] = timees
#     # dfg3['OK_DF'] = np.where(dfg3['Entry_Date'] == dfg3['Datetime'],"OK","")
#     # dfg4 = dfg3[(dfg3["OK_DF"] == "OK")]
#     # print(timees)
#     # print(dfg4)
#     if dfg4.empty:
#         print("No Data")
#     else:
#         if order_side == "B":
#             price_of_stoc = float(dfg4['Close'])
#             # buff = (price_of_stoc*Buy_price_buffer)/100
#             # price_of_stock = round((price_of_stoc+buff),1)
#             # print(price_of_stoc)
#             # print(buff)
#             # print(price_of_stock)
#             price_of_stock = price_of_stoc
#         else:
#             price_of_stock = float(dfg4['Close']) 
#         # timee = str((dfg3['Datetime'].values)[0])[0:19] 
#         # timee1= timee.replace("T", " " )
#         print("1")
#         list_append_on.append(list_to_append)

#         if orders.upper() == "YES" or orders.upper() == "":  
#             for credi in cred:
#                 #postt = pd.DataFrame(credi.margin())['Ledgerbalance'][0]
#                 #print(f"Ledger Balance is : {postt}") 
#                 order = credi.place_order(OrderType=order_side,Exchange='N',ExchangeType='D', ScripCode = scrip_code, Qty=har_quantity,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
#             order = credi_bhav.place_order(OrderType=order_side,Exchange='N',ExchangeType='D', ScripCode = scrip_code, Qty=muk_quantity,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)    
#         else:
#             print(f"Real {CALL_PUT} Order are OFF")
#         print(f"1 Minute {CALL_PUT} Data Selected of "+str(namee)+" ("+str(scrip_code)+")")
#         print(f"{CALL_PUT} {BUY_EXIT} Order Executed of "+str(namee)+" at : Rs "+str(price_of_stock)+" and Quantity is "+str(qtyy)+" on "+str(timees))

#         print("SYMBOL : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timees))
#         if telegram_msg.upper() == "YES" or telegram_msg.upper() == "":
#             parameters1 = {"chat_id" : "6143172607","text" : "Symbol : "+str(namee)+"\n "+str(CALL_PUT)+" "+str(BUY_EXIT)+" AT : "+str(price_of_stock)+"\n QUANTITY : "+str(qtyy)+"\n TIME : "+str(timees)}
#             resp = requests.get(telegram_basr_url, data=parameters1)
#         else:
#             print("Telegram Message are OFF")
#         print("----------------------------------------")

# def data_download(stk_nm,vol_pr,rsi_up_lvll,rsi_dn_lvll):
#     df = credi_bhav.historical_data('N', 'C', stk_nm, '1m', second_last_trading_day,current_trading_day)
#     #print(df.head(5))
#     df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
#     df = df.astype({"Datetime": "datetime64"})
#     df['Name'] = np.where(stk_nm == 999920005,"BANKNIFTY",np.where(stk_nm == 999920000,"NIFTY",""))
#     df['Price_break'] = np.where((df['Close'] > (df.High.rolling(5).max()).shift(-5)),
#                                         'Pri_Up_brk',
#                                         (np.where((df['Close'] < (df.Low.rolling(5).min()).shift(-5)),
#                                                     'Pri_Dwn_brk', "")))
#     df['Vol_break'] = np.where(df['Volume'] > (df.Volume.rolling(5).mean() * vol_pr).shift(-5),
#                                         "Vol_brk","") 
#     df['SMA_21'] = np.round((pta.sma(df['Close'],length=9)),2)
#     df['DEMA_21'] = np.round((pta.dema(df['Close'],length=9)),2)
#     ADX = pta.adx(high=df['High'],low=df['Low'],close=df['Close'],length=14)    
#     df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)     
#     df['Adx_diff'] = df['ADX_14'] - df['ADX_14'].shift(1)
#     df['Adx_ok'] = np.where(df['Adx_diff'] > adx_parameter,"ok","")
#     #print(df.tail(5))
#     df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)   
#     df['Rsi_OK'] = np.where((df["RSI_14"].shift(-1)) > rsi_up_lvll,"Rsi_Up_OK",np.where((df["RSI_14"].shift(-1)) < rsi_dn_lvll,"Rsi_Dn_OK",""))
#     df['SMA_21_diff'] = df['SMA_21'] - df['SMA_21'].shift(1)
#     df['DEMA_21_diff'] = df['DEMA_21'] - df['DEMA_21'].shift(1)     
#     df['SMA_21_ok'] = np.where(df['SMA_21_diff'] > sam_21_slop,"up_ok",np.where(df['SMA_21_diff'] < -sam_21_slop,"dn_ok",""))
#     df['DEMA_21_ok'] = np.where(df['DEMA_21_diff'] > dema_21_slope,"up_ok",np.where(df['DEMA_21_diff'] < -dema_21_slope,"dn_ok",""))
#     df['CROSS'] = np.where(df['DEMA_21'] > df['SMA_21'],"up_ok",np.where(df['DEMA_21'] < df['SMA_21'],"dn_ok",""))
#     df['Signal'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "up_ok") & (df['DEMA_21_ok'] == "up_ok") & (df['CROSS'] == "up_ok"),"Call_Buy","Call_Exit")
#     df['Signal1'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "dn_ok") & (df['DEMA_21_ok'] == "dn_ok") & (df['CROSS'] == "dn_ok"),"Put_Buy","Put_Exit")
#     # df['Signal'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "up_ok") & (df['DEMA_21_ok'] == "up_ok"),"Call_Buy","Call_Exit")
#     # df['Signal1'] = np.where((df['Adx_ok'] == "ok") & (df['SMA_21_ok'] == "dn_ok") & (df['DEMA_21_ok'] == "dn_ok"),"Put_Buy","Put_Exit")
#     df['Cand_Col'] = np.where(df['Close'] > df['Open'],"Green",np.where(df['Close'] < df['Open'],"Red","") ) 
#     df['TimeNow'] = datetime.now()
#     df = df.astype({"Datetime": "datetime64[ns]"})    
#     df["Date"] = df["Datetime"].dt.date
#     df['Minutes'] = df['TimeNow']-df["Datetime"]
#     df['Minutes'] = round((df['Minutes']/np.timedelta64(1,'m')),2) 
#     #print(df.head(5))
#     df.sort_values(['Datetime'], ascending=[True], inplace=True)
#     #print(df.head(5))
#     return df

# posit = pd.DataFrame(credi_bhav.positions()) 
# if posit.empty:
#     #print("Position is Empty")
#     buy_order_list_dummy = []
#     sell_order_list_dummy = []
#     buy_root_list_dummy = []
# else:
#     buy_order = order_book_func(credi_bhav)
#     buy_order_li = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Fully Executed')]
#     exit_order_li = buy_order[(buy_order['BuySell'] == 'S') & (buy_order['OrderStatus'] == 'Fully Executed')]
#     buy_order_list_dummy = (np.unique([str(i) for i in buy_order_li['Datetimeee']])).tolist()
#     sell_order_list_dummy = (np.unique([str(i) for i in exit_order_li['Datetimeee']])).tolist()
#     buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()

# while True:
#     orders,telegram_msg = st.range("ad1").value,st.range("af1").value
#     if orders is None:
#         orders = "yes"
#     if telegram_msg is None:
#         telegram_msg = "yes"
#     # print(buy_order_list_dummy)
#     # print(sell_order_list_dummy)
#     print(orders,telegram_msg)
#     start_time = time.time()
#     five_df1 = pd.DataFrame()
#     five_df2 = pd.DataFrame()
#     five_df3 = pd.DataFrame()
#     five_df4 = pd.DataFrame()
#     five_df5 = pd.DataFrame()

#     for credi in cred:        
#         if posit.empty:
#             pass
#         else:
#             buy_order = order_book_func(credi_bhav)
#             buy_order_li1 = buy_order[(buy_order['OrderStatus'] == 'Pending')]
#             if buy_order_li1.empty:
#                 pass
#             else:
#                 exc_order_id = (np.unique([int(i) for i in buy_order_li1['ExchOrderID']])).tolist()[0] 
#                 print(exc_order_id)
#                 cancel_bulk=[{"ExchOrderID": f"{exc_order_id}"}]
#                 credi.cancel_bulk_order(cancel_bulk)
#                 buy_order_list_dummy = []

#     try:      
#         for sc in stk_list:
#             dfg1 = data_download(sc,Vol_per,UP_Rsi_lvl,DN_Rsi_lvl) 
#             stk_name = (np.unique([str(i) for i in dfg1['Name']])).tolist()[0] 
#             print(stk_name)
#             #print(ADX(dfg1))
#             dfg1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
#             dfg111 = dfg1[(dfg1["Date"] == current_trading_day.date())]
#             dfg1112 = dfg111.tail(10)
#             five_df1 = pd.concat([dfg1, five_df1]) 


#             Call_by_df = dfg1[(dfg1["Signal"] == "Call_Buy")]
#             Call_by_df['Date_Dif'] = abs((Call_by_df["Datetime"] - Call_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
#             Call_by_df['Entry'] = np.where(Call_by_df['Date_Dif'] > 5, "Call_Buy","")
#             Call_by_df1 = Call_by_df[(Call_by_df['Entry'] == "Call_Buy")]
#             Call_by_df1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)           
#             five_df2 = pd.concat([Call_by_df1, five_df2])
            
#             Call_by_df2 = Call_by_df1[(Call_by_df1["Date"] == current_trading_day.date()) & (Call_by_df1["Minutes"] < 5 )]   

#             if Call_by_df2.empty:
#                 pass
#                 #print("Call Buy DF Empty")
#             else:
#                 Call_by_ord = Call_by_df2.tail(1)
#                 Call_by_Closee = (float(Call_by_ord['Close']))
#                 Call_by_Spot = round(Call_by_Closee/100,0)*100
#                 Call_by_time = str(list(Call_by_ord['Datetime'])[0])
#                 Call_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
#                 Call_by_ord2 = Call_by_ord1[(Call_by_ord1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
#                 Expiryyy_Call_by = (np.unique(Call_by_ord2['Expiry']).tolist())[0]      
#                 Call_by_ord3 = Call_by_ord2[Call_by_ord2['Expiry'] == Expiryyy_Call_by]
#                 Call_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
#                 Call_by_ord4 = Call_by_ord3[(Call_by_ord3["CpType"] == 'CE')] 
#                 Call_by_ord5 = Call_by_ord4[(Call_by_ord4['StrikeRate'] < Call_by_Spot)] 
#                 Call_by_ord6 = Call_by_ord5.tail(1)
#                 Call_by_Name = np.unique([str(i) for i in Call_by_ord6['Name']]).tolist()[0]
#                 Call_by_Scripcodee = int(float(Call_by_ord6['ScripCode']))
#                 Call_by_Qtyy = int(np.unique(Call_by_ord6['LotSize']))

#                 print(Call_by_Scripcodee,Call_by_Qtyy,Call_by_time)
#                 #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
#                 if not Call_by_ord6.empty:                    
#                     dfg1_Call_by = credi_bhav.historical_data('N', 'D', Call_by_Scripcodee, '1m', second_last_trading_day,current_trading_day)
#                     ADX = pta.adx(high=dfg1_Call_by['High'],low=dfg1_Call_by['Low'],close=dfg1_Call_by['Close'],length=14)    
#                     dfg1_Call_by['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)     
#                     dfg1_Call_by['Adx_diff'] = dfg1_Call_by['ADX_14'] - dfg1_Call_by['ADX_14'].shift(1)
#                     dfg1_Call_by['Adx_ok'] = np.where(dfg1_Call_by['Adx_diff'] > adx_parameter_opt,"ok","")
#                     #print(dfg1_Call_by.tail(5))
#                     dfg1_Call_by1 = dfg1_Call_by.tail(1)
#                     dfg1_Call_by2 = dfg1_Call_by1[(dfg1_Call_by1["Adx_ok"] == "ok")]

#                     if dfg1_Call_by2.empty:
#                         print("No Call Buy Position Activate")
#                     else:
#                         if Call_by_time in buy_order_list_dummy: 
#                             print(str(stk_name)+" Call is Already Buy")
#                             print("----------------------------------------")
#                         else:
#                             print("Call Buy")                        
#                             rde_exec = order_execution(dfg1_Call_by2,buy_order_list_dummy,Call_by_time,telegram_msg,orders,"IDX OPT","CALL BUY","B",Call_by_Scripcodee,Call_by_Qtyy,Call_by_Name,stk_name)
                    
#             Put_by_df = dfg1[(dfg1["Signal1"] == "Put_Buy")]
#             Put_by_df['Date_Dif'] = abs((Put_by_df["Datetime"] - Put_by_df["Datetime"].shift(1)).astype('timedelta64[m]'))
#             Put_by_df['Entry'] = np.where(Put_by_df['Date_Dif'] > 5, "Put_Buy","")
#             Put_by_df1 = Put_by_df[Put_by_df['Entry'] == "Put_Buy"]
#             Put_by_df1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True) 
#             five_df3 = pd.concat([Put_by_df1, five_df3]) 

#             Put_by_df2 = Put_by_df1[(Put_by_df1["Date"] == current_trading_day.date()) & (Put_by_df1["Minutes"] < 5 )]          
#             if Put_by_df2.empty:
#                 pass
#                 #print("Put Buy DF Empty")
#             else:   
#                 Put_by_ord = Put_by_df2.tail(1)
#                 Put_by_Closee = (float(Put_by_ord['Close']))
#                 Put_by_Spot = round(Put_by_Closee/100,0)*100
#                 Put_by_time = str(list(Put_by_ord['Datetime'])[0])
#                 Put_by_ord1 = exc_new2[exc_new2['Root'] == stk_name]
#                 Put_by_ord2 = Put_by_ord1[(Put_by_ord1['Expiry'].apply(pd.to_datetime) > new_current_trading_day)]
#                 Expiryyy_Put_by = (np.unique(Put_by_ord2['Expiry']).tolist())[0]  
#                 Put_by_ord3 = Put_by_ord2[Put_by_ord2['Expiry'] == Expiryyy_Put_by]
#                 Put_by_ord3.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)
#                 Put_by_ord4 = Put_by_ord3[(Put_by_ord3["CpType"] == 'PE')] 
#                 Put_by_ord5 = Put_by_ord4[(Put_by_ord4['StrikeRate'] > Put_by_Spot)] 
#                 Put_by_ord6 = Put_by_ord5.head(1)    
#                 Put_by_Name = np.unique([str(i) for i in Put_by_ord6['Name']]).tolist()[0]  
#                 Put_by_Scripcodee = int(float(Put_by_ord6['ScripCode']))
#                 Put_by_Qtyy = int(np.unique(Put_by_ord6['LotSize']))
                
#                 print(Put_by_Scripcodee,Put_by_Qtyy,Put_by_time)
#                 #order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,Buy_At,namee)
                
#                 if not Put_by_ord6.empty:
#                     dfg1_Put_by = credi_bhav.historical_data('N', 'D', Put_by_Scripcodee, '1m', second_last_trading_day,current_trading_day)
#                     ADX = pta.adx(high=dfg1_Put_by['High'],low=dfg1_Put_by['Low'],close=dfg1_Put_by['Close'],length=14)    
#                     dfg1_Put_by['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)     
#                     dfg1_Put_by['Adx_diff'] = dfg1_Put_by['ADX_14'] - dfg1_Put_by['ADX_14'].shift(1)
#                     dfg1_Put_by['Adx_ok'] = np.where(dfg1_Put_by['Adx_diff'] > adx_parameter_opt,"ok","")
#                     #print(dfg1_Put_by.tail(5))
#                     dfg1_Put_by1 = dfg1_Put_by.tail(1)
#                     dfg1_Put_by2 = dfg1_Put_by1[(dfg1_Put_by1["Adx_ok"] == "ok")]

#                     if dfg1_Put_by2.empty:
#                         print("No Put Buy Position Activate")
#                     else:
#                         if Put_by_time in buy_order_list_dummy: 
#                             print(str(stk_name)+" Put is Already Buy")
#                             print("----------------------------------------")
#                         else:
#                             print("Put Buy")                        
#                             rde_exec = order_execution(dfg1_Put_by2,buy_order_list_dummy,Put_by_time,telegram_msg,orders,"IDX OPT","PUT BUY","B",Put_by_Scripcodee,Put_by_Qtyy,Put_by_Name,stk_name)

#             posi = pd.DataFrame(credi_bhav.positions()) 
#             #print(posi)
#             if posi.empty:            
#                 print("No First Running Position")
#             else:
#                 posit = posi[(posi['MTOM'] != 0)]        
#                 if posit.empty:
#                     print("No Current Running Position")
#                 else:
#                     buy_order_li = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Fully Executed')]
#                     #print(buy_order_li)
#                     new_df = pd.merge(buy_order_li, posi, on=['ScripCode'], how='inner')
#                     new_df.sort_values(['Datetimeee'], ascending=[False], inplace=True)
#                     new_df1 = new_df.head(1)
#                     Ratee = (np.unique([float(i) for i in new_df1['Rate']])).tolist()[0]
#                     LTPP = (np.unique([float(i) for i in new_df1['LTP']])).tolist()[0]
#                     Qtty1 = (np.unique([float(i) for i in new_df1['Qty']])).tolist()[0]
                    

#                     # print(new_df)
#                     print("Last Buy Rate is : "+str(Ratee))
#                     print("Last LTP Rate is : "+str(LTPP))
                    

#                     # pl = (np.unique([int(i) for i in posit['MTOM']])).tolist()[0]
#                     Qtty=int(posit['LotSize'])
#                     pl = round(((LTPP-Ratee)*Qtty1),2)
#                     print("Last PL Rate is : "+str(pl))
#                     print(Qtty)
#                     if Qtty == 50:
#                         slll = -200
#                         tgtt = 1000
#                     if Qtty == 15:
#                         slll = -400
#                         tgtt = 2000
#                     print(slll,tgtt)
#                     if pl < slll or pl > tgtt:
#                         order = credi_bhav.place_order(OrderType='S',Exchange=list(posit['Exch'])[0],ExchangeType=list(posit['ExchType'])[0], ScripCode = int(posit['ScripCode']), Qty=int(posit['BuyQty'])-int(posit['SellQty']),Price=float(posit['LTP']),IsIntraday=True if list(posit['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
#                         #order = credi_bhav.place_order(OrderType='S',Exchange=list(posit['Exch'])[0],ExchangeType=list(posit['ExchType'])[0], ScripCode = int(posit['ScripCode']), Qty=int(posit['LotSize']),Price=float(posit['LTP']),IsIntraday=True if list(posit['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
#                         print("StopLoss is Greater than -900")
#                         print("Sell stoplOSS order Executed")
#                     else:
#                         posit3 = (np.unique([int(i) for i in posit['ScripCode']])).tolist()  
#                         buy_order_li = order_book_func(credi_bhav)             
#                         for ord in posit3:
#                             buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B')]# & (buy_order_li['AveragePrice'] != 0)]
#                             buy_order_liiist = buy_order_liiist[['Datetimeee','ScripCode']] 
#                             new_df11 = posit[(posit['ScripCode'] == ord)]
#                             new_df1 = pd.merge(buy_order_liiist, new_df11, on=['ScripCode'], how='inner')
#                             Buy_Name = list(new_df1['ScripName'])[0]
#                             Buy_price = (np.unique([float(i) for i in new_df1['BuyAvgRate']])).tolist()[0]    
#                             Buy_Stop_Loss = (round((new_df1['BuyAvgRate'] - (new_df1['BuyAvgRate']*SLL)/100),1)).astype(float)
#                             Buy_Target = (round((((new_df1['BuyAvgRate']*SLL)/100) + new_df1['BuyAvgRate']),1)).astype(float)
#                             Buy_Exc = list(new_df1['Exch'])[0]
#                             Buy_Exc_Type = list(new_df1['ExchType'])[0]
#                             Buy_Qty = new_df1['BuyQty'] - new_df1['SellQty']
#                             Buy_timee = list(new_df1['Datetimeee'])[0]
#                             Buy_timee1 = str(Buy_timee).replace(' ','T')  
                            
#                             dfg1 = credi_bhav.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ord, '1m',last_trading_day,current_trading_day)
#                             #print(dfg1.head(1))
#                             dfg1['ScripCode'] = ord
#                             dfg1['ScripName'] = Buy_Name
#                             dfg1['Entry_Date'] = Buy_timee1
#                             dfg1['Entry_Price'] = Buy_price
                            
#                             dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
#                             dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
                            
#                             dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
#                             dfg2['StopLoss'] = round((dfg2['Entry_Price'] - (dfg2['Entry_Price']*SLL)/100),1)

#                             dfg2['Benchmark'] = dfg2['High'].cummax()
#                             dfg2['TStopLoss'] = dfg2['Benchmark'] * tsl1  
#                             dfg2['Status'] = np.where(dfg2['Close'] < dfg2['TStopLoss'],"TSL",np.where(dfg2['Close'] < dfg2['StopLoss'],"SL",""))
        
#                             five_df4 = pd.concat([dfg2, five_df4])
#                             dfg3 = dfg2[(dfg2["Status"] == "TSL") | (dfg2["Status"] == "SL")]                       

#                             if dfg3.empty:
#                                 dfg3 = dfg2.tail(1)
                                
#                             dfg22 = dfg3.head(1)

#                             final_df = pd.merge(posit,dfg22, on=['ScripCode'], how='inner')  
#                             final_df['Entry'] = np.where((final_df['MTOM'] != 0) & (final_df['BuyQty'] != 0) & (final_df['MTOM'] != "") & (final_df['BuyQty'] != ""),"BUY","")
#                             final_df['Exit'] = np.where(((final_df['Entry'] == "BUY") & (final_df['Status'] == "TSL")) | ((final_df['Entry'] == "BUY") & (final_df['Status'] == "SL")),"SELL","")
#                             #print(final_df.head(1))
#                             final_df = final_df[['ScripName_x','LotSize','Exch','ExchType','OrderFor','ScripCode','Entry_Date','Datetime','BuyValue','BuyAvgRate','SellAvgRate','StopLoss','Benchmark','TStopLoss','Status','LTP','BookedPL','MTOM','BuyQty','Entry','Exit']]	   
#                             final_df.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
#                             #print(final_df.head(1))
#                             final_df.sort_values(['Entry_Date'], ascending=[True], inplace=True)
#                             five_df5 = pd.concat([final_df, five_df5])
                            
#                             order_dff = final_df[(final_df['Exit'] == 'SELL')]

#                             if order_dff.empty:
#                                 print("No Target And Stoploss Hit")
#                             else:
#                                 try: 
#                                     buy_order_liiist = buy_order_li[(buy_order_li['BuySell'] == 'B')]# & (buy_order_li['AveragePrice'] != 0)]
#                                     #print(buy_order_liiist)
#                                     order_dff_Scpt = np.unique([int(i) for i in order_dff['ScripCode']])

#                                     # if order_dff['Root'][0] == "NIFTY":
#                                     #     quant = 50 
#                                     # if order_dff['Root'][0] == "BANKNIFTY":
#                                     #     quant = 15
#                                     for ordd in order_dff_Scpt:
#                                         order_df = order_dff[(order_dff['ScripCode'] == ordd)]
#                                         order = credi_bhav.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['BuyQty']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
#                                         #order = credi_bhav.place_order(OrderType='S',Exchange=list(order_df['Exch'])[0],ExchangeType=list(order_df['ExchType'])[0], ScripCode = int(order_df['ScripCode']), Qty=int(order_df['LotSize']),Price=float(order_df['LTP']),IsIntraday=True if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
#                                         print("Sell order Executed") 
#                                 except Exception as e:
#                                     print(e)
#     except Exception as e:
#         print(e) 
    
#         print("------------------------------------------------") 

#     try:
#         if five_df1.empty:
#             pass
#         else:
#             try:
#                 st.range("a1").options(index=False).value = five_df1 
#             except Exception as e:
#                 print(e)

#         if five_df2.empty:
#             pass
#         else:
#             try:
#                 by.range("a1").options(index=False).value = five_df2
#             except Exception as e:
#                 print(e)

#         if five_df3.empty:
#             pass
#         else:
#             try:
#                 by.range("a50").options(index=False).value = five_df3
#             except Exception as e:
#                 print(e)
        
#         if five_df4.empty:
#             pass
#         else:
#             try:
#                 fl_data.range("a1").options(index=False).value = five_df4
#             except Exception as e:
#                 print(e)
        
#         if five_df5.empty:
#             pass
#         else:
#             try:
#                 st1.range("a1").options(index=False).value = five_df5
#             except Exception as e:
#                 print(e)

#     except Exception as e:
#         print(e) 
