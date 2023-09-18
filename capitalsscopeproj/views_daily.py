#from django.shortcuts import render
import logging
#import mysql.connector
from jugaad_data.nse import NSELive
# from jugaad_data.holidays import holidays
from Dash_app.holidayss import holidays
import pandas as pd
import time
from datetime import date, datetime, timedelta
from dateutil.utils import today
from py5paisa import FivePaisaClient
import xlwings as xw
import os
from zipfile import ZipFile
import requests
from io import BytesIO
import numpy as np
import sqlalchemy
from time import sleep
import environ
from pathlib import Path

logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

nse = NSELive()

# env = Env()
# env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

env=environ.Env(
    DEBUG=(bool,False)
)

environ.Env.read_env(BASE_DIR / ".env")

cred = {
    "APP_NAME": env('APP_NAME'),
    "APP_SOURCE":env('APP_SOURCE'),
    "USER_ID":env('USER_ID'),
    "PASSWORD":env('PASSWORD'),
    "USER_KEY":env('USER_KEY'),
    "ENCRYPTION_KEY":env('ENCRYPTION_KEY'),
}

# user='mukeshbairwa942@gmail.com'
# pwd='navya@1234'
# dob='19860518'

#cred = env('cred')
#cred=env({'cred'})

user=env('user')
pwd=env('pwd')
dob=env('dob')

client = FivePaisaClient(email=user, passwd=pwd, dob=dob, cred=cred)
client.login()
#print(cred)


# mydb = mysql.connector.connect(host="5.183.11.143", user="capitalsscope", password="Jencocotfab@301",db='capitalsscope')
# mydb1 = mysql.connector.connect(host="5.183.11.143", user="mkbairwa942", password="vaa2829m", db='capitalsscope')
# mydb2 = mysql.connector.connect(host="5.183.11.143", user="root", password="Jencocotfab@301", db='capitalsscope')
# print(mydb)
# print(mydb1)
# print(mydb2)

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2023, 1, 23)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

df=client.historical_data('N','C',3045,'1d',from_d,to_d)
#print(df.head(5))

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()
print(dates)

live_idx = nse.live_index('SECURITIES IN F&O')
dff = live_idx['data']
df = pd.DataFrame(dff)
df = df.drop(["meta"], axis=1)
list = df.symbol


# sqlquery = "SELECT * FROM capitalsscope.bhavcopy;"
# sqlquery1 = "SELECT * FROM capitalsscope.cm22Feb2022bhav;"
# df = pd.read_sql(sql=sqlquery1, con=engine)
# print(df)

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
    bh_df = pd.DataFrame(bh_df)
    bh_df.to_sql(name="full_bhavcopy", con=engine, if_exists="append", index=False)
    print(bh_df.head(2))
    return bhav_eq


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
    fo_df = pd.DataFrame(fo_df)
    fo_df.to_sql(name="FO_bhavcopy", con=engine, if_exists="append", index=False)
    print(fo_df.head(2))
    return bhav_fo

def fii_openint_down(lastTradingDay):
    try:
        # print(day)
        dmyformat = datetime.strftime(lastTradingDay, '%d%m%Y')
        url = 'https://archives.nseindia.com/content/nsccl/fao_participant_oi_' + dmyformat + '.csv'
        # tablename = 'fii_dii_open_int'
        fii_op_int = pd.read_csv(url, skiprows=1)
        fii_op_int = fii_op_int.drop(fii_op_int.index[4])
        fii_op_int.insert(0, 'Date', lastTradingDay)
        fii_op_int['Date'] = pd.to_datetime(fii_op_int['Date'])
        fii_op_int.columns = [c.strip() for c in fii_op_int.columns.values.tolist()]
        fii_op_int.to_sql(name="FII_DII_Open_Int", con=engine, if_exists="append", index=False)
        print(fii_op_int.head(1))
        print("Data Successfully updated for " + lastTradingDay)
    except:
        pass
    return fii_op_int

def fii_vol_down(lastTradingDay):
    try:
        dmyformat = datetime.strftime(lastTradingDay, '%d%m%Y')
        url = 'https://archives.nseindia.com/content/nsccl/fao_participant_vol_' + dmyformat + '.csv'
        # tablename = 'fii_dii_volume'
        fii_op_vol = pd.read_csv(url, skiprows=1)
        fii_op_vol = fii_op_vol.drop(fii_op_vol.index[4])
        fii_op_vol.insert(0, 'Date', lastTradingDay)
        fii_op_vol['Date'] = pd.to_datetime(fii_op_vol['Date'])
        fii_op_vol.columns = [c.strip() for c in fii_op_vol.columns.values.tolist()]
        fii_op_vol.to_sql(name="FII_DII_Volume", con=engine, if_exists="append", index=False)
        print(fii_op_vol.head(1))
        print("Data Successfully updated for " + lastTradingDay)
    except:
        pass
    return fii_op_vol

