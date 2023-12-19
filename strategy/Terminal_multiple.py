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

operate = input("Do you want to go with TOTP (yes/no): ")
TGTT_SLL = input("Do you want to go with FIXED or TRALING STOPLOSS (FSL/TSL): ")
if operate.upper() == "YES":
    from five_paisa1 import *
    # p=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
    # print(p)
    username = input("Enter Username : ")
    username1 = str(username)
    username2 = username1.upper()
    print("HII "+str(username2)+" HAVE A GOOD DAY")
    # username_totp = input("Enter TOTP : ")
    # username_totp1 = str(username_totp)
    # print("Hii "+str(username1)+" you enter TOTP is "+str(username_totp1))
    client = credentials(username1)
else:
    from five_paisa import *
    # from five_paisa1 import *

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

users = ["ashwin","haresh"]
# for usew in users:
#     usew = credentials(str(usew))

# ashwin = credentials(str(ashwin))
# haresh = credentials(haresh)
# mukesh = credentials(mukesh)


current_time = (datetime.now()).strftime("%H:%M")

def get_live_data(Exchange,ExchangeType,Symbol):

    try:
        live_data
    except:
        live_data = {}
    try:
        live_data = client.fetch_market_depth_by_symbol([{"Exchange":Exchange,"ExchangeType":ExchangeType,"Symbol":Symbol}])
    except Exception as e:
        pass
    return live_data

def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
    t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
    S = asset_price
    K = strike_price
    r = interest_rate
    if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
        raise Exception
    flag = instrument_type[0].lower()
    imp_v = implied_volatility(premium, S, K, t, r, flag)
    return [imp_v,
            delta(flag,S,K,t,r,imp_v),
            gamma(flag,S,K,t,r,imp_v),
            rho(flag,S,K,t,r,imp_v),
            theta(flag,S,K,t,r,imp_v),
            vega(flag,S,K,t,r,imp_v)]


