import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import numpy as np
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlalchemy
import pandas as pd
import logging
from holidayss import holidays
import pandas as pd
import time
from datetime import date, datetime, timedelta
from dateutil.utils import today
# from py5paisa import FivePaisaClient
# import sqlalchemy
# from time import sleep
# import environ
# from pathlib import Path
# import sys

# logger = logging.getLogger(__name__)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.options.mode.chained_assignment = None

# # nse = NSELive()

# # env = Env()
# # env.read_env()

# sys.path.insert(0, r'/var/www/Capital_vercel1/capitalsscopeproj/Dash_app/holidayss')

# BASE_DIR = Path(__file__).resolve().parent.parent

# env=environ.Env(
#     DEBUG=(bool,False)
# )

# environ.Env.read_env(BASE_DIR / ".env")

# cred = {
#     "APP_NAME": '5P57141743',
#     "APP_SOURCE":'9997',
#     "USER_ID":'5SP0ws0uCmc',
#     "PASSWORD":'C0VIQHnMEpI',
#     "USER_KEY":'BT5DqKIGqnKmHiZnzGXKZ2aBql4oYBRp',
#     "ENCRYPTION_KEY":'tTEQPwp3Gfh2l3LWqDb2UC1sD0IFvzV5',
    
# }

# #cred = env('cred')
# #cred=env({'cred'})

# user='mukeshbairwa942@gmail.com'
# pwd='navya@1234'
# dob='19860518'

# client = FivePaisaClient(email=user, passwd=pwd, dob=dob, cred=cred)
# client.login()
# # print(cred)

# engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

# from_d = (date.today() - timedelta(days=30))
# # from_d = date(2022, 12, 29)

# to_d = (date.today())
# # to_d = date(2023, 1, 23)

# symbol = 'MOTHERSUMI'
# # print(from_d)
# # print(to_d)

# # df=client.historical_data('N','C',3045,'1d',from_d,to_d)
# #print(df.head(5))

# datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
# dates = datess[::-1]
# intraday = datess[-2]
# lastTradingDay = dates[1]

# intradayy = intraday.date()
# #print(intradayy)
# lastTradingDayy =  lastTradingDay.date()
# #print(dates)

# current_time = (datetime.now()).strftime("%H:%M")


# indexx = 'BANKNIFTY'

# eq_bhav = (f"SELECT distinct * FROM capitalsscope.live_Index where Symbol = '{indexx}';")
# data_eq = pd.read_sql(sql=eq_bhav, con=engine)
# data_eq3 = data_eq[data_eq.Date == intraday]
# print(data_eq3.tail(2))

# # X = deque(maxlen=20)
# # Y = deque(maxlen=20)
# # X.append(1)
# # Y.append(1)

# app = dash.Dash(__name__)
# app.layout = html.Div([
#     dcc.Graph(id='live_graph',animate=True),
#     dcc.Interval(id='graph_update',interval=1*10000),
# ])

# @app.callback(Output('live_graph','figure'),
#             [Input('graph_update', 'n_intervals')])
# def update_graph(input_data):
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#     x=data_eq3['Time'],
#     y=round(data_eq3['Ltp'],0),
#     marker=dict(color="red"),
#     name='LTP',
#     showlegend=True)) 
#     fig.update_layout(title={'text':f"LTP of {indexx}",
#                              'font':{'size':20},'x':0.5,'xanchor':'center'})
    
#     return fig
#     # global X
#     # global Y
#     # X.append(df3['Time'])
#     # Y.append(df3['Ltp'])

#     # data = go.Scatter(
#     #     x= list(X),
#     #     y = list(Y),
#     #     name = "Scatter",
#     #     mode='lines+markers'
#     # )
#     # return {'data':[data],'layout':go.Layout(xaxis=dict(range=[min(X),max(X)]),
#     #                                          yaxis=dict(range=[min(Y),max(Y)]))}

# if __name__=="__main__":
#     app.run_server(debug=True)
# #     #app.run_server(host='0.0.0.0', port=8080 ,debug=True)

# ------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='my_interval',
    disabled=False,
    interval=1*3000,
    n_intervals=0,
    max_intervals=100,
    ),
    html.Div(id='output_data',style={"font-size":36}),
    dcc.Input(id="input_text",type="text"),
    dcc.Graph(id="mybarchart"),
])

@app.callback(
    [Output("output_data",'children'),
    Output('mybarchart','figure')],
    [Input('my_interval','n_intervals')]
)

def update_grapg(num):
    "update every 3 second"
    if num ==0:
        raise PreventUpdate
    else:
        y_data = num
        fig=go.Figure(data=[go.Bar(x=[1,2,3,4,5,6,7,8,9],y=[y_data]*9)],
        layout=go.Layout(yaxis=dict(tickfont=dict(size=22))))
    return (y_data,fig)

@app.callback(
    Output('my_interval','max_intervals'),
    [Input('input_text','value')]
)

def stop_interval(retrived_text):
    if retrived_text == 'stop':
        max_intervals = 0
    else:
        raise PreventUpdate
    return (max_intervals)

if __name__=="__main__":
    app.run_server(debug=True)

# nse = NSELive()

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.options.mode.chained_assignment = None

