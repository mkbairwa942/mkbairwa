from django.shortcuts import (render)
from datetime import date, datetime, timedelta
from jugaad_data.holidays import holidays
from zipfile import ZipFile
from io import BytesIO
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go
import sqlalchemy
#import mysql.connector
# from .task import *
from django.core.mail import send_mail
# from . import simpleexample
# from . import Eod_Market_Stock_New


# Create your views here.

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)
#print(to_days)

# df=client.historical_data('N','C',1660,'15m','2021-05-25','2021-06-16')

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()
#print(dates)

# nse = NSELive()

def index(request):
    send_mail_without()
    return HttpResponse("<h1>Hello, </h1>")

def send_mail_without():
    send_mail('CELERY WORK YEAH', "CELERY IS COOL",
        "mukeshkumarbairwa5686@gamil.com",
        ["mukeshbairwa942@gmail.com"],
        fail_silently=False
        )
    return None

def fnolist():
    # df = pd.read_csv("https://www1.nseindia.com/content/fo/fo_mktlots.csv")
    # return [x.strip(' ') for x in df.drop(df.index[3]).iloc[:,1].to_list()]

    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')

    nselist=['NIFTY','NIFTYIT','BANKNIFTY']

    i=0
    for x in range(i, len(positions['data'])):
        nselist=nselist+[positions['data'][x]['symbol']]

    return nselist

def bhavcopy(date):
    dmyformat = datetime.strftime(date, '%d%m%Y')
    ddd = datetime.strftime(date, '%d')
    MMM = datetime.strftime(date, '%b')#.upper()
    yyyy = datetime.strftime(date, '%Y')
    #url = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_' + dmyformat + '.csv'
    url = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22Full%20Bhavcopy%20and%20Security%20Deliverable%20data%22%2C%22type%22%3A%22daily-reports%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equities&mode=single'
    bhav_eq1 = pd.read_csv(url)
    bhav_eq1.columns = bhav_eq1.columns.str.strip()
    bhav_eq1 = bhav_eq1.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    bhav_eq1['DATE1'] = pd.to_datetime(bhav_eq1['DATE1'])
    bhav_eq = bhav_eq1[bhav_eq1['SERIES'] == 'EQ']
    bhav_eq['LAST_PRICE'] = bhav_eq['LAST_PRICE'].astype(float)
    bhav_eq['DELIV_QTY'] = bhav_eq['DELIV_QTY'].astype(float)
    bhav_eq['DELIV_PER'] = bhav_eq['DELIV_PER'].astype(float)
    df1 = bhav_eq.set_index(['SYMBOL', 'SERIES'])
    return df1

#nifty_list = pd.unique(bhavcopy(lastTradingDay)['SYMBOL'])

def bhavcopy_fno(date):
    try:
        dmyformat = datetime.strftime(date, '%d%b%Y').upper()
        ddd = datetime.strftime(date, '%d')
        MMM = datetime.strftime(date, '%b')#.upper()
        yyyy = datetime.strftime(date, '%Y')
        #url1 = 'https://archives.nseindia.com/content/historical/DERIVATIVES/' + yyyy + '/' + MMM + '/fo' + dmyformat + 'bhav.csv.zip'
        url1 = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22F%26O%20-%20Bhavcopy%20(fo.zip)%22%2C%22type%22%3A%22archives%22%2C%22category%22%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date='+ddd+'-'+MMM+'-'+yyyy+'&type=equity&mode=single'
        content = requests.get(url1)      
        if content.status_code == 200:
            zf = ZipFile(BytesIO(content.content))
            match = [s for s in zf.namelist() if ".csv" in s][0]
            bhav_fo = pd.read_csv(zf.open(match), low_memory=False)
            bhav_fo.columns = bhav_fo.columns.str.strip()
            bhav_fo = bhav_fo.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
            #bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT'])
            bhav_fo['EXPIRY_DT'] = pd.to_datetime(bhav_fo['EXPIRY_DT']).dt.date
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo = bhav_fo.drop(["Unnamed: 15"], axis=1)
            #print(bhav_fo.head(1))
        else:
            print("No Data Found of Date :- "+str(date))
    except Exception as e:
        print(e)
    return bhav_fo


nifty_list = pd.unique(bhavcopy_fno(lastTradingDay)['SYMBOL'])

def Eod_Market(request):
    return render(request, 'views_for/eod_market.html')



