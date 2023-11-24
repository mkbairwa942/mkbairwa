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

telegram_first_name = "mkbairwa"
telegram_username = "mkbairwa_bot"
telegram_id = ":758543600"
#telegram_basr_url = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
telegram_basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236"

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

if not os.path.exists("Stocks_Breakout.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Stocks_Breakout.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Stocks_Breakout.xlsx')
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
strategy1.range("a:u").value = None
strategy2.range("a:u").value = None
strategy3.range("a:u").value = None

st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
st.range("a:u").value = None
st1.range("a:u").value = None
st2.range("a:u").value = None
st3.range("a:u").value = None
st4.range("a:i").value = None

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

# script_list = [13587,	1134,	193,	21174,	5142,	14218,	11423,	25690,	11530,	13421,	2868,	3776,	14947,	357,	31475,	9652,	8175,	714,	11233,	3748,	5385,	2716,	3744,	11027,	17625,	3150,]
# stk_list = ['APOLLO',	'ARVIND',	'CDSL',	'CIGNITITEC',	'CTE',	'DATAMATICS',	'DSSL',	'EMIL',	'EMKAY',	'HITECH',	'IWEL',	'MOTILALOFS',	'NAM-INDIA',	'ORBTEXP',	'RELCHEMQ',	'SAGARDEEP',	'SHALBY',	'SUVEN',	'WEIZMANIND',	'AAVAS',	'BUTTERFLY',	'FINEORG',	'INFOBEAN',	'MOLDTECH',	'SIEMENS']
	
script_list = np.unique(exc_equity['Scripcode'])
stk_list = np.unique(exc_equity["Root"])

print("Total Stock : "+str(len(script_list)))
print(script_list)

order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 3045, Qty=10,Price=25)

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


def ordef_func():
    try:
        ordbook = pd.DataFrame(client.order_book())
        #print(ordbook.tail(2))
        pos.range("q1").options(index=False).value = ordbook
    except Exception as e:
                print(e)

    try:
        if ordbook is not None:
            print("Order Book not Empty")        
            ordbook1 = ordbook[ordbook['OrderStatus'] != "Rejected By 5P"]   
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
            ordbook1 = ordbook1[['Datetimeee', 'BuySell', 'DelvIntra','PendingQty','Qty','Rate','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','AtMarket']]
            ordbook1.sort_values(['Datetimeee'], ascending=[False], inplace=True)
            pos.range("a1").options(index=False).value = ordbook1
        else:
            print("Order Book Empty")
    except Exception as e:
                print(e)
    return ordbook1
            
buy_order_li = ordef_func()
buy_order_list = (np.unique([int(i) for i in buy_order_li['ScripCode']])).tolist()
print(buy_order_list)

