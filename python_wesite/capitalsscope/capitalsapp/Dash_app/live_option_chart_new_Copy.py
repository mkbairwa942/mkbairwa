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
# print(intraday)
# print(type(intraday))
# print(intradayy)
# print(type(intradayy))


engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')    
engine1 = sqlalchemy.create_engine('mysql+pymysql://root:Jencocotfab@301@5.183.11.143:3306/capitalsscope')    



idx_list = ['NIFTY', 'BANKNIFTY']

index = 'NIFTY'

def eq_idx(index):#f'current price:- {dff_idx[0]}'
    eq_idx = (f"SELECT distinct * FROM capitalsscope.live_Index where Symbol = '{index}';")
    live_Index = pd.read_sql(sql=eq_idx, con=engine)
    return live_Index

def indexoption(index):
    lot = 'NotMultiply'
    # lotlink = "https://archives.nseindia.com/content/fo/fo_mktlots.csv"
    # lotlon = pd.read_csv(lotlink)
    # trimmed = lotlon.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # lotlon1 = trimmed[trimmed[((lotlon.columns)[1])] == index]
    # lotsize = int(lotlon1[((lotlon.columns)[2])])

    if index == 'NIFTY':
        lotsize = 50
        eq_bhav = (f"SELECT distinct * FROM capitalsscope.live_option_chain_nifty;")
        data_eq = pd.read_sql(sql=eq_bhav, con=engine)
    else:
        lotsize = 100
        eq_bhav = (f"SELECT distinct * FROM capitalsscope.live_option_chain_bank_nifty;")
        data_eq = pd.read_sql(sql=eq_bhav, con=engine)
    data_eq['Date1'] = pd.to_datetime(data_eq['Date'], format="%d-%m-%Y").dt.date
    data_eq['CE_Volume'] = np.where((lot == 'NotMultiply'), data_eq['CE_Volume']/lotsize, data_eq['CE_Volume'])    
    data_eq['CE_Prev_OI'] = np.where((lot == 'NotMultiply'), data_eq['CE_Prev_OI']/lotsize, data_eq['CE_Prev_OI'])    
    data_eq['CE_Chg_OI'] = np.where((lot == 'NotMultiply'), data_eq['CE_Chg_OI']/lotsize, data_eq['CE_Chg_OI'])    
    data_eq['CE_OI'] = np.where((lot == 'NotMultiply'),data_eq['CE_OI']/lotsize, data_eq['CE_OI'])                            
    data_eq['PE_OI'] = np.where((lot == 'NotMultiply'),data_eq['PE_OI']/lotsize, data_eq['PE_OI'])                            
    data_eq['PE_Chg_OI'] = np.where((lot == 'NotMultiply'), data_eq['PE_Chg_OI']/lotsize, data_eq['PE_Chg_OI'])    
    data_eq['PE_Prev_OI'] = np.where((lot == 'NotMultiply'), data_eq['PE_Prev_OI']/lotsize, data_eq['PE_Prev_OI'])    
    data_eq['PE_Volume'] = np.where((lot == 'NotMultiply'), data_eq['PE_Volume']/lotsize, data_eq['PE_Volume'])
    data_eq['CE_Prev_Ltp'] = round(((data_eq['CE_Ltp']) - (data_eq['CE_Prev_Ltp'])),2)
    data_eq['PE_Prev_Ltp'] = round(((data_eq['PE_Ltp']) - (data_eq['PE_Prev_Ltp'])),2)
    data_eq['CE_INTERP'] = np.where((data_eq['CE_Chg_OI'] > 0) & (data_eq['CE_Prev_Ltp'] > 0), 'CALL_BUYING',
                          (np.where((data_eq['CE_Chg_OI'] < 0) & (data_eq['CE_Prev_Ltp'] < 0), 'LONG_UNWIND',
                          (np.where((data_eq['CE_Chg_OI'] > 0) & (data_eq['CE_Prev_Ltp'] < 0), 'CALL_WRITING',
                          (np.where((data_eq['CE_Chg_OI'] < 0) & (data_eq['CE_Prev_Ltp'] > 0), 'SHORT_COVER',
                                                            "-")))))))
    data_eq['PE_INTERP'] = np.where((data_eq['PE_Chg_OI'] > 0) & (data_eq['PE_Prev_Ltp'] > 0), 'PUT_BUYING',
                          (np.where((data_eq['PE_Chg_OI'] < 0) & (data_eq['PE_Prev_Ltp'] < 0), 'LONG_UNWIND',
                          (np.where((data_eq['PE_Chg_OI'] > 0) & (data_eq['PE_Prev_Ltp'] < 0), 'PUT_WRITING',
                          (np.where((data_eq['PE_Chg_OI'] < 0) & (data_eq['PE_Prev_Ltp'] > 0), 'SHORT_COVER',
                                                          "-"))))))) 

    data_eq.insert(0, 'DATE', data_eq.pop('Date1'))                                                      
    # data_eq.drop(['Date1'], axis=1, inplace=True)
    data_eq = data_eq[['DATE', 'Time','CE_INTERP', 'CE_Volume', 'CE_Chg_OI', 'CE_OI', 'CE_Ltp', 'CE_Prev_Ltp', 'StrikeRate',
                                'PE_Prev_Ltp','PE_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Volume','PE_INTERP']]
    print(data_eq.tail(2))
    return data_eq

