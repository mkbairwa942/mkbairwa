
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
#from kite_trade_main import *
import threading
from zoneinfo import ZoneInfo
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta,gamma,rho,theta


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
users = ["MUKESH"]#,"BHAVNA"]#,"ASHWIN","ALPESH"]
credi_muk = None
#credi_bhav = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_muk is None:# and credi_bhav is None:
        try:
            for us in users:
                print("1")
                if us == "MUKESH":
                    credi_muk = credentials("MUKESH")
                    if credi_muk.request_token is None:
                        credi_muk = credentials("MUKESH")
                        print(credi_muk.request_token)
                # if us == "BHAVNA":
                #     credi_bhav = credentials("BHAVNA")
                #     if credi_bhav.request_token is None:
                #         credi_bhav = credentials("BHAVNA")
                #         print(credi_bhav.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_muk]#,credi_bhav]#,credi_ash,credi_alp]
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
fifth_last_trading_day = trading_days[5]
time_change = timedelta(minutes=870) 
upto_df = timedelta(minutes=930) 
new_current_trading_day = current_trading_day + time_change
df_upto_datetime = current_trading_day + upto_df
print(new_current_trading_day)
print(df_upto_datetime)

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

# symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

print("Excel Starting....")

if not os.path.exists("option_data_store.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("Option Chain")
        wb.save("option_data_store.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('option_data_store.xlsx')

for i in ["Symbol","Dashboard","Terminal","EOD Data","Exchange","Fil Exch",]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

symbb = wb.sheets("Symbol")
dash = wb.sheets("Dashboard")
termi = wb.sheets("Terminal")
eod_data = wb.sheets("EOD Data")
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Fil Exch")
oc = wb.sheets("Option Chain")

#symbol1 = '999920005'
stk_list_5paisa = [999920005,999920000]
stk_list_zerodha = [260105,256265]

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

'''
all - scrips across all segments
bse_eq - BSE Equity
nse_eq - NSE Equity
nse_fo - NSE Derivatives
bse_fo - BSE Derivatives
ncd_fo - NSE Currecny
mcx_fo - MCX
'''

segment_fo = "nse_fo"
exc_fo = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment_fo}"
exc_fo1 = pd.read_csv(exc_fo,low_memory=False)
exc_fo1.rename(columns={'ScripType': 'CpType','SymbolRoot': 'Root','BOCOAllowed': 'CO BO Allowed'},inplace=True)
# exc.range("a1").value = exc_fo1

segment_eq = "nse_eq"
exc_eq = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment_eq}"
exc_eq1 = pd.read_csv(exc_eq,low_memory=False)
exc_eq1.rename(columns={'ScripType': 'CpType','SymbolRoot': 'Root','BOCOAllowed': 'CO BO Allowed'},inplace=True)
# flt_exc.range("a1").value = exc_eq1

exchange = None
while True:
    if exchange is None: 
        try:
            exchange_fo = pd.DataFrame(exc_fo1)
            #exchange = exchange[exchange["Exch"] == "N"]
            #exchange = exchange[exchange["ExchType"] == "D"]
            exchange_fo['Expiry1'] = pd.to_datetime(exchange_fo['Expiry']).dt.date
            exchange_fo1 = exchange_fo[(exchange_fo["Exch"] == "N") & (exchange_fo['ExchType'].isin(['D'])) & (exchange_fo['CpType'].isin(['EQ', 'XX']))]
            # exchange1 = exchange[(exchange['ExchType'].isin(['C', 'D']))]
            # exchange1 = exchange1[(exchange1['Series'].isin(['EQ', 'XX']))]
            # exchange2 = exchange[exchange["Series"] == "EQ"]
            #exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]

            exchange_eq = pd.DataFrame(exc_eq1)
            exchange_cash = exchange_eq[(exchange_eq["Exch"] == "N") & (exchange_eq['ExchType'].isin(['C'])) & (exchange_eq["Series"] == "EQ")]
            exchange_all = pd.concat([exchange_fo1, exchange_cash])
            # print(exchange.tail(20))
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)
            
