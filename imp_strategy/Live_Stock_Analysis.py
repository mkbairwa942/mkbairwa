
from collections import namedtuple
import pandas_ta as pta
#from finta import TA
from jugaad_data import *
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import date, datetime,timedelta,timezone
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
from five_paisa1 import *
from kite_trade_main import *
import threading
from zoneinfo import ZoneInfo


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
users = ["BHAVNA"]#,"HARESH","MUKESH","ALPESH"]
credi_bhav = None
# credi_har = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_bhav is None:# and credi_ash is None and credi_alp is None:
        try:
            for us in users:
                print("1")
                # if us == "HARESH":
                #     credi_har = credentials("HARESH")
                #     if credi_har.request_token is None:
                #         credi_har = credentials("HARESH")
                #         print(credi_har.request_token)
                # if us == "MUKESH":
                #     credi_muk = credentials("MUKESH")
                #     if credi_muk.request_token is None:
                #         credi_muk = credentials("MUKESH")
                #         print(credi_muk.request_token)
                # if us == "ALPESH":
                #     credi_alp = credentials("ALPESH")
                #     if credi_alp.request_token is None:
                #         credi_alp = credentials("ALPESH")
                #         print(credi_alp.request_token)
                if us == "BHAVNA":
                    credi_bhav = credentials("BHAVNA")
                    if credi_bhav.request_token is None:
                        credi_bhav = credentials("BHAVNA")
                        print(credi_bhav.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_bhav]#,credi_har,credi_muk,credi_alp]
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
# strategy1.range("a:u").value = None
# strategy2.range("a:u").value = None
# strategy3.range("a:u").value = None

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

            five_paisa_exc = script_code_5paisa['Root'].isin(root_list)            
            five_paisa_exc1 = script_code_5paisa[five_paisa_exc]
            five_paisa_exc2 = five_paisa_exc1[(five_paisa_exc1["Exch"] == "N") & (five_paisa_exc1["Series"] == "EQ")]
            break
        except:
            print("Exchange Download Error....")
            time.sleep(5)

new_excc['value'] = new_excc.apply(lambda x: (x.tradingsymbol,x.instrument_token_x, x.instrument_token_y), axis=1)
flt_exc.range("a:w").value = None
flt_exc.range("a1").options(index=False).value = new_excc
#new_excc = new_excc.head(50)

exc.range("a:w").value = None
exc.range("a1").options(index=False).value = five_paisa_exc2

inst_dict = new_excc.set_index(['tradingsymbol','instrument_token_x','instrument_token_y'])['value'].to_dict()
#print(insttt)

#inst_token = np.unique(eq_exc2['instrument_token']).tolist()
#print(inst_token)

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

def order_execution(df,list_append_on,list_to_append,telegram_msg,orders,CALL_PUT,BUY_EXIT,order_side,scrip_code,qtyy,namee):
    

    
    dfg4 = df.tail(1)
    timeess = dfg4['TimeNow'][0]
    timees = timeess.strftime("%d-%m-%Y %H:%M:%S")
    # if stk_name == "BANKNIFTY":
    #     lotsize = 2
    # if stk_name == "NIFTY":
    #     lotsize = 1
    # har_quantity = (qtyy*lotsize)
    # muk_quantity = (qtyy)
    # print(stk_name)
    # print(har_quantity)
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
                order = credi.place_order(OrderType=order_side,Exchange='N',ExchangeType='C', ScripCode = scrip_code, Qty=qtyy,Price=price_of_stock, IsIntraday=False)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
            #order = credi_bhav.place_order(OrderType=order_side,Exchange='N',ExchangeType='C', ScripCode = scrip_code, Qty=muk_quantity,Price=price_of_stock, IsIntraday=True)# IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)    
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

posit = pd.DataFrame(credi_bhav.positions()) 
if posit.empty:
    #print("Position is Empty")
    buy_order_list_dummy = []
    sell_order_list_dummy = []
    buy_root_list_dummy = []
else:
    buy_order = order_book_func(credi_bhav)
    buy_order_li = buy_order[(buy_order['BuySell'] == 'B') & (buy_order['OrderStatus'] == 'Fully Executed')]
    exit_order_li = buy_order[(buy_order['BuySell'] == 'S') & (buy_order['OrderStatus'] == 'Fully Executed')]
    buy_order_list_dummy = (np.unique([str(i) for i in buy_order_li['ScripCode']])).tolist()
    sell_order_list_dummy = (np.unique([str(i) for i in exit_order_li['ScripCode']])).tolist()
    buy_root_list_dummy = (np.unique([str(i) for i in buy_order_li['Root']])).tolist()

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