data_eq = indexoption(index)

day = intraday

def pcr_data(dateP,index):   
    Date_dropp = pd.to_datetime(dateP)
    data_eq1 = indexoption(index)
    # data_eq1.insert(0, 'DATE', data_eq1.pop('Date1'))

    dff = data_eq1[(data_eq1['DATE'] == Date_dropp.date())]     
    pcr_time = np.unique(dff['Time'])

    live_Index2 = eq_idx(index)
    live_Index1 = live_Index2[live_Index2.Date == Date_dropp]

    pcr_opt = 1
    pcr_chg_opt = 1

    dffg = pd.DataFrame()

    for i in pcr_time:
        new_dff = dff[dff['Time'] == i]
        new_dff['Time'] = i
        new_dff['Sum_CE_OI'] = new_dff['CE_OI'].sum()
        new_dff['Sum_PE_OI'] = new_dff['PE_OI'].sum()
        new_dff['Sum_CE_CHG_OI'] = new_dff['CE_Chg_OI'].sum()
        new_dff['Sum_PE_CHG_OI'] = new_dff['PE_Chg_OI'].sum()
        new_dff['Diff_OI'] = new_dff['Sum_PE_OI']-new_dff['Sum_CE_OI']
        new_dff['Diff_CHG_OI'] = new_dff['Sum_PE_CHG_OI']-new_dff['Sum_CE_CHG_OI']
        new_dff['PCR_OI'] = round((new_dff['Sum_PE_OI']/new_dff['Sum_CE_OI']),2)
        new_dff['PCR_CHG_OI'] = round((new_dff['Sum_PE_CHG_OI']/new_dff['Sum_CE_CHG_OI']),2)
        new_df1 = new_dff.iloc[[0],:]
        dffg = pd.concat([new_df1, dffg])
    dffg.sort_values(['Time'], ascending=[True], inplace=True)
    dffg['Diff_PCR_OI'] = round(((dffg['PCR_OI']) - (dffg['PCR_OI'].shift(1))),2).fillna(0)
    dffg['Signal_OI'] = np.where(dffg['PCR_OI']>pcr_opt,"BUY","SELL")
    dffg['Diff_PCR_CHG_OI'] = round(((dffg['PCR_CHG_OI']) - (dffg['PCR_CHG_OI'].shift(1))),2).fillna(0)
    dffg['Signal_CHG_OI'] = np.where(dffg['PCR_CHG_OI']>pcr_chg_opt,"BUY","SELL")

    data_pcr = pd.merge(dffg,live_Index1, on=['Time'], how='left')
    data_pcr.fillna(0,inplace=True)
    data_pcr['Spot'] = np.where(data_pcr['Ltp'] == 0,(data_pcr['Ltp'].shift(1)),data_pcr['Ltp'])
    # data_pcr.insert(0, 'DATE', data_pcr.pop('Date1'))
    data_pcr = data_pcr[['DATE','Time','Sum_CE_OI','Sum_PE_OI','Sum_CE_CHG_OI','Sum_PE_CHG_OI',
            'Diff_OI','PCR_OI','Diff_PCR_OI','Signal_OI','Spot','Diff_CHG_OI','PCR_CHG_OI',
            'Diff_PCR_CHG_OI','Signal_CHG_OI']]
                                                      
    print(data_pcr.tail(2))
    return data_pcr  
    
data_pcr = pcr_data(intraday,index)

data_eq3 = data_eq[data_eq.DATE == day.date()]
time1 = np.unique(data_eq3['Time'])[-1]

# data_eq.insert(0, 'DATE', data_eq.pop('Date1'))
# data_eq.drop(['Date'], axis=1, inplace=True)

StrikeRate = np.unique(data_eq['StrikeRate'])
column = (data_eq.columns)

dgf = data_eq[(data_eq['DATE'] == day.date()) &  (data_eq['Time'] == time1)]

lengt = round((dgf.shape[0])/2)
print(lengt)
print(type(lengt))

lengt1 = lengt+1
print(lengt1)
print(type(lengt1))
# df.iloc[[1]]
stre=pd.to_numeric(dgf['StrikeRate'].iloc[[lengt]])
#stre = dgf['StrikeRate'].iloc[[lengt]]
print(stre)
stre1=pd.to_numeric(dgf['StrikeRate'].iloc[[lengt1]])
#stre1 = dgf['StrikeRate'].iloc[[lengt1]]
print(stre1)
print(type(stre1))
diff = stre1-stre

print(diff)
print(type(diff))

