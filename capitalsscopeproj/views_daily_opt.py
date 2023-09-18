import logging
from Dash_app.holidayss import holidays
import pandas as pd
import time
from datetime import date, datetime, timedelta
from dateutil.utils import today
from py5paisa import FivePaisaClient
import sqlalchemy
from time import sleep
import environ
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

# nse = NSELive()

# env = Env()
# env.read_env()

sys.path.insert(0, r'/var/www/Capital_vercel1/capitalsscopeproj/Dash_app/holidayss')

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

#cred = env('cred')
#cred=env({'cred'})

user=env('user')
pwd=env('pwd')
dob=env('dob')

client = FivePaisaClient(email=user, passwd=pwd, dob=dob, cred=cred)
client.login()
# print(cred)

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2023, 1, 23)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

# df=client.historical_data('N','C',3045,'1d',from_d,to_d)
#print(df.head(5))

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
#print(intradayy)
lastTradingDayy =  lastTradingDay.date()
print(dates)

current_time = (datetime.now()).strftime("%H:%M")


timelist = ['09:15','09:20','09:25','09:30','09:35','09:40','09:45','09:50','09:55','10:00','10:05','10:10','10:15',
	        '10:20','10:25','10:30','10:35','10:40','10:45','10:50','10:55','11:00','11:05','11:10','11:15','11:20',
            '11:25','11:30','11:35','11:40','11:45','11:50','11:55','12:00','12:05','12:10','12:15','12:20','12:25',
            '12:30','12:35','12:40','12:45','12:50','12:55','13:00','13:05','13:10','13:15','13:20','13:25','13:30',
            '13:35','13:40','13:45','13:50','13:55','14:00','14:05','14:10','14:15','14:20','14:25','14:30','14:35',
            '14:40','14:45','14:50','14:55','15:00','15:05','15:10','15:15','15:20','15:25','15:30']

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
        Time = current_time
        Date = today()
        eq_df.append([Date, Time, Open, High, Low, Close, Ltp, Chg])
        df3 = pd.DataFrame(eq_df)
        df3.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']
        df3['Symbol'] = 'NIFTY'
        df3 = df3[['Symbol', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']]
        df3.to_sql(name="live_Index", con=engine, if_exists="append", index=False)
        # print(df3.tail(2))
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
        df1['Time'] = current_time

        df1.rename(
            {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
            'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
            'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
            'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

        df1 = df1[['Date', 'Time', 'CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]
        # print(df1.tail(2))
        df1.to_sql(name="live_option_chain_nifty", con=engine, if_exists="append", index=False)
        # df1.loc["Total"] = df1.sum()
        print('live_option_chain_nifty',to_d,now)
        return df1, ep1, expiry
    else:
        pass
        print('False',to_d,now)

def live_option_chain_bank_nifty():
    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
        eq_df = []
        Open = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Open'])
        High = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['High'])
        Low = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Low'])
        Close = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['Close'])
        Ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['LastTradedPrice'])
        Chg = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":'BANKNIFTY'}])['Data'][0]['NetChange'])
        Time = current_time
        Date = today()
        eq_df.append([Date, Time, Open, High, Low, Close, Ltp, Chg])
        df3 = pd.DataFrame(eq_df)
        df3.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']
        df3['Symbol'] = 'BANKNIFTY'
        df3 = df3[['Symbol', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg']]
        df3.to_sql(name="live_Index", con=engine, if_exists="append", index=False)
        # print(df3.tail(2))
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
        df1['Time'] = current_time

        df1.rename(
            {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
            'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
            'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
            'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

        df1 = df1[['Date', 'Time', 'CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
                'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]

        df1.to_sql(name="live_option_chain_bank_nifty", con=engine, if_exists="append", index=False)
        # df1.loc["Total"] = df1.sum()
        # print(df1.tail(2))
        print('live_option_chain_bank_nifty',to_d,now)
        return df1, ep1, expiry
    else:
        pass
        print('False',to_d,now)

while True:
    sleep(60)
    current_time = (datetime.now()).strftime("%H:%M")
    print(current_time)
    now = datetime.now()

    intr_time1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
    intr_time2 = now.replace(hour=15, minute=33, second=0, microsecond=0)
    de = date.today()


    if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
        for i in timelist:
            if i == current_time:
                print(i)
                print("True")
                live_option_chain_bank_nifty()
                live_option_chain_nifty()
            else:
                pass
          # print("true")

    else:
        pass
        print('false',to_d,now)
