from jugaad_data.nse import NSELive
from jugaad_data.holidays import holidays
import pandas as pd
from datetime import date, datetime, timedelta
import sqlalchemy
import plotly
import plotly.express as px
import plotly.graph_objs as go
# from django_plotly_dash import DjangoDash
import dash
import os
from dash import dash_table
from dash import Dash, dash_table, dcc, html, Input, Output, callback, DiskcacheManager
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
# import diskcache
# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(cache)
# background_callback_manager = DiskcacheManager(cache)

nse = NSELive()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2022, 12, 30)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()

print(lastTradingDay)
print(intraday)

day = intradayy
print(day)


engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')
    
engine1 = sqlalchemy.create_engine('mysql+pymysql://root:Jencocotfab@301@5.183.11.143:3306/capitalsscope')
    

lot = 'NotMultiply'

eq_bhav = (f"SELECT distinct * FROM capitalsscope.live_option_chain_nifty;")
data_eq = pd.read_sql(sql=eq_bhav, con=engine)
data_eq['Date1'] = pd.to_datetime(data_eq['Date'], format="%d-%m-%Y").dt.date
data_eq['CE_Volume'] = np.where(
    (lot == 'NotMultiply'), data_eq['CE_Volume']/50, data_eq['CE_Volume'])
data_eq['CE_Prev_OI'] = np.where(
    (lot == 'NotMultiply'), data_eq['CE_Prev_OI']/50, data_eq['CE_Prev_OI'])
data_eq['CE_Chg_OI'] = np.where(
    (lot == 'NotMultiply'), data_eq['CE_Chg_OI']/50, data_eq['CE_Chg_OI'])
data_eq['CE_OI'] = np.where((lot == 'NotMultiply'),
                            data_eq['CE_OI']/50, data_eq['CE_OI'])
data_eq['PE_OI'] = np.where((lot == 'NotMultiply'),
                            data_eq['PE_OI']/50, data_eq['PE_OI'])
data_eq['PE_Chg_OI'] = np.where(
    (lot == 'NotMultiply'), data_eq['PE_Chg_OI']/50, data_eq['PE_Chg_OI'])
data_eq['PE_Prev_OI'] = np.where(
    (lot == 'NotMultiply'), data_eq['PE_Prev_OI']/50, data_eq['PE_Prev_OI'])
data_eq['PE_Volume'] = np.where(
    (lot == 'NotMultiply'), data_eq['PE_Volume']/50, data_eq['PE_Volume'])


data_eq.insert(0, 'DATE', data_eq.pop('Date1'))
data_eq.drop(['Date'], axis=1, inplace=True)
print(data_eq.head(5))

datess = data_eq['DATE'].unique()
print(datess)


