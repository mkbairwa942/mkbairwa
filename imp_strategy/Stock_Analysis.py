
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



users = ["MUKESH"]
credi_muk = None

while True:
    if credi_muk is None:
        try:
            for us in users:
                print("1")
                if us == "MUKESH":
                    credi_muk = credentials("MUKESH")
                    if credi_muk.request_token is None:
                        credi_muk = credentials("MUKESH")
                        print(credi_muk.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_muk]
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

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

print("Excel Starting....")

if not os.path.exists("Stock_Analysis.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("Option Chain")
        wb.save("Stock_Analysis.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Stock_Analysis.xlsx')

for i in ["Symbol","Dashboard","Terminal","Option Greeks","EOD Data","Exchange","Fil Exch",]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

eod_data = wb.sheets("EOD Data")
symbb = wb.sheets("Symbol")
dash = wb.sheets("Dashboard")
termi = wb.sheets("Terminal")
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Fil Exch")
oc = wb.sheets("Option Chain")
ocg = wb.sheets("Option Greeks")

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
oc.range("a1").value = df
ocg.range("a1").value = df
oc.range("b1").value = pd.DataFrame({"Trading_days": list(trading_days)})

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value, oc.range("d5").value, oc.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",
ocg.range("d2").value, ocg.range("d3").value, ocg.range("d4").value, ocg.range("d5").value, ocg.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",

def bhavcopy(lastTradingDay):
    dmyformat = datetime.strftime(lastTradingDay, '%d%m%Y')
    print("11")
    ddd = datetime.strftime(lastTradingDay, '%d')
    MMM = datetime.strftime(lastTradingDay, '%b')#.upper()
    yyyy = datetime.strftime(lastTradingDay, '%Y')
    print("22")
    url = 'https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_' + dmyformat + '.csv'
    url1 = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22Full%20Bhavcopy%20and%20Security%20Deliverable%20data%22%2C%22type%22%3A%22daily-reports%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equities&mode=single'
    print(url)
    print("33")
    bhav_eq1 = pd.read_csv(url)
    print(bhav_eq1.head(1))
    print("44")
    bhav_eq1 = pd.DataFrame(bhav_eq1)
    print("55")
    bhav_eq1.columns = bhav_eq1.columns.str.strip()
    bhav_eq1 = bhav_eq1.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    bhav_eq1['DATE1'] = pd.to_datetime(bhav_eq1['DATE1'])
    bhav_eq = bhav_eq1[bhav_eq1['SERIES'] == 'EQ']
    bhav_eq['LAST_PRICE'] = bhav_eq['LAST_PRICE'].replace(' -', 0).astype(float)
    bhav_eq['DELIV_QTY'] = bhav_eq['DELIV_QTY'].replace(' -', 0).astype(float)
    bhav_eq['DELIV_PER'] = bhav_eq['DELIV_PER'].replace(' -', 0).astype(float)
    print("55")
    return bhav_eq

def bhavcopy_fno(lastTradingDay):
    try:
        dmyformat = datetime.strftime(lastTradingDay, '%d%b%Y').upper()
        ddd = datetime.strftime(lastTradingDay, '%d')
        MMM = datetime.strftime(lastTradingDay, '%b')#.upper()
        yyyy = datetime.strftime(lastTradingDay, '%Y')
        #url1 = 'https://archives.nseindia.com/content/historical/DERIVATIVES/' + yyyy + '/' + MMM + '/fo' + dmyformat + 'bhav.csv.zip'
        # url1 = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22F%26O%20-%20Bhavcopy%20(fo.zip)%22%2C%22type%22%3A%22archives%22%2C%22category%22%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equity&mode=single'
        # url1 = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22F%26O%20-%20UDiFF%20Common%20Bhavcopy%20Final%20(zip)%22%2C%22type%22%3A%22archives%22%2C%22category%22%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equity&mode=single'
        url1 = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22F%26O%20-%20UDiFF%20Common%20Bhavcopy%20Final%20(zip)%22%2C%22type%22%3A%22archives%22%2C%22category%22%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equity&mode=single'
        content = requests.get(url1)  
        print(content.status_code)   
        if content.status_code == 200:
            print("Data Found of Date :- "+str(lastTradingDay))
            zf = ZipFile(BytesIO(content.content))
            match = [s for s in zf.namelist() if ".csv" in s][0]
            bhav_fo = pd.read_csv(zf.open(match), low_memory=False)
            bhav_fo.columns = bhav_fo.columns.str.strip()
            bhav_fo = bhav_fo.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
            #bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT'])
            bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT']).dt.date
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo = bhav_fo.drop(["Unnamed: 15"], axis=1)
            print(bhav_fo.head(1))
        else:
            print("No Data Found of Date :- "+str(lastTradingDay))
    except Exception as e:
        print(e)
    return bhav_fo

def bhavcopy_func():
    eq_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            print("Equity Stock Bhavcopy Download of Date :- "+str(i))
            print("1")
            bh_df = bhavcopy(i)
            print("2")
            bh_df = pd.DataFrame(bh_df)
            print("3")
            eq_bhav = pd.concat([bh_df, eq_bhav])
            print("4")
        except Exception as e:
            print(e)

    eq_bhav.sort_values(['SYMBOL', 'DATE1'], ascending=[True, False], inplace=True)
    eq_bhav = eq_bhav[
            ['SYMBOL', 'DATE1', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
            'DELIV_QTY', 'DELIV_PER']]
    eq_bhav.rename(columns={'SYMBOL': 'Name', 'DATE1': 'Date','OPEN_PRICE': 'Open','HIGH_PRICE': 'High', 'LOW_PRICE': 'Low',
                                'CLOSE_PRICE': 'Close','TTL_TRD_QNTY': 'Volume','DELIV_QTY': 'Deliv_qty','DELIV_PER': 'Deliv_per', },inplace=True)
    return eq_bhav

# def bhavcopy_fno_func():
#     fo_bhav = pd.DataFrame()
#     for i in trading_days:
#         try:
#             print("F&O Stock Bhavcopy Download of Date :- "+str(i))
#             fo_bh_df = bhavcopy_fno(i)
#             fo_bh_df = pd.DataFrame(fo_bh_df)  
   
#             fo_bh_df1 = fo_bh_df[(fo_bh_df["INSTRUMENT"] == "FUTSTK")]  
            
              
#             #fo_bh_df = fo_bh_df[(fo_bh_df["INSTRUMENT"] == "FUTSTK") & (fo_bh_df["EXPIRY_DT"] == Expiry_exc)]
#             fo_bhav = pd.concat([fo_bh_df1, fo_bhav])
#         except Exception as e:
#             print(e)
            
#     fo_bhav1 = fo_bhav[((fo_bhav['EXPIRY_DT'].apply(pd.to_datetime) > current_trading_day))]
#     Expiry_exc = (np.unique(fo_bhav1['EXPIRY_DT']).tolist())[0]
#     fo_bhav2 = fo_bhav1[((fo_bhav1['EXPIRY_DT'] == Expiry_exc))]
#     fo_bhav2.sort_values(['SYMBOL', 'TIMESTAMP'], ascending=[True, False], inplace=True)
#     fo_bhav2 = fo_bhav2[
#             ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH',
#             'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI','TIMESTAMP']]
#     fo_bhav2.rename(columns={'SYMBOL': 'Name','TIMESTAMP': 'Date','OPEN_PRICE': 'FO_Open','HIGH_PRICE': 'FO_High', 'LOW_PRICE': 'FO_Low','CLOSE_PRICE': 'FO_Close','TTL_TRD_QNTY': 'FO_Volume','VAL_INLAKH':'Value','OPEN_INT':'OI','CHG_IN_OI':'Chg_OI' },inplace=True)
#     return fo_bhav2

print("Excel : Started")

eq_bhav = bhavcopy_func()
print("Done")
eod_data.range("a1").options(index=False).value = eq_bhav

# while True:
# #def optionchain():
#     xlbooks =xw.sheets.active.name
#     print("Current Active Sheet is : "+str(xlbooks))

#     if xlbooks == "EOD Data":
#         eq_bhav = bhavcopy_func()
#         fo_bhav = bhavcopy_fno_func()

#         delv_data = pd.merge(eq_bhav, fo_bhav, on=['Name','Date'], how='outer')
#         delv_data = delv_data[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume','Deliv_qty', 'Value', 'OI', 'Chg_OI','Deliv_per']]
#         delv_data.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
#         eod_data.range("a1").options(index=False).value = delv_data

#         symb_list = (np.unique(delv_data['Name']).tolist())
#         #print(symb_list)

#         eod_vol_para = 2
#         eod_delv_para = 1.5
#         eod_oi_para = 1.1

#         stk_df = pd.DataFrame()
#         for stkks in symb_list:
#             print(stkks)
#             new_delv_data = delv_data[(delv_data["Name"] == stkks)]  
#             new_delv_data['Price_Chg'] = round((((new_delv_data['Close'] * 100) / (new_delv_data['Close'].shift(-1))) - 100), 2).fillna(0)      
#             new_delv_data['OI_Chg'] = round((((new_delv_data['OI'] * 100) / (new_delv_data['OI'].shift(-1))) - 100), 2).fillna(0)
#             new_delv_data['Vol_Chg'] = round((((new_delv_data['Volume'] * 100) / (new_delv_data['Volume'].shift(-1))) - 100), 2).fillna(0) 

#             new_delv_data['Price_break'] = np.where((new_delv_data['Close'] > (new_delv_data.High.rolling(5).max()).shift(-5)),
#                                                 'Pri_Up_brk',
#                                                 (np.where((new_delv_data['Close'] < (new_delv_data.Low.rolling(5).min()).shift(-5)),
#                                                             'Pri_Dwn_brk', "")))
#             new_delv_data['Vol_break'] = np.where(new_delv_data['Volume'] > (new_delv_data.Volume.rolling(5).mean() * eod_vol_para).shift(-5),
#                                                 "Vol_brk","")  
#             new_delv_data['Delv_break'] = np.where(new_delv_data['Deliv_per'] > (new_delv_data.Deliv_per.rolling(5).mean() * eod_delv_para).shift(-5),
#                                                 "Delv_brk","")  
#             new_delv_data['OI_break'] = np.where(new_delv_data['OI'] > (new_delv_data.OI.rolling(5).mean() * eod_oi_para).shift(-5),
#                                                 "OI_brk","")  
#             new_delv_data['Vol_Price_break'] = np.where((new_delv_data['Vol_break'] == "Vol_brk") & (new_delv_data['Price_break'] == "Pri_Up_brk"), "Vol_Pri_Up_break",np.where((new_delv_data['Vol_break'] == "Vol_brk") & (new_delv_data['Price_break'] == "Pri_Dwn_brk"), "Vol_Pri_Dn_break", ""))
#             stk_df = pd.concat([new_delv_data, stk_df])
#         stk_df.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
#         stk_df1 = stk_df[~stk_df.duplicated(subset=['Name', 'Date'], keep='last')].copy()

#         #eod_data.range("a:t").value = None
#         eod_data.range("a1").options(index=False).value = stk_df1
#         print("EOD DATA & F&O Data Merged")
#     else:
#         print("EOD Data is OFF")  

