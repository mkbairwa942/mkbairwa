import os
from five_paisa import *
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
from datetime import datetime,timedelta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

pd.options.mode.copy_on_write = True

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

live_market_keys = ['NIFTY 50','NIFTY BANK',]#,'Securities in F&O', ]

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

    def get_stock_fno_info(self, symbol, trade_info=False):
        if trade_info:
            url = 'https://www.nseindia.com/api/quote-derivative?symbol=' + symbol + "&section=trade_info"
        else:
            url = 'https://www.nseindia.com/api/quote-derivative?symbol=' + symbol
        data = self.session.get(url, headers=self.headers).json()
        return data

    def live_market_data(self, key, symbol_list=False):
        data = self.session.get(
            f"https://www.nseindia.com/api/equity-stockIndices?index="
            f"{key.upper().replace(' ', '%20').replace('&', '%26')}",
            headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        df = df.drop(["meta"], axis=1)
        df = df.set_index("symbol", drop=True)
        df =  df[['identifier','open','dayHigh','dayLow',
            'lastPrice','previousClose','change','pChange',
            'totalTradedVolume','totalTradedValue','lastUpdateTime']]            
        if symbol_list:
            return list(df.index)
        else:
            return df

nse = NseIndia()

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


def place_trade(Exche,ExchTypee,symbol,scripte,quantity, direction):
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
       
def quote(instruments):
    if instruments:
        try:
            data = kite.quote(instruments)
            for symbol, values in data.items():
                try:
                    option_data[symbol[4:]]
                except:
                    option_data[symbol[4:]] = {}
                option_data[symbol[4:]]["Strike"] = instruments_dict[symbol]["Strike"]
                option_data[symbol[4:]]["Lot"] = instruments_dict[symbol]["Lot"]
                option_data[symbol[4:]]["Expiry"] = instruments_dict[symbol]["Expiry"]
                option_data[symbol[4:]]["Instument Type"] = instruments_dict[symbol]["Instrument Type"]
                option_data[symbol[4:]]["Open"] = values["ohlc"]["open"]
                option_data[symbol[4:]]["High"] = values["ohlc"]["high"]
                option_data[symbol[4:]]["Low"] = values["ohlc"]["low"]
                option_data[symbol[4:]]["Ltp"] = values["last_price"]
                option_data[symbol[4:]]["Close"] = values["ohlc"]["close"]
                option_data[symbol[4:]]["Volume"] = values["volume"]
                option_data[symbol[4:]]["Vwap"] = values["average_price"]
                option_data[symbol[4:]]["OI"] = values["oi"]
                option_data[symbol[4:]]["OI High"] = values["oi_day_high"]
                option_data[symbol[4:]]["OI Low"] = values["oi_day_low"]
                option_data[symbol[4:]]["Buy Qty"] = values["buy_quantity"]
                option_data[symbol[4:]]["Sell Qty"] = values["sell_quantity"]
                option_data[symbol[4:]]["Ltq"] = values["last_quantity"]
                option_data[symbol[4:]]["Change"] = values["net_change"]
                option_data[symbol[4:]]["Bid Price"] = values["depth"]["buy"][0]["price"]
                option_data[symbol[4:]]["Bid Qty"] = values["depth"]["buy"][0]["quantity"]
                option_data[symbol[4:]]["Ask Price"] = values["depth"]["sell"][0]["price"]
                option_data[symbol[4:]]["Ask Qty"] = values["depth"]["sell"][0]["quantity"]
        except:
            pass
    return option_data

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

if not os.path.exists("Breakout_for_opt.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Breakout_for_opt.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Breakout_for_opt.xlsx')
for i in ["stats","Exchange","Expiry","Position","OrderBook","OrderBook_New","Option","Data","Buy","Sale","Final",
            "Stat","Stat1","Stat2","Stat3","Stat4"]:
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
st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
dt.range("i:s").value = None
by.range("a:z").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
st.range("a:z").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:s").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None
st1.range("a:u").value = None
st2.range("a:u").value = None
st3.range("a:u").value = None
st4.range("a:i").value = None
#oc.range("a:z").value = None
dt.range(f"a1:d1").value = ["Namee","Stop Loss","Add Till","Buy At","Target" ,"Term","Time", "","","","","","","","","","","","","","Quantity","Entry","Exit","SL","Status"]
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
            #exchange = exchange[exchange["ExchType"] == "D"]
            exchange['Expiry1'] = pd.to_datetime(exchange['Expiry']).dt.date
            exchange1 = exchange[(exchange['ExchType'].isin(['C', 'D']))]
            exchange1 = exchange1[(exchange1['Series'].isin(['EQ', 'XX']))]
            exchange2 = exchange[exchange["Series"] == "EQ"]
            exchange = exchange[exchange['CpType'].isin(['CE', 'PE'])]
            
            # print(exchange.tail(20))
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)
exc.range("v1").value = exchange1
exc.range("ar1").value = exchange2
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

# dfg = client.historical_data('N', 'C', symbol1, '1d', from_d, to_d)
# print(dfg)
# today_range = np.round(((dfg['High'].iloc[-1]) - dfg['Low'].iloc[-1]),2)

while True:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
    pos.range("a1").value = pd.DataFrame(client.margin())
    pos.range("a4").value = pd.DataFrame(client.positions())
    pos.range("a10").value = pd.DataFrame(client.holdings())  
    # pos.range("a12").value = pd.DataFrame(client.get_tradebook())


    ordbook = pd.DataFrame(client.order_book())
    ob1.range("a1").value = ordbook 
    if ordbook is not None:
        print("Order Book not Empty")
        # print(ordbook.head(1))
        # ordbook = ordbook[ordbook.iloc[9] != "Fully Executed"]
        # ordbook = ordbook[['BrokerOrderTime', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
        # Datetimeee = []
        # for i in range(len(ordbook)):
        #     print(i,ordbook['BrokerOrderTime'])
        #     datee = ordbook['BrokerOrderTime'][i]
        #     timestamp = pd.to_datetime(datee[6:19], unit='ms')
        #     ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
        #     d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
        #     d2 = d1 + timedelta(hours = 5.5)
        #     Datetimeee.append(d2)
    else:
        print("Order Book Empty")

    ob.range("a1").value = ordbook 

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

            input_list = list(df1['CE_OI'])
            input_list1 = list(df1['StrikeRate'])
            max_value = max(input_list)
            index = input_list.index(max_value)
            diff = input_list1[index+1]-input_list1[index]


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

            current_data = df1[(df1["StrikeRate"] == round(underlying_price/diff,0)*diff)]
            oc.range("e5").value = current_data['CE_Ltp'].iloc[-1]*lot_size
            oc.range("e6").value = current_data['PE_Ltp'].iloc[-1]*lot_size

            exc_df = copy.deepcopy(exchange1)
            exc_df = exc_df[(exc_df['Root'].isin(['NIFTY', 'BANKNIFTY'])) & (exc_df["Expiry1"] == oc_expiry.date())]
            nifty_current_ltp = get_live_data("N","C","NIFTY")['Data'][0]["LastTradedPrice"]
            bank_nifty_current_ltp = get_live_data("N","C","BANKNIFTY")['Data'][0]["LastTradedPrice"]
            current_data_nifty = round(nifty_current_ltp/diff,0)*diff
            current_data_bank_nifty = round(bank_nifty_current_ltp/diff,0)*diff

            nifty_cut1 =  current_data_nifty-50
            nifty_cut2 = current_data_nifty
            nifty_cut3 = current_data_nifty+50
            bank_nifty_cut1 = current_data_bank_nifty-100
            bank_nifty_cut2 = current_data_bank_nifty
            bank_nifty_cut3 = current_data_bank_nifty+100

            index1 = exc_df[(exc_df['StrikeRate'].isin([nifty_cut1,nifty_cut2,nifty_cut3,bank_nifty_cut1,bank_nifty_cut2,bank_nifty_cut3]))]
            index1['Concate'] = index1['Name']+":"+index1['Scripcode'].astype(str)
            index1 = index1['Concate'].apply(lambda x: "{}{}".format('N:D:', x))
            index1 = index1.tolist()

            time.sleep(0.5)            
            scpt = dt.range(f"a{2}:c{500}").value            
            sym = dt.range(f"a{2}:a{500}").value
            symbols = list(filter(lambda item: item is not None, sym))
            symb_frame = exchange2[(exchange2['Root'].isin(symbols))]
            symb_frame['Concate'] = "N:C:"+symb_frame['Name']+":"+symb_frame['Scripcode'].astype(str)
            symbolss = list(symb_frame['Concate'])
            symbolss.sort()


            max_min = oc.range(f"e{17}:e{22}").value
            trading_info = dt.range(f"u{2}:x{30}").value  
            
            maxxx = max(list(max_min))
            minnn = min(list(max_min))
            print(maxxx,minnn)

            scpts = pd.DataFrame(scpt, columns=['Symbol','Buy/Sell','ScriptCode'])
            index = ['N:C:NIFTY:999920000','N:C:BANKNIFTY:999920005','N:C:FINNIFTY:999920041'] #999920000 999920005 999920041

            for li in index:                 
                symbolss.append(li)
            for li1 in index1:
                symbolss.append(li1)
            #symbolss.reverse()

            subs_lst = symbolss
            for i in subs_lst:   
                if i not in symbolss:
                    subs_lst.remove(i)
                    try:
                        del live_data[i]
                    except Exception as e:
                        pass
            main_list = pd.DataFrame()
            idx = 0

            for i in symbolss:
                if i:
                    if i not in subs_lst:
                        subs_lst.append(i)
                    if i in subs_lst:
                        try:
                            main_li = pd.DataFrame()
                            Exche = i.split(":")[0]
                            ExchTypee = i.split(":")[1]
                            Namee = i.split(":")[2]
                            Scripcodee = i.split(":")[3]
                            live_data = get_live_data(Exche,ExchTypee,Namee)
                            main_li['Symbol'] = Namee,
                            main_li['Open'] = live_data['Data'][0]['Open'],
                            main_li['High'] = live_data['Data'][0]['High'],
                            main_li['Low'] = live_data['Data'][0]['Low'],
                            main_li['LTP'] = live_data['Data'][0]["LastTradedPrice"],
                            main_li['Volume'] = live_data['Data'][0]["Volume"],
                            main_li['Vwap'] = live_data['Data'][0]["AverageTradePrice"],
                            main_li['Close'] = live_data['Data'][0]["Close"],
                            main_li['OI'] = live_data['Data'][0]["OpenInterest"],
                            main_li['NetChange'] = live_data['Data'][0]["NetChange"] 
                            main_list = pd.concat([main_li, main_list])     
           
                            trade_info = trading_info[idx]
                            # place_trade(Exche,ExchTypee,symbol,scripte,quantity, direction)
                            if trade_info[0] is not None and trade_info[1].upper() is not None:
                                print("11")
                                # print(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]))
                                print(i)
                                # Quantity      Entry	Exit	sl
                                #  1000	        buy	    True	 200
                                print(trade_info[0],trade_info[1],trade_info[2],trade_info[3])

                                if trade_info[1].upper() == "BUY" and trade_info[2] is None:  
                                    print("Buy order")   
                                    dt.range(f"t{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"B")

                                if trade_info[1].upper() == "BUY" and trade_info[2].upper() == "SELL":
                                    print("Sell order")  
                                    dt.range(f"u{idx +2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"S")

                                if trade_info[1].upper() == "SELL" and trade_info[2] is None:  
                                    print("Sell order")                                    
                                    dt.range(f"t{idx +2 }").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"S")

                                if trade_info[1].upper() == "SELL" and trade_info[2].upper() == "BUY":   
                                    print("Buy order")                                   
                                    dt.range(f"u{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"B")

                            #print(i,trading_info)
                        except Exception as e:                
                            pass                
                    
                idx +=1
 
            #main_list.sort_values(['Symbol'], ascending=[True], inplace=True)
            main_list['Time'] = datetime.now()
            main_list3 = main_list
            #main_list3[::-1]
            main_list4 = main_list3.iloc[::-1]
            main_list4 = main_list4[['Symbol','Open','High','Low','LTP','Close','NetChange','Time']]
            dt.range("i1").options(index=False).value = main_list4  


            # positionn = pd.DataFrame(client.positions())
            # positionn.rename(columns={'ScripName': 'Symbol','LTP':'LTPP'}, inplace=True)
            # main_list5 = pd.merge(main_list4, positionn, on=['Symbol'], how='outer')
            # main_list5 = main_list5[['Symbol','Open','High','Low','LTP','Close','NetChange','Time','BuyAvgRate','MTOM','BookedPL']]
            # dt.range("i1").options(index=False).value = main_list5  


            live_market_keys.reverse()
            index_frame = pd.DataFrame()
            index_frame_one = pd.DataFrame()

            for idx in live_market_keys:
                print(idx)
                index_fra = nse.live_market_data(idx) 
                tot_valuee = index_fra["totalTradedValue"].iloc[0]               
                index_fra['Index'] = idx                
                index_fram = index_fra[1:]
                index_fram['Weitage'] = round(((index_fram["totalTradedValue"]*100)/tot_valuee),2)
                post = (index_fram['change'] > 0).sum().sum()
                negat = (index_fram['change'] < 0).sum().sum()
                index_frame = pd.concat([index_fram, index_frame])
                index_row = index_fra[:1] 
                idx_len = len(index_fram['Index'])
                index_row['Post'] = post
                index_row['Negat'] = negat
                index_row['Neutral'] = idx_len-(index_row['Post']+index_row['Negat'])
                index_row['Total'] = idx_len
                index_row['Calc'] = (index_row['Post']*100)/index_row['Total']
                index_row['Per'] = np.round((np.where(index_row['Calc']<50,(index_row['Calc'])-50,(index_row['Calc'])-50)),2)
                index_frame_one = pd.concat([index_row, index_frame_one],axis=0)

            index_frame_one.sort_values(['change','identifier'], ascending=[True,True], inplace=True)
            index_frame_one = index_frame_one[['Index','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','lastUpdateTime','Post','Negat','Neutral','Total','Per']]
            index_frame.sort_values(['Index','change'], ascending=[True,True], inplace=True)
            index_frame = index_frame[['Index','identifier','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','Weitage','totalTradedVolume','totalTradedValue','lastUpdateTime']]
            nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY 50")]
            bank_nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY BANK")]
            nifty_range = nifty2['dayHigh'].iloc[-1] - nifty2['dayLow'].iloc[-1]
            bank_nifty_range = bank_nifty2['dayHigh'].iloc[-1] - bank_nifty2['dayLow'].iloc[-1]      

            st3.range("a1").options(index=False).value = index_frame
            st2.range("a:n").value = None
            st2.range("p1").options(index=False).value = "Today's rangs is"
            st2.range("p3").options(index=False).value = nifty_range
            st2.range("p2").options(index=False).value = bank_nifty_range
            st2.range("a1").options(index=False).value = index_frame_one

            nifty1 = index_frame[(index_frame["Index"] == "NIFTY 50")]
            nifty1 = nifty1[['identifier','change','pChange','Weitage']]            
            bank_nifty1 = index_frame[(index_frame["Index"] == "NIFTY BANK")]
            bank_nifty1 = bank_nifty1[['identifier','change','pChange','Weitage']]
            nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY 50")]
            bank_nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY BANK")]
      

            st4.range("a1").options(index=False).value = nifty1
            st4.range("f1").options(index=False).value = bank_nifty1
            st4.range("k2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*5+COLUMN(B2),2))"
            st4.range("q2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*3+COLUMN(B2),7))"

  

            # def insert_heading(rng,text):
            #     rng.value = text
            #     rng.font.bold = True
            #     rng.font.size = 24
            #     rng.font.color = (0,0,139)


            # insert_heading(pos.range("a10"),"Matplotlib Chart")

            # fig = plt.figure()
            # x = nifty1['identifier']
            # y = nifty1['change']
            # y_pos = range(len(x))
            # plt.bar(y_pos, y)
            # # Rotation of the bars names
            # plt.xticks(y_pos, x, rotation=90,fontsize=5)
            # plt.grid(False)
            # plt.ylabel("Change")
            # plt.title("Total Change")
            # pos.pictures.add(
            #     fig,
            #     name="Matplotlib",
            #     update=True,
            #     left=pos.range("a12").left,
            #     top=pos.range("a12").top,
            #     height=300,
            #     width=700,
            # )

            # insert_heading(pos.range("a33"),"Pandas Chart")
            # ax = nifty1.plot(kind="bar",x='identifier',y='change',color='#50C878',grid=False)
            # fig = ax.get_figure()
            # pos.pictures.add(
            #     fig,
            #     name="Pandas",
            #     update=True,
            #     left=pos.range("a35").left,
            #     top=pos.range("a35").top,
            #     height=300,
            #     width=700,)

        
            #st4.range("q20").options(index=False).value = cht
            
            nift_50 = index_frame_one[index_frame_one['Index'] == "NIFTY 50"] 
            nift_bank = index_frame_one[index_frame_one['Index'] == "NIFTY BANK"] 
            niftt_50 = round(float(nift_50['Per']),2)
            niftt_bank = round(float(nift_bank['Per']),2)

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
           
            SL = SLL_BN
            TG = TGG_BN/2

            print("Today's Nifty range is : "+str(nifty_range))
            print("Today's Banknifty range is : "+str(bank_nifty_range))
            print("Target is : "+str(TG)+" and Stoploss is : "+str(SL))
            print("Nifty_50 Per is : "+str(niftt_50))
            print("BankNifty Per is : "+str(niftt_bank))
            
            main_list = pd.merge(scpts, main_list, on=['Symbol'], how='inner')
            main_list1 = main_list[main_list['Buy/Sell'] == "BUY"] 
            main_list2 = main_list[main_list['Buy/Sell'] == "SELL"] 
            
            funn = 14000
            Profit = 200
            Loss = -200

            funn = pd.DataFrame(client.margin())['AvailableMargin'] 
            fund1 = funn*2
            fund2 = funn         

            if main_list1.empty:
                print("main_list1 Is Empty")
                leght1 = 0
                main_list1['Exp_Qty'] = 0
            else:
                leght1 = fund1/(len(main_list1['LTP']))
                main_list1['Exp_Qty'] = (round((float(leght1)/(main_list1['LTP'])),0))

            if main_list2.empty:
                print("main_list2 Is Empty")
                leght2 = 0
                main_list2['Exp_Qty'] = 0
            else:
                leght2 = fund2/(len(main_list2['LTP']))
                main_list2['Exp_Qty'] = (round((float(leght2)/(main_list2['LTP'])),0))

            st.range("a1").options(index=False).value = main_list   
            
            st1.range("a1").options(index=False).value = main_list
            # sheet_length = len(main_list1['LTP'])
            # print(sheet_length)
            # for i in range(10000):
            #     sheet_length = i+1
            #st4.range("a1").ver
            rng = range('A1').vertical.last_cell

            #st4.range((rng.row + 1, rng.column)).value = main_list
            #st4.range("a1").vertical.last_cell.options(index=False).value = main_list
            Stat4 = main_list 
            #Stat4 = pd.read_excel('E:/STOCK/Capital_vercel1/test1.xlsx', sheet_name='Stat1')
            Stat5 = pd.concat([main_list, Stat4])  
            Stat5.sort_values(['Time'], ascending=[True], inplace=True)
            Stat6 = Stat5.drop_duplicates(subset=['Symbol'], keep='first')
            Stat6['Time_diff'] = (datetime.now() - Stat6['Time'])
            Stat6['Exp_Qty'] = np.where(Stat6['Buy/Sell'] == "BUY",(round((float(leght1)/(Stat6['LTP'])),0)),(round((float(leght2)/(Stat6['LTP'])),0)))
            Stat6.sort_values(['Time'], ascending=[True], inplace=True)
            st1.range("a1").options(index=False).value = Stat6     
        
        except Exception as e:
            pass    

        #    BuySl_price = np.round(CE_strike_ltp-(SL),2)
        #    SellSl_price = np.round(PE_strike_ltp-(SL),2)
        #    BuySl_ATM_price = np.round(CE_strike_ltp-(SL),2)
        #    SellSl_ATM_price = np.round(PE_strike_ltp-(SL),2)
          
        #     df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)
        #     # df = df[0:299]
        #     df['Datetime'] = pd.to_datetime(df['Datetime'])
        #     df['Date'] = pd.to_datetime(df['Datetime']).dt.date
        #     df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
        #     df['Time'] = pd.to_datetime(df['Datetime']).dt.time
        #     df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
        #     df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
        #     df.set_index('Datetime',inplace=True)
        #     fisher_transform = (fisher1(high=df['High'],low=df['Low'],length=20))
        #     df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
        #     df['FISHERT_WH'] = np.round((fisher_transform[fisher_transform.columns[0]]),2)
        #     df['FISHERTs_RED'] = np.round((fisher_transform[fisher_transform.columns[1]]),2)
        #     df['El_Fis_diff'] = np.round(abs((df['FISHERT_WH']-df['FISHERTs_RED'])),2)

        #     # for i in (10,13):
        #     #     df['EMA_'+str(i)] = np.round((ta.trend.ema_indicator(df.Close, window=i)),2)
        #     # df['atr'] = np.round((ta.volatility.average_true_range(df.High,df.Low,df.Close)),2)       

        #     #df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E",""))
        #     #df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["RSI_14"] > 50),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["RSI_14"] < 50),"S_E",""))
        #     df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED ) & (df["El_Fis_diff"] > 0.25),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED) & (df["El_Fis_diff"] > 0.25),"S_E",""))            
        #     df['Entry1'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(1) != "B_E"),"B_E",np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E",""))
        #     df['Ent_A'] = (np.where(df['Entry1'] == "B_E",df['Close'],(np.where(df['Entry1'] == "S_E",df['Close'],npNaN))))
        #     df['Ent_A'] = df['Ent_A'].ffill()
        #     df['Ent_B'] = df['Close']-df['Ent_A']
        #     df['Ent_B'] = np.where(df['Entry'] == "B_E",(df['Close']-df['Ent_A']),np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0))
        #     df['Ent_C'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(-1) != "B_E"),"B_Ex",
        #                 np.where((df['Entry'] == "S_E") & (df['Entry'].shift(-1) != "S_E"),"S_Ex",
        #                 np.where(((df['Entry'] == "B_E") & (df['Ent_B'] <= - SLL_BN)),"B_SL",np.where(((df['Entry'] == "B_E") & (df['Ent_B'] >= TGG_BN)),"B_TP",
        #                 np.where(((df['Entry'] == "S_E") & (df['Ent_B'] <= - SLL_BN)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_B'] >= TGG_BN)),"S_TP",""))))))

        #     df.dropna(inplace=True)

        #     length = len(df)-1
        #     Buying = pd.DataFrame()
        #     Selling = pd.DataFrame()
        #     new_df1 = pd.DataFrame()    

        #     for i in range(len(df)):
        #         if [i+1][0] <= length:
        #             if df['Entry1'].iloc[i + 1] == "B_E":
        #                 bay = (df['Ent_A'].iloc[i + 1])
        #                 buyy = df[i+1:i+2]
        #                 Buying = pd.concat([buyy, Buying])
        #                 sal = df[df['Ent_A'] == bay]
        #                 sal1 = (sal[(sal['Ent_C'] == "B_SL") | (sal['Ent_C'] == "B_TP") | (sal['Ent_C'] == "B_Ex")])
        #                 sal1['Sell_Date'] = (df.Date.iloc[i + 1])
        #                 sal1['Sell_Time'] = (df.Time.iloc[i + 1])
        #                 Selling = pd.concat([sal1[:1], Selling])

        #             if df['Entry1'].iloc[i + 1] == "S_E":
        #                 bay1 = (df['Ent_A'].iloc[i + 1])
        #                 buyy1 = df[i+1:i+2]
        #                 Buying = pd.concat([buyy1, Buying])
        #                 sal1 = df[df['Ent_A'] == bay1]
        #                 sal11 = (sal1[(sal1['Ent_C'] == "S_SL") | (sal1['Ent_C'] == "S_TP") | (sal1['Ent_C'] == "S_Ex")])
        #                 sal11['Sell_Date'] = (df.Date.iloc[i + 1])
        #                 sal11['Sell_Time'] = (df.Time.iloc[i + 1])
        #                 Selling = pd.concat([sal11[:1], Selling])

        #     Buying.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True) 
        #     Buying.rename(columns={'Date': 'Datee', 'Time': 'Timee'}, inplace=True)
        #     Selling.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True)  
        #     Selling.rename(columns={'Sell_Date': 'Datee', 'Sell_Time': 'Timee'}, inplace=True)
        #     new_df1 = pd.merge(Buying, Selling,on=["Datee", "Timee"])
  
        #     dt.range("a1").value = df
        #     by.range("a1").value = Buying
        #     sl.range("a1").value = Selling
        #     fl.range("a1").value = new_df1

        #     if ordbook['Qty'].iloc[-1] != quantity:
        #         print("Order_Book is Empty")
        #         if df['Entry1'].iloc[-2] == "B_E":     
        #             call_counter = 1                  
        #             #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_strike_ltp_script, Qty=quantity,Price=CE_strike_ltp, IsIntraday=True)#, IsStopLossOrder=True, StopLossPrice=BuySl_ATM_price)
        #             # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
        #             print("Call Buy Order Excecuted at : "+str(CE_strike_ltp))
        #         if df['Entry1'].iloc[-2] == "S_E":
        #             put_counter = 1
        #             #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_strike_ltp_script, Qty=quantity,Price=PE_strike_ltp, IsIntraday=True)#,IsStopLossOrder=True, StopLossPrice=SellSl_ATM_price)  
        #             # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
        #             print("Put Buy Order Excecuted at : "+str(PE_strike_ltp))    
        #         else :
        #             print("NO 1st Trade")      

        #     ordbook1 = ordbook[ordbook["OrderStatus"] == "Fully Executed"]
        #     ordbook1 = ordbook1[['Datetimeee', 'BrokerOrderId', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','RemoteOrderID','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','ord_type','AtMarket']]
        #     ordbook2 = ordbook1[ordbook1["BuySell"] == "B"]
        #     #ob.range("a1").value = ordbook1

        #     Datetimeee = list(ordbook1['Datetimeee'])

        #     if ordbook1.isin(['CE']).any().any():

        #         ordbook_CE = ordbook2[ordbook2["ord_type"] == "CE"]

        #         last_ord_type_CE = ordbook_CE["ord_type"].iloc[-1]
        #         last_ord_script_CE = ordbook_CE["ScripCode"].iloc[-1]
        #         last_ord_rate_CE = ordbook_CE["Rate"].iloc[-1]
        #         last_ord_buy_sell_CE = ordbook_CE["BuySell"].iloc[-1]
        #         last_ord_time_CE = ordbook_CE["Datetimeee"].iloc[-1]

        #         CE_ord_ltp = (df1[df1['CE_Script'] == last_ord_script_CE][['CE_Ltp']].values.tolist())[0][0]

        #         # print("Call Data")
        #         # print("(1) last_BuySell_type is : "+str(ordbook1["BuySell"].iloc[-1])+" and last_ord_type is : "+str(ordbook1["ord_type"].iloc[-1]))
        #         # print("(2) last_ord_script_CE is : "+str(last_ord_script_CE))
        #         # print("(3) last_ord_rate_CE is : "+str(last_ord_rate_CE))
        #         # print("(4) CE_ord_ltp is : "+str(CE_ord_ltp))
        #         # print("(5) last_ord_time_CE is : "+str(last_ord_time_CE))


        #         if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "CE"):                
        #             if (CE_ord_ltp > last_ord_rate_CE + TG):
        #                 squareoff = client.squareoff_all()
        #                 call_counter = 0
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #                 print("Call Target Achieved and Profit is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity)) 
        #             if (CE_ord_ltp < last_ord_rate_CE - SL):
        #                 squareoff = client.squareoff_all()
        #                 call_counter = 0
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #                 print("Call Stoploss Hit and Loss is Rs : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity)) 

        #         if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "CE"):  

        #             Targett = last_ord_rate_CE + TG
        #             Stoploss = last_ord_rate_CE - SL
        #             # pwk.sendwhatmsg_instantly("+919610033622","Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919610033622","Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss),10,True,5)
        #             print("CALLLL")
        #             print("Last Call Ord Ltp is : "+str(last_ord_rate_CE)+" and Current Call Ltp is : "+str(CE_ord_ltp)+" and Diff is : "+str(round((CE_ord_ltp-last_ord_rate_CE),2))+" and P&L is : "+str(float(round((CE_ord_ltp-last_ord_rate_CE),2))*quantity))
        #             print("Call Target is : "+str(Targett)+" and Call StopLoss is : "+str(Stoploss))

        #     if ordbook1.isin(['PE']).any().any():

        #         ordbook_PE = ordbook2[ordbook2["ord_type"] == "PE"]

        #         last_ord_type_PE = ordbook_PE["ord_type"].iloc[-1]
        #         last_ord_script_PE = ordbook_PE["ScripCode"].iloc[-1]
        #         last_ord_rate_PE = ordbook_PE["Rate"].iloc[-1]
        #         last_ord_buy_sell_PE = ordbook_PE["BuySell"].iloc[-1]
        #         last_ord_time_PE = ordbook_PE["Datetimeee"].iloc[-1]

        #         PE_ord_ltp = (df1[df1['PE_Script'] == last_ord_script_PE][['PE_Ltp']].values.tolist())[-1][0]

        #         # print("Put Data")
        #         # print("(1) last_BuySell_type is : "+str(ordbook1["BuySell"].iloc[-1])+" and last_ord_type is : "+str(ordbook1["ord_type"].iloc[-1]))
        #         # print("(2) last_ord_script_PE is : "+str(last_ord_script_PE))
        #         # print("(3) last_ord_rate_PE is : "+str(last_ord_rate_PE))
        #         # print("(4) PE_ord_ltp is : "+str(PE_ord_ltp))
        #         # print("(5) last_ord_time_PE is : "+str(last_ord_time_PE))

        #         if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "PE"):                
        #             if (PE_ord_ltp > last_ord_rate_PE + TG):
        #                 put_counter = 0
        #                 squareoff = client.squareoff_all()
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #                 print("Put Target Achieved and Profit is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))
        #             if (PE_ord_ltp < last_ord_rate_PE - SL):
        #                 put_counter = 0
        #                 squareoff = client.squareoff_all()
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #                 print("Put Stoploss Hit and Loss is Rs : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))


        #         if (ordbook1["BuySell"].iloc[-1] == "B") and (ordbook1["ord_type"].iloc[-1] == "PE"):  
        #             Targett = last_ord_rate_PE + TG
        #             Stoploss = last_ord_rate_PE - SL
        #             # pwk.sendwhatmsg_instantly("+919610033622","Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919610033622","Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss),10,True,5)
        #             print("PUTTT")
        #             print("Last Put Ord Ltp is : "+str(last_ord_rate_PE)+" and Current Put Ltp is : "+str(PE_ord_ltp)+" and Diff is : "+str(round((PE_ord_ltp-last_ord_rate_PE),2))+" and P&L is : "+str(float(round((PE_ord_ltp-last_ord_rate_PE),2))*quantity))
        #             print("Put Target is : "+str(Targett)+" and Put StopLoss is : "+str(Stoploss))              
            
        #     else:
        #         print("No data in OrderBook")          

        #     if df['Entry1'].iloc[-2] == "B_E":                       
        #         if (ordbook1["ScripCode"].iloc[-1] == CE_strike_ltp_script) and (ordbook1["BuySell"].iloc[-1] == "B"): # and (ordbook1["TradedQty"].iloc[-1] == lot_size):
        #             # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Already Executed at : "+str(last_ord_time_CE),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Already Executed at : "+str(last_ord_time_CE),10,True,5)
        #             print("Call Buy Order Already Executed at : "+str(last_ord_time_CE))
        #         else:    
        #             if call_counter == 0:
        #                 put_counter = 0
        #                 squareoff = client.squareoff_all() 
        #                 #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = CE_strike_ltp_script, Qty=quantity,Price=CE_strike_ltp, IsIntraday=True)#, IsStopLossOrder=True, StopLossPrice=BuySl_ATM_price)
        #                 call_counter = 1
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Call Buy Order Excecuted at : "+str(CE_strike_ltp),10,True,5)
        #                 print("Call Buy Order Excecuted at : "+str(CE_strike_ltp))
                        
        #     if df['Entry1'].iloc[-2] == "S_E":
        #         if (ordbook1["ScripCode"].iloc[-1] == PE_strike_ltp_script) and (ordbook1["BuySell"].iloc[-1] == "B"): # and (ordbook1["TradedQty"].iloc[-1] == lot_size):
        #             # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Already Executed at : "+str(last_ord_time_PE),10,True,5)
        #             # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Already Executed at : "+str(last_ord_time_PE),10,True,5)
        #             print("Put Buy Order Already Executed at : "+str(last_ord_time_PE))
        #         else:  
        #             if put_counter == 0:
        #                 call_counter = 0
        #                 squareoff = client.squareoff_all()
        #                 #order = client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = PE_strike_ltp_script, Qty=quantity,Price=PE_strike_ltp, IsIntraday=True)#,IsStopLossOrder=True, StopLossPrice=SellSl_ATM_price)  
        #                 put_counter = 1
        #                 # pwk.sendwhatmsg_instantly("+919610033622","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
        #                 # pwk.sendwhatmsg_instantly("+919724256494","Put Buy Order Excecuted at : "+str(PE_strike_ltp),10,True,5)
        #                 print("Put Buy Order Excecuted at : "+str(PE_strike_ltp))                    
        #     else:
        #         print("No Trade")
        #     print("Call counter is : "+str(call_counter))
        #     print("Put counter is : "+str(put_counter))
                   