while True:
    #time.sleep(60)
    start_time = time.time()

    # live_market_keys.reverse()
    # index_frame = pd.DataFrame()
    # index_frame_one = pd.DataFrame()

    # for idx in live_market_keys:
    #     print(idx)
    #     index_fra = nse.live_market_data(idx) 
    #     tot_valuee = index_fra["totalTradedValue"].iloc[0]               
    #     index_fra['Index'] = idx                
    #     index_fram = index_fra[1:]
    #     index_fram['Weitage'] = round(((index_fram["totalTradedValue"]*100)/tot_valuee),2)
    #     post = (index_fram['change'] > 0).sum().sum()
    #     negat = (index_fram['change'] < 0).sum().sum()
    #     index_frame = pd.concat([index_fram, index_frame])
    #     index_row = index_fra[:1] 
    #     idx_len = len(index_fram['Index'])
    #     index_row['Post'] = post
    #     index_row['Negat'] = negat
    #     index_row['Neutral'] = idx_len-(index_row['Post']+index_row['Negat'])
    #     index_row['Total'] = idx_len
    #     index_row['Calc'] = (index_row['Post']*100)/index_row['Total']
    #     index_row['Per'] = np.round((np.where(index_row['Calc']<50,(index_row['Calc'])-50,(index_row['Calc'])-50)),2)
    #     index_frame_one = pd.concat([index_row, index_frame_one],axis=0)

    # index_frame_one.sort_values(['change','identifier'], ascending=[True,True], inplace=True)
    # index_frame_one = index_frame_one[['Index','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','lastUpdateTime','Post','Negat','Neutral','Total','Per']]
    # index_frame.sort_values(['Index','change'], ascending=[True,True], inplace=True)
    # index_frame = index_frame[['Index','identifier','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','Weitage','totalTradedVolume','totalTradedValue','lastUpdateTime']]
    # nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY 50")]
    # bank_nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY BANK")]
    # nifty_range = nifty2['dayHigh'].iloc[-1] - nifty2['dayLow'].iloc[-1]
    # bank_nifty_range = bank_nifty2['dayHigh'].iloc[-1] - bank_nifty2['dayLow'].iloc[-1]      

    # st3.range("a1").options(index=False).value = index_frame
    # st2.range("a:n").value = None
    # st2.range("p1").options(index=False).value = "Today's rangs is"
    # st2.range("p3").options(index=False).value = nifty_range
    # st2.range("p2").options(index=False).value = bank_nifty_range
    # st2.range("a1").options(index=False).value = index_frame_one

    # nifty1 = index_frame[(index_frame["Index"] == "NIFTY 50")]
    # nifty1 = nifty1[['identifier','change','pChange','Weitage']]            
    # bank_nifty1 = index_frame[(index_frame["Index"] == "NIFTY BANK")]
    # bank_nifty1 = bank_nifty1[['identifier','change','pChange','Weitage']]
    # nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY 50")]
    # bank_nifty2 = index_frame_one[(index_frame_one["Index"] == "NIFTY BANK")]


    # st4.range("a1").options(index=False).value = nifty1
    # st4.range("f1").options(index=False).value = bank_nifty1
    # st4.range("k2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*5+COLUMN(B2),2))"
    # st4.range("q2").options(index=False).value = "=INDIRECT(ADDRESS((ROW($B1)-1)*3+COLUMN(B2),7))"


    # def five_df_new1_func(period,scp_lst,from_d,to_d):  
    #     five_df1 = pd.DataFrame()
    #     for a in scp_lst:
    #         try:
    #             print(a)
    #             dfg = client.historical_data('N', 'C', a, period, from_d, to_d)
    #             dfg['Scripcode'] = a
    #             dfg['Date'] = current_trading_day
    #             dfg["SMA_200"] = np.round((pta.sma(dfg["Close"], length=200,offset=0)),2)
    #             dfg["RSI_14"] = np.round((pta.rsi(dfg["Close"], length=14)),2)
    #             dfg1 = dfg.iloc[::-1]
    #             five_df1 = pd.concat([dfg1.iloc[:1], five_df1])
    #         except Exception as e:
    #             print(e)    
    #     five_df = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner')  

    #     five_df_new = five_df[five_df['Name'].isin(opt_li)]
        
    #     five_df_new['OPT'] = 'Y'
    #     five_df_new = five_df_new[['Name','OPT']]
    #     five_df_new1 = pd.merge(five_df, five_df_new, on=['Name'], how='outer')
    #     five_df_new1 = five_df_new1[['Name','Date', 'Open', 'High', 'Low','Close','Volume','SMA_200','RSI_14','Scripcode','OPT']]
    #     five_df_new1.sort_values(['Name'], ascending=[True], inplace=True)
    #     return five_df_new1  
    
    # five_df_new11 = five_df_new1_func('1d',script_list,days_365, current_trading_day)
    
    # Fiv_dt.range("a:i").value = None
    # Fiv_dt.range("a1").options(index=False).value = five_df_new11
    
    end = time.time() - start_time
    
    # five_df_new1 = pd.read_excel('E:\STOCK\Capital_vercel1\Stocks_Breakout.xlsx', sheet_name='Five_data')

 

    # start_time3 = time.time()
 
    # end3 = time.time() - start_time3

    print("Data Analysis Completed")    
  
    print("complete") 

    five_df1 = pd.DataFrame()
    five_df2 = pd.DataFrame()
    five_df3 = pd.DataFrame()
    five_df4 = pd.DataFrame()
    five_df5 = pd.DataFrame()
    five_df6 = pd.DataFrame()

    for a in script_list:
        try:
            # print("1 Day Data Download and Scan "+str(a))
            #print(a)
            dfggg = client.historical_data('N', 'C', a, '1d', days_365, current_trading_day)      
            dfggg['Scripcode'] = a
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
            
            
            
            stk_name = dfg['Name'][0]
            print("1 Day Data Download and Scan "+str(stk_name)+" ("+str(a)+")")
            
            #dfg["Date"] = dfg["Datetime"].dt.date
            dfg = dfg[0:25]

            five_df1 = pd.concat([dfg, five_df1])

            curr_day = (dfggg['Datetime'].apply(pd.to_datetime)).iloc[-1]

            dfgg_up = dfg[(dfg["Vol_Price_break"] == "Vol_Pri_break") & (dfg["Buy/Sell"] != "") & (dfg["P_D_H_B"] == "PDHB") &(dfg["RSI_14"] > 70 ) & (dfg['Date'] == curr_day) & (dfg["Week52"] != "")]# & (dfg["Del_Vol_Pri_break"] != "") ]
            dfgg_dn = dfg[(dfg["Vol_Price_break"] == "Vol_Pri_break") & (dfg["Buy/Sell"] != "") & (dfg["P_D_H_B"] == "PDLB") &(dfg["RSI_14"] < 30 ) & (dfg['Date'] == curr_day) & (dfg["Week52"] != "")]# & (dfg["Del_Vol_Pri_break"] != "")]
            
            five_df2 = pd.concat([dfgg_up, five_df2])            
            five_df3 = pd.concat([dfgg_dn, five_df3])

            up = np.unique([int(i) for i in dfgg_up['Scripcode']]).tolist()
            dn = np.unique([int(i) for i in dfgg_dn['Scripcode']]).tolist()

            five_min_list1 = []
            five_min_list1.append(up)
            five_min_list1.append(dn)

            five_min_list = []
            for list in five_min_list1:
                for number in list:
                    five_min_list.append(number)

            if len(five_min_list) == 0:
                pass        
            else:
                if five_min_list[0]:
                    aa = five_min_list[0]
                    dfg1 = client.historical_data('N', 'C', aa, '5m',last_trading_day,current_trading_day) 
                    dfg1['Scripcode'] = aa  
                            
                    dfg1 = pd.merge(flt_exc_eq, dfg1, on=['Scripcode'], how='inner') 
                    dfg1 = dfg1[['Scripcode','Name','Datetime','Open','High','Low','Close','Volume']]
                    
                    dfg1['Date'] = current_trading_day 
                    dfg1["RSI_14"] = np.round((pta.rsi(dfg1["Close"], length=14)),2) 

                    dfg1.sort_values(['Datetime'], ascending=[False], inplace=True)
                    dfg1['TimeNow'] = datetime.now()
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

                    dfg1 = dfg1.astype({"Datetime": "datetime64"})    
                    dfg1["Date"] = dfg1["Datetime"].dt.date

                    dfg1['Minutes'] = dfg1['TimeNow']-dfg1["Datetime"]
                    dfg1['Minutes'] = round((dfg1['Minutes']/np.timedelta64(1,'m')),2)
                    dfg1['Buy/Sell1'] = np.where(dfg1['Close'] > (dfg1['High']).shift(-1),"Buy_new",np.where(dfg1['Close'] < (dfg1['Low']).shift(-1),"Sell_new",""))
                    dfg1['Buy_At'] = round((dfg1['Close']),1)
                    dfg1['Stop_Loss'] = np.where(dfg1['Buy/Sell1'] == "Buy_new",round((dfg1['Buy_At'] - (dfg1['Buy_At']*1)/100),1),np.where(dfg1['Buy/Sell1'] == "Sell_new",round((((dfg1['Buy_At']*2)/100) + dfg1['Buy_At']),1),""))
                    dfg1['Add_Till'] = round((dfg1['Buy_At']-((dfg1['Buy_At']*0.5)/100)),1)         
                    dfg1['Target'] = np.where(dfg1['Buy/Sell1'] == "Buy_new",round((((dfg1['Buy_At']*2)/100) + dfg1['Buy_At']),1),np.where(dfg1['Buy/Sell1'] == "Sell_new",round((dfg1['Buy_At'] - (dfg1['Buy_At']*2)/100),1),""))
                    dfg1['Term'] = "SFT"

                    stk_name1 = dfg1['Name'][0]
                    print("5 Minute Data Download and Scan "+str(stk_name1)+" ("+str(aa)+")")               

                    five_df4 = pd.concat([dfg1, five_df4])

                    dfgg_up_11 = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_break") & (dfg1["Buy/Sell1"] == "Buy_new") & (dfg1["RSI_14"] > 70 ) & (dfg1["Date"] == current_trading_day.date()) & (dfg1["Minutes"] < 5 )]
                    dfgg_dn_11 = dfg1[(dfg1["Vol_Price_break"] == "Vol_Pri_break") & (dfg1["Buy/Sell1"] == "Sell_new") & (dfg1["RSI_14"] < 30 ) & (dfg1["Date"] == current_trading_day.date()) & (dfg1["Minutes"] < 5 )]

                    #dfgg1 = dfgg1.iloc[[1]]
                    #dfgg1 = dfgg1.iloc[1:2]
                    if len(dfgg_up_11) == 0:
                        print("111")
                    else:
                        print("1111")
                        dfgg_up_1 = dfgg_up_11.iloc[[0]]
                        five_df5 = pd.concat([dfgg_up_1, five_df5])        

                        if dfgg_up_1.empty:
                            parameters = {"chat_id" : "6143172607","text" : "Stock Selected but more than '5 MINUTE' ago : "+str(stk_name1)}
                            resp = requests.get(telegram_basr_url, data=parameters)
                            #print(resp.text)
                            print("Stock Selected for Buy but more than '5 MINUTE' ago : "+str(stk_name1))

                        else:
                            if aa in buy_order_list: 
                                print(str(aa)+" is Already Buy")
                            else:
                                Buy_Scriptcodee = aa
                                Buy_price_of_stock = float(dfgg_up_1['Buy_At'])  
                                Buy_Add_Till = float(dfgg_up_1['Add_Till'])                       
                                Buy_Stop_Loss = float(dfgg_up_1['Stop_Loss'])    
                                Buy_Target = float(dfgg_up_1['Target']) 
                                Buy_timee = str((dfgg_up_1['Datetime'].values)[0])[0:19] 
                                Buy_timee1= Buy_timee.replace("T", " " )
                                # print(Buy_timee1)

                                if Buy_price_of_stock < 100:
                                    Buy_quantity_of_stock = 200
                                if Buy_price_of_stock > 100 and Buy_price_of_stock < 200:
                                    Buy_quantity_of_stock = 100                        
                                if Buy_price_of_stock > 200 and Buy_price_of_stock < 300:
                                    Buy_quantity_of_stock = 80
                                if Buy_price_of_stock > 300:
                                    Buy_quantity_of_stock = 50
                                Req_Amount = Buy_quantity_of_stock*Buy_price_of_stock   

                                order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = Buy_Scriptcodee, Qty=Buy_quantity_of_stock,Price=Buy_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Buy_Stop_Loss)
                            
                                #print("5 Minute Data Selected "+str(stk_name1)+" ("+str(Buy_Scriptcodee)+")")
                                #print("Buy Order of "+str(stk_name1)+" at : Rs "+str(Buy_price_of_stock)+" and Quantity is "+str(Buy_quantity_of_stock)+" on"+str(Buy_timee1))
                            
                                print("SYMBOL : "+str(stk_name1)+"\n BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1))

                                parameters1 = {"chat_id" : "6143172607","text" : "STOCK : "+str(stk_name1)+"\n BUY AT : "+str(Buy_price_of_stock)+"\n ADD TILL : "+str(Buy_Add_Till)+"\n STOP LOSS : "+str(Buy_Stop_Loss)+"\n TARGET : "+str(Buy_Target)+"\n QUANTITY : "+str(Buy_quantity_of_stock)+"\n TIME : "+str(Buy_timee1)}
                                resp = requests.get(telegram_basr_url, data=parameters1)
                                # print(resp.text)

                                # buy_order_list.append(aa)

                    if len(dfgg_dn_11) == 0:
                        print("222")
                    else:
                        print("22")
                        dfgg_dn_1 = dfgg_dn_11.iloc[[0]]
                        five_df6 = pd.concat([dfgg_dn_1, five_df6])

                        if dfgg_dn_1.empty:
                            parameters = {"chat_id" : "6143172607","text" : "Stock Selected but more than '5 MINUTE' ago : "+str(stk_name1)}
                            resp = requests.get(telegram_basr_url, data=parameters)
                            #print(resp.text)
                            print("Stock Selected for Sell but more than '5 MINUTE' ago : "+str(stk_name1))

                        else:
                            if aa in buy_order_list: 
                                print(str(aa)+" is Already Buy")
                            else:
                                Sell_Scriptcodee = aa
                                Sell_price_of_stock = float(dfgg_dn_1['Buy_At'])  
                                Sell_Add_Till = float(dfgg_dn_1['Add_Till'])                       
                                Sell_Stop_Loss = float(dfgg_dn_1['Stop_Loss'])    
                                Sell_Target = float(dfgg_dn_1['Target']) 
                                Sell_timee = str((dfgg_dn_1['Datetime'].values)[0])[0:19] 
                                Sell_timee1= Sell_timee.replace("T", " " )
                                # print(Buy_timee1)

                                if Sell_price_of_stock < 100:
                                    Sell_quantity_of_stock = 200
                                if Sell_price_of_stock > 100 and Sell_price_of_stock < 200:
                                    Sell_quantity_of_stock = 100                        
                                if Sell_price_of_stock > 200 and Sell_price_of_stock < 300:
                                    Sell_quantity_of_stock = 80
                                if Sell_price_of_stock > 300:
                                    Sell_quantity_of_stock = 50
                                Req_Amount = Sell_quantity_of_stock*Sell_price_of_stock   

                                #order = client.place_order(OrderType='S',Exchange='N',ExchangeType='C', ScripCode = Sell_Scriptcodee, Qty=Sell_quantity_of_stock,Price=Sell_price_of_stock, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Sell_Stop_Loss)
                                
                                #print("5 Minute Data Selected "+str(stk_name1)+" ("+str(Sell_Scriptcodee)+")")
                                #print("Sell Order of "+str(stk_name1)+" at : Rs "+str(Sell_price_of_stock)+" and Quantity is "+str(Sell_quantity_of_stock)+" on"+str(Sell_timee1))
                                
                                print("SYMBOL : "+str(stk_name1)+"\n SELL AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1))

                                parameters1 = {"chat_id" : "6143172607","text" : "STOCK : "+str(stk_name1)+"\n SELL AT : "+str(Sell_price_of_stock)+"\n ADD TILL : "+str(Sell_Add_Till)+"\n STOP LOSS : "+str(Sell_Stop_Loss)+"\n TARGET : "+str(Sell_Target)+"\n QUANTITY : "+str(Sell_quantity_of_stock)+"\n TIME : "+str(Sell_timee1)}
                                resp = requests.get(telegram_basr_url, data=parameters1)
                                # print(resp.text)

                                # buy_order_list.append(aa)
                                
                else:
                    print("444")
                    pass           
                    
            #five_df2 = pd.concat([dfg, five_df2])
        except Exception as e:
                print(e) 
        print("------------------------------------------------")
    
    if five_df1.empty:
        pass
    else:
        # five_df11 = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner') 
        five_df1 = five_df1[['Name','Scripcode','Date','TimeNow','Open','High','Low','Close','Volume','Deliv_qty','Deliv_per','RSI_14','Sma_200_break','Week52','P_D_H_B','Price_Chg','Vol_Chg','Vol_Price_break','Deliv_break','Del_Vol_Pri_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df1.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
        Fiv_dt.range("a:az").value = None
        Fiv_dt.range("a1").options(index=False).value = five_df1

    if five_df2.empty:
        pass
    else:
        # five_df12 = pd.merge(flt_exc_eq, five_df2, on=['Scripcode'], how='inner') 
        five_df2 = five_df2[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume',
                             'RSI_14','Sma_200_break','Week52','P_D_H_B','Price_Chg','Vol_Chg','Vol_Price_break','Deliv_break',
                             'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df2.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        delv_dt.range("a:az").value = None
        delv_dt.range("a1").options(index=False).value = five_df2

    
    if five_df3.empty:
        pass
    else:
        # five_df12 = pd.merge(flt_exc_eq, five_df3, on=['Scripcode'], how='inner') 
        five_df3 = five_df3[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume',
                             'RSI_14','Sma_200_break','Week52','P_D_H_B','Price_Chg','Vol_Chg','Vol_Price_break','Deliv_break',
                             'O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df3.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        delv_dt.range("a25").options(index=False).value = five_df3

    if five_df4.empty:
        pass
    else:
        # five_df13 = pd.merge(flt_exc_eq, five_df4, on=['Scripcode'], how='inner') 
        five_df4 = five_df4[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        five_delv.range("a:az").value = None
        five_delv.range("a1").options(index=False).value = five_df4

    if five_df5.empty:
        pass
    else:
        # five_df14 = pd.merge(flt_exc_eq, five_df5, on=['Scripcode'], how='inner') 
        five_df5 = five_df5[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df5.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        fl_data.range("a:az").value = None
        fl_data.range("a1").options(index=False).value = five_df5

    if five_df6.empty:
        pass
    else:
        # five_df12 = pd.merge(flt_exc_eq, five_df6, on=['Scripcode'], how='inner') 
        five_df6 = five_df6[['Name','Scripcode','Datetime','TimeNow','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df6.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        fl_data.range("a50").options(index=False).value = five_df6

    if five_df4.empty:
        pass
    else:
        # five_df13 = pd.merge(flt_exc_eq, five_df4, on=['Scripcode'], how='inner') 
        five_df4 = five_df4[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','Date','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','Vol_Price_break','Buy/Sell1','O=H=L','Pattern','Buy/Sell','R3','R2','R1','Pivot','S1','S2','S3','Mid_point','CPR','CPR_SCAN','Candle']]
        five_df4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        
        not_selected_up = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Buy_new") & (five_df4["RSI_14"] > 70 ) & (five_df4["Date"] == current_trading_day.date())]
        not_selected_dn = five_df4[(five_df4["Vol_Price_break"] == "Vol_Pri_break") & (five_df4["Buy/Sell1"] == "Sell_new") & (five_df4["RSI_14"] < 30 ) & (five_df4["Date"] == current_trading_day.date())]
        
        #First Two Row
        up1 = np.unique([int(i) for i in not_selected_up['Scripcode']]).tolist()
        up4 = pd.DataFrame()
        for j in up1:
            up2 = not_selected_up[(not_selected_up["Scripcode"] == j)]
            up3 = up2.iloc[:2]
            up4 = pd.concat([up3, up4])
            up4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
            by.range("a:az").value = None
            by.range("a1").options(index=False).value = up4

        dn1 = np.unique([int(i) for i in not_selected_dn['Scripcode']]).tolist()
        dn4 = pd.DataFrame()
        for k in dn1:
            dn2 = not_selected_dn[(not_selected_dn["Scripcode"] == k)]
            dn3 = dn2.iloc[:2]
            dn4 = pd.concat([dn3, dn4])
            dn4.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
            by.range("a100").options(index=False).value = dn4



        up11 = np.unique([int(i) for i in not_selected_up['Scripcode']]).tolist()
        up41 = pd.DataFrame()
        for j in up11:
            up21 = not_selected_up[(not_selected_up["Scripcode"] == j)]
            up41 = pd.concat([up21, up41])
            up41.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
            sl.range("a:az").value = None
            sl.range("a1").options(index=False).value = up41
            
        dn11 = np.unique([int(i) for i in not_selected_dn['Scripcode']]).tolist()
        dn41 = pd.DataFrame()
        for k in dn11:
            dn21 = not_selected_dn[(not_selected_dn["Scripcode"] == k)]
            dn41 = pd.concat([dn21, dn41])
            dn41.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
            sl.range("a100").options(index=False).value = dn41
  
    end = time.time() - start_time
 
    # print("Five Paisa Data Download New")

    end4 = time.time() - start_time
    # print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    #print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Stocks_Breakout.xlsx")



