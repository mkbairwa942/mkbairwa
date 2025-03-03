from jugaad_data.nse import NSELive
from jugaad_data.holidays import holidays
import pandas as pd
from datetime import date, datetime, timedelta
import sqlalchemy
import plotly
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash
import os
from dash import Dash, dash_table, dcc, html, Input, Output, callback, DiskcacheManager
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
from dash.dependencies import Input, Output, State
import numpy as np

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

print(lastTradingDay)
print(intraday)

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

eq_bhav = (f"SELECT distinct * FROM capitalsscope.full_bhavcopy where DATE1 between '{from_d}' and '{to_d}';")
data_eq = pd.read_sql(sql=eq_bhav, con=engine)
fo_bhav = (f"SELECT distinct * FROM capitalsscope.FO_bhavcopy where INSTRUMENT in ('FUTSTK','FUTIDX') and TIMESTAMP "
               f"between '{from_d}' and '{to_d}';")
fo_bhav = pd.read_sql(sql=fo_bhav, con=engine)

nifty_list = pd.unique(fo_bhav['SYMBOL'])
# print(nifty_list)

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
# print(eq_data_pd.head(5))

eq_data_pd['Date'] = pd.to_datetime(eq_data_pd['Date'])
day = eq_data_pd.pop('Date')
# print(day.head(5))
# print(eq_data_pd.head(5))
eq_data_pd.insert(0, 'DATE',day )
#eq_data_pd.drop(['Date'], axis=1, inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Eod_Market_Stock_New', external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Label("Analyse the EOD Data of Stock"),

    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=eq_data_pd.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False,'presentation': 'dropdown'} for i in eq_data_pd.columns
            ],
            editable=False,
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            row_selectable='multi',
            row_deletable=False,
            selected_rows=[],
            page_action='native',
            page_current=0,
            fixed_rows={'headers': True},
            page_size=15,
            style_table={'height': '800px', 'overflowY': 'auto','overflowX': 'auto'},
            style_cell={'textAlign': 'center','padding':'5px'},
            style_header={'backgroundColor':'rgb(230, 230, 230)','fontWeight':'bold','border':'1px solid black'},
            style_data_conditional=([
                {'if':{'filter_query':'{Price_Chg} < -2','column_id':'Price_Chg'},'backgroundColor':'rgb(200, 39, 52)','color':'white'},
                {'if':{'filter_query':'{Price_Chg} > 2','column_id':'Price_Chg'},'backgroundColor':'rgb(57, 211, 26)','color':'white'},
                {'if':{'filter_query':'{OI_Chg} < -6','column_id':'OI_Chg'},'backgroundColor':'rgb(200, 39, 52)','color':'white'},
                {'if':{'filter_query':'{OI_Chg} > 6','column_id':'OI_Chg'},'backgroundColor':'rgb(57, 211, 26)','color':'white'},
                {'if':{'filter_query':'{Deliv_per} > 50','column_id':'Deliv_per'},'backgroundColor':'rgb(13, 224, 217)','color':'black'},
                {'if':{'filter_query':'{Vol_Chg} > 55','column_id':'Vol_Chg'},'backgroundColor':'rgb(187, 255, 0)','color':'black'},
                {'if':{'filter_query':'{Closing} < 500','column_id':'Closing'},'backgroundColor':'hotpink','color':'black'},
                            ]),
            style_as_list_view=True

        ),
    ], className='row'),

    ]
)


