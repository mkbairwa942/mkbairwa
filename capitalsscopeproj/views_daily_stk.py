import logging
from jugaad_data.nse import NSELive
from Dash_app.holidayss import holidays
import pandas as pd
import time
from datetime import date, datetime, timedelta
from dateutil.utils import today
from zipfile import ZipFile
import requests
from io import BytesIO
import sqlalchemy
from time import sleep

logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

nse = NSELive()

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2023, 1, 23)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

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

now = datetime.now()
eod_time1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
eod_time2 = now.replace(hour=15, minute=35, second=0, microsecond=0)
print(eod_time1)
print(now)
print(eod_time2)

eq_check = (f"SELECT distinct * FROM capitalsscope.full_bhavcopy order by Date1;")
eq_checkk = pd.read_sql(sql=eq_check, con=engine)
eq_checkkk = ((pd.unique((eq_checkk['DATE1']).tolist()))[-1]).date()


def bhavcopy(lastTradingDay):
    if now > eod_time1 and now < eod_time2 and (date.today() - timedelta(days=1)) == lastTradingDayy and eq_checkkk != lastTradingDayy:
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
        bh_df = pd.DataFrame(bhav_eq)
        bh_df.to_sql(name="full_bhavcopy", con=engine, if_exists="append", index=False)
        print(bh_df.head(2))
        return bh_df
    else:
        pass
        print('False',to_d,now)
    

def bhavcopy_fno(lastTradingDay):
    if now > eod_time1 and now < eod_time2 and (date.today() - timedelta(days=1)) == lastTradingDayy and eq_checkkk != lastTradingDayy:
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
        fo_df = pd.DataFrame(bhav_fo)
        fo_df.to_sql(name="FO_bhavcopy", con=engine, if_exists="append", index=False)
        print(fo_df.head(2))
        return fo_df
    else:
        pass
        print('False',to_d,now)
    

def fii_openint_down(lastTradingDay):
    if now > eod_time1 and now < eod_time2 and (date.today() - timedelta(days=1)) == lastTradingDayy and eq_checkkk != lastTradingDayy:
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
    else:
        pass
        print('False',to_d,now)
    

def fii_vol_down(lastTradingDay):
    if now > eod_time1 and now < eod_time2 and (date.today() - timedelta(days=1)) == lastTradingDayy and eq_checkkk != lastTradingDayy:
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
    else:
        pass
        print('False',to_d,now) 
    

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
        print('live_stock_new',to_d,now)
        return eq_fo_data
    else:
        pass
        print('False',to_d,now)


# print(live_stock_new())

while True:
    sleep(10)
    now = datetime.now()

    intr_time1 = now.replace(hour=9, minute=14, second=0, microsecond=0)
    intr_time2 = now.replace(hour=15, minute=35, second=0, microsecond=0)
    exs = (date.today() - timedelta(days=1))
    de = date.today()

    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
        print("true")
        #bhavcopy(lastTradingDay)
        #bhavcopy_fno(lastTradingDay)
        #fii_openint_down(lastTradingDay)
        #fii_vol_down(lastTradingDay)
        print('live_stock_new',to_d,now)
        live_stock_new()
        # print(live_stock_new())
    else:
        pass
        print('False',to_d,now)