exc.range("a1").value = exchange_fo1
#exc.range("aa1").value = exchange_fo
flt_exc.range("a1").value = exchange_cash
#exc.range("ar1").value = exchange2
df = pd.DataFrame({"FNO Symbol": list(exchange_fo1["Root"].unique())})
df = df.set_index("FNO Symbol",drop=True)
dash.range("a1").value = df
#print(df)

dash.range("d2").value, dash.range("d3").value, dash.range("d4").value, dash.range("d5").value, dash.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",

pre_oc_symbol = pre_oc_expiry = ""
expiries_list = []
instrument_dict = {}
prev_day_oi = {}
stop_thread = False

Option_Chain = "no"
Bid_Ask = "yes"
buy_lst = []
sell_lst = []
orders = "YES"

print("Excel : Started")

while True:
    time.sleep(50)
    xlbooks =xw.sheets.active.name
    print("Current Active Sheet is : "+str(xlbooks))

    try:
        oc_symbol = 'BANKNIFTY'
        oc_expiry = dash.range("e3").value
    except Exception as e:
        print(e)

    if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
        oc.range("g:v").value = None
        instrument_dict = {}
        stop_thread = True
        time.sleep(2)
        if pre_oc_symbol != oc_symbol:
            oc.range("b:b").value = oc.range("d8:e31").value = None
            expiries_list = []
        pre_oc_symbol = oc_symbol
        pre_oc_expiry = oc_expiry
    if oc_symbol is not None:
        
        try:
            if not expiries_list:
                df = copy.deepcopy(exchange_fo)
                df = df[df['Root'] == oc_symbol]
                expiries_list = sorted(list(df["Expiry1"].unique()))
                df = pd.DataFrame({"Expiry Date": expiries_list})
                df = df.set_index("Expiry Date",drop=True)
                dash.range("b1").value = df
        
            if not instrument_dict and oc_expiry is not None:
                print(instrument_dict,oc_expiry)
                df = copy.deepcopy(exchange_fo)
                df = df[df["Root"] == oc_symbol]
                df = df[df["Expiry1"] == oc_expiry.date()]
                print(df.head(1))
                lot_size= list(df["LotSize"])[0]
                # oc.range("e4").value = lot_size
                for i in df.index:
                    instrument_dict[f'NFO:{df["FullName"][i]}'] = {"strikePrice":float(df["StrikeRate"][i]),
                                                                        "instrumentType":df["CpType"][i],
                                                                        "token":df["ScripCode"][i]}
                stop_thread = False
            option_data = {}
            instrument_for_ltp = "NIFTY" if oc_symbol == "NIFTY" else (
                "BANKNIFTY" if oc_symbol == "BANKNIFTY" else oc_symbol)
            underlying_price = (credi_muk.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":instrument_for_ltp}])['Data'][0]['LastTradedPrice'])
            
            ep = []
            for ei in pd.DataFrame((credi_muk.get_expiry("N", oc_symbol))['Expiry'])['ExpiryDate']:
                #print(ei)
                left = ei[6:19]
                timestamp = pd.to_datetime(left, unit='ms')
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
                ep.append([ExpDate, left])

            ep1 = pd.DataFrame(ep)
            ep1.columns = ['ExpDate', 'DayFormat']
            expiry = (ep1['DayFormat'][0])
            opt = pd.DataFrame(credi_muk.get_option_chain("N", oc_symbol, expiry)['Options'])

            CE = []
            PE = []
            for i in opt:
                ce_data = opt[opt['CPType'] == 'CE']
                ce_data = ce_data.sort_values(['StrikeRate'])
                CE.append(ce_data)

                pe_data = opt[opt['CPType'] == 'PE']
                pe_data = pe_data.sort_values(['StrikeRate'])
                PE.append(pe_data)
            option = pd.DataFrame(credi_muk.get_option_chain("N", oc_symbol, expiry)['Options'])

            ce_values1 = option[option['CPType'] == 'CE']
            pe_values1 = option[option['CPType'] == 'PE']
            ce_data = ce_values1.sort_values(['StrikeRate'])
            pe_data = pe_values1.sort_values(['StrikeRate'])
            df1 = pd.merge(ce_data, pe_data, on='StrikeRate')

            df1.rename(
                {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
                'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
                'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
                'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

            df1=(df1[(df1['CE_Ltp'] != 0) & (df1['PE_Ltp'] != 0)])
            df1.index = df1["StrikeRate"]
            df1 = df1.replace(np.nan,0)
            df1["Strike"] = df1.index

            df1.index = [np.nan] * len(df1)

            df1['Call_CHG'] = np.round((100-((df1['CE_Prev_Ltp']*100)/df1['CE_Ltp'])),2)
            df1['Put_CHG'] = np.round((100-((df1['PE_Prev_Ltp']*100)/df1['PE_Ltp'])),2)
            df1['Call_Senti'] = np.where((df1['CE_Chg_OI'] > 0) & (df1['Call_CHG'] > 0) ,"LONG BUILD",
                                            np.where((df1['CE_Chg_OI'] < 0) & (df1['Call_CHG'] < 0),"LONG UNWIND",
                                                    np.where((df1['CE_Chg_OI'] > 0) & (df1['Call_CHG'] < 0),"SHORT BUILD",
                                                            np.where((df1['CE_Chg_OI'] < 0) & (df1['Call_CHG'] > 0),"SHORT UNWIND","NOTHING"))))
            df1['Put_Senti'] = np.where((df1['PE_Chg_OI'] > 0) & (df1['Put_CHG'] > 0),"LONG BUILD",
                            np.where((df1['PE_Chg_OI'] < 0) & (df1['Put_CHG'] < 0),"LONG UNWIND",
                                    np.where((df1['PE_Chg_OI'] > 0) & (df1['Put_CHG'] < 0),"SHORT BUILD",
                                            np.where((df1['PE_Chg_OI'] < 0) & (df1['Put_CHG'] > 0),"SHORT UNWIND","NOTHING"))))
            df1['TimeNow'] = datetime.now()
            df1 = df1[['Call_Senti','CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp','Call_CHG', 'StrikeRate',
                    'Put_CHG','PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script','Put_Senti','TimeNow']]
            
            oc.range("a1").options(index=False).value = df1
            wb.save("option_data_store.xlsx")           
            

        except Exception as e:
            pass   

    # for sht in wb.sheets:
    #     if sht.name != 'Dashboard' and sht.name != 'Fil Exch' and sht.name != 'Exchange' and sht.name != 'Terminal' and sht.name != 'EOD Data':
    #         wb.sheets(sht.name).activate()
    #         wb.sheets(sht.name).api.Range('a1').CurrentRegion.Copy()
    #         # i = 1
    #         # if i == 1:
    #         #     print("A"+str(i))
    #         #     symbb.activate()
    #         #     symbb.range("a"+str(i)).api.PasteSpecial()
    #         # else:
    #         i = symbb.range(1,1).end('down').row+1
    #         print("B"+str(i))  
    #         symbb.activate()
    #         symbb.range("a"+str(i)).api.PasteSpecial()   
    #         print("C"+str(i))  
    #     print("D"+str(i))
    # print("E"+str(i))
    # symbb.activate()
    five = pd.DataFrame() 

    listtu = [1,2]
    for sht in listtu:
        if sht == 1:       
            df_option = pd.read_excel('D:\STOCK\Capital_vercel_new\option_data_store.xlsx',sheet_name='Option Chain')
            five = pd.concat([df_option, five])
        if sht == 2:
            df_Symbol = pd.read_excel('D:\STOCK\Capital_vercel_new\option_data_store.xlsx',sheet_name='Symbol')
            five = pd.concat([df_Symbol, five])
    try:
        if five.empty:
            pass
        else:
            try:
                five.sort_values(['StrikeRate','TimeNow'], ascending=[True,True], inplace=True)
                symbb.range("a1").options(index=False).value = five 
            except Exception as e:
                print(e)
    except Exception as e:
        print(e) 