def place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction):
    try:
        order = client.place_order(OrderType=direction,
                        Exchange=Exche,
                        ExchangeType=ExchTypee,
                        ScripCode = scripte,
                        Qty=int(quantity),
                        Price=0.0,
                        IsIntraday=True,)
                        #IsStopLossOrder=True
                        #StopLossPrice=StopLossPrice)
        print("CALL PLACE TRADE")
        print(f"order :Exche {Exche},ExchTypee {ExchTypee},scripte {scripte}, Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
        return order
    except Exception as e:
        return f"{e}"

Exchange = None
prev_info = {"Symbol": None, "Expiry": None}
instruments_dict = {}
option_data = {}
 

print("----option chain----")

if not os.path.exists("Terminal_multiple.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Terminal_multiple.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Terminal_multiple.xlsx')
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

#st4.range("k2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*5+COLUMN(B2),2))"
# dt.range("a2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$A2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$A2)"
# dt.range("b2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$B2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$B2)"
# dt.range("c2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$C2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$C2)"
# dt.range("d2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$D2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$D2)"
# dt.range("e2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$E2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$E2)"
# dt.range("f2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$F2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$F2)"
# dt.range("g2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$G2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$G2)"
# dt.range("h2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$H2="","",'D:\STOCK\Capital_vercel_new\[Terminal_multiple.xlsx]Strategy3'!$H2)"
# dt.range("w2").options(index=False).value = '=IF(N2<C2,"SL_Hit",IF(F2=0,IF(AND(N2>D2,N2<((E2*0.5%)+E2)),"Buy","Already_Up"),IF(L2>=F2,"Target_Hit",IF(AND(N2>D2,N2<((E2*0.5%)+E2)),"Buy","Already_Up"))))'


# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a1").value = script_code_5paisa
# # exc.range("a1").value = exchange

# exchange = None
# while True:
#     if exchange is None: 
#         try:
#             exchange = pd.DataFrame(script_code_5paisa)
#             #exchange = exchange[exchange["Exch"] == "N"]
#             #exchange = exchange[exchange["ExchType"] == "D"]
#             exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
#             exchange1 = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['CpType'].isin(['EQ', 'XX']))]
#             # exchange1 = exchange[(exchange['ExchType'].isin(['C', 'D']))]
#             # exchange1 = exchange1[(exchange1['Series'].isin(['EQ', 'XX']))]
#             # exchange2 = exchange[exchange["Series"] == "EQ"]
#             #exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]
            
#             # print(exchange.tail(20))
#             break
#         except:
#             print("Exchange Download Error....")
#             time.sleep(10)

def ordef_func():
    try:
        ordbook = pd.DataFrame(client.order_book())
        #print(ordbook.tail(2))
        ob.range("a1").options(index=False).value = ordbook
    except Exception as e:
                print(e)

    try:
        if ordbook is not None:
            print("Order Book not Empty")        
            #ordbook1 = ordbook[ordbook['AveragePrice'] != 0]   
            ordbook1 = ordbook           
            Datetimeee = []
            for i in range(len(ordbook1)):
                datee = ordbook1['BrokerOrderTime'][i]
                timestamp = pd.to_datetime(datee[6:19], unit='ms')
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
                d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
                d2 = d1 + timedelta(hours = 5.5)
                Datetimeee.append(d2)
            ordbook1['Datetimeee'] = Datetimeee
            ordbook1 = ordbook1[['Datetimeee', 'ScripName','BuySell','AveragePrice', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason','Exch','ExchType', 'MarketLot', 'OrderValidUpto','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            #ordbook1['Datetimeee1'] = ordbook1['Datetimeee'] - timedelta(days=3)
            # ordbook2 = pd.DataFrame(ordbook1)
            # print(ordbook2.dtypes())
            
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1

buy_order_li = ordef_func()

#print(buy_order_li['AveragePrice'].dtypes())

def get_oi(data):
    global prev_day_oi,kite,stop_thread
    for symbol, v in data.items():
        if stop_thread:
            break
        while True:
            try:
                prev_day_oi[symbol]
                break
            except:
                try:
                    prev_day_data = kite.historical_data(v["token"],(datetime.now() - timedelta(days=5)).date(),
                                                         (datetime.now()-timedelta(days=1)).date(),"day",oi=True)
                    try:
                        prev_day_oi[symbol] = prev_day_data[-1]["oi"]
                    except:
                        prev_day_oi[symbol] = 0
                    break
                except Exception as e:
                    time.sleep(0.5)
print("Excel : Started")

call_counter = 0
put_counter = 0

# dfg = client.historical_data('N', 'C', symbol1, '1d', from_d, to_d)
# print(dfg)
# today_range = np.round(((dfg['High'].iloc[-1]) - dfg['Low'].iloc[-1]),2)

buy_order_list = []
ord_buy_df_list = []
ord_sell_df_list = []


by.range("a1:x1").color = (54,226,0)
by.range("a1:x1").font.bold = True
by.range("a1:x1").api.WrapText = True


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

while True: 
    for sh_na in users:
        if sh_na == "ashwin":
            #client = credentials(sh_na)
            ash.range("aa1").value = pd.DataFrame(client.margin())
            ash.range("aa10").value = pd.DataFrame(client.holdings())
            ash.range("aa20").value = pd.DataFrame(client.positions()) 

            buy_order_liii = buy_order_li[(buy_order_li['AveragePrice'] != 0)]
            ash.range("aa40").options(index=False).value = buy_order_liii
            

            posit = pd.DataFrame(client.positions()) 
            buy_order_list = np.unique([int(i) for i in posit['ScripCode']])
            print(buy_order_list)

            buy_ord_new = pd.DataFrame()
            for ord in buy_order_list:
                new_df = buy_order_liii[(buy_order_liii['ScripCode'] == ord) & (buy_order_liii['BuySell'] == 'B')]
                new_df.sort_values(['Datetimeee','Rate'], ascending=[True,True], inplace=True)
                new_df1 = new_df.iloc[[0]]
                buy_ord_new = pd.concat([new_df1, buy_ord_new])  
            ash.range("aa70").options(index=False).value = buy_ord_new


            print("Data Analysis Complete for Ashwin")
        

      
    # # pos.range("a12").value = pd.DataFrame(client.get_tradebook())
    
    # if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
    #     oc.range("g:v").value = None
    #     instrument_dict = {}
    #     stop_thread = True
    #     time.sleep(2)
    #     if pre_oc_symbol != oc_symbol:
    #         oc.range("b:b").value = oc.range("d8:e30").value = None
    #         expiries_list = []
    #     pre_oc_symbol = oc_symbol
    #     pre_oc_expiry = oc_expiry
    # if oc_symbol is not None:
        
    #     try:
    #         if not expiries_list:
    #             df = copy.deepcopy(exchange)
    #             df = df[df['Root'] == oc_symbol]
    #             expiries_list = sorted(list(df["Expiry1"].unique()))
    #             df = pd.DataFrame({"Expiry Date": expiries_list})
    #             df = df.set_index("Expiry Date",drop=True)
    #             oc.range("b1").value = df
        
    #         if not instrument_dict and oc_expiry is not None:
    #             df = copy.deepcopy(exchange)
    #             df = df[df["Root"] == oc_symbol]
    #             df = df[df["Expiry1"] == oc_expiry.date()]
    #             lot_size= list(df["LotSize"])[0]
    #             oc.range("e4").value = lot_size
    #             print("1")
    #             for i in df.index:
    #                 instrument_dict[f'NFO:{df["FullName"][i]}'] = {"strikePrice":float(df["StrikeRate"][i]),
    #                                                                     "instrumentType":df["CpType"][i],
    #                                                                     "token":df["Scripcode"][i]}
    #                 #print(instrument_dict)
    #             stop_thread = False
    #             thread = threading.Thread(target=get_oi,args=(instrument_dict,))
    #             thread.start()
    #         option_data = {}
    #         instrument_for_ltp = "NIFTY" if oc_symbol == "NIFTY" else (
    #             "BANKNIFTY" if oc_symbol == "BANKNIFTY" else oc_symbol)
    #         underlying_price = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":instrument_for_ltp}])['Data'][0]['LastTradedPrice'])
    #         print("2")
    #         ep = []
    #         for ei in pd.DataFrame((client.get_expiry("N", oc_symbol))['Expiry'])['ExpiryDate']:
    #             #print(ei)
    #             left = ei[6:19]
    #             timestamp = pd.to_datetime(left, unit='ms')
    #             ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
    #             ep.append([ExpDate, left])

    #         ep1 = pd.DataFrame(ep)
    #         ep1.columns = ['ExpDate', 'DayFormat']
    #         expiry = (ep1['DayFormat'][0])

    #         opt = pd.DataFrame(client.get_option_chain("N", oc_symbol, expiry)['Options'])

    #         CE = []
    #         PE = []
    #         for i in opt:
    #             ce_data = opt[opt['CPType'] == 'CE']
    #             ce_data = ce_data.sort_values(['StrikeRate'])
    #             CE.append(ce_data)

    #             pe_data = opt[opt['CPType'] == 'PE']
    #             pe_data = pe_data.sort_values(['StrikeRate'])
    #             PE.append(pe_data)
    #         option = pd.DataFrame(client.get_option_chain("N", oc_symbol, expiry)['Options'])

    #         ce_values1 = option[option['CPType'] == 'CE']
    #         pe_values1 = option[option['CPType'] == 'PE']
    #         ce_data = ce_values1.sort_values(['StrikeRate'])
    #         pe_data = pe_values1.sort_values(['StrikeRate'])
    #         df1 = pd.merge(ce_data, pe_data, on='StrikeRate')

    #         df1.rename(
    #             {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
    #             'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
    #             'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
    #             'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

    #         df1=(df1[(df1['CE_Ltp'] != 0) & (df1['PE_Ltp'] != 0)])
    #         df1.index = df1["StrikeRate"]
    #         df1 = df1.replace(np.nan,0)
    #         df1["Strike"] = df1.index
    #         df1.index = [np.nan] * len(df1)

    #         input_list = list(df1['CE_OI'])
    #         input_list1 = list(df1['StrikeRate'])
    #         max_value = max(input_list)
    #         index = input_list.index(max_value)
    #         diff = input_list1[index+1]-input_list1[index]


    #         # des_ltp = 85

    #         # CE_strike_ltp = (df1[df1['CE_Ltp'] < des_ltp][['CE_Ltp']].values.tolist())[0][0]
    #         # PE_strike_ltp = (df1[df1['PE_Ltp'] < des_ltp][['PE_Ltp']].values.tolist())[-1][0]
    #         # CE_strike_ltp_script = (df1[df1['CE_Ltp'] < des_ltp][['CE_Script']].values.tolist())[0][0]
    #         # PE_strike_ltp_script = (df1[df1['PE_Ltp'] < des_ltp][['PE_Script']].values.tolist())[-1][0]

    #         oc.range("d8").value = [["Spot LTP",underlying_price],
    #                                 ["Spot LTP Round",round(underlying_price/diff,0)*diff],
    #                                 ["Strike Difference",diff],
    #                                 ["",""],
    #                                 ["Total Call OI",sum(list(df1["CE_OI"]))],
    #                                 ["Total Put OI",sum(list(df1["PE_OI"]))],
    #                                 ["Total Call Change in OI",sum(list(df1["CE_Chg_OI"]))],
    #                                 ["Total Put Change in OI",sum(list(df1["PE_Chg_OI"]))],
    #                                 ["",""],            
    #                                 ["Max Call OI Strike",list(df1[df1["CE_OI"] == max(list(df1["CE_OI"]))]["Strike"])[0]],
    #                                 ["Max Put OI Strike",list(df1[df1["PE_OI"] == max(list(df1["PE_OI"]))]["Strike"])[0]],
    #                                 ["Max Call Change in OI Strike",list(df1[df1["CE_Chg_OI"] == max(list(df1["CE_Chg_OI"]))]["Strike"])[0]],
    #                                 ["Max Put Change in OI Strike",list(df1[df1["PE_Chg_OI"] == max(list(df1["PE_Chg_OI"]))]["Strike"])[0]],
    #                                 ["Max Call Volume Strike",list(df1[df1["CE_Volume"] == max(list(df1["CE_Volume"]))]["Strike"])[0]],
    #                                 ["Max Put Volume Strike",list(df1[df1["PE_Volume"] == max(list(df1["PE_Volume"]))]["Strike"])[0]],
    #                                 ["",""], 
    #                                 ["Max Call OI",max(list(df1["CE_OI"]))],
    #                                 ["Max Put OI",max(list(df1["PE_OI"]))],          
    #                                 ["Max Call Change in OI",max(list(df1["CE_Chg_OI"]))],
    #                                 ["Max Put Change in OI",max(list(df1["PE_Chg_OI"]))],   
    #                                 ["Max Call Volume",max(list(df1["CE_Volume"]))],
    #                                 ["Max Put Volume",max(list(df1["PE_Volume"]))],  
    #                                 ]

    #         df1 = df1[['CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
    #                 'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
    #         oc.range("g1").value = df1
    #         num_col = ['CE_Volume','CE_Chg_OI','PE_Chg_OI','PE_Volume']
    #         df1.style.highlight_max()
    #         df1.style.highlight_max(subset=num_col,color='lightgreen')
    #         df1.style.highlight_min(subset=num_col,color='pink')
            


    #         time.sleep(0.5)            
    #         scpt = dt.range(f"a{1}:h{50}").value            
    #         sym = dt.range(f"a{2}:a{500}").value
    #         symbols = list(filter(lambda item: item is not None, sym))

    #         symb_frame = exchange[(exchange['Name'].isin(symbols))]

    #         symb_frame['Concate'] = symb_frame['Exch']+":"+symb_frame['ExchType']+":"+symb_frame['Name']+":"+symb_frame['Scripcode'].astype(str)+":"+symb_frame['LotSize'].astype(str)

    #         symbolss = list(symb_frame['Concate'])
    #         symbolss.sort()



    #         max_min = oc.range(f"e{17}:e{22}").value
    #         trading_info = by.range(f"u{2}:y{30}").value  
            
    #         maxxx = max(list(max_min))
    #         minnn = min(list(max_min))
    #         print(maxxx,minnn)
           
    #         index = ['N:C:NIFTY:999920000:2000','N:C:BANKNIFTY:999920005:2000','N:C:FINNIFTY:999920041:2000'] #999920000 999920005 999920041

    #         for li in index:                 
    #             symbolss.append(li)

    #         subs_lst = symbolss
    #         for i in subs_lst:   
    #             if i not in symbolss:
    #                 subs_lst.remove(i)
    #                 try:
    #                     del live_data[i]
    #                 except Exception as e:
    #                     pass
    #         main_list = pd.DataFrame()
    #         five_df1 = pd.DataFrame()
    #         five_df2 = pd.DataFrame()
    #         five_df3 = pd.DataFrame()
    #         five_df4 = pd.DataFrame()

    #         idx = 0

    #         for i in symbolss:
    #             if i:
    #                 if i not in subs_lst:
    #                     subs_lst.append(i)
    #                 if i in subs_lst:
    #                     try:
    #                         main_li = pd.DataFrame()
           
    #                         Exche = i.split(":")[0]
    #                         ExchTypee = i.split(":")[1]
    #                         Namee = i.split(":")[2]
    #                         Scripcodee = i.split(":")[3]
    #                         Lotsize = i.split(":")[4]
    #                         #print(Exche,ExchTypee,Namee,Scripcodee,Lotsize)
    #                         live_data = get_live_data(Exche,ExchTypee,Namee)
    #                         main_li['Symbol'] = Namee,
    #                         main_li['Lotsize'] = Lotsize,
    #                         main_li['Open'] = live_data['Data'][0]['Open'],
    #                         main_li['High'] = live_data['Data'][0]['High'],
    #                         main_li['Low'] = live_data['Data'][0]['Low'],
    #                         main_li['LTP'] = live_data['Data'][0]["LastTradedPrice"],
    #                         main_li['Volume'] = live_data['Data'][0]["Volume"],
    #                         main_li['Vwap'] = live_data['Data'][0]["AverageTradePrice"],
    #                         main_li['Close'] = live_data['Data'][0]["Close"],
    #                         main_li['OI'] = live_data['Data'][0]["OpenInterest"],
    #                         main_li['NetChange'] = live_data['Data'][0]["NetChange"]                            
    
    #                         main_list = pd.concat([main_li, main_list])     
           
    #                         trade_info = trading_info[idx]

    #                         #place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction)
                            
    #                         if trade_info[0] is not None and trade_info[2].upper() is not None:


    #                             print(trade_info[0],trade_info[1],trade_info[2],trade_info[3],trade_info[4])

    #                             if trade_info[2].upper() == "BUY" and trade_info[3] is None:  
    #                                 print("Buy order")   
    #                                 #dt.range(f"t{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),float(trade_info[1]),"B")

    #                             if trade_info[2].upper() == "BUY" and trade_info[3].upper() == "SELL":
    #                                 print("Sell order") 
    #                                 #squareoff = client.squareoff_all() 
    #                                 dt.range(f"u{idx +2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),float(trade_info[1]),"S")

    #                             if trade_info[2].upper() == "SELL" and trade_info[3] is None:  
    #                                 print("Sell order")   
    #                                 #squareoff = client.squareoff_all()                                  
    #                                 #dt.range(f"t{idx +2 }").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),float(trade_info[1]),"S")

    #                             if trade_info[2].upper() == "SELL" and trade_info[3].upper() == "BUY":   
    #                                 print("Buy order")                                   
    #                                 #dt.range(f"u{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),float(trade_info[1]),"B")

    #                         #print(i,trading_info)
    #                     except Exception as e:                
    #                         pass                
                    
    #             idx +=1
 
    #         #main_list.sort_values(['Symbol'], ascending=[True], inplace=True)
    #         main_list['Time'] = datetime.now()
    #         main_list3 = main_list
    #         main_list4 = main_list3.iloc[::-1]
    #         main_list4 = main_list4[['Symbol','Open','High','Low','LTP','Close','NetChange','Time']]            

    #         dt.range("j1").options(index=False).value = main_list4 

    #         posii = pd.DataFrame(client.positions())


                
    #         if posii.empty:
    #             print("No Positions")
    #         else:
    #             buy_order_lii = buy_order_li[(buy_order_li['BuySell'] == 'B') & ((buy_order_li['AveragePrice'] != 0))] 
    #             posi = pd.merge(posii,buy_order_lii, on=['ScripCode'], how='inner')
    #             posi = posi[['ScripName_y','ScripCode','BuyAvgRate','Datetimeee']]
    #             posi.rename(columns={'ScripName_y': 'Namee','ScripCode':'Scriptcodee','BuyAvgRate':'Buy_At','Datetimeee':'Datetime'}, inplace=True)
                
    #             posi['Stop_Loss'] = round((posi['Buy_At'] - (posi['Buy_At']*2)/100),1)
    #             posi['Add_Till'] = round((posi['Buy_At']-((posi['Buy_At']*0.5)/100)),1)      
    #             posi['Target'] = round((((posi['Buy_At']*2)/100) + posi['Buy_At']),1)

    #             posi['Term'] = "SFT"
    #             posi.sort_values(['Namee'], ascending=[True], inplace=True)
    #             posi = posi[['Namee','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime']]
    #             dt.range("a1").options(index=False).value = posi

    #             buy_order_list = (np.unique([int(i) for i in buy_order_lii['ScripCode']])).tolist()
    #             print(buy_order_list)

    #             for ae in buy_order_list:
    #                 orderboo = buy_order_lii[(buy_order_lii['ScripCode'] == ae) & (buy_order_lii['BuySell'] == "B") & (buy_order_lii['AveragePrice'] != 0)]
    #                 orderboo.sort_values(['Datetimeee','Rate'], ascending=[True,True], inplace=True)
    #                 dfgg_up_1 = orderboo.iloc[[0]]

    #                 Buy_Scriptcodee = int(dfgg_up_1['ScripCode'])
    #                 Buy_Name = list(dfgg_up_1['ScripName'])[0]
    #                 Buy_price = float(dfgg_up_1['Rate'])                 
    #                 Buy_Stop_Loss = float(round((dfgg_up_1['Rate'] - (dfgg_up_1['Rate']*2)/100),1))  
    #                 Buy_Target = float(round((((dfgg_up_1['Rate']*2)/100) + dfgg_up_1['Rate']),1))
    #                 Buy_Exc = list(dfgg_up_1['Exch'])[0]
    #                 Buy_Exc_Type = list(dfgg_up_1['ExchType'])[0]
    #                 Buy_Qty = int(dfgg_up_1['Qty'])                  
                  

    #                 Buy_timee = list(dfgg_up_1['Datetimeee'])[0]
    #                 Buy_timee1 = str(Buy_timee).replace(' ','T')
    #                 print(Buy_Scriptcodee,Buy_Name,Buy_price,Buy_Stop_Loss,Buy_Target,Buy_Exc_Type,Buy_Qty,Buy_timee1)
    #                 dfg1 = client.historical_data(str(Buy_Exc), str(Buy_Exc_Type), ae, '1m',last_trading_day,current_trading_day)
                                       
    #                 dfg1['Scripcode'] = ae
    #                 dfg1['ScripName'] = Buy_Name
    #                 dfg1['Entry_Date'] = Buy_timee1
    #                 dfg1['Entry_Price'] = Buy_price

    #                 dfg1.sort_values(['ScripName', 'Datetime'], ascending=[True, True], inplace=True)
    #                 st.range("a1").options(index=False).value = dfg1
    #                 dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] <= dfg1['Datetime'],"OK","")
    #                 dfg1['StopLoss'] = Buy_Stop_Loss
    #                 dfg1['Target'] = Buy_Target

    #                 dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
    #                 dfg2['Benchmark'] = dfg2['High'].cummax()
    #                 dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.98
    #                 dfg2['BValue'] = dfg2['Entry_Price']*Buy_Qty
                    
    #                 dfg2['TGT_SL'] = np.where(dfg2['High'] > Buy_Target,"TGT",np.where(dfg2['Low'] < Buy_Stop_Loss,"SL",""))
    #                 dfg2['SValue'] = np.where(dfg2['TGT_SL'] == "SL",Buy_Stop_Loss*Buy_Qty,np.where(dfg2['TGT_SL'] == "TGT",Buy_Target*Buy_Qty,""))  
                    
    #                 dfg2['P&L_SL'] = pd.to_numeric(dfg2['SValue']) - dfg2['BValue']
    #                 dfg2['Qty'] = Buy_Qty
    #                 five_df2 = pd.concat([dfg2, five_df2])
    #                 #st3.range("a1").options(index=False).value = dfg2
                    
                    
                    
    #                 dfg3 = dfg2[(dfg2['TGT_SL'] != '')]    
    #                 dfg4 = dfg3.iloc[0:1]
    #                 five_df1 = pd.concat([dfg4, five_df1])
    #                 #st1.range("a1").options(index=False).value = dfg4
    #                 dfgg2 = dfg2.copy()                    
    #                 dfgg2['TGT_TSL'] = np.where(dfgg2['Close'] < dfgg2['TStopLoss'],"TSL",np.where(dfgg2['Low'] < Buy_Stop_Loss,"SL",""))
                    
    #                 five_df4 = pd.concat([dfgg2, five_df4])
    #                 #st4.range("a1").options(index=False).value = dfgg2
    #                 dfgg3 = dfgg2[(dfgg2['TGT_TSL'] != '')] 
    #                 dfgg4 = dfgg3.iloc[0:1]
    #                 #dfgg4['P&L'] = (dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*Buy_Qty
    #                 dfgg4['P&L_TSL'] = np.where(dfgg4['TGT_TSL'] == "SL",(dfgg4['StopLoss'] - dfgg4['Entry_Price'])*Buy_Qty,np.where(dfgg4['TGT_TSL'] == "TSL",(dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*Buy_Qty,"" ))
    #                 five_df3 = pd.concat([dfgg4, five_df3])
    #                 #st2.range("a1").options(index=False).value = dfgg4

    #             # for i in range(0,len(main_list4)):

    #             #     hhigh = float(main_list4.iloc[i]['High'])
    #             #     llow = float(main_list4.iloc[i]['Low'])

    #             #     TGT_3 = round((get_fibonachi(hhigh,llow,"UP",-0.500)),2)
    #             #     TGT_2 = round((get_fibonachi(hhigh,llow,"UP",-0.382)),2)
    #             #     TGT_1 = round((get_fibonachi(hhigh,llow,"UP",-0.236)),2)
    #             #     PP = round((get_fibonachi(hhigh,llow,"UP",0.000)),2)
    #             #     SL_1 = round((get_fibonachi(hhigh,llow,"UP",0.236)),2)
    #             #     SL_2 = round((get_fibonachi(hhigh,llow,"UP",0.382)),2)
    #             #     SL_3 = round((get_fibonachi(hhigh,llow,"UP",0.500)),2)
                    
    #             #     posi['Stop_Loss'] = SL_2 
    #             #     posi['Add_Till'] = SL_1       
    #             #     posi['Target'] = TGT_2 




             

    #         scpts = pd.DataFrame(scpt[1:],columns=scpt[0])
    #         scpts['Namee'] = scpts['Namee'].apply(lambda x : str(x))
    #         scpts = scpts[scpts['Namee'] != 'None']
    #         scpts['TimeNow'] = datetime.now()
    #         scpts['Minutes'] = pd.to_datetime(scpts['TimeNow'])-pd.to_datetime(scpts["Datetime"])
    #         scpts['Minutes'] = round((scpts['Minutes']/np.timedelta64(1,'m')),2)
    #         scpts['Buy'] = np.where(scpts['Minutes']<5,"Yes","")
    #         scpts['Timeover'] = np.where(scpts['Minutes']>30,"Yes","")

            

    #         # by.range("a1").options(index=False).value = scpts

    #         def round_up(n, decimals = 0): 
    #             multiplier = 10 ** decimals 
    #             return math.ceil(n * multiplier) / multiplier

    #         order_frame = scpts[scpts['Buy'] == 'Yes']
    #         time_over_frame = scpts[scpts['Timeover'] == 'Yes']

    #         order_frame_list = np.unique([str(i) for i in order_frame['Namee']])
    #         time_over_frame_list = np.unique([str(i) for i in order_frame['Namee']])

    #         # print("3")
    #         # print(buy_order_list)
    #         # for aa in order_frame_list:
    #         #     if aa in buy_order_list: 
    #         #         print(str(aa)+" is Already Buy") 
    #         #     else: 
    #         #         order_frame1 = order_frame[order_frame['Namee'] == aa]
    #         #         Buy_Scriptcodee = int(order_frame1['Scriptcodee'])
    #         #         Buy_price_of_stock = float(order_frame1['Buy_At'])                    
    #         #         Buy_price_of_stock = round_up(Buy_price_of_stock, 1)
    #         #         Buy_Stop_Loss = round((float(order_frame1['Buy_At']) - (float(order_frame1['Buy_At'])*2)/100),2)
    #         #         Buy_Stop_Loss = round_up(Buy_Stop_Loss, 1)
    #         #         if Buy_price_of_stock < 100:
    #         #             Buy_quantity_of_stock = 200
    #         #         if Buy_price_of_stock > 100 and Buy_price_of_stock < 200:
    #         #             Buy_quantity_of_stock = 100                        
    #         #         if Buy_price_of_stock > 200 and Buy_price_of_stock < 300:
    #         #             Buy_quantity_of_stock = 80
    #         #         if Buy_price_of_stock > 300:
    #         #             Buy_quantity_of_stock = 50
    #         #         Req_Amount = Buy_quantity_of_stock*Buy_price_of_stock
    #         #         fundd = pd.DataFrame(client.margin())['AvailableMargin'] 
    #         #         print(fundd)
    #         #         if fundd > Req_Amount:
    #         #             Buy_quantity_of_stock = round_up(Buy_quantity_of_stock, 1)
    #         #             buy_order_list.append(aa)
    #         #             print("Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock))
    #         #             order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock,Price=Buy_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
    #         #             pwk.sendwhatmsg_instantly("+919610033622","Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock),10,True,5)
    #         #             # pwk.sendwhatmsg_instantly("+918000637245","Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock),10,True,5)            
    #         #         else:
    #         #             print("Available fund is "+str(fundd)+ " and Required Amount is "+str(Req_Amount)+ "is 'LESS'" )

    #         # print("No Stock yet to Buy")
    #         # by.range("n1").options(index=False).value = order_frame
    #         # by.range("aa1").options(index=False).value = time_over_frame

    #         scpts.rename(columns={'Namee': 'Name'},inplace=True)
    #         main_list4.rename(columns={'Symbol': 'Name'},inplace=True)

    #         flt_df34 = pd.merge(scpts, main_list4, on=['Name'], how='inner')
    #         flt_df34.rename(columns={'Name':'ScripName'},inplace=True)

    #         five_df33 = five_df3.copy()
    #         five_df33 = five_df33[['ScripName','Benchmark','TStopLoss','TGT_TSL']]
    #         flt_df = pd.merge(five_df33, flt_df34, on=['ScripName'], how='outer')
    #         sl.range("a15").options(index=False).value = flt_df
    #         flt_df['Buy_up'] = ((flt_df['Buy_At']*0.5)/100)+flt_df['Buy_At']
    #         flt_df['Buy_dn'] = flt_df['Buy_At']-((flt_df['Buy_At']*0.5)/100)

    #         if TGTT_SLL.upper() == "FSL":
    #             flt_df['Status'] = np.where(flt_df['LTP'] < flt_df['Stop_Loss'],"Sl_Hit",
    #                             np.where((flt_df['LTP'] < flt_df['Buy_up']) & (flt_df['LTP'] > flt_df['Buy_dn']),"Buy_Range",
    #                             np.where((flt_df['LTP'] > flt_df['Target']),"Target_Hit",
    #                             np.where((flt_df['LTP'] < flt_df['Buy_At']),"Already_Dn",
    #                             np.where((flt_df['LTP'] > flt_df['Buy_At']),"Already_Up","")))))
            
    #         if TGTT_SLL.upper() == "TSL" or TGTT_SLL.upper() == "":
    #             flt_df['Status'] = flt_df['TGT_TSL']
    #         posit = pd.DataFrame(client.positions())


    #         if posit.empty:
                
    #             flt_df = flt_df[['Name','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term',
    #                             'Datetime','TimeNow','Minutes','Buy','Open','High','Low','LTP','Close','NetChange','Status']]                                
    #             by.range(f"s1:x1").value = ["BookedPL","MTOM","BuyQty","Entry","Exit","X" ]

    #             flt_df.sort_values(['Datetime', 'Name',], ascending=[True, True], inplace=True)
    #             by.range("a1").options(index=False).value = flt_df

    #         else:
    #             flt_df0 = flt_df.copy()
    #             flt_df1 = pd.merge(flt_df0, posit, on=['ScripName'], how='outer')
    #             sl.range("a20").options(index=False).value = flt_df1
    #             flt_df1 = flt_df1[['ScripName','Scriptcodee','Buy_At','Stop_Loss','Target','Benchmark','TStopLoss',
    #                             'Datetime','TimeNow','Minutes','Buy','Open','High','Low','LTP_x','Close',
    #                             'NetChange','Status','BookedPL','MTOM','BuyQty']]
    #             # flt_df1 = flt_df1[['ScripName','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term',
    #             #                 'Datetime','TimeNow','Minutes','Buy','Open','High','Low','LTP_x','Close',
    #             #                 'NetChange','Status','BookedPL','MTOM','BuyQty']]
    #             sl.range("a1").options(index=False).value = flt_df1
    #             flt_df1['Price'] = flt_df1['LTP_x']
    #             flt_df1['Entry'] = np.where((flt_df1['MTOM'] != 0) & (flt_df1['BuyQty'] != 0) & (flt_df1['MTOM'] != "") & (flt_df1['BuyQty'] != ""),"BUY","")
    #             flt_df1['Exit'] = np.where(((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "Sl_Hit")) | ((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "Target_Hit")) | ((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "TSL")) | ((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "SL")),"SELL","")
    #             flt_df11 = flt_df1[flt_df1['LTP_x'] != 0]
    #             sl.range("a10").options(index=False).value = flt_df11
    #             flt_df11.sort_values(['Datetime', 'ScripName',], ascending=[True, True], inplace=True)

    #             by.range("a1").options(index=False).value = flt_df11

    #         if five_df1.empty:
    #             pass
    #         else:
    #             five_df1.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
    #             five_df1 = five_df1[['Scripcode','Entry_Date','Exit_Date','ScripName','Entry_Price','Close',
    #                                 'StopLoss','Target','Qty','TGT_SL','P&L_SL','BValue']]
    #             five_df1.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True) 
                            
    #             st1.range("a:l").value = None
    #             st1.range("a1").options(index=False).value = five_df1

    #         if five_df3.empty:
    #             pass
    #         else:
    #             five_df3.rename(columns={'Datetime': 'Exit_Date' },inplace=True)
    #             five_df3 = five_df3[['Scripcode','Entry_Date','Exit_Date','ScripName','Entry_Price','Close',
    #                                 'Benchmark','TStopLoss','Qty','TGT_TSL','P&L_TSL','BValue']]
    #             five_df3.sort_values(['Entry_Date', 'Exit_Date',], ascending=[True, True], inplace=True) 
                            
    #             st2.range("a:l").value = None
    #             st2.range("a1").options(index=False).value = five_df3

    #         if five_df2.empty:
    #             pass
    #         else:
    #             # five_df1 = five_df1[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
    #             #                         'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
    #             #                         'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
    #             #                         'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #             five_df2.sort_values(['Entry_Date', 'Datetime',], ascending=[True, True], inplace=True) 
                            
    #             st3.range("a:az").value = None
    #             st3.range("a1").options(index=False).value = five_df2

    #         if five_df4.empty:
    #             pass
    #         else:
    #             # five_df4 = five_df1[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
    #             #                         'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
    #             #                         'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
    #             #                         'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #             five_df4.sort_values(['Entry_Date', 'Datetime',], ascending=[True, True], inplace=True) 
                            
    #             st4.range("a:az").value = None
    #             st4.range("a1").options(index=False).value = five_df4

    #         try:
    #             ordbook = pd.DataFrame(client.order_book())
    #             ob.range("a1").options(index=False).value = ordbook
    #         except Exception as e:
    #             print(e)

    #         try:
    #             if ordbook is not None:
    #                 print("Order Book not Empty")        
    #                 # #ordbook1 = ordbook[ordbook['TerminalId'] != 0]   
    #                 # ordbook1 = ordbook[ordbook['BuySell'] == "B"] 
    #                 # #ordbook1 = ordbook           
    #                 # Datetimeee = []
    #                 # for i in range(len(ordbook1)):
    #                 #     datee = ordbook1['BrokerOrderTime'][i]
    #                 #     timestamp = pd.to_datetime(datee[6:19], unit='ms')
    #                 #     ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
    #                 #     d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
    #                 #     d2 = d1 + timedelta(hours = 5.5)
    #                 #     Datetimeee.append(d2)
    #                 # ordbook1['Datetimeee'] = Datetimeee
    #                 # ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','OrderStatus','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
    #                 # ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
    #                 #ob1.range("a1").options(index=False).value = buy_order_li
    #                 buy_order_liii = buy_order_li[(buy_order_li['AveragePrice'] != 0)]
    #                 ob1.range("a1").options(index=False).value = buy_order_liii
    #                 buy_order_list = np.unique([str(i) for i in buy_order_li['ScripName']])
    #             else:
    #                 print("Order Book Empty")
    #         except Exception as e:
    #                     print(e)
    # 
    #     except Exception as e:
    #         pass    