def Eod_Market_Stock(request):
    global data_fo

    engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

    eq_bhav = (f"SELECT distinct * FROM capitalsscope.full_bhavcopy where DATE1 between '{from_d}' and '{to_d}';")
    data_eq = pd.read_sql(sql=eq_bhav, con=engine)
    fo_bhav = (f"SELECT distinct * FROM capitalsscope.FO_bhavcopy where INSTRUMENT in ('FUTSTK','FUTIDX') and TIMESTAMP "
               f"between '{from_d}' and '{to_d}';")
    fo_bhav = pd.read_sql(sql=fo_bhav, con=engine)
    fo_bhav.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
    fo_bhav.set_index('SYMBOL', inplace=True)
    fo_bhav.dropna(axis=1, inplace=True)
    group_data_fo = fo_bhav.groupby(fo_bhav.index)
    current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
    fo_bhav['current_expiry_1'] = current_expiry_1
    data_fo = fo_bhav[fo_bhav['EXPIRY_DT'] == fo_bhav['current_expiry_1']]
    data_eq = data_eq[data_eq.SYMBOL.isin(nifty_list)]
    data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
    data_fo = data_fo.reset_index(level=0)
    data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
    data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')
    data_eq1 = data_eq1[
        ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
         'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
    data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
                             'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
                             'TTL_TRD_QNTY': 'Volume',
                             'DELIV_QTY': 'Deliv_qty', 'OPEN_INT': 'Open_int', 'DELIV_PER': 'Deliv_per', },
                    inplace=True)
    stk_list = np.unique(data_eq1['Symbol'])
    eq_data_pd = pd.DataFrame()
    for i in stk_list:
        eq_data1 = data_eq1[data_eq1['Symbol'] == i]
        eq_data1.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)
        eq_data1['Price_Chg'] = round(((eq_data1['Closing'] * 100) / (eq_data1['Closing'].shift(-1)) - 100), 2).fillna(
            0)
        eq_data1['OI_Chg'] = round(((eq_data1['Open_int'] * 100) / (eq_data1['Open_int'].shift(-1)) - 100), 2).fillna(0)
        eq_data1['Vol_Chg'] = round(((eq_data1['Volume'] * 100) / (eq_data1['Volume'].shift(-1)) - 100), 2).fillna(0)
        # eq_data1['Price_Chg1'] = eq_data1['Closing'].shift(-1)

        eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 2).shift(-5),
                                           "Deliv_brk", "")
        eq_data1['Price_break'] = np.where((eq_data1['Closing'] > (eq_data1.High.rolling(4).max()).shift(-4)),
                                           'Pri_Up_brk',
                                           (np.where((eq_data1['Closing'] < (eq_data1.Low.rolling(4).min()).shift(-4)),
                                                     'Pri_Dwn_brk', "")))
        # df['Signal'] = np.where((df['Close'] > df['SMA_200']), 'Signal', False)
        eq_data1['Open_int_break'] = np.where(
            eq_data1['Open_int'] > (eq_data1.Open_int.rolling(5).mean() * 2).shift(-5),
            "Open_int_brk", "")
        eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                         "Vol_brk",
                                         "")
        eq_data1['Deliv_Price_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
                                                 (eq_data1['Price_break'] != ""), "Del_Pri_Brk", "")
        eq_data1['Deliv_Open_int_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
                                                    (eq_data1['Open_int'] == "Open_int_brk"), "Del_Op_Int_Brk", "")
        eq_data1['Deliv_Vol_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
                                               (eq_data1['Vol_break'] == "Vol_brk"), "Del_Vol_Brk", "")
        eq_data1['O=H=L'] = np.where((eq_data1['Open'] == eq_data1['High']), 'Open_High',
                                     (np.where((eq_data1['Open'] == eq_data1['Low']), 'Open_Low', "")))
        eq_data1['Pattern'] = np.where((eq_data1['High'] < eq_data1['High'].shift(-1)) &
                                       (eq_data1['Low'] > eq_data1['Low'].shift(-1)), 'Inside_Bar',
                                       (np.where((eq_data1['Low'] < eq_data1['Low'].shift(-1)) &
                                                 (eq_data1['Closing'] > eq_data1['High'].shift(-1)), 'Bullish',
                                                 (np.where((eq_data1['High'] > eq_data1['High'].shift(-1)) &
                                                           (eq_data1['Closing'] < eq_data1['Low'].shift(-1)), 'Bearish',
                                                           "")))))
        eq_data1['R3'] = round(eq_data1['High'] + (
                2 * (((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - eq_data1['Low'])), 2).fillna(0)
        eq_data1['R2'] = round((((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) + eq_data1['High']) - \
                               eq_data1['Low'], 2).fillna(0)
        eq_data1['R1'] = round(
            (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['Low'], 2).fillna(0)
        eq_data1['Pivot'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2).fillna(0)
        eq_data1['S1'] = round(
            (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['High'], 2).fillna(0)
        eq_data1['S2'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - (eq_data1['High'] -
                                                                                                   eq_data1['Low']),
                               2).fillna(0)
        eq_data1['S3'] = round(eq_data1['Low'] - (
                2 * (eq_data1['High'] - ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3))), 2)
        eq_data1['Mid_point'] = round(((eq_data1['High'] + eq_data1['Low']) / 2), 2).fillna(0)
        eq_data1['CPR'] = round(
            abs((round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2)) - eq_data1['Mid_point']),
            2).fillna(0)
        # df['Signal'] = np.where((df['Close'] > df['SMA_200']), True, False)
        eq_data1['CPR_SCAN'] = np.where((eq_data1['CPR'] < ((eq_data1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN",
                                        "")
        eq_data1['Candle'] = np.where(abs(eq_data1['Open'] - eq_data1['Closing']) <
                                      abs(eq_data1['High'] - eq_data1['Low']) * 0.2, "DOZI",
                                      np.where(abs(eq_data1['Open'] - eq_data1['Closing']) >
                                               abs(eq_data1['High'] - eq_data1['Low']) * 0.7, "s", ""))
        eq_data_pd = pd.concat([eq_data1, eq_data_pd])
    eq_data_pd.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)

    plt.subplots()
    eq_data_pd1 = eq_data_pd[eq_data_pd['Symbol'].isin(['SBIN'])]
    Date1 = (eq_data_pd1['Date'])
    Close1 = (eq_data_pd1['Closing'])
    eq_data_pd2 = eq_data_pd[eq_data_pd['Symbol'].isin(['RELIANCE'])]
    Date2 = (eq_data_pd2['Date'])
    Close2 = (eq_data_pd2['Closing'])

    plt.plot(Date1, Close1, marker='o', linestyle='--', color='g', label='SBIN')
    plt.plot(Date2, Close2, marker='d', linestyle='-', color='r', label='RELIANCE')

    plt.xlabel('Date')
    plt.ylabel('Close')
    plt.title('SBIN vs RELIANCE')
    plt.legend(loc='lower right')

    plt.show()

    allData = []
    for i in range(eq_data_pd.shape[0]):
        temp = eq_data_pd.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    return render(request, 'views_for/eod_market_stock.html', {'context1': context1,'stk_list':stk_list})


# def Eod_Market_Stock1(request):

#     global data_fo
#     data_eq = pd.DataFrame()
#     data_fo = pd.DataFrame()

#     for day in dates:
#         try:
#             bhav_eq = bhavcopy(day)
#             data_eq = pd.concat([bhav_eq, data_eq])
#             bhav_fo = bhavcopy_fno(day)
#             bhav_fo = bhav_fo[bhav_fo['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
#             bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
#             bhav_fo.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
#             bhav_fo.set_index('SYMBOL', inplace=True)
#             bhav_fo.dropna(axis=1, inplace=True)
#             # data_fo.rename({'TIMESTAMP': 'date'}, axis=1, inplace=True)
#             group_data_fo = bhav_fo.groupby(bhav_fo.index)
#             current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
#             bhav_fo['current_expiry_1'] = current_expiry_1
#             bhav_fo = bhav_fo[bhav_fo['EXPIRY_DT'] == bhav_fo['current_expiry_1']]

#             data_fo = pd.concat([bhav_fo, data_fo])

#         except Exception as e:
            
#             print(f'erroe {e} for {date}')
#     data_eq = data_eq.reset_index(level=1)
#     data_eq = data_eq[data_eq.index.isin(nifty_list)]

#     # data_eq = data_eq.reset_index(level=1)
#     data_eq['DATE1'] = pd.to_datetime(data_eq['DATE1'])
#     data_eq['DELIV_QTY'] = data_eq['DELIV_QTY'].replace('-', 0).astype(float)
#     data_eq['DELIV_PER'] = data_eq['DELIV_PER'].replace('-', 0).astype(float)
#     # # data_eq.sort_values(by='DATE1')
#     # data = data.astype(float, errors='raise')
#     data_eq = data_eq.reset_index(level=0)
#     data_fo = data_fo.reset_index(level=0)
#     data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
#     data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
#     data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')

#     data_eq1 = data_eq1[
#         ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
#          'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
#     data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
#                              'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
#                              'TTL_TRD_QNTY': 'Volume',
#                              'DELIV_QTY': 'Deliv_qty', 'OPEN_INT': 'Open_int','DELIV_PER': 'Deliv_per',}, inplace=True)

#     stk_list = np.unique(data_eq1['Symbol'])
#     eq_data_pd = pd.DataFrame()
#     for i in stk_list:
#         eq_data1 = data_eq1[data_eq1['Symbol'] == i]
#         eq_data1.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)
#         eq_data1['Price_Chg'] = round(((eq_data1['Closing']*100)/(eq_data1['Closing'].shift(-1))-100),2).fillna(0)
#         eq_data1['OI_Chg'] = round(((eq_data1['Open_int']*100)/(eq_data1['Open_int'].shift(-1))-100),2).fillna(0)
#         eq_data1['Vol_Chg'] = round(((eq_data1['Volume']*100)/(eq_data1['Volume'].shift(-1))-100),2).fillna(0)
#         # eq_data1['Price_Chg1'] = eq_data1['Closing'].shift(-1)
        
#         eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 2).shift(-5),
#                                            "Deliv_brk", "")
#         eq_data1['Price_break'] = np.where((eq_data1['Closing'] > (eq_data1.High.rolling(4).max()).shift(-4)),
#                                            'Pri_Up_brk',
#                                            (np.where((eq_data1['Closing'] < (eq_data1.Low.rolling(4).min()).shift(-4)),
#                                                      'Pri_Dwn_brk', "")))                                  
#         # df['Signal'] = np.where((df['Close'] > df['SMA_200']), 'Signal', False)
#         eq_data1['Open_int_break'] = np.where(
#             eq_data1['Open_int'] > (eq_data1.Open_int.rolling(5).mean() * 2).shift(-5),
#             "Open_int_brk", "")
#         eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 2).shift(-5), "Vol_brk",
#                                          "") 
#         eq_data1['Deliv_Price_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
#                                                (eq_data1['Price_break'] != ""), "Del_Pri_Brk", "")   
#         eq_data1['Deliv_Open_int_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
#                                                (eq_data1['Open_int'] == "Open_int_brk"), "Del_Op_Int_Brk", "")                                                                                                                  
#         eq_data1['Deliv_Vol_break'] = np.where((eq_data1['Deliv_break'] == "Deliv_brk") &
#                                                (eq_data1['Vol_break'] == "Vol_brk"), "Del_Vol_Brk", "")                                                
#         eq_data1['O=H=L'] = np.where((eq_data1['Open'] == eq_data1['High']), 'Open_High',
#                                      (np.where((eq_data1['Open'] == eq_data1['Low']), 'Open_Low', "")))
#         eq_data1['Pattern'] = np.where((eq_data1['High'] < eq_data1['High'].shift(-1)) &
#                                        (eq_data1['Low'] > eq_data1['Low'].shift(-1)), 'Inside_Bar',
#                                        (np.where((eq_data1['Low'] < eq_data1['Low'].shift(-1)) &
#                                                  (eq_data1['Closing'] > eq_data1['High'].shift(-1)), 'Bullish',
#                                                  (np.where((eq_data1['High'] > eq_data1['High'].shift(-1)) &
#                                                            (eq_data1['Closing'] < eq_data1['Low'].shift(-1)), 'Bearish',
#                                                            "")))))

#         eq_data1['R3'] = round(eq_data1['High'] + (
#                 2 * (((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - eq_data1['Low'])), 2).fillna(0)
#         eq_data1['R2'] = round((((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) + eq_data1['High']) - \
#                                eq_data1['Low'], 2).fillna(0)
#         eq_data1['R1'] = round(
#             (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['Low'], 2).fillna(0)
#         eq_data1['Pivot'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2).fillna(0)
#         eq_data1['S1'] = round(
#             (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['High'], 2).fillna(0)
#         eq_data1['S2'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - (eq_data1['High'] -
#                                                                                                    eq_data1['Low']), 2).fillna(0)
#         eq_data1['S3'] = round(eq_data1['Low'] - (
#                 2 * (eq_data1['High'] - ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3))), 2)
#         eq_data1['Mid_point'] = round(((eq_data1['High'] + eq_data1['Low']) / 2), 2).fillna(0)
#         eq_data1['CPR'] = round(
#             abs((round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2)) - eq_data1['Mid_point']),
#             2).fillna(0)
#         # df['Signal'] = np.where((df['Close'] > df['SMA_200']), True, False)
#         eq_data1['CPR_SCAN'] = np.where((eq_data1['CPR'] < ((eq_data1.CPR.rolling(10).min()).shift(-10))), "CPR_SCAN", "")
#         eq_data1['Candle'] = np.where(abs(eq_data1['Open'] - eq_data1['Closing']) <
#                                       abs(eq_data1['High'] - eq_data1['Low']) * 0.2, "DOZI",
#                                       np.where(abs(eq_data1['Open'] - eq_data1['Closing']) >
#                                                abs(eq_data1['High'] - eq_data1['Low']) * 0.7, "s", ""))
#         eq_data_pd = pd.concat([eq_data1, eq_data_pd])
#         eq_data_pd.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)
#         # eq_data_pd.fillna(0)
#         #eq_data_pd.replace(np.NaN,0)
#         # print(eq_data_pd)
#     plt.subplots()
#     eq_data_pd1 = eq_data_pd[eq_data_pd['Symbol'].isin(['SBIN'])]
#     Date1 = (eq_data_pd1['Date'])
#     Close1 = (eq_data_pd1['Closing'])
#     eq_data_pd2 = eq_data_pd[eq_data_pd['Symbol'].isin(['RELIANCE'])]
#     Date2 = (eq_data_pd2['Date'])
#     Close2 = (eq_data_pd2['Closing'])

#     plt.plot(Date1, Close1, marker='o', linestyle='--', color='g', label='SBIN')
#     plt.plot(Date2, Close2, marker='d', linestyle='-', color='r', label='RELIANCE')

#     plt.xlabel('Date')
#     plt.ylabel('Close')
#     plt.title('SBIN vs RELIANCE')
#     plt.legend(loc='lower right')

#     plt.show()

#     allData = []
#     for i in range(eq_data_pd.shape[0]):
#         temp = eq_data_pd.iloc[i]
#         allData.append(dict(temp))
#     context1 = allData
#     # return context1

#     return render(request, 'views_for/eod_market_stock.html', {'context1': context1,'stk_list':stk_list})
#     # return eq_data_pd
#     # return render(request, 'views_for/eod_market_stock.html')


def Eod_Market_Indices(request):
    idx_list = ['Nifty 50', 'Nifty Next 50', 'Nifty 500', 'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'Nifty Auto',
                'Nifty Bank', 'Nifty Energy', 'Nifty Financial Services', 'Nifty FMCG', 'Nifty IT', 'Nifty Media',
                'Nifty Metal', 'Nifty Pharma', 'Nifty PSU Bank', 'Nifty Realty', 'Nifty Commodities',
                'Nifty Infrastructure', 'India VIX', 'Nifty Oil & Gas', 'Nifty Healthcare Index', 'Nifty Housing',
                'Nifty Consumer Durables', 'SECURITIES IN F&O', 'Nifty Private Bank']

    new_data = pd.DataFrame()
    for day in dates:
        try:
            dmyformat = datetime.strftime(day, '%d%m%Y')
            url = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dmyformat + '.csv'
            tablename = 'indices_close_all'
            data_eq = pd.read_csv(url)
            data_eq.rename(columns={'Index Name': 'Index', 'Index Date': 'New_Date', 'Open Index Value': 'Open',
                                    'High Index Value': 'High',
                                    'Closing Index Value': 'Closing', 'Low Index Value': 'Low',
                                    'Points Change': 'PChange',
                                    'Change(%)': 'Change_%',
                                    'Turnover (Rs. Cr.)': 'Turnover', 'Div Yield': 'Div_Yield'}, inplace=True)

            # data = data_eq.loc[data_eq.Index.isin(col)]
            data = data_eq[data_eq.Index.isin(idx_list)]
            data.insert(0, 'Date', day)
            data = data[['Index', 'Date', 'Open', 'High', 'Low', 'Closing', 'PChange', 'Change_%', 'Volume',
                         'Turnover', 'P/E', 'P/B', 'Div_Yield']]

            data['Date'] = pd.to_datetime(data['Date'])
            data['Open'] = data['Open'].replace('-', 0).astype(float)
            data['High'] = data['High'].replace('-', 0).astype(float)
            data['Low'] = data['Low'].replace('-', 0).astype(float)
            data['Closing'] = data['Closing'].replace('-', 0).astype(float)
            data['PChange'] = data['PChange'].replace('-', 0).astype(float)
            data['Change_%'] = data['Change_%'].astype(float)
            data['Volume'] = data['Volume'].replace('-', 0).astype(float)
            data['Turnover'] = data['Turnover'].replace('-', 0).astype(float)
            data['P/E'] = data['P/E'].replace('-', 0).astype(float)
            data['P/B'] = data['P/B'].replace('-', 0).astype(float)
            data['Div_Yield'] = data['Div_Yield'].replace('-', 0).astype(float)
            data.columns = [c.strip() for c in data.columns.values.tolist()]
            new_data = pd.concat([data, new_data])
            #print(new_data)


        except:
            pass
    column = (list(new_data.columns))
    new_data2 = pd.DataFrame()

    for i in idx_list:
        new_data1 = new_data[new_data['Index'] == i]
        new_data1.sort_values(['Index', 'Date'], ascending=[True, False], inplace=True)
        # new_data1['Vol_mean'] = (new_data1.Volume.rolling(5).mean() * 2).shift(-5)
        new_data1['Vol_break'] = np.where(new_data1['Volume'] > (new_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                          True,
                                          "")
        # new_data1['Close_mean'] = (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5)
        new_data1['Close_break'] = np.where(
            new_data1['Closing'] > (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5),
            True, "")
        # new_data1['maxx'] = (new_data1.High.rolling(4).max()).shift(-4)
        # new_data1['minn'] = (new_data1.Low.rolling(4).min()).shift(-4)
        new_data1['Price_break'] = np.where((new_data1['Closing'] > (new_data1.High.rolling(4).max()).shift(-4)),
                                            'Up_break',
                                            (np.where(
                                                (new_data1['Closing'] < (new_data1.Low.rolling(4).min()).shift(-4)),
                                                'Down_break', "")))
        new_data1['O=H=L'] = np.where((new_data1['Open'] == new_data1['High']), 'Open_High',
                                      (np.where((new_data1['Open'] == new_data1['Low']), 'Open_Low', "")))

        new_data1['Pattern'] = np.where((new_data1['High'] < new_data1['High'].shift(-1)) &
                                        (new_data1['Low'] > new_data1['Low'].shift(-1)), 'Inside_Bar',
                                        (np.where((new_data1['Low'] < new_data1['Low'].shift(-1)) &
                                                  (new_data1['Closing'] > new_data1['High'].shift(-1)), 'Bullish',
                                                  (np.where((new_data1['High'] > new_data1['High'].shift(-1)) &
                                                            (new_data1['Closing'] < new_data1['Low'].shift(-1)),
                                                            'Bearish',
                                                            "")))))
        new_data1['R3'] = round(new_data1['High'] + (
                2 * (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - new_data1['Low'])), 2)
        new_data1['R2'] = round(
            (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) + new_data1['High']) - \
            new_data1['Low'], 2)
        new_data1['R1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['Low'], 2)
        new_data1['Pivot'] = round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)
        new_data1['S1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['High'], 2)
        new_data1['S2'] = round(
            ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - (new_data1['High'] -
                                                                                   new_data1['Low']), 2)
        new_data1['S3'] = round(new_data1['Low'] - (
                2 * (new_data1['High'] - ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3))), 2)
        new_data1['Mid_point'] = round(((new_data1['High'] + new_data1['Low']) / 2), 2)
        new_data1['CPR'] = round(
            abs((round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)) - new_data1[
                'Mid_point']), 2)

        new_data1['CPR_SCAN'] = np.where((new_data1['CPR'] < ((new_data1.CPR.rolling(10).min()).shift(-10))), "YES", "")
        # new_data1['cpr_strategy'] = np.where((new_data1['High'] > new_data1['R1']),
        #                                      (new_data1['High'] < new_data1['R2']),
        #                                      (new_data1['Closing'] < new_data1['Pivot']),
        #                                      (new_data1['Low'] > new_data1['S1']), "Cpr_Bearish",
        #                                      np.where((new_data1['High'] < new_data1['R1']),
        #                                               (new_data1['Low'] < new_data1['S1']),
        #                                               (new_data1['Closing'] > new_data1['Pivot']),
        #                                               (new_data1['Low'] > new_data1['S2']), "Cpr_Bullish",))
        new_data1['Candle'] = np.where(abs(new_data1['Open'] - new_data1['Closing']) <
                                       abs(new_data1['High'] - new_data1['Low']) * 0.2, "DOZI",
                                       np.where(abs(new_data1['Open'] - new_data1['Closing']) >
                                                abs(new_data1['High'] - new_data1['Low']) * 0.7, "BIGBODY", ""))

        new_data2 = pd.concat([new_data1, new_data2])
    new_data2.rename(columns={'Change_%': 'Change_per', 'P/E': 'P_E', 'P/B': 'P_B'}, inplace=True)
    column = (list(new_data2.columns))

    # response = new_data2.to_json(orient='records')
    allData = []
    for i in range(new_data2.shape[0]):
        temp = new_data2.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    # return context1

    return render(request, 'views_for/eod_market_indices.html', {'context1': context1,'idx_list':idx_list,'column':column})


def Eod_Market_Futures(request):

    idx_list = ['Nifty 50', 'Nifty Next 50', 'Nifty 500', 'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'Nifty Auto',
                'Nifty Bank', 'Nifty Energy', 'Nifty Financial Services', 'Nifty FMCG', 'Nifty IT', 'Nifty Media',
                'Nifty Metal', 'Nifty Pharma', 'Nifty PSU Bank', 'Nifty Realty', 'Nifty Commodities',
                'Nifty Infrastructure', 'India VIX', 'Nifty Oil & Gas', 'Nifty Healthcare Index', 'Nifty Housing',
                'Nifty Consumer Durables', 'SECURITIES IN F&O', 'Nifty Private Bank']

    new_data = pd.DataFrame()
    for day in dates:
        try:
            dmyformat = datetime.strftime(day, '%d%m%Y')
            url = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dmyformat + '.csv'
            tablename = 'indices_close_all'
            data_eq = pd.read_csv(url)
            data_eq.rename(columns={'Index Name': 'Index', 'Index Date': 'New_Date', 'Open Index Value': 'Open',
                                    'High Index Value': 'High',
                                    'Closing Index Value': 'Closing', 'Low Index Value': 'Low',
                                    'Points Change': 'PChange',
                                    'Change(%)': 'Change_%',
                                    'Turnover (Rs. Cr.)': 'Turnover', 'Div Yield': 'Div_Yield'}, inplace=True)

            # data = data_eq.loc[data_eq.Index.isin(col)]
            data = data_eq[data_eq.Index.isin(idx_list)]
            data.insert(0, 'Date', day)
            data = data[['Index', 'Date', 'Open', 'High', 'Low', 'Closing', 'PChange', 'Change_%', 'Volume',
                         'Turnover', 'P/E', 'P/B', 'Div_Yield']]
   
            data['Date'] = pd.to_datetime(data['Date'])
            data['Open'] = data['Open'].replace('-', 0).astype(float)
            data['High'] = data['High'].replace('-', 0).astype(float)
            data['Low'] = data['Low'].replace('-', 0).astype(float)
            data['Closing'] = data['Closing'].replace('-', 0).astype(float)
            data['PChange'] = data['PChange'].replace('-', 0).astype(float)
            data['Change_%'] = data['Change_%'].astype(float)
            data['Volume'] = data['Volume'].replace('-', 0).astype(float)
            data['Turnover'] = data['Turnover'].replace('-', 0).astype(float)
            data['P/E'] = data['P/E'].replace('-', 0).astype(float)
            data['P/B'] = data['P/B'].replace('-', 0).astype(float)
            data['Div_Yield'] = data['Div_Yield'].replace('-', 0).astype(float)
            data.columns = [c.strip() for c in data.columns.values.tolist()]
            new_data = pd.concat([data, new_data])


        except:
            pass

    new_data2 = pd.DataFrame()

    for i in idx_list:
        new_data1 = new_data[new_data['Index'] == i]
        new_data1.sort_values(['Index', 'Date'], ascending=[True, False], inplace=True)
        # new_data1['Vol_mean'] = (new_data1.Volume.rolling(5).mean() * 2).shift(-5)
        new_data1['Vol_break'] = np.where(new_data1['Volume'] > (new_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                          True,
                                          "")
        # new_data1['Close_mean'] = (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5)
        new_data1['Close_break'] = np.where(
            new_data1['Closing'] > (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5),
            True, "")
        # new_data1['maxx'] = (new_data1.High.rolling(4).max()).shift(-4)
        # new_data1['minn'] = (new_data1.Low.rolling(4).min()).shift(-4)
        new_data1['Price_break'] = np.where((new_data1['Closing'] > (new_data1.High.rolling(4).max()).shift(-4)),
                                            'Up_break',
                                            (np.where(
                                                (new_data1['Closing'] < (new_data1.Low.rolling(4).min()).shift(-4)),
                                                'Down_break', "")))
        new_data1['O=H=L'] = np.where((new_data1['Open'] == new_data1['High']), 'Open_High',
                                      (np.where((new_data1['Open'] == new_data1['Low']), 'Open_Low', "")))

        new_data1['Pattern'] = np.where((new_data1['High'] < new_data1['High'].shift(-1)) &
                                        (new_data1['Low'] > new_data1['Low'].shift(-1)), 'Inside_Bar',
                                        (np.where((new_data1['Low'] < new_data1['Low'].shift(-1)) &
                                                  (new_data1['Closing'] > new_data1['High'].shift(-1)), 'Bullish',
                                                  (np.where((new_data1['High'] > new_data1['High'].shift(-1)) &
                                                            (new_data1['Closing'] < new_data1['Low'].shift(-1)),
                                                            'Bearish',
                                                            "")))))
        new_data1['R3'] = round(new_data1['High'] + (
                2 * (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - new_data1['Low'])), 2)
        new_data1['R2'] = round(
            (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) + new_data1['High']) - \
            new_data1['Low'], 2)
        new_data1['R1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['Low'], 2)
        new_data1['Pivot'] = round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)
        new_data1['S1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['High'], 2)
        new_data1['S2'] = round(
            ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - (new_data1['High'] -
                                                                                   new_data1['Low']), 2)
        new_data1['S3'] = round(new_data1['Low'] - (
                2 * (new_data1['High'] - ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3))), 2)
        new_data1['Mid_point'] = round(((new_data1['High'] + new_data1['Low']) / 2), 2)
        new_data1['CPR'] = round(
            abs((round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)) - new_data1[
                'Mid_point']), 2)

        new_data1['CPR_SCAN'] = np.where((new_data1['CPR'] < ((new_data1.CPR.rolling(10).min()).shift(-10))), "YES", "")
        # new_data1['cpr_strategy'] = np.where((new_data1['High'] > new_data1['R1']),
        #                                      (new_data1['High'] < new_data1['R2']),
        #                                      (new_data1['Closing'] < new_data1['Pivot']),
        #                                      (new_data1['Low'] > new_data1['S1']), "Cpr_Bearish",
        #                                      np.where((new_data1['High'] < new_data1['R1']),
        #                                               (new_data1['Low'] < new_data1['S1']),
        #                                               (new_data1['Closing'] > new_data1['Pivot']),
        #                                               (new_data1['Low'] > new_data1['S2']), "Cpr_Bullish",))
        new_data1['Candle'] = np.where(abs(new_data1['Open'] - new_data1['Closing']) <
                                       abs(new_data1['High'] - new_data1['Low']) * 0.2, "DOZI",
                                       np.where(abs(new_data1['Open'] - new_data1['Closing']) >
                                                abs(new_data1['High'] - new_data1['Low']) * 0.7, "BIGBODY", ""))

        new_data2 = pd.concat([new_data1, new_data2])
    new_data2.rename(columns={'Change_%': 'Change_per', 'P/E': 'P_E', 'P/B': 'P_B'}, inplace=True)
    column = (list(new_data2.columns))
    date = np.unique(new_data2['Date'])
    # response = new_data2.to_json(orient='records')
    allData = []
    for i in range(new_data2.shape[0]):
        temp = new_data2.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    # return context1

    # return render(request, 'views_for/eod_market_indices.html', {'context1': context1})
    return render (request, 'views_for/eod_market_futures.html', {'context1': context1,'idx_list':idx_list,'column':column,'date':date})


def Eod_Stock_Chart(request):
    
    global data_fo

    data_eq = pd.DataFrame()
    data_fo = pd.DataFrame()

    for day in dates:
        try:
            bhav_eq = bhavcopy(day)
            data_eq = pd.concat([bhav_eq, data_eq])
            bhav_fo = bhavcopy_fno(day)
            bhav_fo = bhav_fo[bhav_fo['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
            bhav_fo.set_index('SYMBOL', inplace=True)
            bhav_fo.dropna(axis=1, inplace=True)
            # data_fo.rename({'TIMESTAMP': 'date'}, axis=1, inplace=True)
            group_data_fo = bhav_fo.groupby(bhav_fo.index)
            current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
            bhav_fo['current_expiry_1'] = current_expiry_1
            bhav_fo = bhav_fo[bhav_fo['EXPIRY_DT'] == bhav_fo['current_expiry_1']]

            data_fo = pd.concat([bhav_fo, data_fo])

        except Exception as e:
            
            print(f'erroe {e} for {date}')

    data_eq = data_eq.reset_index(level=1)
    data_eq = data_eq[data_eq.index.isin(nifty_list)]

    # data_eq = data_eq.reset_index(level=1)
    data_eq['DATE1'] = pd.to_datetime(data_eq['DATE1'])
    data_eq['DELIV_QTY'] = data_eq['DELIV_QTY'].replace('-', 0).astype(float)
    data_eq['DELIV_PER'] = data_eq['DELIV_PER'].replace('-', 0).astype(float)
    # # data_eq.sort_values(by='DATE1')
    # data = data.astype(float, errors='raise')
    data_eq = data_eq.reset_index(level=0)
    data_fo = data_fo.reset_index(level=0)
    data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
    data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
    data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')

    data_eq1 = data_eq1[
        ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
         'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
    data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
                             'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
                             'TTL_TRD_QNTY': 'Volume',
                             'DELIV_QTY': 'Deliv_qty', 'DELIV_PER': 'Deliv_per', 'OPEN_INT': 'Open_int'}, inplace=True)
    data_eq1['Date'] = pd.to_datetime(data_eq1['Date']).astype(str)
    stk_list = np.unique(data_eq1['Symbol'])

    column = (list(data_eq1.columns))
    del column[:3]
 
    
    time = np.unique(data_eq1['Date'])
    date = pd.to_datetime(time,format='%Y-%m-%d')


    if request.method == 'POST':
        stock = request.POST.get('stock')
        field1 = request.POST.get('field1')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        print(from_date)
        print(to_date)
       
        data1 = data_eq1[data_eq1.Symbol == stock] 
        data = data1[(data1['Date'] > from_date) & (data1['Date'] <to_date)]   
        data.reset_index(drop=True, inplace=True)

        allData = []
        for i in range(data.shape[0]):
            temp = data.iloc[i]
            allData.append(dict(temp))
        context1 = allData
        data1 = data[field1] 
        
        
        return render(request, 'views_for/eod_stock_chart.html',{'stock':stock,'field1':field1,'idx_list':stk_list,'column':column,'date':date,'data1':data1,'context1':context1})    
    allData = []
    for i in range(data_eq1.shape[0]):
        temp = data_eq1.iloc[i]
        allData.append(dict(temp))
    context2 = allData

    return render(request, 'views_for/eod_stock_chart.html',{'idx_list':stk_list,'column':column,'date':date,'context2':context2})


def Eod_Indices_Chart (request):
    idx_list = ['Nifty 50', 'Nifty Next 50', 'Nifty 500', 'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'Nifty Auto',
                'Nifty Bank', 'Nifty Energy', 'Nifty Financial Services', 'Nifty FMCG', 'Nifty IT', 'Nifty Media',
                'Nifty Metal', 'Nifty Pharma', 'Nifty PSU Bank', 'Nifty Realty', 'Nifty Commodities',
                'Nifty Infrastructure', 'India VIX', 'Nifty Oil & Gas', 'Nifty Healthcare Index', 'Nifty Housing',
                'Nifty Consumer Durables', 'SECURITIES IN F&O', 'Nifty Private Bank']

    new_data = pd.DataFrame()
    for day in dates:
        try:
            dmyformat = datetime.strftime(day, '%d%m%Y')
            url = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dmyformat + '.csv'
            tablename = 'indices_close_all'
            data_eq = pd.read_csv(url)
            data_eq.rename(columns={'Index Name': 'Index', 'Index Date': 'New_Date', 'Open Index Value': 'Open',
                                    'High Index Value': 'High',
                                    'Closing Index Value': 'Closing', 'Low Index Value': 'Low',
                                    'Points Change': 'PChange',
                                    'Change(%)': 'Change_%',
                                    'Turnover (Rs. Cr.)': 'Turnover', 'Div Yield': 'Div_Yield'}, inplace=True)

            # data = data_eq.loc[data_eq.Index.isin(col)]
            data = data_eq[data_eq.Index.isin(idx_list)]
            data.insert(0, 'Date', day)
            data = data[['Index', 'Date', 'Open', 'High', 'Low', 'Closing', 'PChange', 'Change_%', 'Volume',
                         'Turnover', 'P/E', 'P/B', 'Div_Yield']]

            data['Date'] = pd.to_datetime(data['Date'])
            data['Open'] = data['Open'].replace('-', 0).astype(float)
            data['High'] = data['High'].replace('-', 0).astype(float)
            data['Low'] = data['Low'].replace('-', 0).astype(float)
            data['Closing'] = data['Closing'].replace('-', 0).astype(float)
            data['PChange'] = data['PChange'].replace('-', 0).astype(float)
            data['Change_%'] = data['Change_%'].astype(float)
            data['Volume'] = data['Volume'].replace('-', 0).astype(float)
            data['Turnover'] = data['Turnover'].replace('-', 0).astype(float)
            data['P/E'] = data['P/E'].replace('-', 0).astype(float)
            data['P/B'] = data['P/B'].replace('-', 0).astype(float)
            data['Div_Yield'] = data['Div_Yield'].replace('-', 0).astype(float)
            data.columns = [c.strip() for c in data.columns.values.tolist()]
            new_data = pd.concat([data, new_data])
    

        except:
            pass
    column = (list(new_data.columns))
    del column[:3]
    date = str(np.unique(new_data['Date']))

    if request.method == 'POST':
        stock = request.POST.get('stock')
        field = request.POST.get('field')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
          
        data = new_data[new_data.Index == stock]        
        data.reset_index(drop=True, inplace=True)

        allData = []
        for i in range(data.shape[0]):
            temp = data.iloc[i]
            allData.append(dict(temp))
        context1 = allData
        data1 = data[field] 
        
        return render(request, 'views_for/eod_indices_chart.html',{'stock':stock,'field':field,'idx_list':idx_list,'column':column,'data1':data1,'context1':context1})    
    allData = []
    for i in range(new_data.shape[0]):
        temp = new_data.iloc[i]
        allData.append(dict(temp))
    context2 = allData

    return render(request, 'views_for/eod_indices_chart.html',{'idx_list':idx_list,'column':column,'date':date,'context2':context2})

def welcome1(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30,35,25,45]

        trace = go.Scatter(
            x=x1,
            y=y1
        )

        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )

        fig=go.Figure(data=[trace],layout=layout)
        plot_div=plot(fig,output_type='div',include_plotlyjs=False)
        return plot_div
    context = {
        'plot1':scatter()
        }

    return render(request, 'views_for/welcome.html',{'context':context})

def live_option_chart(request):
    lot = 'NotMultiply'
    engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

    eq_bhav = (f"SELECT distinct * FROM capitalsscope.live_option_chain_nifty;")
    data_eq = pd.read_sql(sql=eq_bhav, con=engine)
    #data_eq = data_eq1[data_eq1.Date == intraday]
    data_eq['CE_Volume'] = np.where((lot == 'NotMultiply'), data_eq['CE_Volume']/50,data_eq['CE_Volume'])                                     
    data_eq['CE_Prev_OI'] = np.where((lot == 'NotMultiply'), data_eq['CE_Prev_OI']/50,data_eq['CE_Prev_OI']) 
    data_eq['CE_Chg_OI'] = np.where((lot == 'NotMultiply'), data_eq['CE_Chg_OI']/50,data_eq['CE_Chg_OI']) 
    data_eq['CE_OI'] = np.where((lot == 'NotMultiply'), data_eq['CE_OI']/50,data_eq['CE_OI']) 
    data_eq['PE_OI'] = np.where((lot == 'NotMultiply'), data_eq['PE_OI']/50,data_eq['PE_OI']) 
    data_eq['PE_Chg_OI'] = np.where((lot == 'NotMultiply'), data_eq['PE_Chg_OI']/50,data_eq['PE_Chg_OI']) 
    data_eq['PE_Prev_OI'] = np.where((lot == 'NotMultiply'), data_eq['PE_Prev_OI']/50,data_eq['PE_Prev_OI']) 
    data_eq['PE_Volume'] = np.where((lot == 'NotMultiply'), data_eq['PE_Volume']/50,data_eq['PE_Volume']) 

    TIME = np.unique(data_eq['Time'])
    time0 =  TIME[0]
    time1 = TIME[-1]
    # print(TIME1)
    # print(time1)

    data_eq2 = data_eq[data_eq.Time == time1]
    
    #print(TIME)
    CE_Volume_HIGH = pd.DataFrame()
    PE_Volume_HIGH = pd.DataFrame()
    CE_Chg_OI_HIGH = pd.DataFrame()
    PE_Chg_OI_HIGH = pd.DataFrame()

    for i in TIME:
        dataa = data_eq[data_eq.Time == i]
        Top_CE_Volume = dataa.sort_values(['CE_Volume'], ascending=[False]).iloc[:3]
        Top_PE_Volume = dataa.sort_values(['PE_Volume'], ascending=[False]).iloc[:3]
        Top_CE_Chg_OI = dataa.sort_values(['CE_Chg_OI'], ascending=[False]).iloc[:3]
        Top_PE_Chg_OI = dataa.sort_values(['PE_Chg_OI'], ascending=[False]).iloc[:3]

        CE_Volume_HIGH = pd.concat([Top_CE_Volume, CE_Volume_HIGH])
        PE_Volume_HIGH = pd.concat([Top_PE_Volume, PE_Volume_HIGH])
        CE_Chg_OI_HIGH = pd.concat([Top_CE_Chg_OI, CE_Chg_OI_HIGH])
        PE_Chg_OI_HIGH = pd.concat([Top_PE_Chg_OI, PE_Chg_OI_HIGH])


    data_eq5 = data_eq[data_eq.Date == intraday]
    

    TIME1 = np.unique(data_eq5['Time'])
    time1 = TIME1[-1]


    CE_Volume_HIGH0 = CE_Volume_HIGH[CE_Volume_HIGH.Date == intraday]
    CE_Volume_HIGH1 = CE_Volume_HIGH0[CE_Volume_HIGH0.Time == time1]

    
    PE_Volume_HIGH2 = data_eq[data_eq.Time == time1]
    PE_Volume_HIGH1 = PE_Volume_HIGH2[PE_Volume_HIGH2.Date == intraday]      
    CE_Chg_OI_HIGH2 = data_eq[data_eq.Time == time1]
    CE_Chg_OI_HIGH1 = CE_Chg_OI_HIGH2[CE_Chg_OI_HIGH2.Date == intraday]      
    PE_Chg_OI_HIGH2 = data_eq[data_eq.Time == time1]
    PE_Chg_OI_HIGH1 = PE_Chg_OI_HIGH2[PE_Chg_OI_HIGH2.Date == intraday]  
     

    # print(CE_Volume_HIGH0)
    # print(CE_Volume_HIGH1)

    StrikeRate = np.unique(data_eq['StrikeRate'])
    column = (data_eq.columns)

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        strike11 = request.POST.get('strike11')
        strike12 = request.POST.get('strike12')
        strike21 = request.POST.get('strike21')
        strike22 = request.POST.get('strike22')
        strike31 = request.POST.get('strike31')
        strike32 = request.POST.get('strike32')
        strike41 = request.POST.get('strike41')
        strike42 = request.POST.get('strike42')

        field11 = request.POST.get('field11')
        field12 = request.POST.get('field12')
        field21 = request.POST.get('field21')
        field22 = request.POST.get('field22')
        field31 = request.POST.get('field31')
        field32 = request.POST.get('field32')
        field41 = request.POST.get('field41')
        field42 = request.POST.get('field42')

        strike_data = data_eq[(data_eq['Date'] >= from_date) & (data_eq['Date'] <=to_date)]

        strike_data11 = strike_data[strike_data.StrikeRate == int(strike11)]       
        data11 = strike_data11[field11]
        allData = []
        for i in range(strike_data11.shape[0]):
            temp = strike_data11.iloc[i]
            allData.append(dict(temp))
        context11 = allData

        strike_data12 = strike_data[strike_data.StrikeRate == int(strike12)]       
        data12 = strike_data12[field12]
        allData = []
        for i in range(strike_data12.shape[0]):
            temp = strike_data12.iloc[i]
            allData.append(dict(temp))
        context12 = allData

        strike_data21 = strike_data[strike_data.StrikeRate == int(strike21)]       
        data21 = strike_data21[field21]
        allData = []
        for i in range(strike_data21.shape[0]):
            temp = strike_data21.iloc[i]
            allData.append(dict(temp))
        context21 = allData

        strike_data22 = strike_data[strike_data.StrikeRate == int(strike22)]       
        data22 = strike_data22[field22]
        allData = []
        for i in range(strike_data22.shape[0]):
            temp = strike_data22.iloc[i]
            allData.append(dict(temp))
        context22 = allData

        strike_data31 = strike_data[strike_data.StrikeRate == int(strike31)]       
        data31 = strike_data31[field31]
        allData = []
        for i in range(strike_data31.shape[0]):
            temp = strike_data31.iloc[i]
            allData.append(dict(temp))
        context31 = allData

        strike_data32 = strike_data[strike_data.StrikeRate == int(strike32)]       
        data32 = strike_data32[field32]
        allData = []
        for i in range(strike_data32.shape[0]):
            temp = strike_data32.iloc[i]
            allData.append(dict(temp))
        context32 = allData

        strike_data41 = strike_data[strike_data.StrikeRate == int(strike41)]       
        data41 = strike_data41[field41]
        allData = []
        for i in range(strike_data41.shape[0]):
            temp = strike_data41.iloc[i]
            allData.append(dict(temp))
        context41 = allData

        strike_data42 = strike_data[strike_data.StrikeRate == int(strike42)]       
        data42 = strike_data42[field42]
        allData = []
        for i in range(strike_data42.shape[0]):
            temp = strike_data42.iloc[i]
            allData.append(dict(temp))
        context42 = allData

        return render(request, 'views_for/live_option_chart.html',{
        'strike11':strike11,'strike12':strike12,'strike21':strike21,'strike22':strike22,'strike31':strike31,'strike32':strike32,'strike41':strike41,'strike42':strike42,
        'field11':field11,'field12':field12,'field21':field21,'field22':field22,'field31':field31,'field32':field32,'field41':field41,'field42':field42,
        'data11':data11,'data12':data12,'data21':data21,'data22':data22,'data31':data31,'data32':data32,'data41':data41,'data42':data42,
        'context11':context11,'context12':context12,'context21':context21,'context22':context22,'context31':context31,'context32':context32,'context41':context41,'context42':context42,
        'CE_Volume_HIGH1':CE_Volume_HIGH1,'PE_Volume_HIGH1':PE_Volume_HIGH1,'CE_Chg_OI_HIGH1':CE_Chg_OI_HIGH1,'PE_Chg_OI_HIGH1':PE_Chg_OI_HIGH1,
        'StrikeRate':StrikeRate,'column':column})                        

    allData = []
    for i in range(data_eq.shape[0]):
        temp = data_eq.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    return render(request, 'views_for/live_option_chart.html', {'StrikeRate': StrikeRate, 'column':column,'context1':context1})

    # 'Top_CE_Chg_OI':Top_CE_Chg_OI,'Top_PE_Chg_OI':Top_PE_Chg_OI,'Top_CE_Volume':Top_CE_Volume,'Top_PE_Volume':Top_PE_Volume})



def Chart(request):
     
    global data_fo

    data_eq = pd.DataFrame()
    data_fo = pd.DataFrame()

    for day in dates:
        try:
            bhav_eq = bhavcopy(day)
            data_eq = pd.concat([bhav_eq, data_eq])
            bhav_fo = bhavcopy_fno(day)            
            bhav_fo = bhav_fo[bhav_fo['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
            bhav_fo.set_index('SYMBOL', inplace=True)
            bhav_fo.dropna(axis=1, inplace=True)
            # data_fo.rename({'TIMESTAMP': 'date'}, axis=1, inplace=True)
            group_data_fo = bhav_fo.groupby(bhav_fo.index)
            current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
            bhav_fo['current_expiry_1'] = current_expiry_1
            bhav_fo = bhav_fo[bhav_fo['EXPIRY_DT'] == bhav_fo['current_expiry_1']]

            data_fo = pd.concat([bhav_fo, data_fo])

        except Exception as e:
            
            print(f'erroe {e} for {date}')

    data_eq = data_eq.reset_index(level=1)
    data_eq = data_eq[data_eq.index.isin(nifty_list)]


    # data_eq = data_eq.reset_index(level=1)
    data_eq['DATE1'] = pd.to_datetime(data_eq['DATE1'])
    data_eq['DELIV_QTY'] = data_eq['DELIV_QTY'].replace('-', 0).astype(float)
    data_eq['DELIV_PER'] = data_eq['DELIV_PER'].replace('-', 0).astype(float)
    # # data_eq.sort_values(by='DATE1')
    # data = data.astype(float, errors='raise')
    data_eq = data_eq.reset_index(level=0)
    data_fo = data_fo.reset_index(level=0)
    data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
    data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
    data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')

    data_eq1 = data_eq1[
        ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
         'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
    data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
                             'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
                             'TTL_TRD_QNTY': 'Volume',
                             'DELIV_QTY': 'Deliv_qty', 'DELIV_PER': 'Deliv_per', 'OPEN_INT': 'Open_int'}, inplace=True)
    # # data_eq1['Date']  = data_eq1['Date'].strftime('%m-%d')
    # data_eq1['Date'].apply(lambda x: x.strftime('%d-%m'))
    data_eq1['Date'] = pd.to_datetime(data_eq1['Date']).astype(str)
    # print(data_eq1.tail(20))
    stk_list = np.unique(data_eq1['Symbol'])

    column = (list(data_eq1.columns))
    del column[:3]  

    if request.method == 'POST':
        stock = request.POST.get('stock')
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        field3 = request.POST.get('field3')
        field4 = request.POST.get('field4')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        # print(stock)
        # print(field1)
        # print(field2)
        # print(field3)
        # print(field4)
        # print(from_date)
        # print(to_date)
       
        data1 = data_eq1[data_eq1.Symbol == stock] 
        data = data1[(data1['Date'] > from_date) & (data1['Date'] <to_date)] 
        #data['Date'] = pd.to_datetime(data['Date']).astype(str)  
        # data['Date'] = pd.to_datetime(data['Date']).dt.date

        
        #data['Date'] = data['Date'][8]+data['Date'][9]+"-"+data['Date'][5]+data['Date'][6]+"-"+data['Date'][0]+data['Date'][1]+data['Date'][2]+data['Date'][3]
        data.reset_index(drop=True, inplace=True)
        # print(data.info())


        allData = []
        for i in range(data.shape[0]):
            temp = data.iloc[i]
            allData.append(dict(temp))
        context1 = allData
        data1 = data[field1]
        data2 = data[field2]
        data3 = data[field3]
        data4 = data[field4] 
        
        
        return render(request, 'views_for/chart.html',{'stock':stock,'field1':field1,'field2':field2,'field3':field3,
        'field4':field4,'idx_list':stk_list,'column':column,'data1':data1,'data2':data2,'data3':data3,
        'data4':data4,'context1':context1})    
    allData = []
    for i in range(data_eq1.shape[0]):
        temp = data_eq1.iloc[i]
        allData.append(dict(temp))
    context2 = allData

    return render(request, 'views_for/chart.html',{'idx_list':stk_list,'column':column,'context2':context2})

def Chart1(request):
     
    global data_fo

    data_eq = pd.DataFrame()
    data_fo = pd.DataFrame()

    for day in dates:
        try:
            bhav_eq = bhavcopy(day)
            data_eq = pd.concat([bhav_eq, data_eq])
            bhav_fo = bhavcopy_fno(day)            
            bhav_fo = bhav_fo[bhav_fo['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
            bhav_fo.set_index('SYMBOL', inplace=True)
            bhav_fo.dropna(axis=1, inplace=True)
            # data_fo.rename({'TIMESTAMP': 'date'}, axis=1, inplace=True)
            group_data_fo = bhav_fo.groupby(bhav_fo.index)
            current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
            bhav_fo['current_expiry_1'] = current_expiry_1
            bhav_fo = bhav_fo[bhav_fo['EXPIRY_DT'] == bhav_fo['current_expiry_1']]

            data_fo = pd.concat([bhav_fo, data_fo])

        except Exception as e:
            
            print(f'erroe {e} for {date}')

    data_eq = data_eq.reset_index(level=1)
    data_eq = data_eq[data_eq.index.isin(nifty_list)]


    # data_eq = data_eq.reset_index(level=1)
    data_eq['DATE1'] = pd.to_datetime(data_eq['DATE1'])
    data_eq['DELIV_QTY'] = data_eq['DELIV_QTY'].replace('-', 0).astype(float)
    data_eq['DELIV_PER'] = data_eq['DELIV_PER'].replace('-', 0).astype(float)
    # # data_eq.sort_values(by='DATE1')
    # data = data.astype(float, errors='raise')
    data_eq = data_eq.reset_index(level=0)
    data_fo = data_fo.reset_index(level=0)
    data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
    data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
    data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')

    data_eq1 = data_eq1[
        ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
         'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
    data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
                             'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
                             'TTL_TRD_QNTY': 'Volume',
                             'DELIV_QTY': 'Deliv_qty', 'DELIV_PER': 'Deliv_per', 'OPEN_INT': 'Open_int'}, inplace=True)
    # # data_eq1['Date']  = data_eq1['Date'].strftime('%m-%d')
    # data_eq1['Date'].apply(lambda x: x.strftime('%d-%m'))
    data_eq1['Date'] = pd.to_datetime(data_eq1['Date']).astype(str)
    # print(data_eq1.tail(20))
    stk_list = np.unique(data_eq1['Symbol'])

    column = (list(data_eq1.columns))
    del column[:3]  

    if request.method == 'POST':
        stock = request.POST.get('stock')
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        field3 = request.POST.get('field3')
        field4 = request.POST.get('field4')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        # print(stock)
        # print(field1)
        # print(field2)
        # print(field3)
        # print(field4)
        # print(from_date)
        # print(to_date)
       
        data1 = data_eq1[data_eq1.Symbol == stock] 
        data = data1[(data1['Date'] > from_date) & (data1['Date'] <to_date)] 
        #data['Date'] = pd.to_datetime(data['Date']).astype(str)  
        # data['Date'] = pd.to_datetime(data['Date']).dt.date

        
        #data['Date'] = data['Date'][8]+data['Date'][9]+"-"+data['Date'][5]+data['Date'][6]+"-"+data['Date'][0]+data['Date'][1]+data['Date'][2]+data['Date'][3]
        data.reset_index(drop=True, inplace=True)
        # print(data.info())


        allData = []
        for i in range(data.shape[0]):
            temp = data.iloc[i]
            allData.append(dict(temp))
        context1 = allData
        data1 = data[field1]
        data2 = data[field2]
        data3 = data[field3]
        data4 = data[field4] 
        
        
        return render(request, 'views_for/chart1.html',{'stock':stock,'field1':field1,'field2':field2,'field3':field3,
        'field4':field4,'stk_list':stk_list,'column':column,'data1':data1,'data2':data2,'data3':data3,
        'data4':data4,'context1':context1})    
    allData = []
    for i in range(data_eq1.shape[0]):
        temp = data_eq1.iloc[i]
        allData.append(dict(temp))
    context2 = allData

    return render(request, 'views_for/chart1.html',{'stk_list':stk_list,'column':column,'context2':context2})

def Eod_Market_Options(request):
    return render(request, 'views_for/eod_market_options.html')


def Eod_Market_FII_DII(request):
    return render(request, 'views_for/eod_market_fii_dii.html')


def Intraday_Market(request):
    return render(request, 'views_for/intraday_market.html')


def Intraday_Market_Stock(request):
    global data_fo
    data_eq = pd.DataFrame()
    data_fo = pd.DataFrame()

    for day in dates:
        try:
            bhav_eq = bhavcopy(day)
            data_eq = pd.concat([bhav_eq, data_eq])
            bhav_fo = bhavcopy_fno(day)
            bhav_fo = bhav_fo[bhav_fo['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
            bhav_fo['TIMESTAMP'] = pd.to_datetime(bhav_fo['TIMESTAMP'])
            bhav_fo.rename(columns={'TIMESTAMP': 'DATE'}, inplace=True)
            bhav_fo.set_index('SYMBOL', inplace=True)
            bhav_fo.dropna(axis=1, inplace=True)
            # data_fo.rename({'TIMESTAMP': 'date'}, axis=1, inplace=True)
            group_data_fo = bhav_fo.groupby(bhav_fo.index)
            current_expiry_1 = group_data_fo['EXPIRY_DT'].min()
            bhav_fo['current_expiry_1'] = current_expiry_1
            bhav_fo = bhav_fo[bhav_fo['EXPIRY_DT'] == bhav_fo['current_expiry_1']]

            data_fo = pd.concat([bhav_fo, data_fo])

        except Exception as e:
            
            print(f'erroe {e} for {date}')
    data_eq = data_eq.reset_index(level=1)
    data_eq = data_eq[data_eq.index.isin(nifty_list)]

    # data_eq = data_eq.reset_index(level=1)
    data_eq['DATE1'] = pd.to_datetime(data_eq['DATE1'])
    data_eq['DELIV_QTY'] = data_eq['DELIV_QTY'].replace('-', 0).astype(float)
    data_eq['DELIV_PER'] = data_eq['DELIV_PER'].replace('-', 0).astype(float)
    # # data_eq.sort_values(by='DATE1')
    # data = data.astype(float, errors='raise')
    data_eq = data_eq.reset_index(level=0)
    data_fo = data_fo.reset_index(level=0)
    data_fo.sort_values(['SYMBOL', 'DATE'], ascending=[True, False], inplace=True)
    data_eq.rename(columns={'DATE1': 'DATE'}, inplace=True)
    data_eq1 = pd.merge(data_eq, data_fo, on=['SYMBOL', 'DATE'], how='inner')

    data_eq1 = data_eq1[
        ['SYMBOL', 'DATE', 'PREV_CLOSE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY',
         'DELIV_QTY', 'DELIV_PER', 'OPEN_INT']]
    data_eq1.rename(columns={'SYMBOL': 'Symbol', 'DATE': 'Date', 'PREV_CLOSE': 'Prev', 'OPEN_PRICE': 'Open',
                             'HIGH_PRICE': 'High', 'LOW_PRICE': 'Low', 'CLOSE_PRICE': 'Closing',
                             'TTL_TRD_QNTY': 'Volume',
                             'DELIV_QTY': 'Deliv_qty', 'OPEN_INT': 'Open_int','DELIV_PER': 'Deliv_per',}, inplace=True)

    stk_list = np.unique(data_eq1['Symbol'])
    eq_data_pd = pd.DataFrame()
    for i in stk_list:
        eq_data1 = data_eq1[data_eq1['Symbol'] == i]
        eq_data1.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)
        eq_data1['Price_Chg'] = round(((eq_data1['Closing']*100)/(eq_data1['Closing'].shift(-1))-100),2)
        eq_data1['OI_Chg'] = round(((eq_data1['Open_int']*100)/(eq_data1['Open_int'].shift(-1))-100),2)
        eq_data1['Vol_Chg'] = round(((eq_data1['Volume']*100)/(eq_data1['Volume'].shift(-1))-100),2)
        # eq_data1['Price_Chg1'] = eq_data1['Closing'].shift(-1)
        
        eq_data1['Deliv_break'] = np.where(eq_data1['Deliv_qty'] > (eq_data1.Deliv_qty.rolling(5).mean() * 2).shift(-5),
                                           True, "")
        eq_data1['Price_break'] = np.where((eq_data1['Closing'] > (eq_data1.High.rolling(4).max()).shift(-4)),
                                           'Up_break',
                                           (np.where((eq_data1['Closing'] < (eq_data1.Low.rolling(4).min()).shift(-4)),
                                                     'Down_break', "")))                                   
        # df['Signal'] = np.where((df['Close'] > df['SMA_200']), True, False)
        eq_data1['Open_int_break'] = np.where(
            eq_data1['Open_int'] > (eq_data1.Open_int.rolling(5).mean() * 2).shift(-5),
            True, "")
        eq_data1['Vol_break'] = np.where(eq_data1['Volume'] > (eq_data1.Volume.rolling(5).mean() * 2).shift(-5), True,
                                         "") 
        eq_data1['Deliv_Price_break'] = np.where((eq_data1['Deliv_break'] == "True") &
                                               (eq_data1['Price_break'] != ""), True, "")   
        eq_data1['Deliv_Open_int_break'] = np.where((eq_data1['Deliv_break'] == "True") &
                                               (eq_data1['Open_int'] == "True"), True, "")                                                                                                                   
        eq_data1['Deliv_Vol_break'] = np.where((eq_data1['Deliv_break'] == "True") &
                                               (eq_data1['Vol_break'] == "True"), True, "")                                                
        eq_data1['O=H=L'] = np.where((eq_data1['Open'] == eq_data1['High']), 'Open_High',
                                     (np.where((eq_data1['Open'] == eq_data1['Low']), 'Open_Low', "")))
        eq_data1['Pattern'] = np.where((eq_data1['High'] < eq_data1['High'].shift(-1)) &
                                       (eq_data1['Low'] > eq_data1['Low'].shift(-1)), 'Inside_Bar',
                                       (np.where((eq_data1['Low'] < eq_data1['Low'].shift(-1)) &
                                                 (eq_data1['Closing'] > eq_data1['High'].shift(-1)), 'Bullish',
                                                 (np.where((eq_data1['High'] > eq_data1['High'].shift(-1)) &
                                                           (eq_data1['Closing'] < eq_data1['Low'].shift(-1)), 'Bearish',
                                                           "")))))

        eq_data1['R3'] = round(eq_data1['High'] + (
                2 * (((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - eq_data1['Low'])), 2)
        eq_data1['R2'] = round((((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) + eq_data1['High']) - \
                               eq_data1['Low'], 2)
        eq_data1['R1'] = round(
            (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['Low'], 2)
        eq_data1['Pivot'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2)
        eq_data1['S1'] = round(
            (2 * ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3)) - eq_data1['High'], 2)
        eq_data1['S2'] = round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3) - (eq_data1['High'] -
                                                                                                   eq_data1['Low']), 2)
        eq_data1['S3'] = round(eq_data1['Low'] - (
                2 * (eq_data1['High'] - ((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3))), 2)
        eq_data1['Mid_point'] = round(((eq_data1['High'] + eq_data1['Low']) / 2), 2)
        eq_data1['CPR'] = round(
            abs((round(((eq_data1['High'] + eq_data1['Low'] + eq_data1['Closing']) / 3), 2)) - eq_data1['Mid_point']),
            2)
        # df['Signal'] = np.where((df['Close'] > df['SMA_200']), True, False)
        eq_data1['CPR_SCAN'] = np.where((eq_data1['CPR'] < ((eq_data1.CPR.rolling(10).min()).shift(-10))), "YES", "")
        eq_data1['Candle'] = np.where(abs(eq_data1['Open'] - eq_data1['Closing']) <
                                      abs(eq_data1['High'] - eq_data1['Low']) * 0.2, "DOZI",
                                      np.where(abs(eq_data1['Open'] - eq_data1['Closing']) >
                                               abs(eq_data1['High'] - eq_data1['Low']) * 0.7, "BIGBODY", ""))
        eq_data_pd = pd.concat([eq_data1, eq_data_pd])
        eq_data_pd.sort_values(['Symbol', 'Date'], ascending=[True, False], inplace=True)
        
    allData = []
    for i in range(eq_data_pd.shape[0]):
        temp = eq_data_pd.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    # return context1

    return render(request, 'views_for/intraday_market_stock.html', {'context1': context1,'stk_list':stk_list})
    # return eq_data_pd
    # return render(request, 'views_for/eod_market_stock.html')

    # return render(request, 'views_for/intraday_market_stock.html', {'context1': context1,'stk_list':stk_list,'column':column})
    # return eq_data_pd
    # return render(request, 'views_for/eod_market_stock.html')

    


def Intraday_Market_Indices(request):
    idx_list = ['Nifty 50', 'Nifty Next 50', 'Nifty 500', 'NIFTY Midcap 100', 'NIFTY Smallcap 100', 'Nifty Auto',
                'Nifty Bank', 'Nifty Energy', 'Nifty Financial Services', 'Nifty FMCG', 'Nifty IT', 'Nifty Media',
                'Nifty Metal', 'Nifty Pharma', 'Nifty PSU Bank', 'Nifty Realty', 'Nifty Commodities',
                'Nifty Infrastructure', 'India VIX', 'Nifty Oil & Gas', 'Nifty Healthcare Index', 'Nifty Housing',
                'Nifty Consumer Durables', 'SECURITIES IN F&O', 'Nifty Private Bank']

    new_data = pd.DataFrame()
    for day in dates:
        try:
            dmyformat = datetime.strftime(day, '%d%m%Y')
            url = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dmyformat + '.csv'
            tablename = 'indices_close_all'
            data_eq = pd.read_csv(url)
            data_eq.rename(columns={'Index Name': 'Index', 'Index Date': 'New_Date', 'Open Index Value': 'Open',
                                    'High Index Value': 'High',
                                    'Closing Index Value': 'Closing', 'Low Index Value': 'Low',
                                    'Points Change': 'PChange',
                                    'Change(%)': 'Change_%',
                                    'Turnover (Rs. Cr.)': 'Turnover', 'Div Yield': 'Div_Yield'}, inplace=True)

            # data = data_eq.loc[data_eq.Index.isin(col)]
            data = data_eq[data_eq.Index.isin(idx_list)]
            data.insert(0, 'Date', day)
            data = data[['Index', 'Date', 'Open', 'High', 'Low', 'Closing', 'PChange', 'Change_%', 'Volume',
                         'Turnover', 'P/E', 'P/B', 'Div_Yield']]

            data['Date'] = pd.to_datetime(data['Date'])
            data['Open'] = data['Open'].replace('-', 0).astype(float)
            data['High'] = data['High'].replace('-', 0).astype(float)
            data['Low'] = data['Low'].replace('-', 0).astype(float)
            data['Closing'] = data['Closing'].replace('-', 0).astype(float)
            data['PChange'] = data['PChange'].replace('-', 0).astype(float)
            data['Change_%'] = data['Change_%'].astype(float)
            data['Volume'] = data['Volume'].replace('-', 0).astype(float)
            data['Turnover'] = data['Turnover'].replace('-', 0).astype(float)
            data['P/E'] = data['P/E'].replace('-', 0).astype(float)
            data['P/B'] = data['P/B'].replace('-', 0).astype(float)
            data['Div_Yield'] = data['Div_Yield'].replace('-', 0).astype(float)
            data.columns = [c.strip() for c in data.columns.values.tolist()]
            new_data = pd.concat([data, new_data])


        except:
            pass
    column = (list(new_data.columns))
    new_data2 = pd.DataFrame()

    for i in idx_list:
        new_data1 = new_data[new_data['Index'] == i]
        new_data1.sort_values(['Index', 'Date'], ascending=[True, False], inplace=True)
        # new_data1['Vol_mean'] = (new_data1.Volume.rolling(5).mean() * 2).shift(-5)
        new_data1['Vol_break'] = np.where(new_data1['Volume'] > (new_data1.Volume.rolling(5).mean() * 2).shift(-5),
                                          True,
                                          "")
        # new_data1['Close_mean'] = (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5)
        new_data1['Close_break'] = np.where(
            new_data1['Closing'] > (new_data1.Closing.rolling(5).mean() * 1.1).shift(-5),
            True, "")
        # new_data1['maxx'] = (new_data1.High.rolling(4).max()).shift(-4)
        # new_data1['minn'] = (new_data1.Low.rolling(4).min()).shift(-4)
        new_data1['Price_break'] = np.where((new_data1['Closing'] > (new_data1.High.rolling(4).max()).shift(-4)),
                                            'Up_break',
                                            (np.where(
                                                (new_data1['Closing'] < (new_data1.Low.rolling(4).min()).shift(-4)),
                                                'Down_break', "")))
        new_data1['O=H=L'] = np.where((new_data1['Open'] == new_data1['High']), 'Open_High',
                                      (np.where((new_data1['Open'] == new_data1['Low']), 'Open_Low', "")))

        new_data1['Pattern'] = np.where((new_data1['High'] < new_data1['High'].shift(-1)) &
                                        (new_data1['Low'] > new_data1['Low'].shift(-1)), 'Inside_Bar',
                                        (np.where((new_data1['Low'] < new_data1['Low'].shift(-1)) &
                                                  (new_data1['Closing'] > new_data1['High'].shift(-1)), 'Bullish',
                                                  (np.where((new_data1['High'] > new_data1['High'].shift(-1)) &
                                                            (new_data1['Closing'] < new_data1['Low'].shift(-1)),
                                                            'Bearish',
                                                            "")))))
        new_data1['R3'] = round(new_data1['High'] + (
                2 * (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - new_data1['Low'])), 2)
        new_data1['R2'] = round(
            (((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) + new_data1['High']) - \
            new_data1['Low'], 2)
        new_data1['R1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['Low'], 2)
        new_data1['Pivot'] = round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)
        new_data1['S1'] = round(
            (2 * ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3)) - new_data1['High'], 2)
        new_data1['S2'] = round(
            ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3) - (new_data1['High'] -
                                                                                   new_data1['Low']), 2)
        new_data1['S3'] = round(new_data1['Low'] - (
                2 * (new_data1['High'] - ((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3))), 2)
        new_data1['Mid_point'] = round(((new_data1['High'] + new_data1['Low']) / 2), 2)
        new_data1['CPR'] = round(
            abs((round(((new_data1['High'] + new_data1['Low'] + new_data1['Closing']) / 3), 2)) - new_data1[
                'Mid_point']), 2)

        new_data1['CPR_SCAN'] = np.where((new_data1['CPR'] < ((new_data1.CPR.rolling(10).min()).shift(-10))), "YES", "")
        # new_data1['cpr_strategy'] = np.where((new_data1['High'] > new_data1['R1']),
        #                                      (new_data1['High'] < new_data1['R2']),
        #                                      (new_data1['Closing'] < new_data1['Pivot']),
        #                                      (new_data1['Low'] > new_data1['S1']), "Cpr_Bearish",
        #                                      np.where((new_data1['High'] < new_data1['R1']),
        #                                               (new_data1['Low'] < new_data1['S1']),
        #                                               (new_data1['Closing'] > new_data1['Pivot']),
        #                                               (new_data1['Low'] > new_data1['S2']), "Cpr_Bullish",))
        new_data1['Candle'] = np.where(abs(new_data1['Open'] - new_data1['Closing']) <
                                       abs(new_data1['High'] - new_data1['Low']) * 0.2, "DOZI",
                                       np.where(abs(new_data1['Open'] - new_data1['Closing']) >
                                                abs(new_data1['High'] - new_data1['Low']) * 0.7, "BIGBODY", ""))

        new_data2 = pd.concat([new_data1, new_data2])
    new_data2.rename(columns={'Change_%': 'Change_per', 'P/E': 'P_E', 'P/B': 'P_B'}, inplace=True)
    column = (list(new_data2.columns))

    # response = new_data2.to_json(orient='records')
    allData = []
    for i in range(new_data2.shape[0]):
        temp = new_data2.iloc[i]
        allData.append(dict(temp))
    context1 = allData
    # return context1

    return render(request, 'views_for/intraday_market_indices.html', {'context1': context1,'idx_list':idx_list,'column':column})
    


def Intraday_Market_Futures(request):
    return render(request, 'views_for/intraday_market_futures.html')


def Intraday_Market_Options(request):
    return render(request, 'views_for/intraday_market_options.html')


def Intraday_Market_FII_DII(request):
    return render(request, 'views_for/intraday_market_fii_dii.html')


def Backtest(request):
    return render(request, 'views_for/backtest.html')


def Backtest_Stock(request):
    return render(request, 'views_for/backtest_stock.html')


def Backtest_Indices(request):
    return render(request, 'views_for/backtest_indices.html')


def Backtest_Futures(request):
    return render(request, 'views_for/backtest_futures.html')


def Backtest_Options(request):
    return render(request, 'views_for/backtest_options.html')


def Backtest_FII_DII(request):
    return render(request, 'views_for/backtest_fii_dii.html')


def News(request):
    return render(request, 'views_for/news.html')


def News_India(request):
    response = requests.get('https://api.covid19api.com/countries').json()
    return render(request, 'views_for/news_india.html', {'response': response})


def News_World(request):
    return render(request, 'views_for/news_world.html')


def News_Top(request):
    return render(request, 'views_for/news_top.html')


def News_Latest(request):
    return render(request, 'views_for/news_latest.html')


def News_Most_Readed(request):
    return render(request, 'views_for/news_most_readed.html')

def home(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context ={
        'plot1': scatter()
    }

    return render(request, 'views_for/welcome.html', context)

def welcome(request):
    return render(request, 'views_for/welcome.html')

def stock_dashboard(request):
    return render(request, 'views_for/stock_dashboard.html')

def Intraday_Option_Chart(request):
    return render(request, 'views_for/Intraday_Option_Chart.html')

def Eod_Option_Chart(request):
    return render(request, 'views_for/Eod_Option_Chart.html')

def Eod_Market_Stock_New(request):
    return render(request, 'views_for/Eod_Market_Stock_New.html')

def Analysis(request):
    return render(request, 'views_for/analysis.html')

