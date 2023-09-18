from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.shortcuts import render
import logging
import mysql.connector
from jugaad_data.nse import NSELive
from jugaad_data.holidays import holidays
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

# logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

nse = NSELive()

cred = {
    "APP_NAME": "5P57141743",
    "APP_SOURCE": "9997",
    "USER_ID": "5SP0ws0uCmc",
    "PASSWORD": "C0VIQHnMEpI",
    "USER_KEY": "BT5DqKIGqnKmHiZnzGXKZ2aBql4oYBRp",
    "ENCRYPTION_KEY": "tTEQPwp3Gfh2l3LWqDb2UC1sD0IFvzV5",
}

user = 'mukeshbairwa942@gmail.com'
pwd = 'navya@1234'
dob = '19860518'

client = FivePaisaClient(email=user, passwd=pwd, dob=dob, cred=cred)
client.login()

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
# to_d = date(2023, 1, 20)

now = datetime.now()

eod_time1 = now.replace(hour=12, minute=50, second=0, microsecond=0)
eod_time2 = now.replace(hour=12, minute=51, second=0, microsecond=0)

intr_time1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
intr_time2 = now.replace(hour=15, minute=35, second=0, microsecond=0)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

print(lastTradingDay)
print(intraday)


live_idx = nse.live_index('SECURITIES IN F&O')
dff = live_idx['data']
df = pd.DataFrame(dff)
df = df.drop(["meta"], axis=1)
list = df.symbol


@shared_task
def live_stock_new():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intraday:
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
        return eq_fo_data
    else:
        pass
        print('false')

opt_symbol = "NIFTY"

@shared_task
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

@shared_task
def live_option_chain_nifty():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intraday:
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
        return df1, ep1, expiry
    else:
        pass
        print('false')

@shared_task
def live_option_chain_bank_nifty():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intraday:
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
        return df1, ep1, expiry
    else:
        pass
        print('false')