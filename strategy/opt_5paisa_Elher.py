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
import math 
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from numpy import log as nplog
from numpy import NaN as npNaN
import pywhatkit as pwk
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

symbol1 = '999920005'

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True
current_time = (datetime.now()).strftime("%H:%M")

def fisher1(high, low, length=None, signal=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    hl2_ = hl2(high, low)
    highest_hl2 = hl2_.rolling(length).max()
    lowest_hl2 = hl2_.rolling(length).min()

    #hlr = high_low_range(highest_hl2, lowest_hl2)
    hlr  = highest_hl2-lowest_hl2
    hlr[hlr < 0.001] = 0.001

    position = ((hl2_ - lowest_hl2) / hlr) - 0.5
    v = 0
    m = high.size
    result = [npNaN for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        v = 0.66 * position[i] + 0.67 * v
        if v < -0.99: v = -0.999
        if v >  0.99: v =  0.999
        result.append(0.5 * (nplog((1 + v) / (1 - v)) + result[i - 1]))
    fisher = Series(result, index=high.index)
    signalma = fisher.shift(signal)


    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    props = f"{length}_{signal}"
    fisher.name = f"FISHERT{props}"
    signalma.name = f"FISHERTs{props}"
    fisher.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {fisher.name: fisher, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"FISHERT{props}"
    df.category = fisher.category
    return df

print("----option chain----")

if not os.path.exists("opt_5paisa_Elher.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("opt_5paisa_Elher.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('opt_5paisa_Elher.xlsx')
for i in ["stats","Exchange","Expiry","Position","OrderBook","OrderBook_New","Option","Data","Buy","Sale","Final",]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
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
dt.range("a:q").value = None
by.range("a:z").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
st.range("a:z").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:s").value = None
ob1.range("a:al").value = None
#oc.range("a:z").value = None
oc.range("a:b").value = oc.range("d8:e30").value = oc.range("g1:v4000").value = None

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

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value, oc.range("d5").value, oc.range("d6").value = "Symbol==>>", "Expiry==>>", "LotSize==>>", "Total CE Value==>>", "Total PE Value==>>",

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



call_counter = 0
put_counter = 0

dfg = client.historical_data('N', 'C', symbol1, '1d', from_d, to_d)
print(dfg)
today_range = np.round(((dfg['High'].iloc[-1]) - dfg['Low'].iloc[-1]),2)

while True:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
    pos.range("a1").value = pd.DataFrame(client.margin())
    pos.range("a4").value = pd.DataFrame(client.positions())
    #ob.range("a20").value = pd.DataFrame(client.get_tradebook())


    ordbook = pd.DataFrame(client.order_book())
    # ordbook = ordbook[0:37]
    ordbook1 = ordbook    
    Datetimeee = []
    ord_type = []
    for i in range(len(ordbook)):
        ord_typ = ordbook['ScripName'][i]
        ord_type1 = ord_typ[22:24]
        ord_type.append(ord_type1)
        datee = ordbook['BrokerOrderTime'][i]
        timestamp = pd.to_datetime(datee[6:19], unit='ms')
        ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
        d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
        d2 = d1 + timedelta(hours = 5.5)
        Datetimeee.append(d2)
    ordbook['Datetimeee'] = Datetimeee
    ordbook['ord_type'] = ord_type    
    ob1.range("a1").value = ordbook  

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

            opt = pd.DataFrame(client.get_option_chain("N", oc_symbol, expiry)['Options'])

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
            lengt = round((df1.shape[0])/2)
            re1 = df1['StrikeRate'].iloc[lengt]
            re2 = df1['StrikeRate'].iloc[lengt+1]
            diff = (re2-re1)

            des_ltp = 85

            CE_strike_ltp = (df1[df1['CE_Ltp'] < des_ltp][['CE_Ltp']].values.tolist())[0][0]
            PE_strike_ltp = (df1[df1['PE_Ltp'] < des_ltp][['PE_Ltp']].values.tolist())[-1][0]
            CE_strike_ltp_script = (df1[df1['CE_Ltp'] < des_ltp][['CE_Script']].values.tolist())[0][0]
            PE_strike_ltp_script = (df1[df1['PE_Ltp'] < des_ltp][['PE_Script']].values.tolist())[-1][0]

            # CE_strike = math.trunc(round(underlying_price/diff,0)*diff)
            # PE_strike = math.trunc((round(underlying_price/diff,0)*diff)+diff)
            # CE_strike_ltp = (df1[df1['StrikeRate'] == CE_strike][['CE_Ltp']].values.tolist())[0][0]
            # PE_strike_ltp = (df1[df1['StrikeRate'] == PE_strike][['PE_Ltp']].values.tolist())[-1][0]
            # CE_strike_ltp_script = (df1[df1['StrikeRate'] == CE_strike][['CE_Script']].values.tolist())[0][0]
            # PE_strike_ltp_script = (df1[df1['StrikeRate'] == PE_strike][['PE_Script']].values.tolist())[-1][0]

            oc.range("d8").value = [["Spot LTP",underlying_price],
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

            current_data = df1[(df1["StrikeRate"] == round(underlying_price/diff,0)*diff)]
            oc.range("e5").value = current_data['CE_Ltp'].iloc[-1]*lot_size
            oc.range("e6").value = current_data['PE_Ltp'].iloc[-1]*lot_size

            current_data = lot_size
            quantity = lot_size*1

            # print(quantity)
            # print(today_range)
            today_range = 210

            if today_range >= 0 and today_range <= 200:
                SLL_BN = 20
                TGG_BN = 40
            if today_range > 200 and today_range <= 300:
                SLL_BN = 20
                TGG_BN = 60
            if today_range > 300 and today_range <= 400:
                SLL_BN = 20
                TGG_BN = 80
            if today_range > 400 :
                SLL_BN = 20
                TGG_BN = 100

            # print("Quantity is : "+str(quantity))
            # print("Target is : "+str(TGG)+" and StopLoss is : "+str(SLL))
            
            SL = SLL_BN
            TG = TGG_BN/2
            
            print("Today's range is : "+str(today_range))
            print("Target is : "+str(TG)+" and Stoploss is : "+str(SL))

            BuySl_price = np.round(CE_strike_ltp-(SL),2)
            SellSl_price = np.round(PE_strike_ltp-(SL),2)
            BuySl_ATM_price = np.round(CE_strike_ltp-(SL),2)
            SellSl_ATM_price = np.round(PE_strike_ltp-(SL),2)
          
            df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)
            # df = df[0:299]
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df['Date'] = pd.to_datetime(df['Datetime']).dt.date
            df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
            df['Time'] = pd.to_datetime(df['Datetime']).dt.time
            df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
            df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
            df.set_index('Datetime',inplace=True)
            fisher_transform = (fisher1(high=df['High'],low=df['Low'],length=20))
            df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
            df['FISHERT_WH'] = np.round((fisher_transform[fisher_transform.columns[0]]),2)
            df['FISHERTs_RED'] = np.round((fisher_transform[fisher_transform.columns[1]]),2)
            df['El_Fis_diff'] = np.round(abs((df['FISHERT_WH']-df['FISHERTs_RED'])),2)

            # for i in (10,13):
            #     df['EMA_'+str(i)] = np.round((ta.trend.ema_indicator(df.Close, window=i)),2)
            # df['atr'] = np.round((ta.volatility.average_true_range(df.High,df.Low,df.Close)),2)       

            #df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E",""))
            #df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["RSI_14"] > 50),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["RSI_14"] < 50),"S_E",""))
            df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["El_Fis_diff"] > 0.25),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["El_Fis_diff"] > 0.25),"S_E",""))            
            df['Entry1'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(1) != "B_E"),"B_E",np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E",""))
            df['Ent_A'] = (np.where(df['Entry1'] == "B_E",df['Close'],(np.where(df['Entry1'] == "S_E",df['Close'],npNaN))))
            df['Ent_A'] = df['Ent_A'].ffill()
            df['Ent_B'] = df['Close']-df['Ent_A']
            df['Ent_B'] = np.where(df['Entry'] == "B_E",(df['Close']-df['Ent_A']),np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0))
            df['Ent_C'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(-1) != "B_E"),"B_Ex",
                        np.where((df['Entry'] == "S_E") & (df['Entry'].shift(-1) != "S_E"),"S_Ex",
                        np.where(((df['Entry'] == "B_E") & (df['Ent_B'] <= - SLL_BN)),"B_SL",np.where(((df['Entry'] == "B_E") & (df['Ent_B'] >= TGG_BN)),"B_TP",
                        np.where(((df['Entry'] == "S_E") & (df['Ent_B'] <= - SLL_BN)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_B'] >= TGG_BN)),"S_TP",""))))))

            df.dropna(inplace=True)

            length = len(df)-1
            Buying = pd.DataFrame()
            Selling = pd.DataFrame()
            new_df1 = pd.DataFrame()    

            for i in range(len(df)):
                if [i+1][0] <= length:
                    if df['Entry1'].iloc[i + 1] == "B_E":
                        bay = (df['Ent_A'].iloc[i + 1])
                        buyy = df[i+1:i+2]
                        Buying = pd.concat([buyy, Buying])
                        sal = df[df['Ent_A'] == bay]
                        sal1 = (sal[(sal['Ent_C'] == "B_SL") | (sal['Ent_C'] == "B_TP") | (sal['Ent_C'] == "B_Ex")])
                        sal1['Sell_Date'] = (df.Date.iloc[i + 1])
                        sal1['Sell_Time'] = (df.Time.iloc[i + 1])
                        Selling = pd.concat([sal1[:1], Selling])

                    if df['Entry1'].iloc[i + 1] == "S_E":
                        bay1 = (df['Ent_A'].iloc[i + 1])
                        buyy1 = df[i+1:i+2]
                        Buying = pd.concat([buyy1, Buying])
                        sal1 = df[df['Ent_A'] == bay1]
                        sal11 = (sal1[(sal1['Ent_C'] == "S_SL") | (sal1['Ent_C'] == "S_TP") | (sal1['Ent_C'] == "S_Ex")])
                        sal11['Sell_Date'] = (df.Date.iloc[i + 1])
                        sal11['Sell_Time'] = (df.Time.iloc[i + 1])
                        Selling = pd.concat([sal11[:1], Selling])

            Buying.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True) 
            Buying.rename(columns={'Date': 'Datee', 'Time': 'Timee'}, inplace=True)
            Selling.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True)  
            Selling.rename(columns={'Sell_Date': 'Datee', 'Sell_Time': 'Timee'}, inplace=True)
            new_df1 = pd.merge(Buying, Selling,on=["Datee", "Timee"])
  
            dt.range("a1").value = df
            by.range("a1").value = Buying
            sl.range("a1").value = Selling
            fl.range("a1").value = new_df1

            if ordbook['Qty'].iloc[-1] != quantity:
                print("Order_Book is Empty")
                if df['Entry1'].iloc[-2] == "B_E":     
                    call_counter = 1                  
                    #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_strike_ltp_script, Qty=quantity,Price=CE_strike_ltp, IsIntraday=True)#, IsStopLossOrder=True, StopLossPrice=BuySl_ATM_price)
                    # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
                    print("Call Buy Order Excecuted at : "+str(CE_strike_ltp))
                if df['Entry1'].iloc[-2] == "S_E":
                    put_counter = 1
                    #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_strike_ltp_script, Qty=quantity,Price=PE_strike_ltp, IsIntraday=True)#,IsStopLossOrder=True, StopLossPrice=SellSl_ATM_price)  
                    # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
                    print("Put Buy Order Excecuted at : "+str(PE_strike_ltp))    
                else :
                    print("NO 1st Trade")      

            ordbook1 = ordbook[ordbook["OrderStatus"] == "Fully Executed"]
            ordbook1 = ordbook1[['Datetimeee', 'BrokerOrderId', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','RemoteOrderID','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','ord_type','AtMarket']]
            ordbook2 = ordbook1[ordbook1["BuySell"] == "B"]
            ob.range("a1").value = ordbook1

            Datetimeee = list(ordbook1['Datetimeee'])

            if ordbook1.isin(['CE']).any().any():

                ordbook_CE = ordbook2[ordbook2["ord_type"] == "CE"]

                last_ord_type_CE = ordbook_CE["ord_type"].iloc[-1]
                last_ord_script_CE = ordbook_CE["ScripCode"].iloc[-1]
                last_ord_rate_CE = ordbook_CE["Rate"].iloc[-1]
                last_ord_buy_sell_CE = ordbook_CE["BuySell"].iloc[-1]
                last_ord_time_CE = ordbook_CE["Datetimeee"].iloc[-1]

                CE_ord_ltp = (df1[df1['CE_Script'] == last_ord_script_CE][['CE_Ltp']].values.tolist())[0][0]

                # print("Call Data")
                # print("(1) last_BuySell_type is : "+str(ordbook1["BuySell"].iloc[-1])+" and last_ord_type is : "+str(ordbook1["ord_type"].iloc[-1]))
                # print("(2) last_ord_script_CE is : "+str(last_ord_script_CE))
                # print("(3) last_ord_rate_CE is : "+str(last_ord_rate_CE))
                # print("(4) CE_ord_ltp is : "+str(CE_ord_ltp))
                # print("(5) last_ord_time_CE is : "+str(last_ord_time_CE))


                if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "CE"):                
                    if (CE_ord_ltp > last_ord_rate_CE + TG):
                        squareoff = client.squareoff_all()
                        call_counter = 0
                        # pwk.sendwhatmsg_instantly("+919610033622","Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                        print("Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity)) 
                    if (CE_ord_ltp < last_ord_rate_CE - SL):
                        squareoff = client.squareoff_all()
                        call_counter = 0
                        # pwk.sendwhatmsg_instantly("+919610033622","Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                        print("Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity)) 

                if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "CE"):  

                    Targett = last_ord_rate_CE + TG
                    Stoploss = last_ord_rate_CE - SL
                    # pwk.sendwhatmsg_instantly("+919610033622","Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919610033622","Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss),10,True,5)
                    print("CALLLL")
                    print("Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity))
                    print("Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss))

            if ordbook1.isin(['PE']).any().any():

                ordbook_PE = ordbook2[ordbook2["ord_type"] == "PE"]

                last_ord_type_PE = ordbook_PE["ord_type"].iloc[-1]
                last_ord_script_PE = ordbook_PE["ScripCode"].iloc[-1]
                last_ord_rate_PE = ordbook_PE["Rate"].iloc[-1]
                last_ord_buy_sell_PE = ordbook_PE["BuySell"].iloc[-1]
                last_ord_time_PE = ordbook_PE["Datetimeee"].iloc[-1]

                PE_ord_ltp = (df1[df1['PE_Script'] == last_ord_script_PE][['PE_Ltp']].values.tolist())[-1][0]

                # print("Put Data")
                # print("(1) last_BuySell_type is : "+str(ordbook1["BuySell"].iloc[-1])+" and last_ord_type is : "+str(ordbook1["ord_type"].iloc[-1]))
                # print("(2) last_ord_script_PE is : "+str(last_ord_script_PE))
                # print("(3) last_ord_rate_PE is : "+str(last_ord_rate_PE))
                # print("(4) PE_ord_ltp is : "+str(PE_ord_ltp))
                # print("(5) last_ord_time_PE is : "+str(last_ord_time_PE))

                if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "PE"):                
                    if (PE_ord_ltp > last_ord_rate_PE + TG):
                        put_counter = 0
                        squareoff = client.squareoff_all()
                        # pwk.sendwhatmsg_instantly("+919610033622","Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                        print("Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))
                    if (PE_ord_ltp < last_ord_rate_PE - SL):
                        put_counter = 0
                        squareoff = client.squareoff_all()
                        # pwk.sendwhatmsg_instantly("+919610033622","Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                        print("Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))


                if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "PE"):  
                    Targett = last_ord_rate_PE + TG
                    Stoploss = last_ord_rate_PE - SL
                    # pwk.sendwhatmsg_instantly("+919610033622","Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919610033622","Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss),10,True,5)
                    print("PUTTT")
                    print("Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))
                    print("Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss))              
            
            else:
                print("No data in OrderBook")          

            if df['Entry1'].iloc[-2] == "B_E":                       
                if (ordbook1["ScripCode"].iloc[-1] == CE_strike_ltp_script) and (ordbook1["BuySell"].iloc[-1] == "B"): # and (ordbook1["TradedQty"].iloc[-1] == lot_size):
                    # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Already Executed at : "+str(last_ord_time_CE),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Already Executed at : "+str(last_ord_time_CE),10,True,5)
                    print("Call Buy Order Already Executed at : "+str(last_ord_time_CE))
                else:    
                    if call_counter == 0:
                        put_counter = 0
                        squareoff = client.squareoff_all() 
                        #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_strike_ltp_script, Qty=quantity,Price=CE_strike_ltp, IsIntraday=True)#, IsStopLossOrder=True, StopLossPrice=BuySl_ATM_price)
                        call_counter = 1
                        # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
                        print("Call Buy Order Excecuted at : "+str(CE_strike_ltp))
                        
            if df['Entry1'].iloc[-2] == "S_E":
                if (ordbook1["ScripCode"].iloc[-1] == PE_strike_ltp_script) and (ordbook1["BuySell"].iloc[-1] == "B"): # and (ordbook1["TradedQty"].iloc[-1] == lot_size):
                    # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Already Executed at : "+str(last_ord_time_PE),10,True,5)
                    # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Already Executed at : "+str(last_ord_time_PE),10,True,5)
                    print("Put Buy Order Already Executed at : "+str(last_ord_time_PE))
                else:  
                    if put_counter == 0:
                        call_counter = 0
                        squareoff = client.squareoff_all()
                        #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_strike_ltp_script, Qty=quantity,Price=PE_strike_ltp, IsIntraday=True)#,IsStopLossOrder=True, StopLossPrice=SellSl_ATM_price)  
                        put_counter = 1
                        # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
                        # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
                        print("Put Buy Order Excecuted at : "+str(PE_strike_ltp))                    
            else:
                print("No Trade")
            print("Call counter is : "+str(call_counter))
            print("Put counter is : "+str(put_counter))
        except Exception as e:
            pass                       



