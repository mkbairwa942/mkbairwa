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
from datetime import datetime,timedelta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

pd.options.mode.copy_on_write = True

operate = input("Do you want to go with TOTP (yes/no): ")
if operate.upper() == "YES":
    from five_paisa1 import *
    # p=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
    # print(p)
    username = input("Enter Username : ")
    username1 = str(username)
    print("Hii "+str(username1)+" have a Good Day")
    # username_totp = input("Enter TOTP : ")
    # username_totp1 = str(username_totp)
    # print("Hii "+str(username1)+" you enter TOTP is "+str(username_totp1))
    client = credentials(username1)
else:
    from five_paisa import *

#order = client.place_order(OrderType='S',Exchange='N',ExchangeType='C', ScripCode = 1336, Qty=10,Price=1835, IsIntraday=True)#, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)


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
                        Price=0.0,)
                        #IsIntraday=True,)
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

print("----option chain----")

if not os.path.exists("Terminal.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Terminal.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Terminal.xlsx')
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
st1.range("a:u").value = None
st2.range("a:u").value = None
st3.range("a:u").value = None
st4.range("a:i").value = None
#oc.range("a:z").value = None
dt.range(f"a1:d1").value = ["Namee","Scriptcodee","Stop_Loss","Add_Till","Buy_At","Target" ,"Term","Datetime", "","","","","","","","","","","","","","Quantity","Entry","Exit","SL","Status"]
oc.range("a:b").value = oc.range("d8:e30").value = oc.range("g1:v4000").value = None

#st4.range("k2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*5+COLUMN(B2),2))"
# dt.range("a2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$A2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$A2)"
# dt.range("b2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$B2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$B2)"
# dt.range("c2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$C2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$C2)"
# dt.range("d2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$D2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$D2)"
# dt.range("e2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$E2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$E2)"
# dt.range("f2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$F2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$F2)"
# dt.range("g2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$G2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$G2)"
# dt.range("h2").options(index=False).value = "=IF('D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$H2="","",'D:\STOCK\Capital_vercel_new\[Terminal.xlsx]Strategy3'!$H2)"
dt.range("w2").options(index=False).value = '=IF(N2<C2,"SL_Hit",IF(F2=0,IF(AND(N2>D2,N2<((E2*0.5%)+E2)),"Buy","Already_Up"),IF(L2>=F2,"Target_Hit",IF(AND(N2>D2,N2<((E2*0.5%)+E2)),"Buy","Already_Up"))))'


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

buy_order_list = []
ord_buy_df_list = []
ord_sell_df_list = []


by.range("a1:x1").color = (54,226,0)
by.range("a1:x1").font.bold = True
by.range("a1:x1").api.WrapText = True

def get_fibonachi(high,low,direct,fib_level):
    if direct == "UP":
        fib_price = high - (high-low)*fib_level
        return fib_price
    elif direct == "DOWN":
        fib_price = low + (high-low)*fib_level
        return fib_price  

while True:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value
    pos.range("a1").value = pd.DataFrame(client.margin())
    pos.range("a4").value = pd.DataFrame(client.positions())
    pos.range("a10").value = pd.DataFrame(client.holdings())  
    # pos.range("a12").value = pd.DataFrame(client.get_tradebook())
    
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


            # des_ltp = 85

            # CE_strike_ltp = (df1[df1['CE_Ltp'] < des_ltp][['CE_Ltp']].values.tolist())[0][0]
            # PE_strike_ltp = (df1[df1['PE_Ltp'] < des_ltp][['PE_Ltp']].values.tolist())[-1][0]
            # CE_strike_ltp_script = (df1[df1['CE_Ltp'] < des_ltp][['CE_Script']].values.tolist())[0][0]
            # PE_strike_ltp_script = (df1[df1['PE_Ltp'] < des_ltp][['PE_Script']].values.tolist())[-1][0]

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
            num_col = ['CE_Volume','CE_Chg_OI','PE_Chg_OI','PE_Volume']
            df1.style.highlight_max()
            df1.style.highlight_max(subset=num_col,color='lightgreen')
            df1.style.highlight_min(subset=num_col,color='pink')
            


            time.sleep(0.5)            
            scpt = dt.range(f"a{1}:h{50}").value            
            sym = dt.range(f"a{2}:a{500}").value
            symbols = list(filter(lambda item: item is not None, sym))
            symb_frame = exchange2[(exchange2['Root'].isin(symbols))]
            symb_frame['Concate'] = "N:C:"+symb_frame['Name']+":"+symb_frame['Scripcode'].astype(str)
            symbolss = list(symb_frame['Concate'])
            symbolss.sort()


            max_min = oc.range(f"e{17}:e{22}").value
            trading_info = by.range(f"u{2}:x{30}").value  
            
            maxxx = max(list(max_min))
            minnn = min(list(max_min))
            print(maxxx,minnn)
           
            index = ['N:C:NIFTY:999920000','N:C:BANKNIFTY:999920005','N:C:FINNIFTY:999920041'] #999920000 999920005 999920041

            for li in index:                 
                symbolss.append(li)

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


                                print(trade_info[0],trade_info[1],trade_info[2],trade_info[3])

                                if trade_info[1].upper() == "BUY" and trade_info[2] is None:  
                                    print("Buy order")   
                                    #dt.range(f"t{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"B")

                                if trade_info[1].upper() == "BUY" and trade_info[2].upper() == "SELL":
                                    print("Sell order")  
                                    dt.range(f"u{idx +2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"S")

                                if trade_info[1].upper() == "SELL" and trade_info[2] is None:  
                                    print("Sell order")                                    
                                    #dt.range(f"t{idx +2 }").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"S")

                                if trade_info[1].upper() == "SELL" and trade_info[2].upper() == "BUY":   
                                    print("Buy order")                                   
                                    #dt.range(f"u{idx + 2}").value = place_trade(Exche,ExchTypee,Namee,Scripcodee,int(trade_info[0]),"B")

                            #print(i,trading_info)
                        except Exception as e:                
                            pass                
                    
                idx +=1
 
            #main_list.sort_values(['Symbol'], ascending=[True], inplace=True)
            main_list['Time'] = datetime.now()
            main_list3 = main_list
            main_list4 = main_list3.iloc[::-1]
            main_list4 = main_list4[['Symbol','Open','High','Low','LTP','Close','NetChange','Time']]

            

            posi = pd.DataFrame(client.positions())
            if posi.empty:
                print("No Positions")
            else:
                posi = posi[['ScripName','ScripCode','BuyAvgRate']]
                posi.rename(columns={'ScripName': 'Namee','ScripCode':'Scriptcodee','BuyAvgRate':'Buy_At'}, inplace=True)
                
                # for i in range(0,len(main_list4)):

                #     hhigh = float(main_list4.iloc[i]['High'])
                #     llow = float(main_list4.iloc[i]['Low'])

                #     TGT_3 = round((get_fibonachi(hhigh,llow,"UP",-0.500)),2)
                #     TGT_2 = round((get_fibonachi(hhigh,llow,"UP",-0.382)),2)
                #     TGT_1 = round((get_fibonachi(hhigh,llow,"UP",-0.236)),2)
                #     PP = round((get_fibonachi(hhigh,llow,"UP",0.000)),2)
                #     SL_1 = round((get_fibonachi(hhigh,llow,"UP",0.236)),2)
                #     SL_2 = round((get_fibonachi(hhigh,llow,"UP",0.382)),2)
                #     SL_3 = round((get_fibonachi(hhigh,llow,"UP",0.500)),2)
                    
                #     posi['Stop_Loss'] = SL_2 
                #     posi['Add_Till'] = SL_1       
                #     posi['Target'] = TGT_2 

                posi['Stop_Loss'] = round((posi['Buy_At'] - (posi['Buy_At']*1)/100),1)
                posi['Add_Till'] = round((posi['Buy_At']-((posi['Buy_At']*0.5)/100)),1)      
                posi['Target'] = round((((posi['Buy_At']*2)/100) + posi['Buy_At']),1)

                posi['Term'] = "SFT"
                posi.sort_values(['Namee'], ascending=[True], inplace=True)
                posi = posi[['Namee','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term']]
                dt.range("a1").options(index=False).value = posi


            dt.range("j1").options(index=False).value = main_list4  

            scpts = pd.DataFrame(scpt[1:],columns=scpt[0])
            scpts['Namee'] = scpts['Namee'].apply(lambda x : str(x))
            scpts = scpts[scpts['Namee'] != 'None']
            scpts['TimeNow'] = datetime.now()
            scpts['Minutes'] = pd.to_datetime(scpts['TimeNow'])-pd.to_datetime(scpts["Datetime"])
            scpts['Minutes'] = round((scpts['Minutes']/np.timedelta64(1,'m')),2)
            scpts['Buy'] = np.where(scpts['Minutes']<5,"Yes","")
            scpts['Timeover'] = np.where(scpts['Minutes']>30,"Yes","")
            # by.range("a1").options(index=False).value = scpts

            def round_up(n, decimals = 0): 
                multiplier = 10 ** decimals 
                return math.ceil(n * multiplier) / multiplier

            order_frame = scpts[scpts['Buy'] == 'Yes']
            time_over_frame = scpts[scpts['Timeover'] == 'Yes']

            order_frame_list = np.unique([str(i) for i in order_frame['Namee']])
            time_over_frame_list = np.unique([str(i) for i in order_frame['Namee']])

            # print("3")
            # print(buy_order_list)
            # for aa in order_frame_list:
            #     if aa in buy_order_list: 
            #         print(str(aa)+" is Already Buy") 
            #     else: 
            #         order_frame1 = order_frame[order_frame['Namee'] == aa]
            #         Buy_Scriptcodee = int(order_frame1['Scriptcodee'])
            #         Buy_price_of_stock = float(order_frame1['Buy_At'])                    
            #         Buy_price_of_stock = round_up(Buy_price_of_stock, 1)
            #         Buy_Stop_Loss = round((float(order_frame1['Buy_At']) - (float(order_frame1['Buy_At'])*2)/100),2)
            #         Buy_Stop_Loss = round_up(Buy_Stop_Loss, 1)
            #         if Buy_price_of_stock < 100:
            #             Buy_quantity_of_stock = 200
            #         if Buy_price_of_stock > 100 and Buy_price_of_stock < 200:
            #             Buy_quantity_of_stock = 100                        
            #         if Buy_price_of_stock > 200 and Buy_price_of_stock < 300:
            #             Buy_quantity_of_stock = 80
            #         if Buy_price_of_stock > 300:
            #             Buy_quantity_of_stock = 50
            #         Req_Amount = Buy_quantity_of_stock*Buy_price_of_stock
            #         fundd = pd.DataFrame(client.margin())['AvailableMargin'] 
            #         print(fundd)
            #         if fundd > Req_Amount:
            #             Buy_quantity_of_stock = round_up(Buy_quantity_of_stock, 1)
            #             buy_order_list.append(aa)
            #             print("Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock))
            #             order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock,Price=Buy_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
            #             pwk.sendwhatmsg_instantly("+919610033622","Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock),10,True,5)
            #             # pwk.sendwhatmsg_instantly("+918000637245","Buy Order of "+str(aa)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock),10,True,5)            
            #         else:
            #             print("Available fund is "+str(fundd)+ " and Required Amount is "+str(Req_Amount)+ "is 'LESS'" )

            # print("No Stock yet to Buy")
            # by.range("n1").options(index=False).value = order_frame
            # by.range("aa1").options(index=False).value = time_over_frame

            scpts.rename(columns={'Namee': 'Name'},inplace=True)
            main_list4.rename(columns={'Symbol': 'Name'},inplace=True)
            flt_df = pd.merge(scpts, main_list4, on=['Name'], how='inner')
            flt_df['Buy_up'] = ((flt_df['Buy_At']*0.5)/100)+flt_df['Buy_At']
            flt_df['Buy_dn'] = flt_df['Buy_At']-((flt_df['Buy_At']*0.5)/100)
            flt_df['Status'] = np.where(flt_df['LTP'] < flt_df['Stop_Loss'],"Sl_Hit",
                               np.where((flt_df['LTP'] < flt_df['Buy_up']) & (flt_df['LTP'] > flt_df['Buy_dn']),"Buy_Range",
                               np.where((flt_df['LTP'] > flt_df['Target']),"Target_Hit",
                               np.where((flt_df['LTP'] < flt_df['Buy_At']),"Already_Dn",
                               np.where((flt_df['LTP'] > flt_df['Buy_At']),"Already_Up","")))))
            posit = pd.DataFrame(client.positions())

            if posit.empty:
                flt_df = flt_df[['Name','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term',
                                'Datetime','TimeNow','Minutes','Buy','Open','High','Low','LTP','Close','NetChange','Status']]                                
                by.range(f"s1:x1").value = ["BookedPL","MTOM","BuyQty","Entry","Exit","X" ]
                by.range("a1").options(index=False).value = flt_df

            else:
                posit.rename(columns={'ScripName': 'Name'},inplace=True)
                flt_df1 = pd.merge(flt_df, posit, on=['Name'], how='outer')
                flt_df1 = flt_df1[['Name','Scriptcodee','Stop_Loss','Add_Till','Buy_At','Target','Term',
                                'Datetime','TimeNow','Minutes','Buy','Open','High','Low','LTP_x','Close',
                                'NetChange','Status','BookedPL','MTOM','BuyQty']]
                
                flt_df1['Entry'] = np.where((flt_df1['MTOM'] != 0) & (flt_df1['BuyQty'] != 0),"BUY","")
                flt_df1['Exit'] = np.where(((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "Sl_Hit")) | ((flt_df1['Entry'] == "BUY") & (flt_df1['Status'] == "Target_Hit")),"SELL","")
                


                #by.range("a:x").value = None         
                by.range("a1").options(index=False).value = flt_df1

            try:
                ordbook = pd.DataFrame(client.order_book())
                ob.range("a1").options(index=False).value = ordbook
            except Exception as e:
                print(e)

            try:
                if ordbook is not None:
                    print("Order Book not Empty")        
                    ordbook1 = ordbook[ordbook['TerminalId'] != 0]   
                    #ordbook1 = ordbook           
                    Datetimeee = []
                    for i in range(len(ordbook1)):
                        datee = ordbook1['BrokerOrderTime'][i]
                        timestamp = pd.to_datetime(datee[6:19], unit='ms')
                        ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
                        d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
                        d2 = d1 + timedelta(hours = 5.5)
                        Datetimeee.append(d2)
                    ordbook1['Datetimeee'] = Datetimeee
                    ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','OrderStatus','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
                    ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
                    ob1.range("a1").options(index=False).value = ordbook1
                    buy_order_list = np.unique([str(i) for i in ordbook1['ScripName']])
                else:
                    print("Order Book Empty")
            except Exception as e:
                        print(e)

        except Exception as e:
            pass    

