import os
from five_paisa import *
import time,json,datetime,sys
import xlwings as xw
import pandas as pd
import copy
import numpy as np
import time
import dateutil.parser
import threading
from datetime import datetime,timedelta
import pandas_ta as pta
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from time import sleep
# import urllib.parse as urlparse

# der = pta.indicators()
# print(der)

from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

from_d = (date.today() - timedelta(days=4))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2023, 1, 23)

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
current_time = (datetime.now()).strftime("%H:%M")

print("----option chain----")

if not os.path.exists("opt_5paisa_5Ema.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("opt_5paisa_5Ema.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('opt_5paisa_5Ema.xlsx')
for i in ["Data_1","Data_5","stats","Exchange","Expiry","OrderBook","Option"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data_1")
dt1 = wb.sheets("Data_5")
st = wb.sheets("stats")
exc = wb.sheets("Exchange")
exp = wb.sheets("Expiry")
ob = wb.sheets("OrderBook")
oc = wb.sheets("Option")
dt.range("a:z").value = None
dt1.range("a:z").value = None
st.range("a:z").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
ob.range("a:aj").value = None
#oc.range("a:z").value = None
oc.range("a:b").value = oc.range("d6:e30").value = oc.range("g1:v4000").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)


exc.range("a1").value = script_code_5paisa
# exc.range("a1").value = exchange

exchange = None
while True:
    if exchange is None: 
        try:
            exchange = pd.DataFrame(script_code_5paisa)
            exchange = exchange[exchange["Exch"] == "N"]
            exchange = exchange[exchange["ExchType"] == "D"]
            exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]
            exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
            # print(exchange.tail(20))
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

df = pd.DataFrame({"FNO Symbol": list(exchange["Root"].unique())})
df = df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = df

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value = "Symbol==>>", "Expiry==>>", "LotSize==>>",


pre_oc_symbol = pre_oc_expiry = ""
expiries_list = []
instrument_dict = {}
prev_day_oi = {}
stop_thread = False

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


