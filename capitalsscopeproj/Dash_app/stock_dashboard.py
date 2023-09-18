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
# import diskcache
# cache = diskcache.Cache("./cache")
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

# print(lastTradingDay)
# print(intraday)

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')
engine1 = sqlalchemy.create_engine('mysql+pymysql://root:Jencocotfab@301@5.183.11.143:3306/capitalsscope')

sqlquery2 = (f"select * from capitalsscope.full_bhavcopy where DATE1 between '{from_d}' and '{lastTradingDay}'order "
             f"by DATE1 asc;")

df = pd.read_sql(sql=sqlquery2, con=engine)
# print(df.head(20))
dff = df.groupby('SYMBOL', as_index=False)[['OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE',
                                            'DELIV_PER']].sum()
# print(dff)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = DjangoDash('stock_dashboard', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
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
            page_size=10,
            # page_action='none',
            # style_cell={'whiteSpace': 'normal'},
            # fixed_rows={'headers': True, 'data': 0},
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'SYMBOL'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'OPEN_PRICE'},
                 'width': '16%', 'textAlign': 'left'},
                {'if': {'column_id': 'HIGH_PRICE'},
                 'width': '16%', 'textAlign': 'left'},
                {'if': {'column_id': 'LOW_PRICE'},
                 'width': '16%', 'textAlign': 'left'},
                {'if': {'column_id': 'CLOSE_PRICE'},
                 'width': '16%', 'textAlign': 'left'},
                {'if': {'column_id': 'DELIV_PER'},
                 'width': '16%', 'textAlign': 'left'},
            ],
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                         options=[
                             {'label': 'Open_Price', 'value': 'OPEN_PRICE'},
                             {'label': 'High_Price', 'value': 'HIGH_PRICE'},
                             {'label': 'Low_Price', 'value': 'LOW_PRICE'},
                             {'label': 'Close_Price', 'value': 'CLOSE_PRICE'},
                             {'label': 'Deliv_Per', 'value': 'DELIV_PER'}
                         ],
                         value='CLOSE_PRICE',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),

        html.Div([
            dcc.Dropdown(id='piedropdown',
                         options=[
                             {'label': 'Open_Price', 'value': 'OPEN_PRICE'},
                             {'label': 'High_Price', 'value': 'HIGH_PRICE'},
                             {'label': 'Low_Price', 'value': 'LOW_PRICE'},
                             {'label': 'Close_Price', 'value': 'CLOSE_PRICE'},
                             {'label': 'Deliv_Per', 'value': 'DELIV_PER'}
                         ],
                         value='CLOSE_PRICE',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
        ], className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ], className='six columns'),

    ], className='row'),

])


@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')],
#      manager=long_callback_manager
)
def update_data(chosen_rows, piedropval, linedropval):
    #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(chosen_rows)
    if len(chosen_rows) == 0:
        df_filtered = dff[dff['SYMBOL'].isin(['SBIN', 'BHARTIARTL', 'GAIL', 'IOC', 'HDFCBANK'])]
    else:
        # print(chosen_rows)
        df_filtered = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filtered,
        names='SYMBOL',
        values=piedropval,
        hole=.3,
        labels={'SYMBOL': 'Symbols'},
    )
    list_chosen_symbols = df_filtered['SYMBOL'].tolist()
    df_line = df[df['SYMBOL'].isin(list_chosen_symbols)]

    line_chart = px.line(
        data_frame=df_line,
        x='DATE1',
        y=linedropval,
        color='SYMBOL',
        labels={'SYMBOL': 'Symbols', 'DATE1': 'Date'},
    )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart, line_chart)



