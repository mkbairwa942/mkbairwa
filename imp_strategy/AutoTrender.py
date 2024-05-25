
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
users = ["HARESH","MUKESH"]#,"ASHWIN","ALPESH"]
credi_har = None
credi_muk = None

# credi_ash = None
# credi_alp = None

while True:
    if credi_har is None and credi_muk is None:# and credi_alp is None:
        try:
            for us in users:
                print("1")
                if us == "HARESH":
                    credi_har = credentials("HARESH")
                    if credi_har.request_token is None:
                        credi_har = credentials("HARESH")
                        print(credi_har.request_token)
                if us == "MUKESH":
                    credi_muk = credentials("MUKESH")
                    if credi_muk.request_token is None:
                        credi_muk = credentials("MUKESH")
                        print(credi_muk.request_token)
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

cred = [credi_har,credi_muk]#,credi_ash,credi_alp]
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
        wb.sheets.add("optionchain")
        wb.save("AutoTrender.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('AutoTrender.xlsx')

for i in ["Dashboard","Exchange","Fil Exch","World Market","Nifty 50 Rnaking","F&O Ranking","Stocks Positional",
          "Auto","Auto Ancillaries","Capital Goods","Cements","FMCG","IT","Insurance","Metals","NBFC","Chemicals","Consumer Durables",
          "Oil & Gas","MidCap","Pharma","Power","Private Banks","PSU Banks","Reality","Telecom",
          "Buy Senti > 60","Sell Senti > 60"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

dash = wb.sheets("Dashboard")
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Fil Exch")

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



script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

segment = "nse_fo"
'''
all - scrips across all segments
bse_eq - BSE Equity
nse_eq - NSE Equity
nse_fo - NSE Derivatives
bse_fo - BSE Derivatives
ncd_fo - NSE Currecny
mcx_fo - MCX
'''

script_code_5paisa_url1 = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment}"
script_code_5paisa1 = pd.read_csv(script_code_5paisa_url1,low_memory=False)

exchange = None
while True:    
    if exchange is None: 
        try:   
            #root_list = np.unique(exch['Root']).tolist()      
            root_list = ["BANKNIFTY","NIFTY"]

            exch1 = script_code_5paisa1[(script_code_5paisa1["Exch"] == "N") & (script_code_5paisa1["ScripType"] != "XX")]            
            exch1.rename(columns={'ScripType': 'CpType','SymbolRoot': 'Root','BOCOAllowed': 'CO BO Allowed'},inplace=True)
            exch1.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)
            exc_new = exch1['Root'].isin(root_list)            
            exc_new1 = exch1[exc_new]

            exch = script_code_5paisa[(script_code_5paisa["Exch"] == "N")]
            exch.sort_values(['Root'], ascending=[True], inplace=True)            
            excc = exch['Root'].isin(root_list)            
            excc1 = exch[excc]

            Expiry = excc1[(excc1['Expiry'].apply(pd.to_datetime) >= new_current_trading_day)]
            print(Expiry.head(1))
            print(Expiry.tail(1))
            Expiry.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)   
            exc_new2 = Expiry
            exc_new2.rename(columns={'Scripcode': 'ScripCode' },inplace=True)
            exc_new2["Watchlist"] = exc_new2["Exch"] + ":" + exc_new2["ExchType"] + ":" + exc_new2["Name"]

            # eq_exc = excc1[(excc1["Exch"] == "N") & (excc1["ExchType"] == "C") & (excc1["CpType"] == "EQ")]
            # exc.range("a1").options(index=False).value = eq_exc
            break
        except:
            print("Exchange Download Error....")
            time.sleep(5)

exc.range("a:az").value = None
exc.range("a1").options(index=False).value = exc_new2

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = exc_new1

#symbol1 = '999920005'
stk_list_5paisa = [999920005,999920000]
stk_list_zerodha = [260105,256265]


telegram_msg = "yes"
orders = "yes"
Capital = 20000
StockPriceLessThan = 1000
Buy_price_buffer = 2
Vol_per = 15
UP_Rsi_lvl = 60
DN_Rsi_lvl = 40
adx_parameter = 0.40
adx_parameter_opt = 0.1
sam_2_slop = 1
sam_21_slop = 1.5
dema_21_slope = 2
slll = -900
tgtt = 3000
lotsize = 2
data_from = "5paisa"#,"Zerodha_kite"

SLL = 10
TSL = 15
tsl1 = 1-(TSL/100)
print(tsl1)