while True:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
    ob.range("a1").value = pd.DataFrame(client.margin())
    ob.range("a4").value = pd.DataFrame(client.positions())
    ordbook = pd.DataFrame(client.order_book())
    # Datetimeee = []
    # for i in range(len(ordbook)):
    #     datee = ordbook['BrokerOrderTime'][i]
    #     timestamp = pd.to_datetime(datee[6:19], unit='ms')
    #     ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
    #     d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
    #     d2 = d1 + timedelta(hours = 5.5)
    #     Datetimeee.append(d2)
    # ordbook['Datetimeee'] = Datetimeee
    ob.range("a10").value = ordbook
    #ob.range("a20").value = pd.DataFrame(client.get_tradebook())
    if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
        oc.range("g:v").value = None
        instrument_dict = {}
        stop_thread = True
        time.sleep(2)
        if pre_oc_symbol != oc_symbol:
            oc.range("b:b").value = oc.range("d6:e30").value = None
            expiries_list = []
        pre_oc_symbol = oc_symbol
        pre_oc_expiry = oc_expiry
    if oc_symbol is not None:
        try:
            if not expiries_list:
                df = copy.deepcopy(exchange)
                df = df[df['Root'] == oc_symbol]
                expiries_list = sorted(list(df["Expiry1"].unique()))
                df = pd.DataFrame({"Expiry Date": expiries_list})
                df = df.set_index("Expiry Date",drop=True)
                oc.range("b1").value = df

            if not instrument_dict and oc_expiry is not None:
                df = copy.deepcopy(exchange)
                df = df[df["Root"] == oc_symbol]
                df = df[df["Expiry1"] == oc_expiry.date()]
                lot_size= list(df["LotSize"])[0]
                oc.range("e4").value = lot_size
                

                for i in df.index:
                    instrument_dict[f'NFO:{df["FullName"][i]}'] = {"strikePrice":float(df["StrikeRate"][i]),
                                                                        "instrumentType":df["CpType"][i],
                                                                        "token":df["Scripcode"][i]}
                    #print(instrument_dict)
                stop_thread = False
                thread = threading.Thread(target=get_oi,args=(instrument_dict,))
                thread.start()
            option_data = {}
            instrument_for_ltp = "NIFTY" if oc_symbol == "NIFTY" else (
                "BANKNIFTY" if oc_symbol == "BANKNIFTY" else oc_symbol)
            underlying_price = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":instrument_for_ltp}])['Data'][0]['LastTradedPrice'])

            ep = []
            for ei in pd.DataFrame((client.get_expiry("N", oc_symbol))['Expiry'])['ExpiryDate']:
                #print(ei)
                left = ei[6:19]
                timestamp = pd.to_datetime(left, unit='ms')
                ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
                ep.append([ExpDate, left])

            ep1 = pd.DataFrame(ep)
            ep1.columns = ['ExpDate', 'DayFormat']
            expiry = (ep1['DayFormat'][0])
            # print(expiry)
            opt = pd.DataFrame(client.get_option_chain("N", oc_symbol, expiry)['Options'])

            #opt = pd.DataFrame(client.get_option_chain("N", "NIFTY", oc_expiry1)['Options'])
            CE = []
            PE = []
            for i in opt:
                ce_data = opt[opt['CPType'] == 'CE']
                ce_data = ce_data.sort_values(['StrikeRate'])
                CE.append(ce_data)

                pe_data = opt[opt['CPType'] == 'PE']
                pe_data = pe_data.sort_values(['StrikeRate'])
                PE.append(pe_data)
            option = pd.DataFrame(client.get_option_chain("N", oc_symbol, expiry)['Options'])
            # print(option.tail(5))
            # pe_values = pd.DataFrame(client.get_option_chain("N", opt_symbol, expiry)['Options'])
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
            des_ltp = 20
            
            CE_des_ltp_script = (df1[df1['CE_Ltp'] < des_ltp][['CE_Script']].values.tolist())[0][0]
            PE_des_ltp_script = (df1[df1['PE_Ltp'] < des_ltp][['PE_Script']].values.tolist())[-1][0]
            CE_des_ltp = (df1[df1['CE_Ltp'] < des_ltp][['CE_Ltp']].values.tolist())[0][0]
            PE_des_ltp = (df1[df1['PE_Ltp'] < des_ltp][['PE_Ltp']].values.tolist())[-1][0]
            # CE_AM_ltp = (round(underlying_price/diff,0)*diff)
            # PE_AM_ltp = (round(underlying_price/diff,0)*diff)+diff

            # print(CE_des_ltp_script)
            # print(PE_des_ltp_script)

            df1.index = df1["StrikeRate"]
            df1 = df1.replace(np.nan,0)
            df1["Strike"] = df1.index
            df1.index = [np.nan] * len(df1)
            lengt = round((df1.shape[0])/2)
            re1 = df1['StrikeRate'].iloc[lengt]
            re2 = df1['StrikeRate'].iloc[lengt+1]
            diff = (re2-re1)

            oc.range("d6").value = [["Spot LTP",underlying_price],
                                    ["Spot LTP Round",round(underlying_price/diff,0)*diff],
                                    ["Strike Difference",diff],
                                    ["",""],
                                    ["Total Call OI",sum(list(df1["CE_OI"]))],
                                    ["Total Put OI",sum(list(df1["PE_OI"]))],
                                    ["Total Call Change in OI",sum(list(df1["CE_Chg_OI"]))],
                                    ["Total Put Change in OI",sum(list(df1["PE_Chg_OI"]))],
                                    ["",""],            
                                    ["Max Call OI",max(list(df1["CE_OI"]))],
                                    ["Max Put OI",max(list(df1["PE_OI"]))],
                                    ["Max Call OI Strike",list(df1[df1["CE_OI"] == max(list(df1["CE_OI"]))]["Strike"])[0]],
                                    ["Max Put OI Strike",list(df1[df1["PE_OI"] == max(list(df1["PE_OI"]))]["Strike"])[0]],
                                    ["",""],           
                                    ["Max Call Change in OI",max(list(df1["CE_Chg_OI"]))],
                                    ["Max Put Change in OI",max(list(df1["PE_Chg_OI"]))],    
                                    ["Max Call Change in OI Strike",list(df1[df1["CE_Chg_OI"] == max(list(df1["CE_Chg_OI"]))]["Strike"])[0]],
                                    ["Max Put Change in OI Strike",list(df1[df1["PE_Chg_OI"] == max(list(df1["PE_Chg_OI"]))]["Strike"])[0]],
                                    ]
            df1 = df1[['CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                    'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
            oc.range("g1").value = df1
            quantity = lot_size*1
            print(quantity)
            symbol1 = '35002'
            SL = 5
            BuySl_price = np.round(CE_des_ltp-(SL*1),2)
            SellSl_price = np.round(PE_des_ltp-(SL*-1),2)
            #print(CE_AM_ltp)
            print(CE_des_ltp)
            print(BuySl_price)
            #print(PE_AM_ltp)
            print(PE_des_ltp)
            print(SellSl_price)
           
            dff = client.historical_data('N', 'D', symbol1, '1m', from_d, to_d)
            #dff = dff[4:1483] 
            dff['Datetime'] = pd.to_datetime(dff['Datetime'])
            dff['Date'] = pd.to_datetime(dff['Datetime']).dt.date
            dff['Date'] = dff['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
            dff['Time'] = pd.to_datetime(dff['Datetime']).dt.time
            dff['Time'] = dff['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
            dff = dff[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
            dff["MA_5"] = np.round((pta.ema(dff["Close"], length=5)),2)
            dff["MA_20"] = np.round((pta.ema(dff["Close"], length=20)),2)
            #dff["El_Fish"] = pta.fisher(dff["High"],dff["Low"],length=20)
            dff['Diff_20_Ema'] = dff['MA_20']-dff['Close']
            dff['Sell_Entry'] = np.where(((np.where((dff['Low'].shift(1))>(dff['MA_5'].shift(1)),"Sell",""))=="Sell") & ((np.where(dff['Close']<dff['MA_5'],"Sell",""))=="Sell"),"Sell","")
            dff['Buy_Entry'] = np.where(((np.where((dff['High'].shift(1))<(dff['MA_5'].shift(1)),"Buy",""))=="Buy") & ((np.where(dff['Close']>dff['MA_5'],"Buy",""))=="Buy"),"Buy","")
            #dff['Diff_20_Ema'] = dff['Close']-dff['MA_20']
            dff = dff[4:]   
            df3 = dff  
            # print(df3.tail(3)) 

            dt.range("a1").value = df3
            #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_des_ltp_script, Qty=quantity,Price=CE_des_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=BuySl_price,TrailingSL=1)
            #print("order")
            if df3['Buy_Entry'].iloc[-1] == "Buy":       
                if (ordbook["BuySell"].iloc[-1] == "B") and (ordbook["ScripCode"].iloc[-1] == CE_des_ltp_script): # and (ordbook["TradedQty"].iloc[-1] == lot_size):
                    print("Call Buy Order Already Executed in 1 minute")
                else: 
                    squareoff = client.squareoff_all()
                    order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_des_ltp_script, Qty=quantity,Price=CE_des_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=BuySl_price)    
                    print("Call Buy Order Excecuted in 1 minute")
            if df3['Sell_Entry'].iloc[-1] == "Sell":
                if (ordbook["BuySell"].iloc[-1] == "B") and (ordbook["ScripCode"].iloc[-1] == PE_des_ltp_script): # and (ordbook["TradedQty"].iloc[-1] == lot_size):
                    print("Put Buy Order Already Executed in 1 minute")
                else:   
                    squareoff = client.squareoff_all()
                    order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_des_ltp_script, Qty=quantity,Price=PE_des_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=SellSl_price)
                    print("Put Buy Order Excecuted in 1 minute")                    
            else:
                print("No Trade in 1 minute")
            # print("hi...")
            dfff = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)
            #dfff = dfff[4:228] 
            dfff['Datetime'] = pd.to_datetime(dfff['Datetime'])
            dfff['Date'] = pd.to_datetime(dfff['Datetime']).dt.date
            dfff['Date'] = dfff['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
            dfff['Time'] = pd.to_datetime(dfff['Datetime']).dt.time
            dfff['Time'] = dfff['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
            dfff = dfff[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
            dfff["MA_5"] = np.round((pta.ema(dfff["Close"], length=5)),2)
            dfff["MA_20"] = np.round((pta.ema(dfff["Close"], length=20)),2)
            #dfff["El_Fish"] = pta.fisher(dfff["High"],dfff["Low"],length=5)
            dfff['Diff_20_Ema'] = dfff['MA_20']-dfff['Close']
            dfff['Sell_Entry'] = np.where(((np.where((dfff['Low'].shift(1))>(dfff['MA_5'].shift(1)),"Sell",""))=="Sell") & ((np.where(dfff['Close']<dfff['MA_5'],"Sell",""))=="Sell"),"Sell","")
            dfff['Buy_Entry'] = np.where(((np.where((dfff['High'].shift(1))<(dfff['MA_5'].shift(1)),"Buy",""))=="Buy") & ((np.where(dfff['Close']>dfff['MA_5'],"Buy",""))=="Buy"),"Buy","")
            
            dfff = dfff[4:]   
            df4 = dfff  
            # print(df4.tail(3))  

            dt1.range("a1").value = df4
            if df4['Buy_Entry'].iloc[-1] == "Buy":       
                if (ordbook["BuySell"].iloc[-1] == "B") and (ordbook["ScripCode"].iloc[-1] == CE_des_ltp_script): # and (ordbook["TradedQty"].iloc[-1] == lot_size):
                    print("Call Buy Order Already Executed in 5 minute")
                else:    
                    squareoff = client.squareoff_all() 
                    order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_des_ltp_script, Qty=quantity,Price=CE_des_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=BuySl_price)
                    print("Call Buy Order Excecuted in 5 minute")
            if df4['Sell_Entry'].iloc[-1] == "Sell":
                if (ordbook["BuySell"].iloc[-1] == "B") and (ordbook["ScripCode"].iloc[-1] == PE_des_ltp_script): # and (ordbook["TradedQty"].iloc[-1] == lot_size):
                    print("Put Buy Order Already Executed in 5 minute")
                else:  
                    squareoff = client.squareoff_all()
                    order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_des_ltp_script, Qty=quantity,Price=PE_des_ltp, IsIntraday=True,IsStopLossOrder=True, StopLossPrice=SellSl_price)  
                    print("Put Buy Order Excecuted in 5 minute")                    
            else:
                print("No Trade in 5 minute")

        except Exception as e:
            pass                       


            

                                    
    



# def get_live_data(instruments):
#     global kite, live_data
#     try:
#         live_data
#     except:
#         live_data = {}
#     try:
#         live_data = kite.quote(instruments)
#     except Exception as e:
#         #print(f"Get live data Failed {{{e}}}")
#         pass
#     return live_data

# def place_trade(symbol, quantity, direction):
#     try:
#         order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=symbol[0:3],
#                          tradingsymbol=symbol[4:],
#                          transaction_type=kite.TRANSACTION_TYPE_BUY if direction == "Buy" else kite.TRANSACTION_TYPE_SELL,
#                          quantity=int(quantity),
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=0.0,
#                          validity=kite.VALIDITY_DAY,
#                          tag="TA Python")
#         print(f"order : Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
#         return order
#     except Exception as e:
#         return f"{e}"

# def get_orderbook():
#     global orders
#     try:
#         orders
#     except:
#         orders = {}
#     try:
#         data = pd.DataFrame(kite.orders())
#         data = data[data["tag"] == "TA Python"]
#         data = data.filter(["order_timestamp","exchange","tradingsymbol","transaction_type","quantity","average_price","status","status_message_raw"])
#         data.columns = data.columns.str.replace("_"," ")
#         data.columns = data.columns.str.title()
#         data = data.set_index(["Order Timestamp"],drop=True)
#         print(data)
#         data = data.sort_index(ascending=True)
#         orders = data
#     except Exception as e:
#         print(e)
#         pass
#     return orders

# def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
#     t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
#     S = asset_price
#     K = strike_price
#     r = interest_rate
#     if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
#         raise Exception
#     flag = instrument_type[0].lower()
#     imp_v = implied_volatility(premium, S, K, t, r, flag)
#     return [imp_v,
#             delta(flag,S,K,t,r,imp_v),
#             gamma(flag,S,K,t,r,imp_v),
#             rho(flag,S,K,t,r,imp_v),
#             theta(flag,S,K,t,r,imp_v),
#             vega(flag,S,K,t,r,imp_v)]

# Exchange = None
# prev_info = {"Symbol": None, "Expiry": None}
# instruments_dict = {}
# option_data = {}

# # def instruments(symbol, expiry):
# #     instruments_dict = {}
# #     option_data = {}
# #     if Exchange is None:
# #         while True:
# #             try:
# #                 Exchange = pd.DataFrame(kite.instruments("NFO"))
# #                 break
# #             except:
# #                 pass
# #     if symbol and not expiry is None:
# #         try:
# #             df = copy.deepcopy(Exchange)
# #             df = df[(df["segment"] == "NFO-OPT") &
# #                         (df["name"] == symbol.upper())]
# #             df = df[df["expiry"] == sorted(list(df["expiry"].unique()))[expiry]]
# #             for i in df.index:
# #                 instruments_dict[f'NFO:{df["tradingsymbol"][i]}'] = {"Strike": float(df["strike"][i]),
# #                                                                               "Segment": df["segment"][i],
# #                                                                  "Instrument Type": df["instrument_type"][i],
# #                                                                  "Expiry": df["expiry"][i],
# #                                                                  "Lot": df["lot_size"][i]}
# #         except:
# #             pass
# #     prev_info = {"Symbol": symbol, "Expiry": expiry}
# #     return instruments_dict

# # pfe = instruments('NIFTY','29-03-2023')
# # print(pfe)

        
# def quote(instruments):
#     if instruments:
#         try:
#             data = kite.quote(instruments)
#             print(data.tail(50))
#             for symbol, values in data.items():
#                 try:
#                     option_data[symbol[4:]]
#                 except:
#                     option_data[symbol[4:]] = {}
#                 option_data[symbol[4:]]["Strike"] = instruments_dict[symbol]["Strike"]
#                 option_data[symbol[4:]]["Lot"] = instruments_dict[symbol]["Lot"]
#                 option_data[symbol[4:]]["Expiry"] = instruments_dict[symbol]["Expiry"]
#                 option_data[symbol[4:]]["Instument Type"] = instruments_dict[symbol]["Instrument Type"]
#                 option_data[symbol[4:]]["Open"] = values["ohlc"]["open"]
#                 option_data[symbol[4:]]["High"] = values["ohlc"]["high"]
#                 option_data[symbol[4:]]["Low"] = values["ohlc"]["low"]
#                 option_data[symbol[4:]]["Ltp"] = values["last_price"]
#                 option_data[symbol[4:]]["Close"] = values["ohlc"]["close"]
#                 option_data[symbol[4:]]["Volume"] = values["volume"]
#                 option_data[symbol[4:]]["Vwap"] = values["average_price"]
#                 option_data[symbol[4:]]["OI"] = values["oi"]
#                 option_data[symbol[4:]]["OI High"] = values["oi_day_high"]
#                 option_data[symbol[4:]]["OI Low"] = values["oi_day_low"]
#                 option_data[symbol[4:]]["Buy Qty"] = values["buy_quantity"]
#                 option_data[symbol[4:]]["Sell Qty"] = values["sell_quantity"]
#                 option_data[symbol[4:]]["Ltq"] = values["last_quantity"]
#                 option_data[symbol[4:]]["Change"] = values["net_change"]
#                 option_data[symbol[4:]]["Bid Price"] = values["depth"]["buy"][0]["price"]
#                 option_data[symbol[4:]]["Bid Qty"] = values["depth"]["buy"][0]["quantity"]
#                 option_data[symbol[4:]]["Ask Price"] = values["depth"]["sell"][0]["price"]
#                 option_data[symbol[4:]]["Ask Qty"] = values["depth"]["sell"][0]["quantity"]
#         except:
#             pass
#     return option_data

# gfg = quote('NSE:NIFTY 50')
# print(gfg)

# def start_excel():
#     global kite, live_data
#     print("Excel Starting....")
#     if not os.path.exists("TA_Python.xlsx"):
#         try:
#             wb = xw.Book()
#             wb.save("TA_Python.xlsx")
#             wb.close()
#         except Exception as e:
#             print(f"Error : {e}")
#             sys.exit()
#     wb = xw.Book('TA_Python.xlsx')
#     for i in ["Data","Exchange","OrderBook"]:
#         try:
#             wb.sheets(i)
#         except:
#             wb.sheets.add(i)
#     dt = wb.sheets("Data")
#     ex = wb.sheets("Exchange")
#     ob = wb.sheets("OrderBook")
#     ex.range("a:n").value = ob.range("a:h").value = dt.range("p:q").value = None
#     dt.range(f"a1:q1").value = ["Sr No","Symbol","Open","high","Low","LTP","Volume","Vwap","Best Bid Price",
#                                 "Best Ask Price","Close","OI","IV","Delta","Gamma","Rho","Theta","Vega","Qty","Direction","Entry Signal","Exit Signal","Entry","Exit"]
    
#     subs_lst = []
#     while True:
#         try:
#             master_contract = pd.DataFrame(kite.instruments())
#             #master_contract = master_contract.drop(["instrument_token","exchange_token","last_price","tick_size"],axis=1)
#             master_contract["watchlist_symbol"] = master_contract["exchange"] + ":" + master_contract["tradingsymbol"]
#             master_contract.columns = master_contract.columns.str.replace("_"," ")
#             master_contract.columns = master_contract.columns.str.title()
#             ex.range("a1").value = master_contract

#             df = copy.deepcopy(master_contract)
#             df = df[df["Segment"] == "NFO-OPT"]
#             nfo_dict = {}
#             for i in df.index:
#                 nfo_dict[f'NFO:{df["Tradingsymbol"][i]}'] = [df["Expiry"][i],df["Strike"][i],df["Name"][i]]
#             break
#         except Exception as e:
#             time.sleep(1)
#     while True:
#         try:
#             time.sleep(0.5)
#             get_live_data(subs_lst)
#             symbols = dt.range(f"b{2}:b{500}").value
#             trading_info = dt.range(f"s{2}:x{500}").value

#             for i in subs_lst:
#                 if i not in symbols:
#                     subs_lst.remove(i)
#                     try:
#                         del live_data[i]
#                     except Exception as e:
#                         pass
#             main_list = []
#             idx = 0
#             for i in symbols:
#                 lst = [None,None,None,None,None,None,None,None,
#                         None,None,None,None,None,None,None,None]
#                 if i:
#                     if i not in subs_lst:
#                         subs_lst.append(i)
#                     if i in subs_lst:
#                         try:
#                             lst = [live_data[i]["ohlc"]["open"],
#                                    live_data[i]["ohlc"]["high"],
#                                    live_data[i]["ohlc"]["low"],
#                                    live_data[i]["last_price"]]
#                             try:
#                                 lst += [live_data[i]["volume"],
#                                         live_data[i]["average_price"],
#                                         live_data[i]["depth"]["buy"][0]["price"],
#                                         live_data[i]["depth"]["sell"][0]["price"],
#                                         live_data[i]["ohlc"]["close"],
#                                         live_data[i]["oi"]]
#                                 try:
#                                     lst += greeks(premium=live_data[i]["last_price"],
#                                                     expiry=nfo_dict[i][0],
#                                                     asset_price=live_data["NSE:NIFTY 50" if nfo_dict[i][2] == "NIFTY" else ("NSE:NIFTY BANK" if nfo_dict[i][2] == "BANKNIFTY" else f"NSE:{nfo_dict[i][2]}")]["last_price"],
#                                                     strike_price=nfo_dict[i][1],
#                                                     interest_rate=0.1,
#                                                     instrument_type=i[-2:])
#                                 except Exception as e:
#                                     lst += ["-","-","-","-","-","-"]

#                             except:
#                                 lst += [0,0,0,0,live_data[i]["ohlc"]["close"],0,"-","-","-","-","-","-"]
#                             trade_info = trading_info[idx]
#                             if trade_info[0] is not None and trade_info[1] is not None:
#                                 if type(trade_info[0]) is float and type(trade_info[1]) is str:
#                                     if trade_info[1].upper() == "BUY" and trade_info[2] is True:
#                                         if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
#                                             dt.range(f"w{idx + 2}").value = place_trade(i,int(trade_info[0]),"Buy")
#                                         elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
#                                             dt.range(f"x{idx +2}").value = place_trade(i, int(trade_info[0]), "Sell")
#                                     if trade_info[1].upper() == "SELL" and trade_info[2] is True:
#                                         if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
#                                             dt.range(f"w{idx +2 }").value = place_trade(i, int(trade_info[0]), "Sell")
#                                         elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
#                                             dt.range(f"x{idx + 2}").value = place_trade(i, int(trade_info[0]),"Buy")
#                         except Exception as e:
#                             pass
#                 main_list.append(lst)
#                 idx +=1
            
#             dt.range("c2").value = main_list
#             if wb.sheets.active.name == "OrderBook":
#                 ob.range("a1").value = get_orderbook()
#         except Exception as e:
#             print(e)

# if __name__=='__main__':
#     # get_login_credentials()
#     # get_access_token()
#     # get_kite()

#     # user_id = "YR6706"       # Login Id
#     # password = "vaa6762m"      # Login password
#     # twofa = "274957"         # Login Pin or TOTP
#     # enctoken = get_enctoken(user_id, password, twofa)
#     # kite = KiteApp(enctoken=enctoken)

#     enctoken = "pl2QjIkbYC21S2iKAYEE7JBKF2gMnvj2SoXPBvsblM27blj4R3YorWzyJphfuefkfbtfxlBvm50nbcKcjNvJrUs5bCUelQLL+SPbgaPFTeMtNXOzSGJFAQ=="
#     kite = KiteApp(enctoken=enctoken)
#     get_orderbook()
#     # quote('NIFTY')
#     start_excel()