def live_stock_new():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
        print(datetime.now())
        fo_pd = pd.DataFrame()
        eq_pd = pd.DataFrame()
        for j in list:
            eq_df = []
            delivqty = (nse.trade_info(j)['securityWiseDP']['deliveryQuantity'])
            delivper = (nse.trade_info(j)['securityWiseDP']['deliveryToTradedQuantity'])
            Time = time.strftime(r"%H:%M", time.localtime())
            Date = today()
            eq_df.append([delivqty, delivper, Time, Date])
            df3 = pd.DataFrame(eq_df)
            df3.columns = ['delivqty', 'delivper', 'Time', 'Date']
            df3['symbol'] = j
            eq_pd = pd.concat([df3, eq_pd])
            try:
                fo_df = []
                for quote in nse.stock_quote_fno(j)['stocks']:
                    ident = quote['metadata']['identifier']
                    expdte = quote['metadata']['expiryDate']
                    Fut_ltp = quote['metadata']['lastPrice']
                    Oi = quote['marketDeptOrderBook']['tradeInfo']['openInterest']
                    fo_df.append([Oi, ident, expdte, Fut_ltp])
                df1 = pd.DataFrame(fo_df)
                df1.columns = ['Open_int', 'Identify', 'Exp_date', 'Fut_ltp']
                df1['symbol'] = j
                df1['Inst'] = df1['Identify'].str[:3]
                df2 = df1[df1['Inst'].isin(['FUT'])]
                fo_data = df2[df2['Exp_date'] == nse.stock_quote_fno(j)['expiryDates'][0]]
                fo_pd = pd.concat([fo_data, fo_pd])
            except:
                pass
        eq_fo = pd.merge(fo_pd, eq_pd, on=['symbol'], how='left')
        eq_fo_data = pd.merge(df, eq_fo, on=['symbol'], how='left')

        eq_fo_data = eq_fo_data[['symbol', 'Date', 'Time', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'Fut_ltp',
                                'previousClose', 'change', 'pChange', 'totalTradedVolume', 'delivqty', 'delivper',
                                'Open_int', 'Exp_date', 'yearHigh', 'yearLow', 'nearWKH', 'nearWKL']]
        eq_fo_data.rename({'symbol': 'Symbol', 'open': 'Open', 'dayHigh': 'High', 'dayLow': 'Low', 'lastPrice': 'Closing',
                        'delivqty': 'Deliv_qty',
                        'delivper': 'Deliv_per', 'previousClose': 'Prv_close', 'totalTradedVolume': 'Volume'},
                        axis=1, inplace=True)
        cols = ['Open', 'High', 'Low', 'Closing', 'Fut_ltp', 'Prv_close', 'Open_int', 'change', 'pChange', 'Volume',
                'Deliv_qty', 'Deliv_per', 'yearHigh', 'yearLow', 'nearWKH', 'nearWKL']

        eq_fo_data[cols] = eq_fo_data[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        eq_fo_data.sort_values(['Symbol', 'Date', 'Time'], ascending=[True, False, False], inplace=True)
        eq_fo_data.to_sql(name="live_stock_new", con=engine, if_exists="append", index=False)
        print(datetime.now())
        print('live_stock_new')
        return eq_fo_data
    else:
        pass
        print('false')


# print(live_stock_new())

opt_symbol = "NIFTY"


def expirt_date():
    ep = []
    for ei in pd.DataFrame((client.get_expiry("N", opt_symbol))['Expiry'])['ExpiryDate']:
        left = ei[6:19]
        timestamp = pd.to_datetime(left, unit='ms')
        ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
        ep.append([ExpDate, left])

    ep1 = pd.DataFrame(ep)
    ep1.columns = ['ExpDate', 'DayFormat']
    expiry = (ep1['DayFormat'][0])
    return ep, expiry


# print(expirt_date())


def live_option_chain_nifty():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:

        eq_df = []
        Open = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['Open'])
        High = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['High'])
        Low = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['Low'])
        Close = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['Close'])
        Ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['LastTradedPrice'])
        Chg = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'NIFTY'}])['Data'][0]['NetChange'])
        Time = time.strftime(r"%H:%M", time.localtime())
        Date = today()
        eq_df.append([Date, Time, Open, High, Low, Close, Ltp, Chg])
        df3 = pd.DataFrame(eq_df)
        df3.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']
        df3['Symbol'] = 'NIFTY'
        df3 = df3[['Symbol', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']]
        df3.to_sql(name="live_Index", con=engine, if_exists="append", index=False)

        ep = []
        for ei in pd.DataFrame((client.get_expiry("N", "NIFTY"))['Expiry'])['ExpiryDate']:
            left = ei[6:19]
            timestamp = pd.to_datetime(left, unit='ms')
            ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
            ep.append([ExpDate, left])

        ep1 = pd.DataFrame(ep)
        ep1.columns = ['ExpDate', 'DayFormat']
        expiry = (ep1['DayFormat'][0])
        opt = pd.DataFrame(client.get_option_chain("N", "NIFTY", expiry)['Options'])
        CE = []
        PE = []
        for i in opt:
            ce_data = opt[opt['CPType'] == 'CE']
            ce_data = ce_data.sort_values(['StrikeRate'])
            CE.append(ce_data)

            pe_data = opt[opt['CPType'] == 'PE']
            pe_data = pe_data.sort_values(['StrikeRate'])
            PE.append(pe_data)
        option = pd.DataFrame(client.get_option_chain("N", "NIFTY", expiry)['Options'])
        # pe_values = pd.DataFrame(client.get_option_chain("N", opt_symbol, expiry)['Options'])
        ce_values1 = option[option['CPType'] == 'CE']
        pe_values1 = option[option['CPType'] == 'PE']
        ce_data = ce_values1.sort_values(['StrikeRate'])
        pe_data = pe_values1.sort_values(['StrikeRate'])
        df1 = pd.merge(ce_data, pe_data, on='StrikeRate')
        df1['Date'] = today()
        df1['Time'] = time.strftime(r"%H:%M", time.localtime())

        df1.rename(
            {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
            'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
            'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
            'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

        df1 = df1[['Date', 'Time', 'CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]

        df1.to_sql(name="live_option_chain_nifty", con=engine, if_exists="append", index=False)
        # df1.loc["Total"] = df1.sum()
        print('live_option_chain_nifty')
        return df1, ep1, expiry
    else:
        pass
        print('false')

def live_option_chain_bank_nifty():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:

        eq_df = []
        Open = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Open'])
        High = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['High'])
        Low = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Low'])
        Close = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Close'])
        Ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['LastTradedPrice'])
        Chg = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['NetChange'])
        Time = time.strftime(r"%H:%M", time.localtime())
        Date = today()
        eq_df.append([Date, Time, Open, High, Low, Close, Ltp, Chg])
        df3 = pd.DataFrame(eq_df)
        df3.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']
        df3['Symbol'] = 'BANKNIFTY'
        df3 = df3[['Symbol', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']]
        df3.to_sql(name="live_Index", con=engine, if_exists="append", index=False)

        ep = []
        for ei in pd.DataFrame((client.get_expiry("N", "BANKNIFTY"))['Expiry'])['ExpiryDate']:
            left = ei[6:19]
            timestamp = pd.to_datetime(left, unit='ms')
            ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
            ep.append([ExpDate, left])

        ep1 = pd.DataFrame(ep)
        ep1.columns = ['ExpDate', 'DayFormat']
        expiry = (ep1['DayFormat'][0])
        opt = pd.DataFrame(client.get_option_chain("N", "BANKNIFTY", expiry)['Options'])
        CE = []
        PE = []
        for i in opt:
            ce_data = opt[opt['CPType'] == 'CE']
            ce_data = ce_data.sort_values(['StrikeRate'])
            CE.append(ce_data)

            pe_data = opt[opt['CPType'] == 'PE']
            pe_data = pe_data.sort_values(['StrikeRate'])
            PE.append(pe_data)
        option = pd.DataFrame(client.get_option_chain("N", "BANKNIFTY", expiry)['Options'])
        # pe_values = pd.DataFrame(client.get_option_chain("N", opt_symbol, expiry)['Options'])
        ce_values1 = option[option['CPType'] == 'CE']
        pe_values1 = option[option['CPType'] == 'PE']
        ce_data = ce_values1.sort_values(['StrikeRate'])
        pe_data = pe_values1.sort_values(['StrikeRate'])
        df1 = pd.merge(ce_data, pe_data, on='StrikeRate')
        df1['Date'] = today()
        df1['Time'] = time.strftime(r"%H:%M", time.localtime())

        df1.rename(
            {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
            'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
            'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
            'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

        df1 = df1[['Date', 'Time', 'CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]

        df1.to_sql(name="live_option_chain_bank_nifty", con=engine, if_exists="append", index=False)
        # df1.loc["Total"] = df1.sum()
        print('live_option_chain_bank_nifty')
        return df1, ep1, expiry
    else:
        pass
        print('false')

while True:
    sleep(10)
    now = datetime.now()

    eod_time1 = now.replace(hour=12, minute=5, second=0, microsecond=0)
    eod_time2 = now.replace(hour=12, minute=7, second=0, microsecond=0)
    # print(eod_time1)
    # print(now)
    # print(eod_time2)
    intr_time1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
    intr_time2 = now.replace(hour=15, minute=35, second=0, microsecond=0)
    # print(intr_time1)
    # print(now)
    # print(intr_time2)
    de = date.today()
    # print(type(de))
    # print(type(lastTradingDay))
    # print(type(intraday))

    if now > eod_time1 and now < eod_time2 and (date.today() - timedelta(days=1)) == lastTradingDayy:
        # print("true")
        bhavcopy(lastTradingDay)
        # print(bhavcopy(lastTradingDay).head(3))
        bhavcopy_fno(lastTradingDay)
        # print(bhavcopy_fno(lastTradingDay).head(3))
        fii_openint_down(lastTradingDay)
        # print(fii_openint_down(lastTradingDay).head(3))
        fii_vol_down(lastTradingDay)
        # print(fii_vol_down(lastTradingDay).head(3))
        print("true")
    elif now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
        print("true")
        live_option_chain_bank_nifty()
        # print(live_option_chain())
        live_option_chain_nifty()
        # print(live_option_chain())
        live_stock_new()
        # print(live_stock_new())
    else:
        pass
        print('false')