# from_d = (date.today() - timedelta(days=30))
# # from_d = date(2022, 12, 29)

# to_d = (date.today())
# # to_d = date(2022, 12, 30)

# symbol = 'MOTHERSUMI'
# # print(from_d)
# # print(to_d)

# datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
# dates = datess[::-1]
# intraday = datess[-1]
# lastTradingDay = dates[1]

# # print(lastTradingDay)
# # print(intraday)

# engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')
# engine1 = sqlalchemy.create_engine('mysql+pymysql://root:Jencocotfab@301@5.183.11.143:3306/capitalsscope')

# sqlquery2 = (f"select * from capitalsscope.full_bhavcopy where DATE1 between '{from_d}' and '{lastTradingDay}'order "
#              f"by DATE1 asc;")

# df = pd.read_sql(sql=sqlquery2, con=engine)
# # print(df.head(20))
# dff = df.groupby('SYMBOL', as_index=False)[['OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE',
#                                             'DELIV_PER']].sum()
# # print(dff)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# app = DjangoDash('stock_dashboard', external_stylesheets=external_stylesheets)

# app.layout = html.Div([
#     html.Div([
#         dash_table.DataTable(
#             id='datatable_id',
#             data=dff.to_dict('records'),
#             columns=[
#                 {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
#             ],
#             editable=False,
#             filter_action='native',
#             sort_action='native',
#             sort_mode='multi',
#             row_selectable='multi',
#             row_deletable=False,
#             selected_rows=[],
#             page_action='native',
#             page_current=0,
#             page_size=10,
#             # page_action='none',
#             # style_cell={'whiteSpace': 'normal'},
#             # fixed_rows={'headers': True, 'data': 0},
#             # virtualization=False,
#             style_cell_conditional=[
#                 {'if': {'column_id': 'SYMBOL'},
#                  'width': '20%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'OPEN_PRICE'},
#                  'width': '16%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'HIGH_PRICE'},
#                  'width': '16%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'LOW_PRICE'},
#                  'width': '16%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'CLOSE_PRICE'},
#                  'width': '16%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'DELIV_PER'},
#                  'width': '16%', 'textAlign': 'left'},
#             ],
#         ),
#     ], className='row'),

#     html.Div([
#         html.Div([
#             dcc.Dropdown(id='linedropdown',
#                          options=[
#                              {'label': 'Open_Price', 'value': 'OPEN_PRICE'},
#                              {'label': 'High_Price', 'value': 'HIGH_PRICE'},
#                              {'label': 'Low_Price', 'value': 'LOW_PRICE'},
#                              {'label': 'Close_Price', 'value': 'CLOSE_PRICE'},
#                              {'label': 'Deliv_Per', 'value': 'DELIV_PER'}
#                          ],
#                          value='CLOSE_PRICE',
#                          multi=False,
#                          clearable=False
#                          ),
#         ], className='six columns'),

#         html.Div([
#             dcc.Dropdown(id='piedropdown',
#                          options=[
#                              {'label': 'Open_Price', 'value': 'OPEN_PRICE'},
#                              {'label': 'High_Price', 'value': 'HIGH_PRICE'},
#                              {'label': 'Low_Price', 'value': 'LOW_PRICE'},
#                              {'label': 'Close_Price', 'value': 'CLOSE_PRICE'},
#                              {'label': 'Deliv_Per', 'value': 'DELIV_PER'}
#                          ],
#                          value='CLOSE_PRICE',
#                          multi=False,
#                          clearable=False
#                          ),
#         ], className='six columns'),
#     ], className='row'),

#     html.Div([
#         html.Div([
#             dcc.Graph(id='linechart'),
#         ], className='six columns'),

#         html.Div([
#             dcc.Graph(id='piechart'),
#         ], className='six columns'),

#     ], className='row'),

# ])


# @app.callback(
#     [Output('piechart', 'figure'),
#      Output('linechart', 'figure')],
#     [Input('datatable_id', 'selected_rows'),
#      Input('piedropdown', 'value'),
#      Input('linedropdown', 'value')],
# #      manager=long_callback_manager
# )
# def update_data(chosen_rows, piedropval, linedropval):
#     #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     print(chosen_rows)
#     if len(chosen_rows) == 0:
#         df_filtered = dff[dff['SYMBOL'].isin(['SBIN', 'BHARTIARTL', 'GAIL', 'IOC', 'HDFCBANK'])]
#     else:
#         # print(chosen_rows)
#         df_filtered = dff[dff.index.isin(chosen_rows)]

#     pie_chart = px.pie(
#         data_frame=df_filtered,
#         names='SYMBOL',
#         values=piedropval,
#         hole=.3,
#         labels={'SYMBOL': 'Symbols'},
#     )
#     list_chosen_symbols = df_filtered['SYMBOL'].tolist()
#     df_line = df[df['SYMBOL'].isin(list_chosen_symbols)]

#     line_chart = px.line(
#         data_frame=df_line,
#         x='DATE1',
#         y=linedropval,
#         color='SYMBOL',
#         labels={'SYMBOL': 'Symbols', 'DATE1': 'Date'},
#     )
#     line_chart.update_layout(uirevision='foo')

#     return (pie_chart, line_chart)



