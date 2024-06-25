import numpy as np
import pandas as pd
from datetime import datetime,timedelta
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta,gamma,rho,theta


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

cred = [credi_muk]#,credi_ash,credi_alp]
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

if not os.path.exists("Option_Greeks.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("Option Chain")
        wb.save("Option_Greeks.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Option_Greeks.xlsx')

for i in ["Symbol","Dashboard","EOD Data","Exchange","Fil Exch","World Market","Nifty 50 Rnaking","F&O Ranking","Stocks Positional",
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
oc.range("a:b").value = oc.range("d8:e30").value = oc.range("g1:v4000").value = None



# variables

S = 23501.10
K = 23400
r = 0.10
T = 5/365
sigma = 0.633
price = 165.15
flag = 'c'

T = (datetime(2024,6,27,15,30,0)-datetime(2024,6,25,15,30,0))/timedelta(days=1)/365
dt = (datetime(2024,6,26,15,30,0)-datetime.now())/timedelta(days=1)/365
print(dt)
print(T)

# d1 = (np.log(S/K)+((r+sigma**2/2)*T))/(sigma*np.sqrt(T))
# print(d1)
# d2 = d1-(sigma*np.sqrt(T))
# print(d2)
# call = S*norm.cdf(d1,0,1)-norm.cdf(d2,0,1)*K*np.exp(-r*T)
# print(call)
# put = norm.cdf(-d2,0,1)*K*np.exp(-r*T)-S*norm.cdf(-d1,0,1)
# print(put)
# Call_price = bs('c',S,K,T,r,sigma)
# print(Call_price)
# Put_price = bs('p',S,K,T,r,sigma)
# print(Put_price)

iv = implied_volatility(price,S,K,T,r,flag)
print(iv)
deltaa = delta(flag,S,K,T,r,iv)
print(deltaa)
rhoo = rho(flag,S,K,T,r,iv)
print(rhoo)
gamaa = gamma(flag,S,K,T,r,iv)
print(gamaa)
thetaa = theta(flag,S,K,T,r,iv)
print(thetaa)


#global pre_oc_symbol,pre_oc_expiry
try:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
except Exception as e:
    print(e)
# if oc_symbol is None:
#     pre_oc_symbol = pre_oc_expiry = ""

pre_oc_symbol = pre_oc_expiry = ""
expiries_list = []
instrument_dict = {}
prev_day_oi = {}
stop_thread = False

oc_symbol = "BANKNIFTY"
#expiry = 1719392400000

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
print(ep1)
expiry_new = (ep1['ExpDate'][0])
#print("2")
print(expiry)
print("2")
print(expiry_new)

opt = pd.DataFrame(credi_muk.get_option_chain("N",oc_symbol , expiry)['Options'])
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

df1 = df1[['CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
        'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
#print(df1.tail(1))
# 
#df1['CE_IV'] = df['DEMA_21'] - df['DEMA_21'].shift(1) implied_volatility(price,S,K,T,r,flag)
Strik_list = np.unique(df1['StrikeRate'])
#print(Strik_list)
opt_data_frame = pd.DataFrame()
#timees = timeess.strftime("%d-%m-%Y %H:%M:%S")
expiry_new1 = datetime.strptime(expiry_new, '%d-%m-%Y')
print(expiry_new)
print(expiry_new1)
dt = (expiry_new1-datetime.now())/timedelta(days=1)/365
for stk in Strik_list:
    #print(stk)
    
    scpt = df1[df1['StrikeRate'] == stk]
    CE_price = float(scpt['CE_Ltp'])
    PE_price = float(scpt['PE_Ltp'])
    S = float(underlying_price)
    #S = 52027.85
    K = 37500
    r = 0.10
    #T = 5/365
    price = 13091
    #flag = 'c'
    # print(CE_price)
    # print(PE_price)
    # print(S)
    # print(stk)
    #print(scpt)
    try:
        ce_iv = implied_volatility(CE_price,S,stk,dt,r,'c')        
        ce_deltaa = delta('c',S,stk,dt,r,ce_iv)
        ce_thetaa = theta('c',S,stk,dt,r,ce_iv)
        ce_gamaa = gamma('c',S,stk,dt,r,ce_iv)
        ce_rhoo = rho('c',S,stk,dt,r,ce_iv)

        scpt['CE_IV'] = round((ce_iv*100),2)
        scpt['CE_Delta'] = round((ce_deltaa),3)
        scpt['CE_Theta'] = round((ce_thetaa),3)
        scpt['CE_Gamma'] = round((ce_gamaa),3)
        scpt['CE_Rho'] = round((ce_rhoo),3)

        pe_iv = implied_volatility(PE_price,S,stk,dt,r,'p')
        pe_deltaa = delta('p',S,stk,dt,r,pe_iv)
        pe_thetaa = theta('p',S,stk,dt,r,pe_iv)
        pe_gamaa = gamma('p',S,stk,dt,r,pe_iv)
        pe_rhoo = rho('p',S,stk,dt,r,pe_iv)

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
        
opt_data_frame = opt_data_frame[['CE_Rho','CE_Gamma','CE_Theta','CE_Delta','CE_IV','CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
        'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script','PE_IV','PE_Delta','PE_Theta','PE_Gamma','PE_Rho']]
opt_data_frame.sort_values(['StrikeRate'], ascending=[True], inplace=True)
oc.range("g1").value = opt_data_frame
print("Done")


            #stk_code = exchange_fo[exchange_fo['']]

        
