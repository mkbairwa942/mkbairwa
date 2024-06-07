
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

for i in ["Symbol","Dashboard","Exchange","Fil Exch","World Market","Nifty 50 Rnaking","F&O Ranking","Stocks Positional",
          "Auto","Auto Ancillaries","Capital Goods","Cements","FMCG","IT","Insurance","Metals","NBFC","Chemicals","Consumer Durables",
          "Oil & Gas","MidCap","Pharma","Power","Private Banks","PSU Banks","Reality","Telecom",
          "Buy Senti > 60","Sell Senti > 60"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)

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
            # print(exchange.tail(20))
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)
            
exc.range("a1").value = exchange_fo1
flt_exc.range("a1").value = exchange_cash
#exc.range("ar1").value = exchange2
df = pd.DataFrame({"FNO Symbol": list(exchange_fo1["Root"].unique())})
df = df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = df

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value, oc.range("d5").value, oc.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",




df = pd.DataFrame({"FNO Symbol": list(exchange_fo1["Root"].unique())})
df = df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = df

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
            oc.range("g:v").value = None
            instrument_dict = {}
            stop_thread = True
            time.sleep(2)
            if pre_oc_symbol != oc_symbol:
                oc.range("b:b").value = oc.range("d8:e30").value = None
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

                oc.range("d8").value = [["PCR TODAY",pcr],
                                        ["Spot LTP",underlying_price],
                                        ["Spot LTP Round",round(underlying_price/diff,0)*diff],
                                        ["Strike Difference",diff],
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
                oc.range("g1").value = df1

            
    
            except Exception as e:
                pass   
    else:
        print("Option Chain is OFF")
    
    if xlbooks =="Dashboard":
        try:
            oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
        except Exception as e:
            print(e)
        scpt = symbb.range(f"c{2}:c{15}").value
        scpt1 = symbb.range(f"a{2}:d{15}").value
        symbols = dash.range(f"a{2}:a{15}").value
        trading_info = dash.range(f"a{2}:x{15}").value

        symbb.range(f"a1:d1").value = ["Exch","ExchType","Name","ScripCode"]

        scpt_list = []

        idxex = 0
        for ii in scpt:
            if ii:
                trade1 = scpt1[idxex]
                namew = trade1[0]+":"+trade1[1]+":"+trade1[2]
                aaa={"Exchange": f"{trade1[0]}", "ExchangeType":f"{trade1[1]}", "Symbol": f"{trade1[2]}"}
                scpt_list.append(aaa) 
            idxex += 1

        gg=[
            {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
            {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"}]  

        for tt in gg:
            scpt_list.append(tt) 
            
        #print(scpt_list)
        dfg1 = credi_muk.fetch_market_depth_by_symbol(scpt_list)
        dfg2 = dfg1['Data']
        dfg3 = pd.DataFrame(dfg2)
        dfg3['TimeNow'] = datetime.now()
        dfg3['Spot'] = round(dfg3['LastTradedPrice']/100,0)*100
        #dfg3['Root'] = np.where(dfg3['ScripCode'] == 999920000,"NIFTY",np.where(dfg3['ScripCode'] == 999920005,"BANKNIFTY",""))
        dfg3 = dfg3[['ScripCode','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow']]
        dfg4 = pd.merge(dfg3, exchange_cash, on=['ScripCode'], how='inner')
        #dash.range("a1").options(index=False).value = dfg3
        dfg5 = dfg4[dfg4['ExchType'] == 'C']

        listo = (np.unique(dfg5['Root']).tolist())
    
        scpt_listtt = []

        for i in listo: 
            #print(i)
            dfg6 = dfg5[dfg5['Root'] == i]
            stk_name = i
            #print(dfg6.head(1))
            Spot = int(dfg6['Spot'])   
            print(stk_name)
            print("Spot Price is : "+str(Spot)) 
            
            dfc2 = exchange_fo[exchange_fo['Root'] == stk_name]
            #print(np.unique(dfc2['Root']).tolist())
            dfc3 = dfc2[(dfc2['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
            Expiryyy = (np.unique(dfc3['Expiry']).tolist())[0]      
            #print(Expiryyy)
            dfc = dfc3[dfc3['Expiry'] == Expiryyy]
            dfc.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)

            dfgg_CE1 = dfc[(dfc["CpType"] == 'CE')] 
            dfgg_CE2 = dfgg_CE1[(dfgg_CE1['StrikeRate'] < Spot)] 
            dfgg_CE3 = dfgg_CE2.tail(1)
            #print(dfgg_CE3)
            dfgg_CE_scpt = (np.unique([int(i) for i in dfgg_CE3['ScripCode']])).tolist()[0]
            scpt_listtt.append(dfgg_CE_scpt)
            
            dfgg_CE01 = dfc[(dfc["CpType"] == 'CE')] 
            dfgg_CE02 = dfgg_CE01[(dfgg_CE01['StrikeRate'] == Spot)] 
            dfgg_CE03 = dfgg_CE02.tail(1)
            #print(dfgg_CE3)
            dfgg_CE_scpt0 = (np.unique([int(i) for i in dfgg_CE03['ScripCode']])).tolist()[0]
            scpt_listtt.append(dfgg_CE_scpt0)
            
            dfgg_PE01 = dfc[(dfc["CpType"] == 'PE')]        
            dfgg_PE02 = dfgg_PE01[(dfgg_PE01['StrikeRate'] == Spot)]                        
            dfgg_PE03 = dfgg_PE02.head(1)
            #print(dfgg_PE3)
            dfgg_PE_scpt0 = (np.unique([int(i) for i in dfgg_PE03['ScripCode']])).tolist()[0]
            scpt_listtt.append(dfgg_PE_scpt0)

            dfgg_PE1 = dfc[(dfc["CpType"] == 'PE')]        
            dfgg_PE2 = dfgg_PE1[(dfgg_PE1['StrikeRate'] > Spot)]                        
            dfgg_PE3 = dfgg_PE2.head(1)
            #print(dfgg_PE3)
            dfgg_PE_scpt = (np.unique([int(i) for i in dfgg_PE3['ScripCode']])).tolist()[0]
            scpt_listtt.append(dfgg_PE_scpt)

        posi = pd.DataFrame(credi_muk.positions())
        #posi1 = pd.DataFrame(credi_ash.positions())
        if posi.empty:
            print("First Position of Haresh Empty")
        else:
            try:
                symbb.range("f1").options(index=False).value = posi
                if posi.empty:
                    print("First Position of Mukesh Empty")
                else:
                    symbb.range("f10").options(index=False).value = posi
                #dt.range("a10").options(index=False).value = posi1
                posit3 = (np.unique([int(i) for i in posi['ScripCode']])).tolist()#[0] 
                #print(posit3)
                for t in posit3:
                    scpt_listtt.append(t) 
            except Exception as e:
                print(f"Error : {e}")

        
        scpt_listtt1 = np.unique(scpt_listtt)
        #print(scpt_listtt1)
        Data_fr = []

        for dtt in scpt_listtt1:
            #print(dtt)
            a={"Exchange": "N", "ExchangeType": "D", "ScripCode": f"{dtt}"}
            Data_fr.append(a) 

        #print(Data_fr)
        dfggg = credi_muk.fetch_market_depth(Data_fr)
        dfggg1 = dfggg['Data']
        dfggg2 = pd.DataFrame(dfggg1)
        dfggg2['TimeNow'] = datetime.now()
        dfggg2['Spot'] = round(dfggg2['LastTradedPrice']/100,0)*100
        dfggg2 = dfggg2[['ScripCode','Open','High','Low','Close','LastTradedPrice','Spot','TimeNow','TotalBuyQuantity','TotalSellQuantity']]
        #sl.range("a20").options(index=False).value = dfggg2

        #print(dfgg2)
        
        # print(exchange_opt.head(2))
        # print(dfggg2.head(2))
        #exchange_opt = exchange_opt[['ScripCode','Root','Name','Exch','ExchType','CpType','LotSize']]
        dfgg3 = pd.merge(dfggg2, exchange_fo, on=['ScripCode'], how='inner')
        dfgg3 = dfgg3[['Root','Name','ScripCode','Exch','ExchType','CpType','Open','High','Low','Close','LastTradedPrice','LotSize','TotalBuyQuantity','TotalSellQuantity']]
        #sl.range("a30").options(index=False).value = dfgg3

        dfgg4 = pd.merge(dfgg3, dfg5, on=['Root'], how='inner')
        dfgg4.rename(columns={'Name_x': 'Name','Exch_x': 'Exch','ExchType_x': 'ExchType','ScripCode_x': 'ScripCode','CpType_x':'Type','LotSize_x':'Lot','Open_x': 'Open_OPT','High_x': 'High_OPT','Low_x': 'Low_OPT','Close_x': 'Close_OPT','LastTradedPrice_x': 'LTP_OPT',
                            'ScripCode_y': 'ScpCode_SPOT','Open_y': 'Open_SPOT','High_y': 'High_SPOT','Low_y': 'Low_SPOT','Close_y': 'Close_SPOT','LastTradedPrice_y': 'LTP_SPOT',}, inplace=True)
        dfgg4['Diff_QTY'] = dfgg4['TotalSellQuantity'] - dfgg4['TotalBuyQuantity']
        
        #sl.range("a40").options(index=False).value = dfgg4
        
        dfgg5 = dfgg4[['Name','Root','Exch','ExchType','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
        try:
            if posi.empty:
                print("First Position is Empty")
                dfgg5 =dfgg5[['Name','Root','Exch','ExchType','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot']]
                dash.range(f"m1:x1").value = ['LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM','Buy_lvl','TGT','SLL','BUY','SELL','Status']
                #dash.range("a1").options(index=False).value = dfgg5
            else:
                posit = posi #posit[(posit['MTOM'] != 0)]
                #posit3 = (np.unique([int(i) for i in posit['ScripCode']])).tolist()     
                dfgg6 = pd.merge(dfgg5, posi, on=['ScripCode'], how='outer')
                dfgg6 =dfgg6[['Name','Root','Exch_x','ExchType_x','Type','ScripCode','TimeNow','LTP_SPOT','Spot','LTP_OPT','Diff_QTY','Lot',
                            'LTP','BuyAvgRate','SellAvgRate','BuyQty','SellQty','BookedPL','MTOM']]
                dfgg6.sort_values(['Spot','Type'], ascending=[False, True], inplace=True)
                dash.range(f"t1:x1").value = ["Buy_lvl","TGT","SLL","BUY","SELL","Status"]   
                #dt.range("a2:s15").value = None     
                dfgg6.sort_values(['BookedPL'], ascending=[True], inplace=True)    
                dash.range("a1").options(index=False).value = dfgg6

        except Exception as e:
            print(f"Error : {e}")

        idx = 0
        for i in symbols:
            if i:
                try:
                    
                    #print("1")
                    trade_info = trading_info[idx]
                    #print(trade_info)
                    Exch = trade_info[2]
                    Exc_typ = trade_info[3]
                    typee = trade_info[4]
                    scpt_code = int(trade_info[5])
                    lt_spt = trade_info[7]
                    pricee = trade_info[9]
                    lotee = trade_info[11]
                    mtomm = trade_info[18]
                    tgtt = trade_info[20]
                    slll = trade_info[21]                
                    buyy = trade_info[22]
                    selll = trade_info[23]
                    by_qty = trade_info[15]
                    sl_qty = trade_info[16]
                    

                    # print(i)
                    # print(scpt_code)
                    # print(buy_lst)
                    # print(sell_lst)     
                    if buyy is None:
                        if scpt_code in buy_lst:
                            buy_lst.remove(scpt_code)
                    if selll is None:
                        if scpt_code in sell_lst:
                            sell_lst.remove(scpt_code)
                    if slll is not None and buyy is not None:
                        var =  ((lt_spt)*0.2)/100                    
                        # print(var)
                        # print(scpt_code)
                        # print(buy_lst)
                        # print("-01")
                        if typee == "CE" and slll < lt_spt and slll > lt_spt-var:  

                            if scpt_code in buy_lst: 
                                print(str(scpt_code)+" Call is Already Buy")
                            else:
                                if orders.upper() == "YES" or orders.upper() == "":  
                                    for credi in cred:                            
                                        order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                        print("Buy Call Order Executed")
                                        buy_lst.append(scpt_code)

                        if typee == "PE" and slll > lt_spt and slll < lt_spt+var:                        
                            if scpt_code in buy_lst: 
                                print(str(scpt_code)+" Put is Already Buy")
                            else:
                                if orders.upper() == "YES" or orders.upper() == "":  
                                    for credi in cred: 
                                        order = credi.place_order(OrderType='B',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(buyy)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                        print("Buy Put Order Executed")
                                        buy_lst.append(scpt_code)
                    #print("0")        

                    if mtomm is not None:
                        #print("01")
                        if selll is not None:
                            #print("02")
                            if float(mtomm) > 0 or float(mtomm) < 0:
                                if scpt_code in sell_lst: 
                                    print(str(scpt_code)+" Sell Already Exited")
                                else:
                                    if orders.upper() == "YES" or orders.upper() == "":  
                                        for credi in cred:
                                            order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                                            print("Sell Order Executed")
                                            sell_lst.append(scpt_code)
                    
                    # if mtomm is not None: 
                    #     if float(mtomm) < float(Fixed_SL) or float(mtomm) > float(Fixed_TGT):
                    #         if orders.upper() == "YES" or orders.upper() == "":  
                    #             for credi in cred:
                    #                 order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(selll)*int(lotee),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    #                 print("SLL Or TGT Executed")
                    #                 sell_lst.append(scpt_code)

                    #print("1")  
                    # if mtomm is not None: 
                    #     #print("11")
                    #     if slll is not None:
                    #         #print("12")
                    #         if float(mtomm) > 0 or float(mtomm) < 0:
                    #             #print("13")
                    #             if typee == "CE" and lt_spt < slll:
                    #                 if scpt_code in sell_lst: 
                    #                     print(str(scpt_code)+" call Stop Loss Hit Already")
                    #                 else:
                    #                     if orders.upper() == "YES" or orders.upper() == "":  
                    #                         for credi in cred:
                    #                             order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    #                             print("Call Stop Loss Hit")
                    #                             sell_lst.append(scpt_code)
                    #             if typee == "PE" and lt_spt > slll:
                    #                 if scpt_code in sell_lst: 
                    #                     print(str(scpt_code)+" Put Stop Loss Already")
                    #                 else:
                    #                     if orders.upper() == "YES" or orders.upper() == "":  
                    #                         for credi in cred:
                    #                             order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    #                             print("Put Stop Loss Hit")
                    #                             sell_lst.append(scpt_code)
                    # #print("2")   
                    # if mtomm is not None:  
                    #     #print("21")
                    #     if tgtt is not None:
                    #         #print("22")
                    #         if float(mtomm) > 0 or float(mtomm) < 0:
                    #             #print("23")
                    #             if typee == "CE" and lt_spt > tgtt:
                    #                 #print("24")
                    #                 if scpt_code in sell_lst: 
                    #                     #print("25")
                    #                     print(str(scpt_code)+" Call Target Hit Already ")
                    #                 else:
                    #                     #print("26")
                    #                     if orders.upper() == "YES" or orders.upper() == "":  
                    #                         #print("27")
                    #                         ide = idx+2
                    #                         print(ide)
                    #                             #dt.range(f"a1:d1").value
                    #                         dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
                    #                         #for credi in cred:
                    #                             #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    #                         print("Call Target Hit")
                    #                         #print("28")
                    #                         sell_lst.append(scpt_code)
                    #                         #print("29")
                    #             if typee == "PE" and lt_spt < tgtt:
                    #                 #print("30")
                    #                 if scpt_code in sell_lst: 
                    #                     #print("31")
                    #                     print(str(scpt_code)+" Put Target Hit Already")
                    #                 else:
                    #                     #print("32")
                    #                     if orders.upper() == "YES" or orders.upper() == "":  
                    #                         #print("33")
                    #                         #for credi in cred:
                    #                             # print("34")
                                            
                    #                         ide = idx+2
                    #                         print(ide)
                    #                             #dt.range(f"a1:d1").value
                    #                         dt.range(f'x{ide}').value = int(by_qty)-int(sl_qty)
                    #                             #order = credi.place_order(OrderType='S',Exchange=str(Exch),ExchangeType=str(Exc_typ), ScripCode = int(scpt_code), Qty=int(by_qty)-int(sl_qty),Price=float(pricee),IsIntraday=True)# if list(order_df['OrderFor'])[0] == "I" else False)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                    #                         print("Put Target Hit")
                    #                         #print("35")
                    #                         sell_lst.append(scpt_code)
                    #                         #print("36")

                    #print("3")    
                except Exception as e:
                    print(e)            
            idx += 1
        # dt.range(f"w2:w15").value = ''
        # dt.range(f"x2:x15").value = ''
        dash.range("y2").value = '=IF(T2="","",IF(AND(E2="CE",H2>T2),"Buy",IF(AND(E2="PE",H2<T2),"Buy","")))'  
        dash.range("v2").value = '=IF(H2="","",IF(E2="CE",(H2-H2*0.2%)+1,IF(E2="PE",(H2+H2*0.2%)-1,"")))'    
        scpt_list = []
        scpt_listtt = []

        #dash.range("a1").options(index=False).value = dfgg5

    else:
        print("Bid Ask Diff is OFF")

