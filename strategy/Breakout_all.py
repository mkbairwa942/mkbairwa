#import yfinance as yf
#import ta
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
from zipfile import ZipFile
import requests
import itertools

from_d = (date.today() - timedelta(days=15))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

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

nse = NseIndia()

# pdf = nse.get_stock_info("RELIANCE", trade_info=True)["securityWiseDP"]
# print(pdf)

stk_li = np.unique(bhavcopy(last_trading_day)['SYMBOL'])

opt_li = pd.unique(bhavcopy_fno(last_trading_day)['SYMBOL'])

stk_list = stk_li

print("---- Data Process Started ----")

if not os.path.exists("Breakout_all.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Breakout_all.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Breakout_all.xlsx')
for i in ["Exchange","Filt_Exc","Bhavcopy","FO_Bhavcopy","Five_data","Delv_data","Five_Delv","Final_Data","Position","Strategy1","Strategy2","Strategy3","Buy","Sale",
           "Expiry","stats",]:
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
print(str(days_count)+" Days EOD Data Download")

def bhavcopy_fno_func():
    fo_bhav = pd.DataFrame()
    for i in trading_days:
        try:
            fo_bh_df = bhavcopy_fno(i)
            fo_bh_df = pd.DataFrame(fo_bh_df)
            fo_bh_df = fo_bh_df
            fo_bhav = pd.concat([fo_bh_df, fo_bhav])
        except OSError as e:
            print(e)
            

    fo_bhav.sort_values(['SYMBOL', 'TIMESTAMP'], ascending=[True, False], inplace=True)
    fo_bhav = fo_bhav[
            ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH',
            'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI','TIMESTAMP']]
    # fo_bhav.rename(columns={'SYMBOL': 'Name', 'DATE1': 'Date','OPEN_PRICE': 'Open','HIGH_PRICE': 'High', 'LOW_PRICE': 'Low',
    #                              'CLOSE_PRICE': 'Close','TTL_TRD_QNTY': 'Volume','DELIV_QTY': 'Deliv_qty','DELIV_PER': 'Deliv_per', },inplace=True)
    return fo_bhav

fo_bhav = bhavcopy_fno_func()
bhv_fo.range("a:i").value = None                          
bhv_fo.range("a1").options(index=False).value = fo_bhav
print(str(days_count)+" Days OI Data Download")

stop_thread = False

script_list = np.unique(flt_exc_eq['Scripcode'])

