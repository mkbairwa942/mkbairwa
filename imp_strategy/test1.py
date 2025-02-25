
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
users = ["MUKESH","BHAVNA"]#,"ASHWIN","ALPESH"]
credi_muk = None
credi_bhav = None
# credi_ash = None
# credi_alp = None

while True:
    if credi_muk is None and credi_bhav is None:
        try:
            for us in users:
                print("1")
                if us == "MUKESH":
                    credi_muk = credentials("MUKESH")
                    if credi_muk.request_token is None:
                        credi_muk = credentials("MUKESH")
                        print(credi_muk.request_token)
                if us == "BHAVNA":
                    credi_bhav = credentials("BHAVNA")
                    if credi_bhav.request_token is None:
                        credi_bhav = credentials("BHAVNA")
                        print(credi_bhav.request_token)
            break
        except:
            print("credentials Download Error....")
            time.sleep(5)

cred = [credi_muk,credi_bhav]#,credi_ash,credi_alp]
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

if not os.path.exists("AutoTrender.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("Option Chain")
        wb.save("AutoTrender.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('AutoTrender.xlsx')

for i in ["Symbol","Dashboard","Option Greeks","EOD Data","Exchange","Fil Exch","World Market","Nifty 50 Rnaking","F&O Ranking","Stocks Positional",
          "Auto","Auto Ancillaries","Capital Goods","Cements","FMCG","IT","Insurance","Metals","NBFC","Chemicals","Consumer Durables",
          "Oil & Gas","MidCap","Pharma","Power","Private Banks","PSU Banks","Reality","Telecom",
          "Buy Senti > 60","Sell Senti > 60"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

eod_data = wb.sheets("EOD Data")
symbb = wb.sheets("Symbol")
dash = wb.sheets("Dashboard")
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Fil Exch")
oc = wb.sheets("Option Chain")
ocg = wb.sheets("Option Greeks")

wor_mar = wb.sheets("World Market")
nif_50_rank = wb.sheets("Nifty 50 Rnaking")
f_o_rank = wb.sheets("F&O Ranking")
stk_pos = wb.sheets("Stocks Positional")

auto = wb.sheets("Auto")
auto_anc = wb.sheets("Auto Ancillaries")
cap_good = wb.sheets("Capital Goods")
ceme = wb.sheets("Cements")
fmcg = wb.sheets("FMCG")
it = wb.sheets("IT")
insu = wb.sheets("Insurance")
metal = wb.sheets("Metals")
nbfc = wb.sheets("NBFC")
chemi = wb.sheets("Chemicals")
con_dur = wb.sheets("Consumer Durables")
oil_gas = wb.sheets("Oil & Gas")
phar = wb.sheets("Pharma")
power = wb.sheets("Power")
pri_bank = wb.sheets("Private Banks")
psu_bank = wb.sheets("PSU Banks")
reality = wb.sheets("Reality")
telecom = wb.sheets("Telecom")

buy_senti = wb.sheets("Buy Senti > 60")
sell_senti = wb.sheets("Sell Senti > 60")

wor_mar.range("a:u").value = None
nif_50_rank.range("a:u").value = None
f_o_rank.range("a:u").value = None
stk_pos.range("a:u").value = None

auto.range("a:u").value = None
auto_anc.range("a:u").value = None
cap_good.range("a:u").value = None
ceme.range("a:u").value = None
fmcg.range("a:u").value = None
it.range("a:u").value = None
insu.range("a:u").value = None
metal.range("a:u").value = None
nbfc.range("a:u").value = None
chemi.range("a:u").value = None
con_dur.range("a:u").value = None
oil_gas.range("a:u").value = None
phar.range("a:u").value = None
power.range("a:u").value = None
pri_bank.range("a:u").value = None
psu_bank.range("a:u").value = None
reality.range("a:u").value = None
telecom.range("a:u").value = None

buy_senti.range("a:u").value = None
sell_senti.range("a:u").value = None
# oc.range("a:b").value = oc.range("d8:e30").value = oc.range("g1:v4000").value = None
# ocg.range("a:b").value = ocg.range("d8:e30").value = ocg.range("g1:af4000").value = None

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
            exchange_fo1 = exchange_fo[(exchange_fo["Exch"] == "N") & (exchange_fo['ExchType'].isin(['D']))]# & (exchange_fo['CpType'].isin(['EQ', 'XX']))]
            # exchange1 = exchange[(exchange['ExchType'].isin(['C', 'D']))]
            # exchange1 = exchange1[(exchange1['Series'].isin(['EQ', 'XX']))]
            # exchange2 = exchange[exchange["Series"] == "EQ"]
            #exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]

            exchange_eq = pd.DataFrame(exc_eq1)
            exchange_cash = exchange_eq[(exchange_eq["Exch"] == "N") & (exchange_eq['ExchType'].isin(['C'])) & (exchange_eq["Series"] == "EQ")]
            # print(exchange.tail(20))
            exchange_all = pd.concat([exchange_fo1, exchange_cash])
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

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value, oc.range("d5").value, oc.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",
ocg.range("d2").value, ocg.range("d3").value, ocg.range("d4").value, ocg.range("d5").value, ocg.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",

df = pd.DataFrame({"FNO Symbol": list(exchange_fo1["Root"].unique())})
df = df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = df
ocg.range("a1").value = df

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
            print("Equity Stock Bhavcopy Download of Date :- "+str(i))
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

def bhavcopy_fno_func():
    fo_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            print("F&O Stock Bhavcopy Download of Date :- "+str(i))
            fo_bh_df = bhavcopy_fno(i)
            fo_bh_df = pd.DataFrame(fo_bh_df)  
   
            fo_bh_df1 = fo_bh_df[(fo_bh_df["INSTRUMENT"] == "FUTSTK")]  
            
              
            #fo_bh_df = fo_bh_df[(fo_bh_df["INSTRUMENT"] == "FUTSTK") & (fo_bh_df["EXPIRY_DT"] == Expiry_exc)]
            fo_bhav = pd.concat([fo_bh_df1, fo_bhav])
        except Exception as e:
            print(e)
            
    fo_bhav1 = fo_bhav[((fo_bhav['EXPIRY_DT'].apply(pd.to_datetime) > current_trading_day))]
    Expiry_exc = (np.unique(fo_bhav1['EXPIRY_DT']).tolist())[0]
    fo_bhav2 = fo_bhav1[((fo_bhav1['EXPIRY_DT'] == Expiry_exc))]
    fo_bhav2.sort_values(['SYMBOL', 'TIMESTAMP'], ascending=[True, False], inplace=True)
    fo_bhav2 = fo_bhav2[
            ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH',
            'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI','TIMESTAMP']]
    fo_bhav2.rename(columns={'SYMBOL': 'Name','TIMESTAMP': 'Date','OPEN_PRICE': 'FO_Open','HIGH_PRICE': 'FO_High', 'LOW_PRICE': 'FO_Low','CLOSE_PRICE': 'FO_Close','TTL_TRD_QNTY': 'FO_Volume','VAL_INLAKH':'Value','OPEN_INT':'OI','CHG_IN_OI':'Chg_OI' },inplace=True)
    return fo_bhav2

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
#def optionchain():
    xlbooks =xw.sheets.active.name
    print("Current Active Sheet is : "+str(xlbooks))

    if xlbooks == "Option Chain":
    #global pre_oc_symbol,pre_oc_expiry
        try:
            oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
        except Exception as e:
            print(e)
        # if oc_symbol is None:
        #     pre_oc_symbol = pre_oc_expiry = ""

        if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
            oc.range("g:z").value = None
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
                    #print(df)
                    #df = df[(df['Expiry1'].apply(pd.to_datetime) >= current_trading_day)]
                    expiries_list = sorted(list(df["Expiry1"].unique()))
                    #print(expiries_list)
                    df = pd.DataFrame({"Expiry Date": expiries_list})
                    df = df.set_index("Expiry Date",drop=True)
                    oc.range("b1").value = df
            
                if not instrument_dict and oc_expiry is not None:
                    print(instrument_dict,oc_expiry)
                    df = copy.deepcopy(exchange_fo)
                    df = df[df["Root"] == oc_symbol]
                    df = df[df["Expiry1"] == oc_expiry.date()]
                    print(df.head(1))
                    lot_size= list(df["LotSize"])[0]
                    oc.range("e4").value = lot_size
                    print("1")
                    for i in df.index:
                        instrument_dict[f'NFO:{df["FullName"][i]}'] = {"strikePrice":float(df["StrikeRate"][i]),
                                                                            "instrumentType":df["CpType"][i],
                                                                            "token":df["ScripCode"][i]}
                    stop_thread = False
                    # thread = threading.Thread(target=get_oi,args=(instrument_dict,))
                    # thread.start()
                option_data = {}
                instrument_for_ltp = "NIFTY" if oc_symbol == "NIFTY" else (
                    "BANKNIFTY" if oc_symbol == "BANKNIFTY" else oc_symbol)
                underlying_price = (credi_muk.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":instrument_for_ltp}])['Data'][0]['LastTradedPrice'])
                print("2")
                
                ep = []
                for ei in pd.DataFrame((credi_muk.get_expiry("N", oc_symbol))['Expiry'])['ExpiryDate']:
                    #print(ei)
                    left = ei[6:19]
                    timestamp = pd.to_datetime(left, unit='ms')
                    ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
                    ep.append([ExpDate, left])

                ep1 = pd.DataFrame(ep)
                ep1.columns = ['ExpDate', 'DayFormat']
                expiryy = ep1[pd.to_datetime(ep1["ExpDate"],infer_datetime_format=True) == oc_expiry]
                expiry = (int(expiryy['DayFormat']))
                expiry_new = (expiryy['ExpDate'])

                print(expiry,expiry_new)

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
                print(oc_symbol,expiry)
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
                #dash.range("g1").value = df1

                input_list = list(df1['CE_Volume'])
                input_list1 = list(df1['StrikeRate'])
                max_value = max(input_list)
                index = input_list.index(max_value)
                diff = input_list1[index+1]-input_list1[index]

                CE_Chg_OII = sum(df1["CE_Chg_OI"])
                PE_Chg_OII = sum(df1["PE_Chg_OI"])
                pcr = round((PE_Chg_OII/CE_Chg_OII),2)

                stk_code1 = exchange_cash[exchange_cash["Root"] == oc_symbol]
                stk_code = int(float(stk_code1['ScripCode']))

                dff = credi_muk.historical_data('N', 'C', stk_code, '5m', second_last_trading_day,current_trading_day)
                dff1 = dff.tail(5)
                maxe = []
                mine = []
                open = list(dff1['Open'])
                close = list(dff1['Close'])
                max_value = max(open)
                maxe.append(max_value)
                min_value = min(open)
                mine.append(min_value)
                max_value1 = max(close)
                maxe.append(max_value1)
                min_value1 = min(close)
                mine.append(min_value1)
                maxe1 = max(maxe)
                mine1 = min(mine)             
                rangee = round((maxe1-mine1),2)
                print(rangee)

                oc.range("d8").value = [["PCR TODAY",pcr],
                                        ["Spot LTP",underlying_price],
                                        ["Spot LTP Round",round(underlying_price/diff,0)*diff],
                                        ["Strike Difference",diff],
                                        ["Last 5 Candle Range is",rangee],
                                        ["",""],
                                        ["Total Call OI",sum(list(df1["CE_OI"]))],
                                        ["Total Put OI",sum(list(df1["PE_OI"]))],
                                        ["Total Call Change in OI",sum(list(df1["CE_Chg_OI"]))],
                                        ["Total Put Change in OI",sum(list(df1["PE_Chg_OI"]))],
                                        ["",""],            
                                        ["Max Call OI Strike",list(df1[df1["CE_OI"] == max(list(df1["CE_OI"]))]["Strike"])[0]],
                                        ["Max Put OI Strike",list(df1[df1["PE_OI"] == max(list(df1["PE_OI"]))]["Strike"])[0]],
                                        ["Max Call Change in OI Strike",list(df1[df1["CE_Chg_OI"] == max(list(df1["CE_Chg_OI"]))]["Strike"])[0]],
                                        ["Max Put Change in OI Strike",list(df1[df1["PE_Chg_OI"] == max(list(df1["PE_Chg_OI"]))]["Strike"])[0]],
                                        ["Max Call Volume Strike",list(df1[df1["CE_Volume"] == max(list(df1["CE_Volume"]))]["Strike"])[0]],
                                        ["Max Put Volume Strike",list(df1[df1["PE_Volume"] == max(list(df1["PE_Volume"]))]["Strike"])[0]],
                                        ["",""], 
                                        ["Max Call OI",max(list(df1["CE_OI"]))],
                                        ["Max Put OI",max(list(df1["PE_OI"]))],          
                                        ["Max Call Change in OI",max(list(df1["CE_Chg_OI"]))],
                                        ["Max Put Change in OI",max(list(df1["PE_Chg_OI"]))],   
                                        ["Max Call Volume",max(list(df1["CE_Volume"]))],
                                        ["Max Put Volume",max(list(df1["PE_Volume"]))],  
                                        ]

                #df1['Call_Senti'] = np.where()
                #print(df1.head(1))
                df1['Call_CHG'] = 100-((df1['CE_Prev_Ltp']*100)/df1['CE_Ltp'])
                df1['Put_CHG'] = 100-((df1['PE_Prev_Ltp']*100)/df1['PE_Ltp'])
                df1['Call_Senti'] = np.where((df1['CE_Chg_OI'] > 0) & (df1['Call_CHG'] > 0) ,"LONG BUILD",
                                             np.where((df1['CE_Chg_OI'] < 0) & (df1['Call_CHG'] < 0),"LONG UNWIND",
                                                      np.where((df1['CE_Chg_OI'] > 0) & (df1['Call_CHG'] < 0),"SHORT BUILD",
                                                               np.where((df1['CE_Chg_OI'] < 0) & (df1['Call_CHG'] > 0),"SHORT UNWIND",""))))
                df1['Put_Senti'] = np.where((df1['PE_Chg_OI'] > 0) & (df1['Put_CHG'] > 0),"LONG BUILD",
                                np.where((df1['PE_Chg_OI'] < 0) & (df1['Put_CHG'] < 0),"LONG UNWIND",
                                        np.where((df1['PE_Chg_OI'] > 0) & (df1['Put_CHG'] < 0),"SHORT BUILD",
                                                np.where((df1['PE_Chg_OI'] < 0) & (df1['Put_CHG'] > 0),"SHORT UNWIND",""))))
                #print(df1.head(1))
                # df1 = df1[['CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                #         'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
                df1 = df1[['Call_Senti','CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp','Call_CHG', 'StrikeRate',
                        'Put_CHG','PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script','Put_Senti']]
                oc.range("g1").value = df1


                #stk_code = exchange_fo[exchange_fo['']]

            
     
            except Exception as e:
                pass   
    else:
        print("Option Chain is OFF")
    
    # if xlbooks == "Option Chain":


    # else:
    #     print("Option Chain is OFF")
  

    if xlbooks == "Option Greeks":
    #global pre_oc_symbol,pre_oc_expiry
        try:
            oc_symbol,oc_expiry = ocg.range("e2").value,ocg.range("e3").value
        except Exception as e:
            print(e)
        # if oc_symbol is None:
        #     pre_oc_symbol = pre_oc_expiry = ""

        if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
            ocg.range("g:af").value = None
            instrument_dict = {}
            stop_thread = True
            time.sleep(2)
            if pre_oc_symbol != oc_symbol:
                ocg.range("b:b").value = ocg.range("d8:e30").value = None
                expiries_list = []
            pre_oc_symbol = oc_symbol
            pre_oc_expiry = oc_expiry
        if oc_symbol is not None:
            
            try:
                if not expiries_list:
                    df = copy.deepcopy(exchange_fo)
                    df = df[df['Root'] == oc_symbol]
                    #print(df)
                    #df = df[(df['Expiry1'].apply(pd.to_datetime) >= current_trading_day)]
                    expiries_list = sorted(list(df["Expiry1"].unique()))
                    #print(expiries_list)
                    df = pd.DataFrame({"Expiry Date": expiries_list})
                    df = df.set_index("Expiry Date",drop=True)
                    ocg.range("b1").value = df
            
                if not instrument_dict and oc_expiry is not None:
                    print(instrument_dict,oc_expiry)
                    df = copy.deepcopy(exchange_fo)
                    df = df[df["Root"] == oc_symbol]
                    df = df[df["Expiry1"] == oc_expiry.date()]
                    print(df.head(1))
                    lot_size= list(df["LotSize"])[0]
                    ocg.range("e4").value = lot_size
                    print("1")
                    for i in df.index:
                        instrument_dict[f'NFO:{df["FullName"][i]}'] = {"strikePrice":float(df["StrikeRate"][i]),
                                                                            "instrumentType":df["CpType"][i],
                                                                            "token":df["ScripCode"][i]}
                    stop_thread = False
                    # thread = threading.Thread(target=get_oi,args=(instrument_dict,))
                    # thread.start()
                option_data = {}
                instrument_for_ltp = "NIFTY" if oc_symbol == "NIFTY" else (
                    "BANKNIFTY" if oc_symbol == "BANKNIFTY" else oc_symbol)
                underlying_price = (credi_muk.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":instrument_for_ltp}])['Data'][0]['LastTradedPrice'])
                print("2")
                ep = []
                for ei in pd.DataFrame((credi_muk.get_expiry("N", oc_symbol))['Expiry'])['ExpiryDate']:
                    #print(ei)
                    left = ei[6:19]
                    timestamp = pd.to_datetime(left, unit='ms')
                    ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
                    ep.append([ExpDate, left])

                ep1 = pd.DataFrame(ep)
                ep1.columns = ['ExpDate', 'DayFormat']
                expiryy = ep1[pd.to_datetime(ep1["ExpDate"],infer_datetime_format=True) == oc_expiry]
                expiry = (int(expiryy['DayFormat']))
                expiry_new = (expiryy['ExpDate'])

                print(expiry,expiry_new)
                opt = pd.DataFrame(credi_muk.get_option_chain("N", oc_symbol, expiry)['Options'])
                underlying_price = (credi_muk.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"}])['Data'][0]['LastTradedPrice'])
                print(underlying_price)
                CE = []
                PE = []
                for i in opt:
                    ce_data = opt[opt['CPType'] == 'CE']
                    ce_data = ce_data.sort_values(['StrikeRate'])
                    CE.append(ce_data)

                    pe_data = opt[opt['CPType'] == 'PE']
                    pe_data = pe_data.sort_values(['StrikeRate'])
                    PE.append(pe_data)
                print(oc_symbol,expiry)
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
                #dash.range("g1").value = df1

                input_list = list(df1['CE_Volume'])
                input_list1 = list(df1['StrikeRate'])
                max_value = max(input_list)
                index = input_list.index(max_value)
                diff = input_list1[index+1]-input_list1[index]

                CE_Chg_OII = sum(df1["CE_Chg_OI"])
                PE_Chg_OII = sum(df1["PE_Chg_OI"])
                pcr = round((PE_Chg_OII/CE_Chg_OII),2)

                stk_code1 = exchange_cash[exchange_cash["Root"] == oc_symbol]
                stk_code = int(float(stk_code1['ScripCode']))

                dff = credi_muk.historical_data('N', 'C', stk_code, '5m', second_last_trading_day,current_trading_day)
                dff1 = dff.tail(5)
                maxe = []
                mine = []
                open = list(dff1['Open'])
                close = list(dff1['Close'])
                max_value = max(open)
                maxe.append(max_value)
                min_value = min(open)
                mine.append(min_value)
                max_value1 = max(close)
                maxe.append(max_value1)
                min_value1 = min(close)
                mine.append(min_value1)
                maxe1 = max(maxe)
                mine1 = min(mine)             
                rangee = round((maxe1-mine1),2)
                print(rangee)

                ocg.range("d20").value = [["PCR TODAY",pcr],
                                        ["Spot LTP",underlying_price],
                                        ["Spot LTP Round",round(underlying_price/diff,0)*diff],
                                        ["Strike Difference",diff],
                                        ["Last 5 Candle Range is",rangee],
                                        ["",""],
                                        ["Total Call OI",sum(list(df1["CE_OI"]))],
                                        ["Total Put OI",sum(list(df1["PE_OI"]))],
                                        ["Total Call Change in OI",sum(list(df1["CE_Chg_OI"]))],
                                        ["Total Put Change in OI",sum(list(df1["PE_Chg_OI"]))],
                                        ["",""],            
                                        ["Max Call OI Strike",list(df1[df1["CE_OI"] == max(list(df1["CE_OI"]))]["Strike"])[0]],
                                        ["Max Put OI Strike",list(df1[df1["PE_OI"] == max(list(df1["PE_OI"]))]["Strike"])[0]],
                                        ["Max Call Change in OI Strike",list(df1[df1["CE_Chg_OI"] == max(list(df1["CE_Chg_OI"]))]["Strike"])[0]],
                                        ["Max Put Change in OI Strike",list(df1[df1["PE_Chg_OI"] == max(list(df1["PE_Chg_OI"]))]["Strike"])[0]],
                                        ["Max Call Volume Strike",list(df1[df1["CE_Volume"] == max(list(df1["CE_Volume"]))]["Strike"])[0]],
                                        ["Max Put Volume Strike",list(df1[df1["PE_Volume"] == max(list(df1["PE_Volume"]))]["Strike"])[0]],
                                        ["",""], 
                                        ["Max Call OI",max(list(df1["CE_OI"]))],
                                        ["Max Put OI",max(list(df1["PE_OI"]))],          
                                        ["Max Call Change in OI",max(list(df1["CE_Chg_OI"]))],
                                        ["Max Put Change in OI",max(list(df1["PE_Chg_OI"]))],   
                                        ["Max Call Volume",max(list(df1["CE_Volume"]))],
                                        ["Max Put Volume",max(list(df1["PE_Volume"]))],  
                                        ]

                df1 = df1[['CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                        'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
                Strik_list = np.unique(df1['StrikeRate'])
                opt_data_frame = pd.DataFrame()
                r = 0.10                

                expiry_new = pd.to_datetime((list(map(lambda x: datetime.strptime(x,'%d-%m-%Y').strftime('%d-%m-%Y'), expiryy['ExpDate']))[0]),format='%d-%m-%Y')
                print(expiry_new)
                print(expiry_new)
                upto = timedelta(minutes=930) 
                new_current = expiry_new + upto
                print(new_current)
                dte = (new_current-datetime.now())/timedelta(days=1)/365
                
                for stk in Strik_list:
                    #print(stk)                    
                    scpt = df1[df1['StrikeRate'] == stk]
                    CE_price = float(scpt['CE_Ltp'])
                    PE_price = float(scpt['PE_Ltp'])
                    S = float(underlying_price)
                    try:
                        ce_iv = implied_volatility(CE_price,S,stk,dte,r,'c')        
                        ce_deltaa = delta('c',S,stk,dte,r,ce_iv)
                        ce_thetaa = theta('c',S,stk,dte,r,ce_iv)
                        ce_gamaa = gamma('c',S,stk,dte,r,ce_iv)
                        ce_rhoo = rho('c',S,stk,dte,r,ce_iv)

                        scpt['CE_IV'] = round((ce_iv*100),2)
                        scpt['CE_Delta'] = round((ce_deltaa),3)
                        scpt['CE_Theta'] = round((ce_thetaa),3)
                        scpt['CE_Gamma'] = round((ce_gamaa),3)
                        scpt['CE_Rho'] = round((ce_rhoo),3)

                        pe_iv = implied_volatility(PE_price,S,stk,dte,r,'p')
                        pe_deltaa = delta('p',S,stk,dte,r,pe_iv)
                        pe_thetaa = theta('p',S,stk,dte,r,pe_iv)
                        pe_gamaa = gamma('p',S,stk,dte,r,pe_iv)
                        pe_rhoo = rho('p',S,stk,dte,r,pe_iv)

                        scpt['PE_IV'] = round((pe_iv*100),2)
                        scpt['PE_Delta'] = round((pe_deltaa),3)
                        scpt['PE_Theta'] = round((pe_thetaa),3)
                        scpt['PE_Gamma'] = round((pe_gamaa),3)
                        scpt['PE_Rho'] = round((pe_rhoo),3)
                        
                        opt_data_frame = pd.concat([scpt, opt_data_frame])
                        #print(opt_data_frame)
                        #print(ce_iv)
                    except Exception as e:
                        print(e) 
                        
                opt_data_frame.sort_values(['StrikeRate'], ascending=[True], inplace=True)
                opt_data_frame1 = pd.merge(df1, opt_data_frame, on='StrikeRate',how="outer")
                opt_data_frame1 = opt_data_frame1[['CE_Rho','CE_Gamma','CE_Theta','CE_Delta','CE_IV','CE_Script_x', 'CE_Volume_x', 'CE_Prev_OI_x', 'CE_Chg_OI_x', 'CE_OI_x', 'CE_Prev_Ltp_x', 'CE_Ltp_x', 'StrikeRate',
                        'PE_Ltp_x', 'PE_Prev_Ltp_x', 'PE_OI_x', 'PE_Chg_OI_x', 'PE_Prev_OI_x', 'PE_Volume_x', 'PE_Script_x','PE_IV','PE_Delta','PE_Theta','PE_Gamma','PE_Rho']]
                ocg.range("g1").value = opt_data_frame1
                                
            except Exception as e:
                pass   
    else:
        print("Option Greeks is OFF")
    
    if xlbooks =="Dashboard":
        try:
            oc_symbol,oc_expiry,strategg = oc.range("e2").value,oc.range("e3").value,dash.range("ab1").value
        except Exception as e:
            print(e)
        scptt = symbb.range(f"c{2}:c{15}").value
        scpt1 = symbb.range(f"a{2}:d{15}").value
        symbb.range(f"a1:d1").value = ["Exch","ExchType","Name","ScripCode"]

        scpt_list = []
        scpt_code_list = []

        idxex = 0
        for ii in scptt:
            if ii:
                trade1 = scpt1[idxex]
                aaa={"Exchange": f"{trade1[0]}", "ExchangeType":f"{trade1[1]}", "Symbol": f"{trade1[2]}"}
                aaaa={"Exchange": f"{trade1[0]}", "ExchangeType":f"{trade1[1]}", "ScripCode": f"{trade1[3]}"}
                scpt_list.append(aaa) 
                scpt_code_list.append(aaaa)
            idxex += 1
        gg=[
            {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
            {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"}]  

        for tt in gg:
            scpt_list.append(tt) 

        posi = pd.DataFrame(credi_muk.positions())
        if posi.empty:
            print("First Position of Mukesh Empty")
        else:
            posit_list = (np.unique([int(i) for i in posi['ScripCode']])).tolist()
            for dtt in posit_list:
                a={"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{dtt}"}
                scpt_code_list.append(a)
            

        # print(posit_list)
        # print(scpt_list)
        # print(scpt_code_list)
        # scpt_list1 = {k:v for k,v in scpt_list.items() if list(scpt_list.values()).count(v)==1}
        # scpt_code_list1 = {k:v for k,v in scpt_code_list.items() if list(scpt_code_list.values()).count(v)==1}

        dfg1 = credi_muk.fetch_market_depth_by_symbol(scpt_list)

        dfg2 = dfg1['Data']
        dfg3 = pd.DataFrame(dfg2)  
      
        dfg11 = credi_muk.fetch_market_depth(scpt_code_list)
        dfg22 = dfg11['Data']
        dfg33 = pd.DataFrame(dfg22)
        dash_frame = pd.concat([dfg3, dfg33])
        dash_frame['TimeNow'] = datetime.now()
        dash_frame['Spot'] = round(dash_frame['LastTradedPrice']/100,0)*100
        #print(dash_frame)
        dash_frame['Diff_QTY'] = dash_frame['TotalSellQuantity'] - dash_frame['TotalBuyQuantity']
        dash_frame = dash_frame[['ScripCode','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow','Diff_QTY']]
        
        dfg4 = pd.merge(dash_frame, exchange_all, on=['ScripCode'], how='inner')
        dfg5 = dfg4[~dfg4.duplicated(subset=['ScripCode'], keep='last')].copy()

        posi = pd.DataFrame(credi_muk.positions())
        if posi.empty:
            print("First Position of Mukesh Empty")
            dash.range("a1").options(index=False).value = dfg5
        else:

            posi.rename(columns={'ScripName': 'Name','LTP': 'LastTradedPrice'}, inplace=True)
                                 #,'CpType_x':'Type','LotSize_x':'Lot','Open_x': 'Open_OPT','High_x': 'High_OPT','Low_x': 'Low_OPT','Close_x': 'Close_OPT','LastTradedPrice_x': 'LTP_OPT',
                             #'ScripCode_y': 'ScpCode_SPOT','Open_y': 'Open_SPOT','High_y': 'High_SPOT','Low_y': 'Low_SPOT','Close_y': 'Close_SPOT','LastTradedPrice_y': 'LTP_SPOT',}, inplace=True)
            # print(dfg4)
            # print(posi)
            dfg6 = pd.merge(dfg5, posi, on=['ScripCode'], how='outer')
            dfg6 = dfg6[['Name_x','Exch_x','ExchType_x','CpType','ScripCode','Root','TimeNow','Diff_QTY','Spot','LastTradedPrice_x','LotSize_x','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM','BuyValue','OrderFor']]
            dfg6.sort_values(['ExchType_x','Name_x','OrderFor'], ascending=[True,True,True], inplace=True)
            #dfg6.drop_duplicates()
            dash.range("a1").options(index=False).value = dfg6
            try:
                symbb.range("f1").options(index=False).value = posi
                if posi.empty:
                    print("First Position of Mukesh Empty")
                else:
                    symbb.range("f10").options(index=False).value = posi
            except Exception as e:
                print(f"Error : {e}")

        #symbols = list(filter(lambda item: item is not None, sym))
        symbols = dash.range(f"a{2}:a{15}").value
        trading_info = dash.range(f"a{2}:x{15}").value
        idx = 0
        for i in symbols:
            if i:
                try:
                    
                    #print("1")
                    trade_info = trading_info[idx]
                    #print(trade_info)
                    Exch = trade_info[1]
                    Exc_typ = trade_info[2]
                    typee = trade_info[3]
                    scpt_code = trade_info[4]
                    lt_spt = trade_info[8]
                    pricee = trade_info[9]
                    lotee = trade_info[10]
                    mtomm = trade_info[16]
                    buy_lvl = trade_info[19]
                    tgtt = trade_info[20]
                    slll = trade_info[21]                
                    buyy = trade_info[22]
                    selll = trade_info[23]
                    # by_qty = trade_info[22]
                    # sl_qty = trade_info[23]
                    
                    print(buy_lst)
                    print(sell_lst)

                    if buyy is None:
                        if scpt_code in buy_lst:
                            buy_lst.remove(scpt_code)
                    if selll is None:
                        if scpt_code in sell_lst:
                            sell_lst.remove(scpt_code)
                    if scpt_code in buy_lst: 
                        print(str(scpt_code)+" Call is Already Buy")
                    else:
                        print("1")
                        if buyy is not None:
                            print("2")
                            if orders.upper() == "YES" or orders.upper() == "":  
                                for credi in cred:                            
                                    order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Buy Call Order Executed")
                                    buy_lst.append(scpt_code)

                    if scpt_code in sell_lst: 
                        print(str(scpt_code)+" Sell Already Exited")
                    else:   
                        print("3")             
                        if selll is not None:
                            print("4")
                            if orders.upper() == "YES" or orders.upper() == "":  
                                for credi in cred:                            
                                    order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                    print("Sell Call Order Executed")
                                    sell_lst.append(scpt_code)

        #             # print(i)
        #             # print(scpt_code)
        #             # print(buy_lst)
        #             # print(sell_lst)     
        #             if buyy is None:
        #                 if scpt_code in buy_lst:
        #                     buy_lst.remove(scpt_code)
        #             if selll is None:
        #                 if scpt_code in sell_lst:
        #                     sell_lst.remove(scpt_code)
        #             if slll is not None and buyy is not None:
        #                 var =  ((lt_spt)*0.2)/100                    
        #                 # print(var)
        #                 # print(scpt_code)
        #                 # print(buy_lst)
        #                 # print("-01")
        #                 if typee == "CE" and slll < lt_spt and slll > lt_spt-var:  

        #                     if scpt_code in buy_lst: 
        #                         print(str(scpt_code)+" Call is Already Buy")
        #                     else:
        #                         if orders.upper() == "YES" or orders.upper() == "":  
        #                             for credi in cred:                            
        #                                 order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #                                 print("Buy Call Order Executed")
        #                                 buy_lst.append(scpt_code)

        #                 if typee == "PE" and slll > lt_spt and slll < lt_spt+var:                        
        #                     if scpt_code in buy_lst: 
        #                         print(str(scpt_code)+" Put is Already Buy")
        #                     else:
        #                         if orders.upper() == "YES" or orders.upper() == "":  
        #                             for credi in cred: 
        #                                 order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #                                 print("Buy Put Order Executed")
        #                                 buy_lst.append(scpt_code)
        #             #print("0")        

        #             if mtomm is not None:
        #                 #print("01")
        #                 if selll is not None:
        #                     #print("02")
        #                     if float(mtomm) > 0 or float(mtomm) < 0:
        #                         if scpt_code in sell_lst: 
        #                             print(str(scpt_code)+" Sell Already Exited")
        #                         else:
        #                             if orders.upper() == "YES" or orders.upper() == "":  
        #                                 for credi in cred:
        #                                     order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #                                     print("Sell Order Executed")
        #                                     sell_lst.append(scpt_code)
                    
        #             # if mtomm is not None: 
        #             #     if float(mtomm) < float(Fixed_SL) or float(mtomm) > float(Fixed_TGT):
        #             #         if orders.upper() == "YES" or orders.upper() == "":  
        #             #             for credi in cred:
        #             #                 order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #             #                 print("SLL Or TGT Executed")
        #             #                 sell_lst.append(scpt_code)

        #             #print("1")  
        #             # if mtomm is not None: 
        #             #     #print("11")
        #             #     if slll is not None:
        #             #         #print("12")
        #             #         if float(mtomm) > 0 or float(mtomm) < 0:
        #             #             #print("13")
        #             #             if typee == "CE" and lt_spt < slll:
        #             #                 if scpt_code in sell_lst: 
        #             #                     print(str(scpt_code)+" call Stop Loss Hit Already")
        #             #                 else:
        #             #                     if orders.upper() == "YES" or orders.upper() == "":  
        #             #                         for credi in cred:
        #             #                             order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #             #                             print("Call Stop Loss Hit")
        #             #                             sell_lst.append(scpt_code)
        #             #             if typee == "PE" and lt_spt > slll:
        #             #                 if scpt_code in sell_lst: 
        #             #                     print(str(scpt_code)+" Put Stop Loss Already")
        #             #                 else:
        #             #                     if orders.upper() == "YES" or orders.upper() == "":  
        #             #                         for credi in cred:
        #             #                             order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #             #                             print("Put Stop Loss Hit")
        #             #                             sell_lst.append(scpt_code)
        #             # #print("2")   
        #             # if mtomm is not None:  
        #             #     #print("21")
        #             #     if tgtt is not None:
        #             #         #print("22")
        #             #         if float(mtomm) > 0 or float(mtomm) < 0:
        #             #             #print("23")
        #             #             if typee == "CE" and lt_spt > tgtt:
        #             #                 #print("24")
        #             #                 if scpt_code in sell_lst: 
        #             #                     #print("25")
        #             #                     print(str(scpt_code)+" Call Target Hit Already ")
        #             #                 else:
        #             #                     #print("26")
        #             #                     if orders.upper() == "YES" or orders.upper() == "":  
        #             #                         #print("27")
        #             #                         ide = idx+2
        #             #                         print(ide)
        #             #                             #dt.range(f"a1:d1").value
        #             #                         dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
        #             #                         #for credi in cred:
        #             #                             #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #             #                         print("Call Target Hit")
        #             #                         #print("28")
        #             #                         sell_lst.append(scpt_code)
        #             #                         #print("29")
        #             #             if typee == "PE" and lt_spt < tgtt:
        #             #                 #print("30")
        #             #                 if scpt_code in sell_lst: 
        #             #                     #print("31")
        #             #                     print(str(scpt_code)+" Put Target Hit Already")
        #             #                 else:
        #             #                     #print("32")
        #             #                     if orders.upper() == "YES" or orders.upper() == "":  
        #             #                         #print("33")
        #             #                         #for credi in cred:
        #             #                             # print("34")
                                            
        #             #                         ide = idx+2
        #             #                         print(ide)
        #             #                             #dt.range(f"a1:d1").value
        #             #                         dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
        #             #                             #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
        #             #                         print("Put Target Hit")
        #             #                         #print("35")
        #             #                         sell_lst.append(scpt_code)
        #             #                         #print("36")

                    #print("3")    
                except Exception as e:
                    print(e)            
            idx += 1
        #dash.range(f"v2:w15").value = ''
            #dash.range(f"x2:x15").value = ''
        # dash.range("y2").value = '=IF(T2="","",IF(AND(E2="CE",H2>T2),"Buy",IF(AND(E2="PE",H2<T2),"Buy","")))'  
        # dash.range("v2").value = '=IF(H2="","",IF(E2="CE",(H2-H2*0.2%)+1,IF(E2="PE",(H2+H2*0.2%)-1,"")))'    
        # scpt_list = []
        # scpt_listtt = []

        #dash.range("a1").options(index=False).value = dfgg5
    else:
        print("Bid Ask Diff is OFF")

    if xlbooks == "EOD Data":
        eq_bhav = bhavcopy_func()
        fo_bhav = bhavcopy_fno_func()

        delv_data = pd.merge(eq_bhav, fo_bhav, on=['Name','Date'], how='outer')
        delv_data = delv_data[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume','Deliv_qty', 'Value', 'OI', 'Chg_OI','Deliv_per']]
        delv_data.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
        eod_data.range("a1").options(index=False).value = delv_data

        symb_list = (np.unique(delv_data['Name']).tolist())
        #print(symb_list)

        eod_vol_para = 2
        eod_delv_para = 1.5
        eod_oi_para = 1.1

        stk_df = pd.DataFrame()
        for stkks in symb_list:
            print(stkks)
            new_delv_data = delv_data[(delv_data["Name"] == stkks)]  
            new_delv_data['Price_Chg'] = round((((new_delv_data['Close'] * 100) / (new_delv_data['Close'].shift(-1))) - 100), 2).fillna(0)      
            new_delv_data['OI_Chg'] = round((((new_delv_data['OI'] * 100) / (new_delv_data['OI'].shift(-1))) - 100), 2).fillna(0)
            new_delv_data['Vol_Chg'] = round((((new_delv_data['Volume'] * 100) / (new_delv_data['Volume'].shift(-1))) - 100), 2).fillna(0) 

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
            stk_df = pd.concat([new_delv_data, stk_df])
        stk_df.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
        stk_df1 = stk_df[~stk_df.duplicated(subset=['Name', 'Date'], keep='last')].copy()

        #eod_data.range("a:t").value = None
        eod_data.range("a1").options(index=False).value = stk_df1
        print("EOD DATA & F&O Data Merged")
    else:
        print("EOD Data is OFF")  

