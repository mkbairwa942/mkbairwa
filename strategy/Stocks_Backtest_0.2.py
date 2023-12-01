#import yfinance as yf
#import ta
#from ta import add_all_ta_features
#from ta.utils import dropna
import pandas_ta as pta
#from finta import TA
# import talib
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import datetime,timedelta,date,time
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
from five_paisa import *

telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"




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
last_trading_day = trading_dayss[1]
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

nse = NSELive()

price_limit = 300
Available_Cash = 12000
Exposer = 2

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

# print(bhavcopy(lastTradingDay))

def bhavcopy_fno(lastTradingDay):
    dmyformat = datetime.strftime(lastTradingDay, '%d%b%Y').upper()
    MMM = datetime.strftime(lastTradingDay, '%b').upper()
    yyyy = datetime.strftime(lastTradingDay, '%Y')
    url1 = 'https://archives.nseindia.com/content/historical/DERIVATIVES/' + yyyy + '/' + MMM + '/fo' + dmyformat + 'bhav.csv.zip'
    content = requests.get(url1)
    zf = ZipFile(BytesIO(content.content))
    match = [s for s in zf.namelist() if ".csv" in s][0]
    bhav_fo = pd.read_csv(zf.open(match), low_memory=False)
    bhav_fo.columns = bhav_fo.columns.str.strip()
    bhav_fo = bhav_fo.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT'])
    bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
    bhav_fo = bhav_fo.drop(["Unnamed: 15"], axis=1)
    return bhav_fo

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
    
    def week52(self):
        url = 'https://www.nseindia.com/market-data/new-52-week-high-low-equity-market'
        data = self.session.get(url, headers=self.headers)
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

tre = nse.week52()
print

print("---- Data Process Started ----")