delv_data = pd.merge(eq_bhav, fo_bhav, on=['Name','Date'], how='inner')
#delv_data.sort_values(['Date', 'Name'], ascending=[False, True], inplace=True)
delv_data = delv_data[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume','Deliv_qty', 'Deliv_per', 'Value', 'OI', 'Chg_OI']]
#strategy3.range("a1").options(index=False).value = delv_data

eod_vol_para = 2
eod_delv_para = 1.5
eod_oi_para = 1.1

juyjyu = pd.DataFrame()
for stkks in inst_dict:
    new_delv_data = delv_data[(delv_data["Name"] == stkks[0])]  
    new_delv_data['Price_Chg'] = round(((new_delv_data['Close'] * 100) / (new_delv_data['Close'].shift(-1)) - 100), 2).fillna(0)      
    new_delv_data['OI_Chg'] = round(((new_delv_data['OI'] * 100) / (new_delv_data['OI'].shift(-1)) - 100), 2).fillna(0)
    new_delv_data['Vol_Chg'] = round(((new_delv_data['Volume'] * 100) / (new_delv_data['Volume'].shift(-1)) - 100), 2).fillna(0) 

    new_delv_data['Price_break'] = np.where((new_delv_data['Close'] > (new_delv_data.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((new_delv_data['Close'] < (new_delv_data.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    new_delv_data['Vol_break'] = np.where(new_delv_data['Volume'] > (new_delv_data.Volume.rolling(5).mean() * eod_vol_para).shift(-5),
                                        "Vol_brk","")  
    new_delv_data['Delv_break'] = np.where(new_delv_data['Deliv_per'] > (new_delv_data.Deliv_per.rolling(5).mean() * eod_delv_para).shift(-5),
                                        "Delv_brk","")  
    new_delv_data['OI_break'] = np.where(new_delv_data['OI'] > (new_delv_data.OI.rolling(5).mean() * eod_oi_para).shift(-5),
                                        "OI_brk","")  
    new_delv_data['Vol_Price_break'] = np.where((new_delv_data['Vol_break'] == "Vol_brk") & (new_delv_data['Price_break'] == "Pri_Up_brk"), "Vol_Pri_Up_break",np.where((new_delv_data['Vol_break'] == "Vol_brk") & (new_delv_data['Price_break'] == "Pri_Dwn_brk"), "Vol_Pri_Dn_break", ""))
    juyjyu = pd.concat([new_delv_data, juyjyu])
juyjyu.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)

strategy3.range("a:s").value = None
strategy3.range("a1").options(index=False).value = juyjyu
print("EOD DATA &  F&O Data Merged")


print(len(juyjyu))
df_lenn = len(juyjyu)
strategy3.range(f'm2:o{df_lenn}').color = (255, 255, 255)
for a in strategy3.range(f'm2:m{df_lenn}'):
    if float(a.value) > 2:
        a.color = (0, 153, 255)
for b in strategy3.range(f'm2:m{df_lenn}'):
    if float(b.value) < -2:
        b.color = (204, 51, 0)
for e in strategy3.range(f'n2:n{df_lenn}'):
    if float(e.value) > 6:
        e.color = (0, 255, 255)
for f in strategy3.range(f'n2:n{df_lenn}'):
    if float(f.value) < -6:
        f.color = (204, 0, 0)
for c in strategy3.range(f'o2:o{df_lenn}'):
    if float(c.value) > 50:
        c.color = (204, 153, 0)
for c in strategy3.range(f'i2:i{df_lenn}'):
    if float(c.value) > 50:
        c.color = (204, 140, 0)

int_vol_para = 2
int_delv_para = 1.5
int_oi_para = 1.03
telegram_msg = "yes"
orders = "yes"

def Down_Stock_Data(period,data):    
    data_fram = pd.DataFrame()
    #for inst in inst_dict:      
    try:
        print(data[0])
        df = pd.DataFrame(credi_muk.historical_data(data[1], last_trading_day, to_d, period, continuous=False, oi=True))
        df1 = pd.DataFrame(credi_muk.historical_data(data[2], last_trading_day, to_d, period, continuous=False, oi=True))
        # print(df.head(1))
        # print(df1.head(1))
        dfgh = pd.merge(df, df1, on=['date'], how='inner')
        data1 = pd.DataFrame(datastk(data[0]))  
        data1["Date"] = df["date"].dt.date 
        dfgh['TimeNow'] = datetime.now(tz=ZoneInfo('Asia/Kolkata'))     
        dfgh['Name'] = data[0]
        dfgh['Minutes'] = dfgh['TimeNow']-df["date"]
        dfgh['Minutes'] = round((dfgh['Minutes']/np.timedelta64(1,'m')),2)
        dfgh['Deliv_per'] = data1[data[0]][0]
        dfgh.sort_values(['Name', 'date'], ascending=[False, False], inplace=True)
        data_fram = pd.concat([dfgh, data_fram])
        #data1 = (data1[['Name','Del_Per']]).reset_index(drop=True)
    except Exception as e:
        print(e)
    #print(data_fram.head(5))
    data_fram = data_fram[['Name','date','open_x','high_x','low_x','close_x','volume_x','oi_y','Deliv_per','TimeNow','Minutes']]
    data_fram.rename(columns={'date': 'DateTime','open_x': 'Open','high_x': 'High','low_x': 'Low','close_x': 'Close','volume_x': 'Volume','oi_y': 'OI',},inplace=True)
    data_fram['Price_Chg'] = round(((data_fram['Close'] * 100) / (data_fram['Close'].shift(-1)) - 100), 2).fillna(0)      

    data_fram['Vol_Chg'] = round(((data_fram['Volume'] * 100) / (data_fram['Volume'].shift(-1)) - 100), 2).fillna(0) 
    data_fram['OI_Chg'] = round(((data_fram['OI'] * 100) / (data_fram['OI'].shift(-1)) - 100), 2).fillna(0)
    data_fram['Price_break'] = np.where((data_fram['Close'] > (data_fram.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((data_fram['Close'] < (data_fram.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    data_fram['Vol_break'] = np.where(data_fram['Volume'] > (data_fram.Volume.rolling(5).mean() * int_vol_para).shift(-5),
                                        "Vol_brk","")  
    data_fram['Delv_break'] = np.where(data_fram['Deliv_per'] > (data_fram.Deliv_per.rolling(5).mean() * int_delv_para).shift(-5),
                                        "Delv_brk","")  
    data_fram['OI_break'] = np.where(data_fram['OI'] > (data_fram.OI.rolling(5).mean() * int_oi_para).shift(-5),
                                        "OI_brk","") 
    data_fram['Vol_Price_break'] = np.where((data_fram['Vol_break'] == "Vol_brk") & (data_fram['Price_break'] == "Pri_Up_brk"), "Vol_Pri_Up_break",np.where((data_fram['Vol_break'] == "Vol_brk") & (data_fram['Price_break'] == "Pri_Dwn_brk"), "Vol_Pri_Dn_break", ""))
    #print(data_fram.head(1))
    #data_fram.sort_values(['Name','DateTime'], ascending=[True,True], inplace=True)
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
            df2 = df1[(df1["Vol_Price_break"] != "") & (df1["Close"] < 500)]# & (df1["Date"] == current_trading_day.date())]
            df3 =  pd.merge(df2, five_paisa_exc2, on=['Name'], how='inner')
            df3 = df3[['Scripcode','Name','DateTime','Open','High','Low','Close','Volume','OI','Deliv_per','TimeNow','Minutes','Price_Chg','Vol_Chg','OI_Chg','Price_break','Vol_break','Delv_break','OI_break','Vol_Price_break']]
            dfg1 = df3.head(1)
            five_df2 = pd.concat([df3, five_df2])

            Call_by_df2 = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_Up_break") & (dfg1["Minutes"] < 5 )]
            if Call_by_df2.empty:
                pass
                #print("Stock Buy DF Empty")
            else:
                #print(Call_by_df2)
                Call_by_ord = Call_by_df2.tail(1)
                Call_by_Closee = (float(Call_by_ord['Close']))
                Call_by_Scripcodee = int(float(Call_by_ord['Scripcode']))
                Call_by_time = str(Call_by_ord['TimeNow'])
                Call_by_Qtyy = round((5000/Call_by_Closee),0)
                Call_by_Name = np.unique([str(i) for i in Call_by_ord['Name']]).tolist()[0]

                #print(Call_by_Closee,Call_by_Scripcodee,Call_by_time,Call_by_Qtyy,Call_by_Name)
                if Call_by_Scripcodee in buy_order_list_dummy: 
                    print(str(Call_by_Name)+" Stock is Already Buy")
                    print("----------------------------------------")
                else:
                    print("Stock Buy")                        
                    rde_exec = order_execution(Call_by_ord,buy_order_list_dummy,Call_by_Scripcodee,telegram_msg,orders,"STOCK","BUY","B",Call_by_Scripcodee,Call_by_Qtyy,Call_by_Name)#,stk_name)
        except Exception as e:
            print(e)

    try:
        if five_df1.empty:
            pass
        else:
            try:
                five_df1.sort_values(['Name','DateTime'], ascending=[True,False], inplace=True)
                st1.range("a:q").value = None
                st1.range("a1").options(index=False).value = five_df1 
            except Exception as e:
                print(e)
        
        if five_df2.empty:
            pass
        else:
            try:
                five_df2.sort_values(['DateTime','Name'], ascending=[False,True], inplace=True)
                st2.range("a:q").value = None
                st2.range("a1").options(index=False).value = five_df2 
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    end = time.time() - start_time
    print(f"Kite Data Download Time: {end:.2f}s")