while True:
    start_time = time.time()

    def five_df_new1_func():       
        five_df1 = pd.DataFrame()
        for a in script_list:
            try:
                print(a)
                dfg = client.historical_data('N', 'C', a, '1d', current_trading_day, current_trading_day)
                dfg['Scripcode'] = a
                dfg['Date'] = current_trading_day
                five_df1 = pd.concat([dfg, five_df1])
            except Exception as e:
                print(e)    
        five_df = pd.merge(flt_exc_eq, five_df1, on=['Scripcode'], how='inner')  

        five_df_new = five_df[five_df['Name'].isin(opt_li)]
        five_df_new['OPT'] = 'Y'
        five_df_new = five_df_new[['Name','OPT']]
        five_df_new1 = pd.merge(five_df, five_df_new, on=['Name'], how='outer')
        five_df_new1 = five_df_new1[['Name','Date', 'Open', 'High', 'Low','Close','Volume','Scripcode','OPT']]
        five_df_new1.sort_values(['Name'], ascending=[True], inplace=True)
        return five_df_new1
    
    five_df_new1 = five_df_new1_func()
    Fiv_dt.range("a:i").value = None
    Fiv_dt.range("a1").options(index=False).value = five_df_new1
    
    end = time.time() - start_time
    
    # five_df_new1 = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout.xlsx', sheet_name='Five_data')

    print("Five Paisa Data Download")

    start_time1 = time.time()
    def oi_func():
        oi_data = None
        oi_data = pd.DataFrame()
        for b in opt_li:
            
            try:
                print(b)
                eq_df = []
                OI = nse.get_stock_fno_info(b, trade_info=False)['stocks'][0]['marketDeptOrderBook']['tradeInfo']['openInterest']
                Chg_OI = nse.get_stock_fno_info(b, trade_info=False)['stocks'][0]['marketDeptOrderBook']['tradeInfo']['changeinOpenInterest']
                P_Chg_OI = round((nse.get_stock_fno_info(b, trade_info=False)['stocks'][0]['marketDeptOrderBook']['tradeInfo']['pchangeinOpenInterest']),2)
                eq_df.append([OI,Chg_OI,P_Chg_OI])
                df33 = pd.DataFrame(eq_df)
                df33.columns = ['OI','Chg_OI', 'P_Chg_OI']
                df33['Name'] = b
                oi_data = pd.concat([df33, oi_data])
            except Exception as e:
                print(e)
        return oi_data

    oi_data = oi_func()  
    print("Live OI Data Download")
    end1 = time.time() - start_time1

    start_time2 = time.time()
    def dlvv_data_func():
        dlvv_data = None
        dlvv_data = pd.DataFrame()
        for c in stk_list:            
            try:
                print(c)
                eq_df = []
                Deliv_qty = nse.get_stock_info(c, trade_info=True)["securityWiseDP"]["deliveryQuantity"]
                Deliv_per = nse.get_stock_info(c, trade_info=True)["securityWiseDP"]["deliveryToTradedQuantity"]
                eq_df.append([Deliv_qty, Deliv_per])
                df3 = pd.DataFrame(eq_df)
                df3.columns = ['Deliv_qty', 'Deliv_per']
                df3['Name'] = c
                dlvv_data = pd.concat([df3, dlvv_data])
            except Exception as e:
                print(e)
        return dlvv_data
    end2 = time.time() - start_time2

    dlvv_data = dlvv_data_func()
    print("Live Delivery Data Download")
    dlv_data = pd.merge(dlvv_data, oi_data, on=['Name'], how='outer')
    dlv_data.sort_values(['Name'], ascending=[True], inplace=True)

    delv_dt.range("a:e").value = None
    delv_dt.range("a1").options(index=False).value = dlv_data
    print("Live Delivery & OI Data Merged")

    fiv_dlv = pd.merge(five_df_new1, dlv_data, on=['Name'], how='inner')
    fiv_dlv = fiv_dlv[['Name','Date', 'Open', 'High', 'Low','Close','Volume','Deliv_qty', 'Deliv_per','OI','Chg_OI','P_Chg_OI','Scripcode','OPT']]
    fiv_dlv.sort_values(['Name'], ascending=[True], inplace=True)
   
    five_delv.range("a:j").value = None
    five_delv.range("a1").options(index=False).value = fiv_dlv
    print("FivePaisa & Live Delivery Data Merged")

    #data_eq1 = pd.concat([eq_bhav, five_df_new1])
    data_eq1 = pd.concat([eq_bhav, fiv_dlv])
    data_eq1.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)

    print("EOD & Live Data Merged")
    print("Data Analysis Started....")

    start_time3 = time.time()
    def final_data_func():
        eq_data_pd = pd.DataFrame()
        for d in stk_list:
            print(d)
            eq_data1 = data_eq1[data_eq1['Name'] == d]
            eq_data1.sort_values(['Name', 'Date'], ascending=[True, False], inplace=True)
            eq_data1['Time'] = datetime.now()

            eq_data1['Delv_Chg'] = round(((eq_data1['Deliv_qty'] * 100) / (eq_data1['Deliv_qty'].shift(-1)) - 100), 2).fillna(0)      

            eq_data1['Price_Chg'] = round(((eq_data1['Close'] * 100) / (eq_data1['Close'].shift(-1)) - 100), 2).fillna(0)      
            
            eq_data1['Vol_Chg'] = round(((eq_data1['Volume'] * 100) / (eq_data1['Volume'].shift(-1)) - 100), 2).fillna(0)
    
            eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 1.5).shift(-5),
                                                "Deliv_brk", "")
            eq_data1['Price_break'] = np.where((eq_data1['Close'] > (eq_data1.High.rolling(5).max()).shift(-5)),
                                                'Pri_Up_brk',
                                                (np.where((eq_data1['Close'] < (eq_data1.Low.rolling(5).min()).shift(-5)),
                                                            'Pri_Dwn_brk', "")))
            eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 1.5).shift(-5),
                                                "Vol_brk","")                                        
            eq_data1['Deliv_Price_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
                                                        (eq_data1['Price_break'] != ""), "Del_Pri_Brk", "")
            eq_data1['Deliv_Vol_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
                                                    (eq_data1['Vol_break'] == "Vol_brk"), "Del_Vol_Brk", "")
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
                                            "Buy", np.where((eq_data1['Vol_break'] == "Vol_brk")
                                                & (eq_data1['Price_break'] == "Pri_Dwn_brk") , "Sell", ""))
                                        
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
                                                                                                        eq_data1['Low']),
                                    2).fillna(0)
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

    eq_data_pd = final_data_func()
    fl_data.range("a:aj").value = None
    fl_data.range("a1").options(index=False).value = eq_data_pd
    # eq_data_pd = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout.xlsx', sheet_name='Final_Data')

    print("Data Analysis Completed")    

    eq_data_pd = pd.merge(eq_data_pd, future_dataframe, on=['Name'], how='inner')
    eq_data_pd['concate'] = eq_data_pd['Deliv_break'] + eq_data_pd['Price_break'] + eq_data_pd['Vol_break'] + eq_data_pd['Deliv_Price_break'] +eq_data_pd['Deliv_Vol_break']

    stat = eq_data_pd[(eq_data_pd["concate"] != "") & (eq_data_pd["Date"] == current_trading_day)] 
    stat["Watchlist"] = "N" + ":" + "C" + ":" + stat["Name"]                
    st.range("a1:ah2000").value = None
    st.range("a1").options(index=False).value = stat

    stat1 = eq_data_pd[(eq_data_pd["Vol_break"] == "Vol_brk") & (eq_data_pd["Deliv_break"] != "") & (eq_data_pd["Price_break"] != "") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Date"] == current_trading_day)]                 
    exp.range("a1:ah2000").value = None
    exp.range("a1").options(index=False).value = stat1


    orders_select1 = eq_data_pd[(eq_data_pd["Vol_break"] == "Vol_brk") & (eq_data_pd["Price_break"] != "") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Date"] == current_trading_day) & (eq_data_pd["OPT"] == "Y")]
    # orders_select1 = pd.merge(orders_select1, future_dataframe, on=['Name'], how='inner')
    orders_select1["Watchlist"] = "N" + ":" + "C" + ":" + orders_select1["Name"]
    print(orders_select1.tail(1))
    orders_select1 = orders_select1[['Name','Scripcode_y','Date','Time','Open','High','Low','Close','OPT','LotSize','Delv_Chg','Price_Chg','Vol_Chg','Buy/Sell','Price_break','Deliv_break','O=H=L','Watchlist']]
    strategy1.range("a:r").value = None
    strategy1.range("a1").options(index=False).value = orders_select1

    orders_select2 = eq_data_pd[(eq_data_pd["Vol_break"] == "Vol_brk") & (eq_data_pd["Price_break"] != "") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Deliv_break"] != "") & (eq_data_pd["O=H=L"] != "") & (eq_data_pd["Date"] == current_trading_day) & (eq_data_pd["Close"] < 300)]
    orders_select2["Watchlist"] = "N" + ":" + "C" + ":" + orders_select2["Name"]
    orders_select2 = orders_select2[['Name','Scripcode_y','Date','Time','Open','High','Low','Close','OPT','LotSize','Delv_Chg','Price_Chg','Vol_Chg','Buy/Sell','Price_break','Deliv_break','O=H=L','Watchlist']]
    strategy2.range("a:r").value = None
    strategy2.range("a1").options(index=False).value = orders_select2

    orders_select3 = eq_data_pd[(eq_data_pd["Vol_break"] == "Vol_brk") & (eq_data_pd["Price_break"] != "") & (eq_data_pd["Buy/Sell"] != "") & (eq_data_pd["Deliv_break"] != "") & (eq_data_pd["Date"] == current_trading_day) & (eq_data_pd["Close"] < 300)]
    orders_select3["Watchlist"] = "N" + ":" + "C" + ":" + orders_select3["Name"]
    orders_select3 = orders_select3[['Name','Scripcode_y','Date','Time','Open','High','Low','Close','OPT','LotSize','Delv_Chg','Price_Chg','Vol_Chg','Buy/Sell','Price_break','Deliv_break','O=H=L','Watchlist']]
    strategy3.range("a:r").value = None
    strategy3.range("a1").options(index=False).value = orders_select3

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
    
    # position_read = pd.read_excel('E:\STOCK\Capital_vercel1\Breakout.xlsx', sheet_name='Position')
    # positt = pd.concat([posit, position_read])
    # positt.sort_values(['Name', 'Time'], ascending=[True, False], inplace=True)
    # pos.range("a:w").value = None
    # pos.range("a1").options(index=False).value = posit
    # print("Stocks Are Selected")

    end4 = time.time() - start_time
    print(f"Five Paisa Data Download Time: {end:.2f}s")
    print(f"Live OI Data Download Time: {end1:.2f}s")
    print(f"Live Delivery Data Download Time: {end2:.2f}s")
    print(f"Data Analysis Completed Time: {end3:.2f}s")
    print(f"Total Data Analysis Completed Time: {end4:.2f}s")

    wb.save("Breakout_all.xlsx")