Top_CE_Volume = [x[0] for x in (dgf.sort_values(['CE_Volume'], ascending=[False]).iloc[:4][['StrikeRate']].values.tolist())]
Top_PE_Volume = [x[0] for x in (dgf.sort_values(['PE_Volume'], ascending=[False]).iloc[:4][['StrikeRate']].values.tolist())]
Top_CE_Chg_OI = [x[0] for x in (dgf.sort_values(['CE_Chg_OI'], ascending=[False]).iloc[:4][['StrikeRate']].values.tolist())]
Top_PE_Chg_OI = [x[0] for x in (dgf.sort_values(['PE_Chg_OI'], ascending=[False]).iloc[:4][['StrikeRate']].values.tolist())]

def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #124edb 0%,
                    #124edb {max_bound_percentage}%,
                    #1c1b1b {max_bound_percentage}%,
                    #1c1b1b 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles

def data_bars1(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #09e338 0%,
                    #09e338 {max_bound_percentage}%,
                    #1c1b1b {max_bound_percentage}%,
                    #1c1b1b 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #eb346b 0%,
                    #eb346b {max_bound_percentage}%,
                    #1c1b1b {max_bound_percentage}%,
                    #1c1b1b 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    col_max = df[column].max()
    col_min = df[column].min()
    ranges = [
        ((col_max - col_min) * i) + col_min
        for i in bounds
    ]
    midpoint = (col_max + col_min) / 2.

    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        min_bound_percentage = bounds[i - 1] * 100
        max_bound_percentage = bounds[i] * 100

        style = {
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'paddingBottom': 2,
            'paddingTop': 2
        }
        if max_bound > midpoint:
            background = (
                """
                    linear-gradient(90deg,
                    #1c1b1b 0%,
                    #1c1b1b 50%,
                    {color_above} 50%,
                    {color_above} {max_bound_percentage}%,
                    #1c1b1b {max_bound_percentage}%,
                    #1c1b1b 100%)
                """.format(
                    max_bound_percentage=max_bound_percentage,
                    color_above=color_above
                )
            )
        else:
            background = (
                """
                    linear-gradient(90deg,
                    #1c1b1b 0%,
                    #1c1b1b {min_bound_percentage}%,
                    {color_below} {min_bound_percentage}%,
                    {color_below} 50%,
                    #1c1b1b 50%,
                    #1c1b1b 100%)
                """.format(
                    min_bound_percentage=min_bound_percentage,
                    color_below=color_below
                )
            )
        style['background'] = background
        styles.append(style)

    return styles

def data_bars_diverging(df, column, color_above='#ebeb1a', color_below='#f5440f'):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    col_max = df[column].max()
    col_min = df[column].min()
    ranges = [
        ((col_max - col_min) * i) + col_min
        for i in bounds
    ]
    midpoint = (col_max + col_min) / 2.

    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        min_bound_percentage = bounds[i - 1] * 100
        max_bound_percentage = bounds[i] * 100

        style = {
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'paddingBottom': 2,
            'paddingTop': 2
        }
        if max_bound > midpoint:
            background = (
                """
                    linear-gradient(90deg,
                    #1c1b1b 0%,
                    #1c1b1b 50%,
                    {color_above} 50%,
                    {color_above} {max_bound_percentage}%,
                    #1c1b1b {max_bound_percentage}%,
                    #1c1b1b 100%)
                """.format(
                    max_bound_percentage=max_bound_percentage,
                    color_above=color_above
                )
            )
        else:
            background = (
                """
                    linear-gradient(90deg,
                    #1c1b1b 0%,
                    #1c1b1b {min_bound_percentage}%,
                    {color_below} {min_bound_percentage}%,
                    {color_below} 50%,
                    #1c1b1b 50%,
                    #1c1b1b 100%)
                """.format(
                    min_bound_percentage=min_bound_percentage,
                    color_below=color_below
                )
            )
        style['background'] = background
        styles.append(style)

    return styles

colour_CE_Volume = data_bars(data_eq, 'CE_Volume')
colour_PE_Volume = data_bars(data_eq, 'PE_Volume')
colour_CE_OI = data_bars1(data_eq, 'CE_OI')
colour_PE_OI = data_bars1(data_eq, 'PE_OI')
colour_CE_Chg_OI = data_bars_diverging(data_eq, 'CE_Chg_OI', color_above='#ebeb1a', color_below='#f5440f')
colour_PE_Chg_OI = data_bars_diverging(data_eq, 'PE_Chg_OI', color_above='#ebeb1a', color_below='#f5440f')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('live_option_chart_new',
                 external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Div([dcc.Markdown('# Analyse the Data of Option',
             style={'textAlign': 'center'})]),
    html.Div([dcc.Markdown('# Option Data',
             style={'textAlign': 'center'})]),
    html.Div([
        html.Div([dbc.Label("Select a Date")], className='three columns'),
        html.Div([dbc.Label("Select a Time")], className='three columns'), 
        html.Div([dbc.Label("Select a Option")], className='three columns'),                    
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='Date_drop',
            placeholder="Select Date",
            options=[{"label": x, "value": x} for x in sorted(data_eq.DATE.unique())],            
            multi=False,
            clearable=True,
            disabled=False,
            style={'display': True},
            value=day,
            className='dcc_compon',           
            ),], className='three columns'),
                     
        html.Div([
            dcc.Dropdown(id='Time_drop',
            placeholder="Select Time",
            options=[],            
            multi=False,
            clearable=True,
            disabled=False,
            style={'display': True},
            value=time1,
            className='dcc_compon'
            ),], className='three columns'),   

        html.Div([
            dcc.Dropdown(id='optionns',
            placeholder="Select Option",
            options = [{"label": x, "value": x} for x in sorted(idx_list)],               
            # options=idx_list,         
            multi=False,
            clearable=True,
            disabled=False,
            style={'display': True},
            value=index,
            className='dcc_compon'
            ),], className='three columns'),                
    ],className='row'),     

    html.Div([dash_table.DataTable(id='my_table',
                                    columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in data_eq.columns],                                      
                                    data=data_eq.to_dict('records'),
                                    editable=False,
                                    # filter_action='native',
                                    sort_action='native',
                                    sort_mode='multi',
                                    #row_selectable='multi',
                                    row_deletable=False,
                                    #selected_rows=[],
                                    page_action='native',
                                    page_current=0,
                                    page_size=20,
                                    style_cell={'textAlign': 'center', 'padding': '5px'},                                       
                                    # style_data={'width': '150px', 'minWidth': '150px', 'maxWidth': '150px','overflow': 'hidden','textOverflow': 'ellipsis',},
                                    style_header={'backgroundColor': 'white','color': '#1c1b1b', 'fontWeight': 'bold', 'border': '1px solid black'},
                                    style_data={'backgroundColor': '#1c1b1b','color': 'white'},
                                    style_data_conditional=(
                                        colour_CE_Volume + colour_PE_Volume + 
                                        colour_CE_Chg_OI + colour_PE_Chg_OI + 
                                        colour_CE_OI +  colour_PE_OI  +
                                        
                                        [{'if':{'filter_query':'{StrikeRate} > 100','column_id':'StrikeRate'},'backgroundColor':'#c98122','color':'white'}, 
                                         {'if':{'filter_query':'{CE_Prev_Ltp} > 0','column_id':'CE_Prev_Ltp'},'backgroundColor':'#1c1b1b','color':'#3adb12'},
                                         {'if':{'filter_query':'{CE_Prev_Ltp} < 0','column_id':'CE_Prev_Ltp'},'backgroundColor':'#1c1b1b','color':'#ed091c'},
                                         {'if':{'filter_query':'{PE_Prev_Ltp} > 0','column_id':'PE_Prev_Ltp'},'backgroundColor':'#1c1b1b','color':'#3adb12'},
                                         {'if':{'filter_query':'{PE_Prev_Ltp} < 0','column_id':'PE_Prev_Ltp'},'backgroundColor':'#1c1b1b','color':'#ed091c'},
                                         {'if':{'filter_query':'{CE_INTERP} = CALL_BUYING','column_id':'CE_INTERP'},'backgroundColor':'#04d10b','color':'white'},
                                         {'if':{'filter_query':'{CE_INTERP} = LONG_UNWIND','column_id':'CE_INTERP'},'backgroundColor':'#de120b','color':'white'},
                                         {'if':{'filter_query':'{CE_INTERP} = CALL_WRITING','column_id':'CE_INTERP'},'backgroundColor':'#de120b','color':'white'},
                                         {'if':{'filter_query':'{CE_INTERP} = SHORT_COVER','column_id':'CE_INTERP'},'backgroundColor':'#04d10b','color':'white'},
                                         {'if':{'filter_query':'{PE_INTERP} = PUT_BUYING','column_id':'PE_INTERP'},'backgroundColor':'#de120b','color':'white'},
                                         {'if':{'filter_query':'{PE_INTERP} = LONG_UNWIND','column_id':'PE_INTERP'},'backgroundColor':'#04d10b','color':'white'},
                                         {'if':{'filter_query':'{PE_INTERP} = PUT_WRITING','column_id':'PE_INTERP'},'backgroundColor':'#04d10b','color':'white'},
                                         {'if':{'filter_query':'{PE_INTERP} = SHORT_COVER','column_id':'PE_INTERP'},'backgroundColor':'#de120b','color':'white'}]),
                                        # {'if':{'filter_query':'{Deliv_per} > 50','column_id':'Deliv_per'},'backgroundColor':'rgb(13, 224, 217)','color':'black'},
                                        # {'if':{'filter_query':'{Vol_Chg} > 55','column_id':'Vol_Chg'},'backgroundColor':'rgb(187, 255, 0)','color':'black'},
                                        # {'if':{'filter_query':'{Closing} < 500','column_id':'Closing'},'backgroundColor':'hotpink','color':'black'},
                                        
                                        
                                    style_as_list_view=True,
                                )],className='row'),                                   

    html.Div([dbc.Label("Show number of rows")]),

    html.Div([dcc.Dropdown(id='row_drop',
                           value=20, clearable=False, style={'width': '35%'},
                           options=[6, 8, 10, 16, 20, 50, 100])]),

    html.Div([dcc.Markdown('# PCR Data',
             style={'textAlign': 'center'})]),

    html.Div([dash_table.DataTable(id='pcr_table',
                                    columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in data_pcr.columns],                                      
                                    data=data_pcr.to_dict('records'),
                                    editable=False,
                                    sort_action='native',
                                    sort_mode='multi',
                                    row_deletable=False,
                                    page_action='none',
                                    fixed_rows={'headers': True},
                                    # page_current=0,
                                    # page_size=15,
                                    style_table={'height': '400px', 'overflowY': 'auto'},
                                    style_cell={'textAlign': 'center', 'padding': '5px'},                                     
                                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'border': '1px solid black'},
                                    style_data={'backgroundColor': '#1c1b1b','color': 'white'},
                                    style_data_conditional=(                                       
                                    [{'if':{'filter_query':'{Signal_OI} = SELL','column_id':'Signal_OI'},'backgroundColor':'#eb3107','color':'white'},
                                    {'if':{'filter_query':'{Signal_OI} = BUY','column_id':'Signal_OI'},'backgroundColor':'#2ee605','color':'white'},
                                    {'if':{'filter_query':'{Signal_CHG_OI} = SELL','column_id':'Signal_CHG_OI'},'backgroundColor':'#eb3107','color':'white'},
                                    {'if':{'filter_query':'{Signal_CHG_OI} = BUY','column_id':'Signal_CHG_OI'},'backgroundColor':'#2ee605','color':'white'}]), 
                  
                                    )],className='row'),                                   

    html.Div([ 
    html.Div([html.Label(f'Current price is:-' ,id='idr',style={'font-weight':'bold','text-align':'center'})],className='row'),  
    # html.Div([html.Label([f'current price:- {dff_idx[0]}'],style={'font-weight':'bold','text-align':'center'})],className='row'),
    html.Div([html.Label(['Top Strike Prices :-'],style={'font-weight':'bold','text-align':'center'})],className='row'),
    html.Div([
    html.Div([html.Label(['Top Four CE_Volume'])], className='three columns'), 
    html.Div([html.Label(['Top Four PE_Volume'])], className='three columns'),
    html.Div([html.Label(['Top Four CE_Chg_OI'])], className='three columns'),
    html.Div([html.Label(['Top Four PE_Chg_OI'])], className='three columns'),   
        ],className='row'),
    html.Div([        
    html.Div([html.Label([f'1 : {Top_CE_Volume[0]}'],style={'text-align':'left'})], className='three columns'),                                 
    html.Div([html.Label([f'1 : {Top_PE_Volume[0]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'1 : {Top_CE_Chg_OI[0]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'1 : {Top_PE_Chg_OI[0]}'],style={'text-align':'left'})], className='three columns'),
        ],className='row'),
    html.Div([        
    html.Div([html.Label([f'2 : {Top_CE_Volume[1]}'],style={'text-align':'left'})], className='three columns'),                                 
    html.Div([html.Label([f'2 : {Top_PE_Volume[1]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'2 : {Top_CE_Chg_OI[1]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'2 : {Top_PE_Chg_OI[1]}'],style={'text-align':'left'})], className='three columns'),
        ],className='row'),
    html.Div([        
    html.Div([html.Label([f'3 : {Top_CE_Volume[2]}'],style={'text-align':'left'})], className='three columns'),                                 
    html.Div([html.Label([f'3 : {Top_PE_Volume[2]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'3 : {Top_CE_Chg_OI[2]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'3 : {Top_PE_Chg_OI[2]}'],style={'text-align':'left'})], className='three columns'),
        ],className='row'),
    html.Div([        
    html.Div([html.Label([f'4 : {Top_CE_Volume[3]}'],style={'text-align':'left'})], className='three columns'),                                 
    html.Div([html.Label([f'4 : {Top_PE_Volume[3]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'4 : {Top_CE_Chg_OI[3]}'],style={'text-align':'left'})], className='three columns'),
    html.Div([html.Label([f'4 : {Top_PE_Chg_OI[3]}'],style={'text-align':'left'})], className='three columns'),
        ],className='row'),
    
                ],className='row'),               
    html.Div([
    html.Div([html.Label(['Select Data for Chart 1'],style={'font-weight':'bold','text-align':'center'})]),
    html.Div([
        html.Div([dcc.Dropdown(id='Drop_11',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Volume[0]),          
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'),          
        html.Div([dcc.Dropdown(id='Drop_12',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value='CE_Volume',           
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_13',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Volume[1]),          
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_14',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True, value='CE_Volume',         
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
        html.Div([dcc.Dropdown(id='Drop_15',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Volume[2]),          
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_16',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True, value='CE_Volume',         
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),   
           ],className='row'), 
        html.Div([dcc.Graph(id='graph_1')],className='row'),],className='row'),

    html.Div([
    html.Div([html.Label(['Select Data for Chart 2'],style={'font-weight':'bold','text-align':'center'})]),
    html.Div([
        html.Div([dcc.Dropdown(id='Drop_21',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Volume[0]),             
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'),          
        html.Div([dcc.Dropdown(id='Drop_22',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value='PE_Volume',        
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_23',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Volume[1]),         
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_24',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True, value='PE_Volume',         
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
        html.Div([dcc.Dropdown(id='Drop_25',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Volume[2]),         
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_26',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True, value='PE_Volume',         
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
           ],className='row'), 
        html.Div([dcc.Graph(id='graph_2')],className='row'),],className='row'),

    html.Div([
    html.Div([html.Label(['Select Data for Chart 3'],style={'font-weight':'bold','text-align':'center'})]),
    html.Div([        
        html.Div([dcc.Dropdown(id='Drop_31',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Chg_OI[0]),          
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'),          
        html.Div([dcc.Dropdown(id='Drop_32',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value='CE_Chg_OI',            
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_33',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Chg_OI[1]),            
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_34',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True,value='CE_Chg_OI',           
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
        html.Div([dcc.Dropdown(id='Drop_35',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_CE_Chg_OI[2]),            
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_36',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True,value='CE_Chg_OI',           
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
           ],className='row'), 
        html.Div([dcc.Graph(id='graph_3')],className='row'),],className='row'),        

    html.Div([
    html.Div([html.Label(['Select Data for Chart 4'],style={'font-weight':'bold','text-align':'center'})]),
    html.Div([
        html.Div([dcc.Dropdown(id='Drop_41',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Chg_OI[0]),          
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'),          
        html.Div([dcc.Dropdown(id='Drop_42',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value='PE_Chg_OI',           
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_43',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Chg_OI[1]),           
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_44',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True,value='PE_Chg_OI',          
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
        html.Div([dcc.Dropdown(id='Drop_45',placeholder="Select Strike",multi=False,clearable=True,disabled=False,style={'display': True},searchable=True,value=(Top_PE_Chg_OI[2]),           
            options=[{"label": x, "value": x} for x in sorted(data_eq.StrikeRate.unique())],className='dcc_compon',),], className='two columns'), 
        html.Div([dcc.Dropdown(id='Drop_46',placeholder="Select Field",multi=False,clearable=True,disabled=False,style={'display': True}, searchable=True,value='PE_Chg_OI',          
            options=[{"label": x, "value": x} for x in column],className='dcc_compon',),], className='two columns'),    
           ],className='row'), 
        html.Div([dcc.Graph(id='graph_4')],className='row'),],className='row'),                    
                                   
 

]) 

@app.callback(
    Output('Time_drop','options'),
    Input('Date_drop','value'))

def update_dropdown_options(Date_drop):
    date_v = pd.to_datetime(Date_drop)
    dfff = data_eq[data_eq.DATE == date_v.date()] 
    return [{'label':i,'value':i}for i in dfff['Time'].unique()]

@app.callback(
    Output('Time_drop','value'),
    Input('Time_drop','options'))
def get_date_value(time_v):
    return [k['value']for k in time_v][-1]

@app.callback(    
    [Output('my_table', 'data'),
     Output('idr', 'children'),
     Output('my_table', 'page_size')],
    
    [Input('Date_drop', 'value'),
     Input('Time_drop', 'value'),
     Input('optionns', 'value'),     
     Input('row_drop', 'value')],)

def update_dropdown_options(Date_drop,Time_drop,optionns,row_drop):
    print(Date_drop,Time_drop,optionns,row_drop)
    Date_dropp = pd.to_datetime(Date_drop)
    data_eq1 = indexoption(optionns)

    #data_eq1.insert(0, 'DATE', data_eq1.pop('Date1'))
    #data_eq1.drop(['Date'], axis=1, inplace=True)
    dff = data_eq1[(data_eq1['DATE'] == Date_dropp.date()) &  (data_eq1['Time'] == Time_drop)] 

    live_Index2 = eq_idx(optionns)
    live_Index1 = live_Index2[live_Index2.Date == Date_dropp]

    time_ix = np.unique(live_Index1['Time'])[-1]
    dff_idx1 = [x[0] for x in (live_Index1[(live_Index1['Date'] == Date_dropp) &  (live_Index1['Time'] == time_ix)][['Ltp']].values.tolist())]

    if optionns == 'NIFTY':
        dff_idx = (round(([x[0] for x in (live_Index1[(live_Index1['Date'] == Date_dropp) &  (live_Index1['Time'] == time_ix)][['Ltp']].values.tolist())][0])/50,0)*50)
    else:
        dff_idx = (round(([x[0] for x in (live_Index1[(live_Index1['Date'] == Date_dropp) &  (live_Index1['Time'] == time_ix)][['Ltp']].values.tolist())][0])/100,0)*100)

    newstrike = []

    roww = int(row_drop/2)

    for i in range (0,roww):
        if optionns == 'NIFTY':           
            x=(dff_idx+(i*50))
            newstrike.append(x)
        else:
            x=(dff_idx+(i*100))
            newstrike.append(x)
    for i in range (0,roww): 
        if optionns == 'NIFTY':    
            x=(dff_idx+(i*-50))
            newstrike.append(x)
        else:
            x=(dff_idx+(i*-100))
            newstrike.append(x)
    strikelist = [x for x in sorted(newstrike)]
    data = dff[dff.StrikeRate.isin(strikelist)]

    return data.to_dict('records'),dff_idx1, row_drop

@app.callback(     
    Output('graph_1', 'figure'),
    [Input('Date_drop', 'value'),
     Input('Drop_11', 'value'),
     Input('Drop_12', 'value'),
     Input('Drop_13', 'value'),
     Input('Drop_14', 'value'),
     Input('Drop_15', 'value'),
     Input('Drop_16', 'value'),])

def build_graph1(Date_drop,Drop_11,Drop_12, Drop_13, Drop_14,Drop_15, Drop_16):
    date_v = pd.to_datetime(Date_drop)
    dfff = data_eq[data_eq.DATE == date_v.date()] 
    dff11_12 = dfff[dfff.StrikeRate == Drop_11]       
    dff13_14 = dfff[dfff.StrikeRate == Drop_13] 
    dff15_16 = dfff[dfff.StrikeRate == Drop_15]    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=dff11_12['Time'],
    y=dff11_12[Drop_12],
    hovertext='<b>Date</b>: '+dff11_12['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff11_12['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff11_12['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff11_12[Drop_12]]+'<br>',
    hoverinfo="text",
    marker=dict(color="red"),
    name=Drop_12,
    showlegend=True))   

    fig.add_trace(go.Scatter(
    x=dff13_14['Time'],
    y=dff13_14[Drop_14],
    hovertext='<b>Date</b>: '+dff13_14['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff13_14['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff13_14['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff13_14[Drop_14]]+'<br>',
    hoverinfo="text",
    marker=dict(color="green"), 
    name=Drop_14,    
    showlegend=True))

    fig.add_trace(go.Scatter(
    x=dff15_16['Time'],
    y=dff15_16[Drop_16],
    hovertext='<b>Date</b>: '+dff15_16['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff15_16['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff15_16['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff15_16[Drop_16]]+'<br>',
    hoverinfo="text",
    marker=dict(color="blue"), 
    name=Drop_14,    
    showlegend=True))
    
    fig.update_layout(title={'text':f"{Drop_12} value of {Drop_11} & {Drop_14} value of {Drop_13} & {Drop_16} value of {Drop_15}",
                             'font':{'size':20},'x':0.5,'xanchor':'center'})
    # fig.show()
    return fig
      
@app.callback(    
    Output('graph_2', 'figure'),
    [Input('Date_drop', 'value'),
     Input('Drop_21', 'value'),
     Input('Drop_22', 'value'),
     Input('Drop_23', 'value'),
     Input('Drop_24', 'value'),
     Input('Drop_25', 'value'),
     Input('Drop_26', 'value'),])

def build_graph2(Date_drop,Drop_21,Drop_22, Drop_23, Drop_24,Drop_25, Drop_26):
    date_v = pd.to_datetime(Date_drop)
    dfff = data_eq[data_eq.DATE == date_v.date()]   
    dff21_22 = dfff[dfff.StrikeRate == Drop_21]       
    dff23_24 = dfff[dfff.StrikeRate == Drop_23]   
    dff25_26 = dfff[dfff.StrikeRate == Drop_25]    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=dff21_22['Time'],
    y=dff21_22[Drop_22],
    hovertext='<b>Date</b>: '+dff21_22['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff21_22['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff21_22['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff21_22[Drop_22]]+'<br>',
    hoverinfo="text",
    marker=dict(color="red"),
    name=Drop_22,
    showlegend=True))  

    fig.add_trace(go.Scatter(
    x=dff23_24['Time'],
    y=dff23_24[Drop_24],
    hovertext='<b>Date</b>: '+dff23_24['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff23_24['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff23_24['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff23_24[Drop_24]]+'<br>',
    hoverinfo="text",
    marker=dict(color="green"), 
    name=Drop_24,      
    showlegend=True))

    fig.add_trace(go.Scatter(
    x=dff25_26['Time'],
    y=dff25_26[Drop_26],
    hovertext='<b>Date</b>: '+dff25_26['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff25_26['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff25_26['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff25_26[Drop_26]]+'<br>',
    hoverinfo="text",
    marker=dict(color="blue"), 
    name=Drop_26,      
    showlegend=True))
    
    fig.update_layout(title={'text':f"{Drop_22} value of {Drop_21} & {Drop_24} value of {Drop_23} & {Drop_26} value of {Drop_25}",
                             'font':{'size':20},'x':0.5,'xanchor':'center'})
    # fig.show()
    return fig    
   
@app.callback(    
    Output('graph_3', 'figure'),
    [Input('Date_drop', 'value'),
     Input('Drop_31', 'value'),
     Input('Drop_32', 'value'),
     Input('Drop_33', 'value'),
     Input('Drop_34', 'value'),
     Input('Drop_35', 'value'),
     Input('Drop_36', 'value'),])

def build_graph3(Date_drop,Drop_31,Drop_32, Drop_33, Drop_34,Drop_35, Drop_36):
    date_v = pd.to_datetime(Date_drop)
    dfff = data_eq[data_eq.DATE == date_v.date()] 
    dff31_32 = dfff[dfff.StrikeRate == Drop_31]       
    dff33_34 = dfff[dfff.StrikeRate == Drop_33]
    dff35_36 = dfff[dfff.StrikeRate == Drop_35]     
    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=dff31_32['Time'],
    y=dff31_32[Drop_32],
    hovertext='<b>Date</b>: '+dff31_32['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff31_32['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff31_32['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff31_32[Drop_32]]+'<br>',
    hoverinfo="text",
    marker=dict(color="red"),
    name=Drop_32,
    showlegend=True))   

    fig.add_trace(go.Scatter(
    x=dff33_34['Time'],
    y=dff33_34[Drop_34],
    hovertext='<b>Date</b>: '+dff33_34['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff33_34['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff33_34['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff33_34[Drop_34]]+'<br>',
    hoverinfo="text",
    marker=dict(color="green"), 
    name=Drop_34,    
    showlegend=True))

    
    fig.add_trace(go.Scatter(
    x=dff35_36['Time'],
    y=dff35_36[Drop_36],
    hovertext='<b>Date</b>: '+dff35_36['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff35_36['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff35_36['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff35_36[Drop_36]]+'<br>',
    hoverinfo="text",
    marker=dict(color="blue"), 
    name=Drop_36,    
    showlegend=True))
    
    fig.update_layout(title={'text':f"{Drop_32} value of {Drop_31} & {Drop_34} value of {Drop_33} & {Drop_36} value of {Drop_35}",
                             'font':{'size':20},'x':0.5,'xanchor':'center'})
    # fig.show()
    return fig
      
@app.callback(    
    Output('graph_4', 'figure'),
    [Input('Date_drop', 'value'),
     Input('Drop_41', 'value'),
     Input('Drop_42', 'value'),
     Input('Drop_43', 'value'),
     Input('Drop_44', 'value'),
     Input('Drop_45', 'value'),
     Input('Drop_46', 'value'),])

def build_graph4(Date_drop,Drop_41,Drop_42, Drop_43, Drop_44,Drop_45, Drop_46):
    date_v = pd.to_datetime(Date_drop)
    dfff = data_eq[data_eq.DATE == date_v.date()]   
    dff41_42 = dfff[dfff.StrikeRate == Drop_41]       
    dff43_44 = dfff[dfff.StrikeRate == Drop_43] 
    dff45_46 = dfff[dfff.StrikeRate == Drop_45]      
    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=dff41_42['Time'],
    y=dff41_42[Drop_42],
    hovertext='<b>Date</b>: '+dff41_42['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff41_42['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff41_42['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff41_42[Drop_42]]+'<br>',
    hoverinfo="text",
    marker=dict(color="red"),
    name=Drop_42,
    showlegend=True))  

    fig.add_trace(go.Scatter(
    x=dff43_44['Time'],
    y=dff43_44[Drop_44],
    hovertext='<b>Date</b>: '+dff43_44['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff43_44['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff43_44['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff43_44[Drop_44]]+'<br>',
    hoverinfo="text",
    marker=dict(color="green"), 
    name=Drop_44,      
    showlegend=True))

    fig.add_trace(go.Scatter(
    x=dff45_46['Time'],
    y=dff45_46[Drop_46],
    hovertext='<b>Date</b>: '+dff45_46['DATE'].astype(str)+'<br>'+
        '<b>Time</b>: '+dff45_46['Time'].astype(str)+'<br>'+
        '<b>Strike</b>: '+dff45_46['StrikeRate'].astype(str)+'<br>'+
        '<b>Value</b>: '+[f'{x:,.0f}' for x in dff45_46[Drop_46]]+'<br>',
    hoverinfo="text",
    marker=dict(color="blue"), 
    name=Drop_46,      
    showlegend=True))
    
    fig.update_layout(title={'text':f"{Drop_42} value of {Drop_41} & {Drop_44} value of {Drop_43} & {Drop_46} value of {Drop_45}",
                             'font':{'size':20},'x':0.5,'xanchor':'center'})
    # fig.show()
    return fig     

@app.callback(    
    [Output('pcr_table', 'data'),
     Output('pcr_table', 'page_size')],
    
    [Input('Date_drop', 'value'),
     Input('Time_drop', 'value'),
     Input('optionns', 'value'),     
     Input('row_drop', 'value')],)

def pcr(Date_drop,Time_drop,optionns,row_drop):

    
    print(Date_drop,Time_drop,optionns,row_drop)
    Date_dropp = pd.to_datetime(Date_drop)
    dffg = pcr_data(Date_dropp,index)

    return dffg.to_dict('records'), row_drop