if not os.path.exists("Stocks_Backtest_0.1.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Stocks_Backtest_0.1.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Stocks_Backtest_0.1.xlsx')
for i in ["Exchange","Filt_Exc","Bhavcopy","FO_Bhavcopy","Five_data","Delv_data","Five_Delv","Final_Data","Position","Strategy1","Strategy2","Strategy3","Buy","Sale",
           "Expiry","stats","Stat","Stat1","Stat2","Stat3","Stat4"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Filt_Exc")
bhv = wb.sheets("Bhavcopy")
bhv_fo = wb.sheets("FO_Bhavcopy")
Fiv_dt = wb.sheets("Five_data")
delv_dt = wb.sheets("Delv_data")
five_delv = wb.sheets("Five_Delv")
fl_data = wb.sheets("Final_Data")
pos = wb.sheets("Position")
strategy1 = wb.sheets("Strategy1")
strategy2 = wb.sheets("Strategy2")
strategy3 = wb.sheets("Strategy3")

exc.range("a:u").value = None
flt_exc.range("a:u").value = None
bhv.range("a:u").value = None
bhv_fo.range("a:u").value = None
# Fiv_dt.range("a:u").value = None
# delv_dt.range("a:u").value = None
# five_delv.range("a:u").value = None
# fl_data.range("a:u").value = None
pos.range("a:u").value = None
# strategy1.range("a:u").value = None
# strategy2.range("a:u").value = None
# strategy3.range("a:u").value = None

st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
# st.range("a:u").value = None
# st1.range("a:u").value = None
# st2.range("a:u").value = None
# st3.range("a:u").value = None
# st4.range("a:i").value = None

by = wb.sheets("Buy")
sl = wb.sheets("Sale")
st = wb.sheets("stats")
exp = wb.sheets("Expiry")

# st.range("a:z").value = None
# exp.range("a:z").value = None

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# exc.range("a:s").value = None
# exc.range("a1").options(index=False).value = script_code_5paisa
print("Excel : Started")
exchange = None

def round_up(n, decimals = 0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier

while True:    
    if exchange is None: 
        try:
            exc_equity = pd.DataFrame(script_code_5paisa)
            exc_equity = exc_equity[(exc_equity["Exch"] == "N") & (exc_equity["ExchType"] == "C")]
            exc_equity = exc_equity[exc_equity["Series"] == "EQ"]
            exc_equity = exc_equity[exc_equity["CpType"] == "XX"]
            exc_equity["Watchlist"] = exc_equity["Exch"] + ":" + exc_equity["ExchType"] + ":" + exc_equity["Name"]
            exc_equity.sort_values(['Name'], ascending=[True], inplace=True)
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

symb = pd.DataFrame({"Name": list(exc_equity["Root"].unique())})
symb = symb.set_index("Name",drop=True)

flt_exc_eq = pd.merge(symb, exc_equity, on=['Name'], how='inner')
flt_exc_eq.sort_values(['Name'], ascending=[True], inplace=True)
flt_exc_eq = flt_exc_eq[['ExchType','Name', 'ISIN', 'FullName', 'CO BO Allowed','Scripcode','Watchlist']]

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = exc_equity

print("Exchange Data Download")

stop_thread = False

script_list = [1185,	19867,	100,	10457,	1663,	2144,	383,	404,	7848,	480,	559,	20160,	21749,	21740,	11731,	11423,	7358,	21690,	17851,	25690,	15214,	4525,	19277,	13966,	10619,	1455,	14203,	7852,	13982,	1720,	19020,	3637,	6951,	2841,	12686,	17957,	20830,	10822,	357,	14111,	17400,	21469,	926,	2493,	6656,	25718,	2711,	2739,	10990,	15157,	5279,	19410,	10453,	14139,	11520,	13598,	15342,	5068,	7200,	11050,	13826,	3021,	13801,	5162,	3493,	5428,	14208,	3857,	3063,	8652,	3766,	3812,]
script_list.sort()
# stk_list = ['APOLLO',	'ARVIND',	'CDSL',	'CIGNITITEC',	'CTE',	'DATAMATICS',	'DSSL',	'EMIL',	'EMKAY',	'HITECH',	'IWEL',	'MOTILALOFS',	'NAM-INDIA',	'ORBTEXP',	'RELCHEMQ',	'SAGARDEEP',	'SHALBY',	'SUVEN',	'WEIZMANIND',	'AAVAS',	'BUTTERFLY',	'FINEORG',	'INFOBEAN',	'MOLDTECH',	'SIEMENS']
	
#script_list = np.unique(exc_equity['Scripcode'])
stk_list = np.unique(exc_equity["Root"])

print("Total Stock : "+str(len(script_list)))

print(script_list)

#order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 3045, Qty=10,Price=25)

def bhavcopy_func():
    eq_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            print(i)
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
     
    #eq_bhav = eq_bhav[['Name', 'Date', 'Deliv_qty', 'Deliv_per']]
    eq_bhav['Date'] = eq_bhav['Date'].astype('datetime64[ns]')    
    return eq_bhav

eq_bhav = bhavcopy_func()
bhv.range("a:i").value = None                          
bhv.range("a1").options(index=False).value = eq_bhav
print(str(days_count)+" Days STOCK Data Download")

def fiveminute_data(scode,time,start,end):    
    dfg1 = client.historical_data('N', 'C', scode, time,start,end) 
    dfg1['Scripcode'] = aa  

    dfg1 = pd.merge(flt_exc_eq, dfg1, on=['Scripcode'], how='inner') 
    dfg1 = dfg1[['Scripcode','Name','Datetime','Open','High','Low','Close','Volume']]

    dfg1['Date'] = current_trading_day 
    dfg1["RSI_14"] = np.round((pta.rsi(dfg1["Close"], length=14)),2) 
    
    dfg1.sort_values(['Datetime'], ascending=[False], inplace=True)
    dfg1['TimeNow'] = datetime.now()
    dfg1['Cand_col'] = np.where(dfg1['Close'] > dfg1['Open'],"Green",np.where(dfg1['Close'] < dfg1['Open'],"Red","Dozi"))
    dfg1['Cand_Body'] = dfg1['High'] - dfg1['Low']
    dfg1['Top_Wick'] = np.where((dfg1['Cand_col'] == "Green"),dfg1['High'] - dfg1['Close'],np.where((dfg1['Cand_col'] == "Red"),dfg1['High'] - dfg1['Open'],0))
    dfg1['Bot_Wick'] = np.where((dfg1['Cand_col'] == "Green"),dfg1['Open'] - dfg1['Low'],np.where((dfg1['Cand_col'] == "Red"),dfg1['Close'] - dfg1['Low'],0)) 
    dfg1['Cand_Size'] = np.round((np.where(dfg1['Cand_col'] == "Red",(dfg1['Bot_Wick'].astype(float)/dfg1['Cand_Body'].astype(float))*100,np.where(dfg1['Cand_col'] == "Green",(dfg1['Top_Wick'].astype(float)/dfg1['Cand_Body'].astype(float))*100,0))),2)
    #dfg1['Cand_Size'] = np.where((dfg1['Cand_col'] == "Red"),(dfg1['Bot_wick']/dfg1['Cand_Body'])*100,np.where((dfg1['Cand_col'] == "Green"),(dfg1['Top_wick']/dfg1['Cand_Body'])*100,""))
    
    dfg1['Price_Chg'] = round(((dfg1['Close'] * 100) / (dfg1['Close'].shift(-1)) - 100), 2).fillna(0)      
    
    dfg1['Vol_Chg'] = round(((dfg1['Volume'] * 100) / (dfg1['Volume'].shift(-1)) - 100), 2).fillna(0)

    dfg1['Price_break'] = np.where((dfg1['Close'] > (dfg1.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((dfg1['Close'] < (dfg1.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    dfg1['Vol_break'] = np.where(dfg1['Volume'] > (dfg1.Volume.rolling(5).mean() * 2.5).shift(-5),
                                        "Vol_brk","")       
                                                                                                        
    dfg1['Vol_Price_break'] = np.where((dfg1['Vol_break'] == "Vol_brk") &
                                                (dfg1['Price_break'] != ""), "Vol_Pri_break", "")
    
    dfg1['O=H=L'] = np.where((dfg1['Open'] == dfg1['High']), 'Open_High',
                                    (np.where((dfg1['Open'] == dfg1['Low']), 'Open_Low', "")))
    dfg1['Pattern'] = np.where((dfg1['High'] < dfg1['High'].shift(-1)) &
                                    (dfg1['Low'] > dfg1['Low'].shift(-1)), 'Inside_Bar',
                                    (np.where((dfg1['Low'] < dfg1['Low'].shift(-1)) &
                                                (dfg1['Close'] > dfg1['High'].shift(-1)), 'Bullish',
                                                (np.where((dfg1['High'] > dfg1['High'].shift(-1)) &
                                                        (dfg1['Close'] < dfg1['Low'].shift(-1)), 'Bearish',
                                                        "")))))
    dfg1["Buy/Sell"] = np.where((dfg1['Vol_break'] == "Vol_brk") & (dfg1['Price_break'] == "Pri_Up_brk"),
                                    "BUY", np.where((dfg1['Vol_break'] == "Vol_brk")
                                        & (dfg1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                
    dfg1['R3'] = round(dfg1['High'] + (
            2 * (((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) - dfg1['Low'])), 2).fillna(0)
    dfg1['R2'] = round((((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) + dfg1['High']) - \
                            dfg1['Low'], 2).fillna(0)
    dfg1['R1'] = round(
        (2 * ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3)) - dfg1['Low'], 2).fillna(0)
    dfg1['Pivot'] = round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3), 2).fillna(0)
    dfg1['S1'] = round(
        (2 * ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3)) - dfg1['High'], 2).fillna(0)
    dfg1['S2'] = round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3) - (dfg1['High'] -
                                                                                            dfg1['Low']),2).fillna(0)
                        
    dfg1['S3'] = round(dfg1['Low'] - (
            2 * (dfg1['High'] - ((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3))), 2)
    dfg1['Mid_point'] = round(((dfg1['High'] + dfg1['Low']) / 2), 2).fillna(0)
    dfg1['CPR'] = round(
        abs((round(((dfg1['High'] + dfg1['Low'] + dfg1['Close']) / 3), 2)) - dfg1['Mid_point']),
        2).fillna(0)
    dfg1['CPR_SCAN'] = np.where((dfg1['CPR'] < ((dfg1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                    "")
    dfg1['Candle'] = np.where(abs(dfg1['Open'] - dfg1['Close']) <
                                    abs(dfg1['High'] - dfg1['Low']) * 0.2, "DOZI",
                                    np.where(abs(dfg1['Open'] - dfg1['Close']) >
                                            abs(dfg1['High'] - dfg1['Low']) * 0.7, "s", ""))
    return dfg1

def one_Day_Data(scode,time,start,end):
    print("1 Day Data Download and Scan "+str(aa))
    dfggg = client.historical_data('N', 'C', scode,time,start,end)      
    dfggg['Scripcode'] = aa
    dfggg = pd.merge(flt_exc_eq, dfggg, on=['Scripcode'], how='inner') 
    dfggg = dfggg[['Scripcode','Name','Datetime','Open','High','Low','Close','Volume']]
    dfggg = dfggg.astype({"Datetime": "datetime64[ns]"})
    #dfggg["Date"] = dfggg["Datetime"].dt.date
    dfggg["Date"] = dfggg['Datetime'].apply(pd.to_datetime)
    name1 = dfggg['Name'][0]
    eq_bhav1 = eq_bhav[eq_bhav["Name"] == name1]

    dfggg22 = pd.concat([dfggg, eq_bhav1], axis=0, sort=False)

    dfg = dfggg22.drop_duplicates(subset=['Volume'],keep='last')

    dfg['Date_Now'] = current_trading_day
    dfg["SMA_200"] = np.round((pta.sma(dfg["Close"], length=200,offset=0)),2)
    dfg["RSI_14"] = np.round((pta.rsi(dfg["Close"], length=14)),2)

    dfg['TimeNow'] = datetime.now()
    dfg['200+'] = ((dfg['SMA_200']*1)/100)+(dfg['SMA_200'])

    dfg['200-'] = (dfg['SMA_200'])-((dfg['SMA_200']*1)/100)

    dfg.sort_values(['Date'], ascending=[False], inplace=True)

    dfg['Price_Chg'] = round(((dfg['Close'] * 100) / (dfg['Close'].shift(-1)) - 100), 2).fillna(0)      
    
    dfg['Vol_Chg'] = round(((dfg['Volume'] * 100) / (dfg['Volume'].shift(-1)) - 100), 2).fillna(0)

    dfg['Deliv_break'] = np.where(dfg['Deliv_qty'] > (dfg.Deliv_qty.rolling(5).mean() * 1.1).shift(-5),"Deliv_brk", "")

    dfg['Price_break'] = np.where((dfg['Close'] > (dfg.High.rolling(5).max()).shift(-5)),
                                        'Pri_Up_brk',
                                        (np.where((dfg['Close'] < (dfg.Low.rolling(5).min()).shift(-5)),
                                                    'Pri_Dwn_brk', "")))
    dfg['Vol_break'] = np.where(dfg['Volume'] > (dfg.Volume.rolling(5).mean() * 1.5).shift(-5),
                                        "Vol_brk","")       
                                                                                                        
    dfg['Vol_Price_break'] = np.where((dfg['Vol_break'] == "Vol_brk") &
                                                (dfg['Price_break'] != ""), "Vol_Pri_break", "")
    
    dfg['Del_Vol_Pri_break'] = np.where((dfg['Deliv_break'].shift(-1) == "Deliv_brk") &
                                            (dfg['Vol_Price_break'] == "Vol_Pri_break"), "Del_Vol_Pri_break", "")
    
    dfg['Sma_200_break'] = np.where((dfg['Close'] < dfg['200+']) & (dfg['Close'] > dfg['200-']),"Nr. 200_Sma Break","")

    dfg['Week52'] = np.where((dfg['High'] > (dfg.High.rolling(245).max()).shift(-245)),
                                        'Week52High',
                                        (np.where((dfg['Low'] < (dfg.Low.rolling(245).min()).shift(-245)),
                                                    'Week52Low', "")))

    dfg['P_D_H_B'] = np.where(dfg['Close'] > dfg['High'].shift(-1),"PDHB",np.where(dfg['Close'] < dfg['Low'].shift(-1),"PDLB",""))


    dfg['O=H=L'] = np.where((dfg['Open'] == dfg['High']), 'Open_High',
                                    (np.where((dfg['Open'] == dfg['Low']), 'Open_Low', "")))
    dfg['Pattern'] = np.where((dfg['High'] < dfg['High'].shift(-1)) &
                                    (dfg['Low'] > dfg['Low'].shift(-1)), 'Inside_Bar',
                                    (np.where((dfg['Low'] < dfg['Low'].shift(-1)) &
                                                (dfg['Close'] > dfg['High'].shift(-1)), 'Bullish',
                                                (np.where((dfg['High'] > dfg['High'].shift(-1)) &
                                                        (dfg['Close'] < dfg['Low'].shift(-1)), 'Bearish',
                                                        "")))))
    dfg["Buy/Sell"] = np.where((dfg['Vol_break'] == "Vol_brk") & (dfg['Price_break'] == "Pri_Up_brk"),
                                    "BUY", np.where((dfg['Vol_break'] == "Vol_brk")
                                        & (dfg['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                
    dfg['R3'] = round(dfg['High'] + (
            2 * (((dfg['High'] + dfg['Low'] + dfg['Close']) / 3) - dfg['Low'])), 2).fillna(0)
    dfg['R2'] = round((((dfg['High'] + dfg['Low'] + dfg['Close']) / 3) + dfg['High']) - \
                            dfg['Low'], 2).fillna(0)
    dfg['R1'] = round(
        (2 * ((dfg['High'] + dfg['Low'] + dfg['Close']) / 3)) - dfg['Low'], 2).fillna(0)
    dfg['Pivot'] = round(((dfg['High'] + dfg['Low'] + dfg['Close']) / 3), 2).fillna(0)
    dfg['S1'] = round(
        (2 * ((dfg['High'] + dfg['Low'] + dfg['Close']) / 3)) - dfg['High'], 2).fillna(0)
    dfg['S2'] = round(((dfg['High'] + dfg['Low'] + dfg['Close']) / 3) - (dfg['High'] -
                                                                                            dfg['Low']),2).fillna(0)
                        
    dfg['S3'] = round(dfg['Low'] - (
            2 * (dfg['High'] - ((dfg['High'] + dfg['Low'] + dfg['Close']) / 3))), 2)
    dfg['Mid_point'] = round(((dfg['High'] + dfg['Low']) / 2), 2).fillna(0)
    dfg['CPR'] = round(
        abs((round(((dfg['High'] + dfg['Low'] + dfg['Close']) / 3), 2)) - dfg['Mid_point']),
        2).fillna(0)
    dfg['CPR_SCAN'] = np.where((dfg['CPR'] < ((dfg.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                    "")
    dfg['Candle'] = np.where(abs(dfg['Open'] - dfg['Close']) <
                                    abs(dfg['High'] - dfg['Low']) * 0.2, "DOZI",
                                    np.where(abs(dfg['Open'] - dfg['Close']) >
                                            abs(dfg['High'] - dfg['Low']) * 0.7, "s", ""))
    return dfg
    
   
while True:
    #time.sleep(60)
    start_time = time.time()

   
    end = time.time() - start_time


    print("Data Analysis Completed")    
  
    print("complete") 

    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()
    bhv_fo1 = pd.DataFrame()
    one_day = pd.DataFrame()

    for aa in script_list:
        try:        
            dfg1 = fiveminute_data(aa,'5m',last_trading_day,current_trading_day)

            dfg1["Times"] = dfg1['Datetime'].apply(lambda x: x.split('T')[-1])
            dfg1 = dfg1.astype({"Datetime": "datetime64"})    
            dfg1["Date"] = dfg1["Datetime"].dt.date
            dfg1['Minutes'] = dfg1['TimeNow']-dfg1["Datetime"]
            dfg1['Minutes'] = round((dfg1['Minutes']/np.timedelta64(1,'m')),2)
            dfg1['Buy/Sell1'] = np.where(dfg1['High'] > (dfg1['High']).shift(-1),"Buy_new",np.where(dfg1['Close'] < (dfg1['Low']).shift(-1),"Sell_new",""))
            dfg1['Buy_At'] = round((dfg1['Close']),1)
            dfg1['Stop_Loss'] = np.where(dfg1['Buy/Sell1'] == "Buy_new",round((dfg1['Buy_At'] - (dfg1['Buy_At']*2)/100),1),np.where(dfg1['Buy/Sell1'] == "Sell_new",round((((dfg1['Buy_At']*2)/100) + dfg1['Buy_At']),1),""))
            dfg1['Add_Till'] = round((dfg1['Buy_At']-((dfg1['Buy_At']*0.5)/100)),1)         
            dfg1['Target'] = np.where(dfg1['Buy/Sell1'] == "Buy_new",round((((dfg1['Buy_At']*2)/100) + dfg1['Buy_At']),1),np.where(dfg1['Buy/Sell1'] == "Sell_new",round((dfg1['Buy_At'] - (dfg1['Buy_At']*2)/100),1),""))
            dfg1['Term'] = "SFT"
            dfgg_up_1122 = dfg1[(dfg1["Date"] == last_trading_day.date())]
            maxxx = dfgg_up_1122['High'].max()
            minnn = dfgg_up_1122['Low'].min()
            dfg1['P_D_H_L_B'] = np.where(dfg1['Close'] > maxxx,"PDHB",np.where(dfg1['Close'] < minnn,"PDLB",""))         
            dfg1['Filt_Buy_Sell'] = np.where((dfg1["Vol_Price_break"].shift(-1) == "Vol_Pri_break") & (dfg1["Buy/Sell1"].shift(-1) == "Buy_new") & (dfg1["RSI_14"].shift(-1) > 65 ) & (dfg1["P_D_H_L_B"].shift(-1) == "PDHB" ) & (dfg1["Date"].shift(-1) == current_trading_day.date()),"Filt_Buy","")# & (dfg1["Minutes"].shift(-1) < 5 )]
            
            stk_name1 = dfg1['Name'][0]
            print("5 Minute Data Download and Scan "+str(stk_name1)+" ("+str(aa)+")")               

            dfgg_dn_11 = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_break") & (dfg1["Buy/Sell1"] == "Sell_new") & (dfg1["RSI_14"] < 35 ) & (dfg1["P_D_H_L_B"] == "PDLB" ) & (dfg1["Date"] == current_trading_day.date())]# & (dfg1["Minutes"] < 5 )]
            
            dfgg_up_11 = dfg1[(dfg1["Filt_Buy_Sell"] == "Filt_Buy") & (dfg1["RSI_14"] > 65) & (dfg1["Buy/Sell1"] == "Buy_new")]

            if len(dfgg_up_11) == 0:
                print("111")
            else:
                print("1111")
                dfg126 = dfg1[(dfg1["Date"] == current_trading_day.date())]
                five_df1 = pd.concat([dfg126, five_df1])
                dfgg_up_11.sort_values(['Name', 'Datetime'], ascending=[True, True], inplace=True)
                dfgg_up_1 = dfgg_up_11.iloc[[0]]
                dfgg_up_1['TGT_SL'] = "Entry"
                five_df2 = pd.concat([dfgg_up_1, five_df2])

                dfg22 = dfg1                
                close = list(dfgg_up_1['Close'])
                entry = close[0]
                sllll = float(round((dfgg_up_1['Close'] - (dfgg_up_1['Close']*2)/100),1))
                targettt = float(round((((dfgg_up_1['Close']*2)/100) + dfgg_up_1['Close']),1))
                trail = 1
                forwardMove = 1
                SL = sllll
                # print(entry,sllll,targettt,trail,forwardMove,SL)


                roww = dfg22.shape[0]
                print(roww)
                count = 0
                for i in range(0, len(dfg22)):
                    print(entry,sllll,targettt,dfg22.iloc[i]['Close'],dfg22.iloc[i]['Name'], dfg22.iloc[i]['Times'])
                    if dfg22.iloc[i]['High'] > targettt + 1 :
                        print("yes")
                    if dfg22.iloc[i]['Low'] < sllll - 1 :
                        print("no")

                # if dfg22['High'] > targettt+1:
                #     sllll+1
                # else:
                #      sllll+0


                # for i in range(0,len(dfg22['Close'])-1):
                #     print(i)
                #     diff = round((entry-close[i]),2)
                #     point = int(diff/forwardMove) if diff > 0 else 0
                #     SLmove = point*trail

                #     if sllll - SL < SLmove:
                #         SL = sllll - SLmove
                #         print(f'{i } {dfg22.loc[i]["Datetime"]} close{close[i]} New SL {SL} Diff {diff}')
                #     elif SL<= close[i]:
                #         print('SL Hit : ',dfg22.loc[i]['Datetime'],close[i],' ',SL)
                #         break
                #     else:
                #        print(f'{i } {dfg22.loc[i]["Datetime"]} close{close[i]} SL {SL} Diff {diff}')



                # targettt = float(round((((dfgg_up_1['Close']*2)/100) + dfgg_up_1['Close']),1))
                # sllll = float(round((dfgg_up_1['Close'] - (dfgg_up_1['Close']*2)/100),1))
                timee = list(dfgg_up_1['Datetime'])[0] 
                print(timee)  
               
                dfg22['TGT_SL'] = np.where(dfg22['High'] > targettt,"TGTT",np.where(dfg22['Low'] < sllll,"SLLL",""))
                dfg222 = dfg22[(dfg22["TGT_SL"] != "") & (dfg22["Date"] == current_trading_day.date()) & (dfg22["Datetime"] > timee)]
                dfg222.sort_values(['Name', 'Datetime'], ascending=[True, True], inplace=True)
                dfg2222 = dfg222.iloc[[0]]                
                five_df4 = pd.concat([dfg2222, five_df4])
       
                datae = [dfgg_up_1, dfg2222]
                final_df = pd.concat(datae)
                final_df['Time_use'] = (final_df['Date'] - final_df['Date'].shift(1)) / pd.Timedelta(minutes=1)
                final_df['P&L'] = final_df['Close'] - final_df['Close'].shift(1)
                five_df5 = pd.concat([final_df, five_df5])
               
                dfggg = one_Day_Data(aa, '1d', days_365, current_trading_day)
                dfgggg = dfggg.iloc[[0]]  
                bhv_fo1 = pd.concat([dfgggg, bhv_fo1])

                five_df1221 = pd.merge(dfgg_up_1, dfgggg, on=['Scripcode'], how='inner')
                five_df12211 = five_df1221[(five_df1221["Vol_Price_break_y"] == "Vol_Pri_break") & (five_df1221["Buy/Sell1"] == "Buy_new") & (five_df1221["RSI_14_y"] > 65 ) & (five_df1221["P_D_H_L_B"] == "PDHB" )]# & (five_df1221["Date"] == current_trading_day.date())]# & (dfg1["Minutes"] < 5 )]
                one_day = pd.concat([five_df12211, one_day])    

        except Exception as e:
                print(e) 
        print("------------------------------------------------")
    
    bhv_fo1.sort_values(['Name'], ascending=[True], inplace=True)
    bhv_fo.range("a:az").value = None
    bhv_fo.range("a1").options(index=False).value = bhv_fo1

    one_day.sort_values(['Name_x'], ascending=[True], inplace=True)
    by.range("a:az").value = None
    by.range("a1").options(index=False).value = one_day


    if five_df1.empty:
        pass
    else:
        # five_df11 = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner') 
        five_df1 = five_df1[['Name','Scripcode','Datetime','Date','Times','TimeNow','Minutes','Open','High','Low','Close','Volume',
        'RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','Buy/Sell1',
        'Buy_At','Stop_Loss','Add_Till','Target','Term','P_D_H_L_B','Filt_Buy_Sell',
        'Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size',
        'R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        									

        five_df1.sort_values(['Name', 'Date','Times',], ascending=[True, False,False], inplace=True)
        Fiv_dt.range("a:az").value = None
        Fiv_dt.range("a1").options(index=False).value = five_df1

    if five_df2.empty:
        pass
    else:
        #five_df12 = pd.merge(flt_exc_eq, five_df2, on=['Scripcode'], how='inner') 
        five_df2 = five_df2[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
                             'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
                             'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
                             'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df2.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True)      		
        		
        delv_dt.range("a:az").value = None
        delv_dt.range("a1").options(index=False).value = five_df2

    
    if five_df3.empty:
        pass
    else:
        pass
        # five_df12 = pd.merge(flt_exc_eq, five_df3, on=['Scripcode'], how='inner') 
        # five_df3 = five_df3[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume',
        #                      'RSI_14','Sma_200_break','Week52','Filt_buy','P_D_H_B','Price_Chg','Vol_Chg','Vol_Price_break','Deliv_break',
        #                      'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        #five_df3.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        #delv_dt.range("a25").options(index=False).value = five_df3

    if five_df4.empty:
        pass
    else:
        # five_df13 = pd.merge(flt_exc_eq, five_df4, on=['Scripcode'], how='inner') 
        five_df4 = five_df4[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Open','High','Low','Close','Volume',
                             'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
                             'Buy_At','Stop_Loss','Add_Till','Target','Term','Filt_Buy_Sell',
                             'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True) 
        five_delv.range("a:az").value = None
        five_delv.range("a1").options(index=False).value = five_df4

    if five_df5.empty:
        pass
    else:
        # five_df14 = pd.merge(flt_exc_eq, five_df5, on=['Scripcode'], how='inner') 
        five_df5 = five_df5[['Name','Scripcode','Date','Times','TimeNow','Minutes','TGT_SL','Time_use','P&L','Buy_At','Stop_Loss','Add_Till','Target',
                             'Open','High','Low','Close','Volume',
                             'RSI_14','Cand_col','Cand_Body','Top_Wick','Bot_Wick','Cand_Size','Price_Chg','Vol_Chg','Vol_Price_break',                             
                             'Term','Filt_Buy_Sell',
                             'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]

        five_df5.sort_values(['Name', 'Date','Times'], ascending=[True, False,True], inplace=True)      
        fl_data.range("a:az").value = None
        fl_data.range("a1").options(index=False).value = five_df5

    if five_df6.empty:
        pass
    else:
        pass
        # five_df12 = pd.merge(flt_exc_eq, five_df6, on=['Scripcode'], how='inner') 
        #five_df6 = five_df6[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume','RSI_14','Filt_buy','P_D_H_L_B','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        #five_df6.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        #fl_data.range("a50").options(index=False).value = five_df6

    # if five_df4.empty:
    #     pass
    # else:
    #     pass
    #     # five_df13 = pd.merge(flt_exc_eq, five_df4, on=['Scripcode'], how='inner') 
    #     #five_df4 = five_df4[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Filt_buy','P_D_H_L_B','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
    #     #five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        
    #     not_selected_up = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Buy_new") & (five_df4["RSI_14"] > 65 ) & (five_df4["Date"] == current_trading_day.date())]
    #     not_selected_dn = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Sell_new") & (five_df4["RSI_14"] < 30 ) & (five_df4["Date"] == current_trading_day.date())]
        
    #     #First Two Row
    #     up1 = np.unique([int(i) for i in not_selected_up['Scripcode']]).tolist()
    #     up4 = pd.DataFrame()
    #     for j in up1:
    #         up2 = not_selected_up[(not_selected_up["Scripcode"] == j)]
    #         up3 = up2.iloc[:2]
    #         up4 = pd.concat([up3, up4])
    #         up4.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True)            
    #         by.range("a:az").value = None
    #         by.range("a1").options(index=False).value = up4

    #     dn1 = np.unique([int(i) for i in not_selected_dn['Scripcode']]).tolist()
    #     dn4 = pd.DataFrame()
    #     for k in dn1:
    #         dn2 = not_selected_dn[(not_selected_dn["Scripcode"] == k)]
    #         dn3 = dn2.iloc[:2]
    #         dn4 = pd.concat([dn3, dn4])
    #         dn4.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True)            
    #         by.range("a100").options(index=False).value = dn4



    #     up11 = np.unique([int(i) for i in not_selected_up['Scripcode']]).tolist()
    #     up41 = pd.DataFrame()
    #     for j in up11:
    #         up21 = not_selected_up[(not_selected_up["Scripcode"] == j)]
    #         up41 = pd.concat([up21, up41])
    #         up41.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True)            
    #         sl.range("a:az").value = None
    #         sl.range("a1").options(index=False).value = up41
            
    #     dn11 = np.unique([int(i) for i in not_selected_dn['Scripcode']]).tolist()
    #     dn41 = pd.DataFrame()
    #     for k in dn11:
    #         dn21 = not_selected_dn[(not_selected_dn["Scripcode"] == k)]
    #         dn41 = pd.concat([dn21, dn41])
    #         dn41.sort_values(['Name', 'Date','Times'], ascending=[True, False,False], inplace=True)             
    #         sl.range("a100").options(index=False).value = dn41
  
    end = time.time() - start_time
 
    # print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    # print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    #print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Stocks_Backtest_0.1.xlsx")



