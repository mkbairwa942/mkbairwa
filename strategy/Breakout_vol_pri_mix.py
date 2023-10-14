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
from five_paisa import *
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

#client = credentials('alpesh','091254')

from_d = (date.today() - timedelta(days=10))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

days_365 = (date.today() - timedelta(days=365))
print(days_365)

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
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

# pdf = nse.get_stock_info("RELIANCE", trade_info=True)["securityWiseDP"]
# print(pdf)
print("hii")
stk_li = np.unique(bhavcopy(last_trading_day)['SYMBOL'])

opt_li = pd.unique(bhavcopy_fno(last_trading_day)['SYMBOL'])

stk_list = stk_li

print("---- Data Process Started ----")

if not os.path.exists("Breakout_vol_pri_mix.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Breakout_vol_pri_mix.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Breakout_vol_pri_mix.xlsx')
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

exc.range("a:s").value = None
exc.range("a1").options(index=False).value = script_code_5paisa
print("Excel : Started")
exchange = None

while True:    
    if exchange is None: 
        try:
            exc_equity = pd.DataFrame(script_code_5paisa)
            exc_equity = exc_equity[(exc_equity["Exch"] == "N") & (exc_equity["ExchType"] == "C")]
            exc_equity = exc_equity[exc_equity["Series"] == "EQ"]
            exc_equity = exc_equity[exc_equity["CpType"] == "XX"]
            exc_equity["Watchlist"] = exc_equity["Exch"] + ":" + exc_equity["ExchType"] + ":" + exc_equity["Name"]

            exc_fut = pd.DataFrame(script_code_5paisa)
            exc_fut = exc_fut[(exc_fut["Exch"] == "N") & (exc_fut["ExchType"] == "D") & (exc_fut["CpType"] == "XX")]
            exc_fut["Watchlist"] = exc_fut["Exch"] + ":" + exc_fut["ExchType"] + ":" + exc_fut["Name"]
            
            exc_opt = pd.DataFrame(script_code_5paisa)
            exc_opt = exc_opt[(exc_opt["Exch"] == "N") & (exc_opt["ExchType"] == "D") & (exc_opt["CpType"] != "XX") & (exc_opt["CpType"] != "EQ")]
            exc_opt["Watchlist"] = exc_opt["Exch"] + ":" + exc_opt["ExchType"] + ":" + exc_opt["Name"]
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

symb = pd.DataFrame({"Name": list(exc_equity["Root"].unique())})
symb = symb.set_index("Name",drop=True)
#oc.range("a1").options(index=False).value = symb

flt_exc_eq = pd.merge(symb, exc_equity, on=['Name'], how='inner')
flt_exc_eq.sort_values(['Name'], ascending=[True], inplace=True)
flt_exc_eq = flt_exc_eq[['ExchType','Name', 'ISIN', 'FullName', 'CO BO Allowed','Scripcode','Watchlist']]

flt_exc_fut = exc_fut
flt_exc_fut.sort_values(['Root','Expiry'], ascending=[True,True], inplace=True)
flt_exc_fut = flt_exc_fut[['ExchType','Name','Expiry', 'ISIN', 'FullName','LotSize','QtyLimit', 'CO BO Allowed','Scripcode','Watchlist']]

flt_exc_opt = exc_opt
flt_exc_opt.sort_values(['Root','Expiry','StrikeRate'], ascending=[True,True,True], inplace=True)
flt_exc_opt = flt_exc_opt[['ExchType','Name','Expiry', 'ISIN', 'FullName','LotSize','QtyLimit', 'CO BO Allowed','Scripcode','Watchlist']]

flt_exc.range("a:az").value = None
flt_exc.range("a1").options(index=False).value = flt_exc_eq
flt_exc.range("i1").options(index=False).value = flt_exc_fut
flt_exc.range("u1").options(index=False).value = flt_exc_opt
print("Exchange Data Download")

fut_li = np.unique(exc_fut['Root'])

future_dataframe = pd.DataFrame()
for i in fut_li:
    data_fra = exc_fut[exc_fut['Root'] == i]
    future_dataframe = pd.concat([data_fra[:1], future_dataframe])
future_dataframe.sort_values(['Root'], ascending=[True], inplace=True)
future_dataframe = future_dataframe[['ExchType','Root','Expiry', 'ISIN', 'FullName','LotSize','QtyLimit', 'CO BO Allowed','Scripcode','Watchlist']]
future_dataframe.rename(columns={'Root': 'Name'},inplace=True)
flt_exc.range("ag1").options(index=False).value = future_dataframe

# oc.range("d2").options(index=False).value, oc.range("d3").options(index=False).value, oc.range("d4").options(index=False).value = "Symbol==>>", "Expiry==>>", "LotSize==>>",
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
    return eq_bhav

eq_bhav = bhavcopy_func()
bhv.range("a:i").value = None                          
bhv.range("a1").options(index=False).value = eq_bhav
print(str(days_count)+" Days STOCK Data Download")

# def bhavcopy_fno_func():
#     fo_bhav = pd.DataFrame()
#     for i in trading_days:
#         try:
#             print(i)
#             fo_bh_df = bhavcopy_fno(i)
#             fo_bh_df = pd.DataFrame(fo_bh_df) 
#             fo_bh_df = fo_bh_df[(fo_bh_df["OPTION_TYP"] == "XX")]
#             fo_bh_df = fo_bh_df[(fo_bh_df["EXPIRY_DT"] >= current_trading_day)]
#             fo_bh_df.sort_values(['EXPIRY_DT'],ascending=[True], inplace=True)
#             #fo_bh_df = fo_bh_df.iloc[:1]
#             fo_bh_df = fo_bh_df[fo_bh_df.groupby('SYMBOL')['EXPIRY_DT'].transform(lambda x: x.eq(x.min()))]
#             fo_bhav = pd.concat([fo_bh_df, fo_bhav])
#         except OSError as e:
#             print(e)
            

#     fo_bhav.sort_values(['SYMBOL', 'TIMESTAMP'], ascending=[True, False], inplace=True)
#     fo_bhav = fo_bhav[
#             ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH',
#             'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI','TIMESTAMP']]
#     fo_bhav.rename(columns={'SYMBOL': 'Name','TIMESTAMP': 'Date','OPEN_PRICE': 'FO_Open','HIGH_PRICE': 'FO_High', 'LOW_PRICE': 'FO_Low','CLOSE_PRICE': 'FO_Close','TTL_TRD_QNTY': 'FO_Volume','VAL_INLAKH':'Value','OPEN_INT':'OI','CHG_IN_OI':'Chg_OI' },inplace=True)
#     return fo_bhav

# fo_bhav = bhavcopy_fno_func()
# bhv_fo.range("a:i").value = None                          
# bhv_fo.range("a1").options(index=False).value = fo_bhav
# print(str(days_count)+" Days F&O Data Download")

# delv_data = pd.merge(eq_bhav, fo_bhav, on=['Name','Date'], how='outer')
# delv_data = delv_data[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume',
#          'Deliv_qty', 'Deliv_per', 'Value', 'OI', 'Chg_OI']]
# delv_dt.range("a1").options(index=False).value = delv_data
# print("EOD DATA &  F&O Data Merged")
delv_data = eq_bhav

stop_thread = False

script_list = [12533,	17598,	4037,	9158,	10181,	1628,	2181,	5142,	4064,	18520,	5204,	489,	14908,	1627,	18866,	17957,	8687,	357,	14111,	15332,	14853,	5264,	13598,	714,	15342,	17945,	9219,	18863,	5585,	14602]
stk_list = ['AAATECH',	'ASALCBR',	'AUSOMENT',	'BALAJITELE',	'BALKRISHNA',	'BECTORFOOD',	'BOSCHLTD',	'CIGNITITEC',	'CUBEXTUB',	'CUPID',	'GMDCLTD',	'ICEMAKE',	'KDDL',	'LINDEINDIA',	'MAZDA',	'MMTC',	'MUKTAARTS',	'NAM-INDIA',	'NETWORK18',	'NMDC',	'OMAXE',	'PDSL',	'SELAN',	'SHALBY',	'SHALPAINTS',	'SUVENPHAR',	'TPLPLASTEH',	'VERTOZ',	'VIJAYA',	'WEBELSOLAR']
#script_list = np.unique(flt_exc_eq['Scripcode'])
print("Total Stock : "+str(len(script_list)))

while True:
    #time.sleep(60)
    start_time = time.time()

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


    def five_df_new1_func(period,scp_lst,from_d,to_d):  
        five_df1 = pd.DataFrame()
        for a in scp_lst:
            try:
                print(a)
                dfg = client.historical_data('N', 'C', a, period, from_d, to_d)
                dfg['Scripcode'] = a
                dfg['Date'] = current_trading_day
                dfg["SMA_200"] = np.round((pta.sma(dfg["Close"], length=200,offset=0)),2)
                dfg["RSI_14"] = np.round((pta.rsi(dfg["Close"], length=14)),2)
                dfg1 = dfg.iloc[::-1]
                five_df1 = pd.concat([dfg1.iloc[:1], five_df1])
            except Exception as e:
                print(e)    
        five_df = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner')  

        five_df_new = five_df[five_df['Name'].isin(opt_li)]
        
        five_df_new['OPT'] = 'Y'
        five_df_new = five_df_new[['Name','OPT']]
        five_df_new1 = pd.merge(five_df, five_df_new, on=['Name'], how='outer')
        five_df_new1 = five_df_new1[['Name','Date', 'Open', 'High', 'Low','Close','Volume','SMA_200','RSI_14','Scripcode','OPT']]
        five_df_new1.sort_values(['Name'], ascending=[True], inplace=True)
        return five_df_new1  
    
    five_df_new11 = five_df_new1_func('1d',script_list,days_365, current_trading_day)
    
    Fiv_dt.range("a:i").value = None
    Fiv_dt.range("a1").options(index=False).value = five_df_new11
    
    end = time.time() - start_time
    
    # five_df_new1 = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout_vol_pri_mix.xlsx', sheet_name='Five_data')

    print("Five Paisa Data Download")

    data_eq1 = pd.concat([delv_data, five_df_new11])
    data_eq1.bfill(axis ='rows')
    data_eq1.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
    data_eq1.bfill(axis ='rows')
    sl.range("a1").options(index=False).value = data_eq1
    print("Data Analysis Started....")

    start_time3 = time.time()
    def final_data_func(scp_lst,data_fram):
        eq_data_pd = pd.DataFrame()
        for d in scp_lst:
            print(d)
            eq_data1 = data_fram[data_fram['Name'] == d]
            eq_data1.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)

            eq_data1['Time'] = datetime.now()

            eq_data1['200+'] = ((eq_data1['SMA_200']*1)/100)+(eq_data1['SMA_200'])
            eq_data1['200-'] = (eq_data1['SMA_200'])-((eq_data1['SMA_200']*1)/100)
            
            eq_data1['Delv_Chg'] = round(((eq_data1['Deliv_qty'] * 100) / (eq_data1['Deliv_qty'].shift(-1)) - 100), 2).fillna(0)      

            eq_data1['Price_Chg'] = round(((eq_data1['Close'] * 100) / (eq_data1['Close'].shift(-1)) - 100), 2).fillna(0)      
            
            eq_data1['Vol_Chg'] = round(((eq_data1['Volume'] * 100) / (eq_data1['Volume'].shift(-1)) - 100), 2).fillna(0)

            #eq_data1['OI_Chg'] = round(((eq_data1['OI']*100)/(eq_data1['OI'].shift(-1))-100),2)
            
            eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 1.5).shift(-5),"Deliv_brk", "")

            eq_data1['Price_break'] = np.where((eq_data1['Close'] > (eq_data1.High.rolling(5).max()).shift(-5)),
                                                'Pri_Up_brk',
                                                (np.where((eq_data1['Close'] < (eq_data1.Low.rolling(5).min()).shift(-5)),
                                                            'Pri_Dwn_brk', "")))
            eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                                "Vol_brk","")     
            #eq_data1['OI_break'] = np.where(eq_data1['OI'] > (eq_data1.OI.rolling(5).mean() * 1.5).shift(-5),"OI_brk", "")     
                                                                                                                  
            eq_data1['Vol_Price_break'] = np.where((eq_data1['Vol_break'] == "Vol_brk") &
                                                        (eq_data1['Price_break'] != ""), "Vol_Pri_break", "")
            eq_data1['Del_Vol_Pri_break'] = np.where((eq_data1['Deliv_break'].shift(-1) == "Deliv_brk") &
                                                    (eq_data1['Vol_Price_break'] == "Vol_Pri_break"), "Del_Vol_Pri_break", "")
            #eq_data1['OI_Vol_Pri_break'] = np.where((eq_data1['OI_break'].shift(-1) == "OI_brk") & (eq_data1['Vol_Price_break'] == "Vol_Pri_break"), "OI_Vol_Pri_break", "")
                                                    
            eq_data1['Sma_200_break'] = np.where((eq_data1['Close'] < eq_data1['200+']) & (eq_data1['Close'] > eq_data1['200-']),"Nr. 200_Sma Break","")
            
            eq_data1['O=H=L'] = np.where((eq_data1['Open'] == eq_data1['High']), 'Open_High',
                                            (np.where((eq_data1['Open'] == eq_data1['Low']), 'Open_Low', "")))
            eq_data1['Pattern'] = np.where((eq_data1['High'] < eq_data1['High'].shift(-1)) &
                                            (eq_data1['Low'] > eq_data1['Low'].shift(-1)), 'Inside_Bar',
                                            (np.where((eq_data1['Low'] < eq_data1['Low'].shift(-1)) &
                                                        (eq_data1['Close'] > eq_data1['High'].shift(-1)), 'Bullish',
                                                        (np.where((eq_data1['High'] > eq_data1['High'].shift(-1)) &
                                                                (eq_data1['Close'] < eq_data1['Low'].shift(-1)), 'Bearish',
                                                                "")))))
            eq_data1["Buy/Sell"] = np.where((eq_data1['Vol_break'] == "Vol_brk") & (eq_data1['Price_break'] == "Pri_Up_brk"),
                                            "BUY", np.where((eq_data1['Vol_break'] == "Vol_brk")
                                                & (eq_data1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                        
            eq_data1['R3'] = round(eq_data1['High'] + (
                    2 * (((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) - eq_data1['Low'])), 2).fillna(0)
            eq_data1['R2'] = round((((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) + eq_data1['High']) - \
                                    eq_data1['Low'], 2).fillna(0)
            eq_data1['R1'] = round(
                (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3)) - eq_data1['Low'], 2).fillna(0)
            eq_data1['Pivot'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3), 2).fillna(0)
            eq_data1['S1'] = round(
                (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3)) - eq_data1['High'], 2).fillna(0)
            eq_data1['S2'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) - (eq_data1['High'] -
                                                                                                       eq_data1['Low']),2).fillna(0)
                                   
            eq_data1['S3'] = round(eq_data1['Low'] - (
                    2 * (eq_data1['High'] - ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3))), 2)
            eq_data1['Mid_point'] = round(((eq_data1['High'] + eq_data1['Low']) / 2), 2).fillna(0)
            eq_data1['CPR'] = round(
                abs((round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3), 2)) - eq_data1['Mid_point']),
                2).fillna(0)
            eq_data1['CPR_SCAN'] = np.where((eq_data1['CPR'] < ((eq_data1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                            "")
            eq_data1['Candle'] = np.where(abs(eq_data1['Open'] - eq_data1['Close']) <
                                            abs(eq_data1['High'] - eq_data1['Low']) * 0.2, "DOZI",
                                            np.where(abs(eq_data1['Open'] - eq_data1['Close']) >
                                                    abs(eq_data1['High'] - eq_data1['Low']) * 0.7, "s", ""))
            eq_data_pd = pd.concat([eq_data1, eq_data_pd])
        eq_data_pd.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
        return eq_data_pd

    end3 = time.time() - start_time3

    eq_data_pd = final_data_func(stk_list,data_eq1)
    eq_data_pd.loc[:,['RSI_14','Scripcode']].fillna(method='ffill', inplace=True)
    #eq_data_pd['Scripcode'].fillna(method='ffill', inplace = True)
    fl_data.range("a:aj").value = None
    fl_data.range("a1").options(index=False).value = eq_data_pd
    # eq_data_pd = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout_vol_pri_mix.xlsx', sheet_name='Final_Data')

    print("Data Analysis Completed")    

    #eq_data_pd = pd.merge(eq_data_pd, future_dataframe, on=['Name'], how='outer')
    #eq_data_pd['concate'] = eq_data_pd['Deliv_break'] + eq_data_pd['Price_break'] + eq_data_pd['Vol_break'] + eq_data_pd['Del_Vol_Pri_break']

    # stat1 = eq_data_pd[(eq_data_pd["Vol_break"] == "Vol_brk") & (eq_data_pd["Price_break"] != "") & (eq_data_pd["Buy/Sell"] != "")]                 
    # exp.range("a1:ah2000").value = None
    # exp.range("a1").options(index=False).value = stat1


    orders_select1 = eq_data_pd[(eq_data_pd["Vol_Price_break"] == "Vol_Pri_break") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Date"] == current_trading_day) & (eq_data_pd["RSI_14"] > 70 )]
    orders_select1["Watchlist"] = "N" + ":" + "C" + ":" + orders_select1["Name"]
    print(orders_select1.tail(1))
    orders_select1 = orders_select1[['Name','Buy/Sell','Scripcode','Date','Time','Open','High','Low','Close','Volume','RSI_14','OPT','Delv_Chg','Price_Chg','Vol_Chg','Price_break','Deliv_break','O=H=L','Watchlist']]
    strategy1.range("a:r").value = None
    strategy1.range("a1").options(index=False).value = orders_select1

    # orders_select2 = eq_data_pd[(eq_data_pd["Vol_Price_break"] == "Vol_Price_break") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Date"] == current_trading_day) & (eq_data_pd["RSI_14"] > 70 )]
    # orders_select2["Watchlist"] = "N" + ":" + "C" + ":" + orders_select2["Name"]
    # orders_select2 = orders_select2[['Name','Buy/Sell','Scripcode','Date','Time','Open','High','Low','Close','Volume','RSI_14','OPT','Delv_Chg','Price_Chg','Vol_Chg','Price_break','Deliv_break','O=H=L','Watchlist']]
    # strategy2.range("a:r").value = None
    # strategy2.range("a1").options(index=False).value = orders_select2

    # orders_select3 = eq_data_pd[(eq_data_pd["Vol_Price_break"] == "Vol_Price_break") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Deliv_break"] != "") & (eq_data_pd["Close"] < 300)]
    # orders_select3["Watchlist"] = "N" + ":" + "C" + ":" + orders_select3["Name"]
    # orders_select3 = orders_select3[['Name','Buy/Sell','Scripcode','Date','Time','Open','High','Low','Close','Volume','RSI_14','OPT','Delv_Chg','Price_Chg','Vol_Chg','Price_break','Deliv_break','O=H=L','Watchlist']]
    # strategy3.range("a:r").value = None
    # strategy3.range("a1").options(index=False).value = orders_select3
     
    print("complete") 

    intraday_list = np.unique([int(i) for i in orders_select1['Scripcode']])

    def five_df_intra(scp_lst,period,from_d,to_d):  
        five_df1 = pd.DataFrame()
        for a in scp_lst:
            try:
                print(a)
                dfg = client.historical_data('N', 'C', a, period, from_d, to_d)
                dfg['Scripcode'] = a
                dfg['Date'] = current_trading_day 
                dfg["RSI_14"] = np.round((pta.rsi(dfg["Close"], length=14)),2)            
                five_df1 = pd.concat([dfg, five_df1])
            except Exception as e:
                print(e) 
                  
        five_df = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner')  
        
        #five_df_new = five_df[five_df['Name'].isin(opt_li)]
        #five_df_new['OPT'] = 'Y'
        #five_df_new = five_df_new[['Name','OPT']]
        #five_df_new1 = pd.merge(five_df, five_df_new, on=['Name'], how='outer')
        five_df = five_df[['Name','Datetime', 'Open', 'High', 'Low','Close','Volume','RSI_14','Scripcode']]
        five_df.sort_values(['Name','Datetime'], ascending=[True,False], inplace=True)
        return five_df  
    
    five_df_intra_new = five_df_intra(intraday_list,'5m',last_trading_day,current_trading_day)
    five_delv.range("a:i").value = None
    five_delv.range("a1").options(index=False).value = five_df_intra_new
    
    end = time.time() - start_time
    
    # five_df_new1 = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout_vol_pri_mix.xlsx', sheet_name='Five_data')

    print("Five Paisa Data Download New")


    # intraday_list = np.unique(orders_select1['Scripcode'])
    # five_df_new_intra = five_df_new1_func('5m',intraday_list,current_trading_day,current_trading_day)
    # five_delv.range("a1").options(index=False).value = five_df_new_intra

    intraday_sym_list = np.unique([str(i) for i in orders_select1['Name']])

    def final_data_func_intra(scp_lst,data_fram):
        eq_data_pd = pd.DataFrame()
        for d in scp_lst:
            print(d)
            eq_data1 = data_fram[data_fram['Name'] == d]
            eq_data1.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)

            eq_data1['TimeNow'] = datetime.now()

            # eq_data1['200+'] = ((eq_data1['SMA_200']*1)/100)+(eq_data1['SMA_200'])
            # eq_data1['200-'] = (eq_data1['SMA_200'])-((eq_data1['SMA_200']*1)/100)
            
            #eq_data1['Delv_Chg'] = round(((eq_data1['Deliv_qty'] * 100) / (eq_data1['Deliv_qty'].shift(-1)) - 100), 2).fillna(0)      

            eq_data1['Price_Chg'] = round(((eq_data1['Close'] * 100) / (eq_data1['Close'].shift(-1)) - 100), 2).fillna(0)      
            
            eq_data1['Vol_Chg'] = round(((eq_data1['Volume'] * 100) / (eq_data1['Volume'].shift(-1)) - 100), 2).fillna(0)

            #eq_data1['OI_Chg'] = round(((eq_data1['OI']*100)/(eq_data1['OI'].shift(-1))-100),2)
            
            #eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 1.5).shift(-5),"Deliv_brk", "")

            eq_data1['Price_break'] = np.where((eq_data1['Close'] > (eq_data1.High.rolling(5).max()).shift(-5)),
                                                'Pri_Up_brk',
                                                (np.where((eq_data1['Close'] < (eq_data1.Low.rolling(5).min()).shift(-5)),
                                                            'Pri_Dwn_brk', "")))
            eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                                "Vol_brk","")     
            #eq_data1['OI_break'] = np.where(eq_data1['OI'] > (eq_data1.OI.rolling(5).mean() * 1.5).shift(-5),"OI_brk", "")     
                                                                                                                  
            eq_data1['Vol_Price_break'] = np.where((eq_data1['Vol_break'] == "Vol_brk") &
                                                        (eq_data1['Price_break'] != ""), "Vol_Pri_break", "")
            #eq_data1['Del_Vol_Pri_break'] = np.where((eq_data1['Deliv_break'].shift(-1) == "Deliv_brk") &
            #                                        (eq_data1['Vol_Price_break'] == "Vol_Pri_break"), "Del_Vol_Pri_break", "")
            #eq_data1['OI_Vol_Pri_break'] = np.where((eq_data1['OI_break'].shift(-1) == "OI_brk") & (eq_data1['Vol_Price_break'] == "Vol_Pri_break"), "OI_Vol_Pri_break", "")
                                                    
            #eq_data1['Sma_200_break'] = np.where((eq_data1['Close'] < eq_data1['200+']) & (eq_data1['Close'] > eq_data1['200-']),"Nr. 200_Sma Break","")
            
            eq_data1['O=H=L'] = np.where((eq_data1['Open'] == eq_data1['High']), 'Open_High',
                                            (np.where((eq_data1['Open'] == eq_data1['Low']), 'Open_Low', "")))
            eq_data1['Pattern'] = np.where((eq_data1['High'] < eq_data1['High'].shift(-1)) &
                                            (eq_data1['Low'] > eq_data1['Low'].shift(-1)), 'Inside_Bar',
                                            (np.where((eq_data1['Low'] < eq_data1['Low'].shift(-1)) &
                                                        (eq_data1['Close'] > eq_data1['High'].shift(-1)), 'Bullish',
                                                        (np.where((eq_data1['High'] > eq_data1['High'].shift(-1)) &
                                                                (eq_data1['Close'] < eq_data1['Low'].shift(-1)), 'Bearish',
                                                                "")))))
            eq_data1["Buy/Sell"] = np.where((eq_data1['Vol_break'] == "Vol_brk") & (eq_data1['Price_break'] == "Pri_Up_brk"),
                                            "BUY", np.where((eq_data1['Vol_break'] == "Vol_brk")
                                                & (eq_data1['Price_break'] == "Pri_Dwn_brk") , "SELL", ""))
                                        
            eq_data1['R3'] = round(eq_data1['High'] + (
                    2 * (((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) - eq_data1['Low'])), 2).fillna(0)
            eq_data1['R2'] = round((((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) + eq_data1['High']) - \
                                    eq_data1['Low'], 2).fillna(0)
            eq_data1['R1'] = round(
                (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3)) - eq_data1['Low'], 2).fillna(0)
            eq_data1['Pivot'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3), 2).fillna(0)
            eq_data1['S1'] = round(
                (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3)) - eq_data1['High'], 2).fillna(0)
            eq_data1['S2'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3) - (eq_data1['High'] -
                                                                                                       eq_data1['Low']),2).fillna(0)
                                   
            eq_data1['S3'] = round(eq_data1['Low'] - (
                    2 * (eq_data1['High'] - ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3))), 2)
            eq_data1['Mid_point'] = round(((eq_data1['High'] + eq_data1['Low']) / 2), 2).fillna(0)
            eq_data1['CPR'] = round(
                abs((round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Close']) / 3), 2)) - eq_data1['Mid_point']),
                2).fillna(0)
            eq_data1['CPR_SCAN'] = np.where((eq_data1['CPR'] < ((eq_data1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                            "")
            eq_data1['Candle'] = np.where(abs(eq_data1['Open'] - eq_data1['Close']) <
                                            abs(eq_data1['High'] - eq_data1['Low']) * 0.2, "DOZI",
                                            np.where(abs(eq_data1['Open'] - eq_data1['Close']) >
                                                    abs(eq_data1['High'] - eq_data1['Low']) * 0.7, "s", ""))
            eq_data_pd = pd.concat([eq_data1, eq_data_pd])
        eq_data_pd.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
        return eq_data_pd
    eq_data_pd_intra = final_data_func_intra(intraday_sym_list,five_df_intra_new)
    eq_data_pd_intra = eq_data_pd_intra.astype({"Datetime": "datetime64"})
    # eq_data_pd_intra['Duration'] = eq_data_pd_intra['TimeNow'] - eq_data_pd_intra['Datetime']  
    # eq_data_pd_intra['duration_in_s'] = eq_data_pd_intra['Duration'].total_seconds()
    # eq_data_pd_intra['minutes'] = divmod(eq_data_pd_intra['duration_in_s'], 60)[0]
    eq_data_pd_intra['Minutes'] = eq_data_pd_intra['TimeNow']-eq_data_pd_intra["Datetime"]
    eq_data_pd_intra['Minutes'] = eq_data_pd_intra['Minutes']/np.timedelta64(1,'m')
    #eq_data_pd_intra['minutes'] = (eq_data_pd_intra['TimeNow']-eq_data_pd_intra["Datetime"]).astype('timedelta64[h]')
    by.range("a1").options(index=False).value = eq_data_pd_intra
    
    
    #eq_data_pd_intra["Date"] = eq_data_pd_intra["Datetime"].str.split(' ').str[0]
    #print(eq_data_pd_intra.head(2))
    # eq_data_pd_intra["Time"] = pd.to_datetime(eq_data_pd_intra["Datetime"])
    #eq_data_pd_intra["Time"] = eq_data_pd_intra["Datetime"].str.split('T').str[-1]
    
    #eq_data_pd_intra["Date"] = pd.to_datetime(eq_data_pd_intra["Datetime"])
    eq_data_pd_intra["Date"] = eq_data_pd_intra["Datetime"].dt.date
    print(eq_data_pd_intra.head(1))
    orders_select4 = eq_data_pd_intra[(eq_data_pd_intra["Vol_Price_break"] == "Vol_Pri_break") & (eq_data_pd_intra["Buy/Sell"] != "")  & (eq_data_pd_intra["Date"] == current_trading_day.date()) & (eq_data_pd_intra["RSI_14"] > 70 )]
    orders_select4["Watchlist"] = "N" + ":" + "C" + ":" + orders_select4["Name"]
    orders_select4 = orders_select4[['Name','Buy/Sell','Scripcode','Datetime','TimeNow','Minutes','Open','High','Low','Close','Volume','RSI_14','Price_Chg','Vol_Chg','O=H=L','Watchlist']]
    
    intraday_sym_list_new = np.unique([str(i) for i in orders_select4['Name']])
    print(intraday_sym_list_new)
    eq_data_pd5 = pd.DataFrame()
    for int_list in intraday_sym_list_new:
        eq_data5 = orders_select4[orders_select4['Name'] == int_list]
        print(eq_data5)
        eq_data5['Buy/Sell1'] = np.where(eq_data5['Close'] > (eq_data5['High']).shift(-1),"Buy_new","") 
        eq_data_pd5 = pd.concat([eq_data5, eq_data_pd5])                                        
        print(int_list)
    eq_data_pd5.sort_values(['Name', 'Datetime'], ascending=[True, False], inplace=True)
    strategy2.range("a:ae").value = None
    strategy2.range("a1").options(index=False).value = eq_data_pd5


    eq_data_pd5.sort_values(['Name', 'Datetime'], ascending=[True, True], inplace=True)
    orders_select5 = eq_data_pd5[(eq_data_pd5["Buy/Sell1"] == "Buy_new") ]


    intraday_sym_list_new1 = np.unique([str(i) for i in orders_select5['Name']])
    five_df_new1 = pd.DataFrame()
    for aa in intraday_sym_list_new1:
        eq_data5 = orders_select5[orders_select5['Name'] == aa]
        five_df_new1 = pd.concat([eq_data5.iloc[:1], five_df_new1])
    five_df_new1.sort_values(['Name',], ascending=[True], inplace=True)
    five_df_new1['Buy_At'] = round((five_df_new1['Close']),2)
    five_df_new1['Stop_Loss'] = round((five_df_new1['Buy_At'] - (five_df_new1['Buy_At']*2)/100),2)
    five_df_new1['Add_Till'] = ""
    
    five_df_new1['Target'] = round((((five_df_new1['Buy_At']*2)/100) + five_df_new1['Buy_At']),2)
    five_df_new1['Term'] = "SFT"
    
    five_df_new1 = five_df_new1[['Name','Scripcode','Stop_Loss','Add_Till','Buy_At','Target','Term','Datetime','TimeNow','Minutes']]
    strategy3.range("a:ae").value = None
    strategy3.range("a1").options(index=False).value = five_df_new1
    

    # posit = orders_select1
      
    # total_profit = Available_Cash/10
    # print(total_profit)
    # posit['Qty'] = np.round(((((Available_Cash*Exposer)/(len(posit['Name'])))/(posit['Close']))),0)
    # posit['Value'] = np.round((posit['Qty']*posit['Close']),2)
    # posit['Profit'] = np.round(((posit['Open']*2)/100),2)
    # posit['Loss'] = np.round(((posit['Open']*1)/100),2)
    # posit['Target'] = np.where((posit['Buy/Sell'] == "Buy"), np.round((posit['Open'] + posit['Profit']),2), np.where((posit['Buy/Sell'] == "Sell"), np.round((posit['Open'] - posit['Profit']),2), 0))
    # posit['StopLoss'] = np.where((posit['Buy/Sell'] == "Buy"), np.round((posit['Open'] - posit['Loss']),2), np.where((posit['Buy/Sell'] == "Sell"), np.round((posit['Open'] + posit['Loss']),2), 0))
    # posit['Buy_Status'] = np.where((posit['Buy/Sell'] == "Buy") & (posit['Close'] > posit['Target']), "TGT", np.where((posit['Buy/Sell'] == "Buy") & (posit['Close'] < posit['StopLoss']), "SL", np.where((posit['Buy/Sell'] == "Sell") & (posit['Close'] < posit['Target']), "TGT", np.where((posit['Buy/Sell'] == "Sell") & (posit['Close'] > posit['StopLoss']), "SL", "Pending"))))
    
    # position_read = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout_vol_pri_mix.xlsx', sheet_name='Position')
    # positt = pd.concat([posit, position_read])
    # positt.sort_values(['Name', 'Time'], ascending=[True, False], inplace=True)
    # pos.range("a:w").value = None
    # pos.range("a1").options(index=False).value = posit
    # print("Stocks Are Selected")

    end4 = time.time() - start_time
    print(f"Five Paisa Data Download Time: {end:.2f}s")
    # print(f"Live OI Data Download Time: {end1:.2f}s")
    # print(f"Live Delivery Data Download Time: {end2:.2f}s")
    print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Breakout_vol_pri_mix.xlsx")



