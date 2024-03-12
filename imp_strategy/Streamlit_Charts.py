import streamlit as st
import pandas as pd
from datetime import datetime
from five_paisa import *
from bokeh.plotting import figure,column
from bokeh.models import HoverTool
import numpy as np
import pandas_ta as pta
import altair as alt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

#credi_har = credentials("HARESH")

from_d = (date.today() - timedelta(days=15))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

days_365 = (date.today() - timedelta(days=50))
print(days_365)

# holida = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
# holida["Date"] = holida["Date1"].dt.date
# holida1 = np.unique(holida['Date'])

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C")#, holidays=holida1)
trading_dayss = trading_days_reverse[::-1]
# trading_dayss1 = ['2024-01-20', '2024-01-19','2024-01-18']
# trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[0]
second_last_trading_day = trading_days[2]

# trading_days = trading_dayss[1:]
# current_trading_day = trading_dayss[1]
# last_trading_day = trading_days[1]
# second_last_trading_day = trading_days[2]


print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last 365 Day is :- "+str(days_365))

st.set_page_config(layout="wide",page_title="Candlestick App with Technical Indicators")
@st.cache_data
def load_exc():
    '''
    all - scrips across all segments
    bse_eq - BSE Equity
    nse_eq - NSE Equity
    nse_fo - NSE Derivatives
    bse_fo - BSE Derivatives
    ncd_fo - NSE Currecny
    mcx_fo - MCX
    '''
    segment_fo = "nse_fo"
    exc_fo = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment_fo}"
    exc_fo1 = pd.read_csv(exc_fo,low_memory=False)
    # print(len(exc_fo1))
    exc_fo2 = exc_fo1[(exc_fo1["Exch"] == "N")]# & (exc_fo1["Series"] == "XX")]# & (script_code_5paisa1['ExchType'].isin(['D']))]
    exc_fo3 = exc_fo2[(exc_fo2['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
    exc_fo_list = (np.unique(exc_fo3['SymbolRoot']).tolist())

    segment_eq = "nse_eq"
    exc_eq = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment_eq}"
    exc_eq1 = pd.read_csv(exc_eq,low_memory=False)
    exc_eq2 = exc_eq1[(exc_eq1['SymbolRoot'].isin(exc_fo_list))]
    return exc_eq2



symb  = load_exc()
# print(symb)
# print(len(symb))
exc_eq_list_scpt = (np.unique(symb['ScripCode']).tolist())
exc_eq_list_sym = (np.unique(symb['SymbolRoot']).tolist())

st.sidebar.header('User Input Features')
select_symbol = st.sidebar.selectbox('Symbol',list(exc_eq_list_sym))
df_frame = symb[symb['SymbolRoot'] == select_symbol]
df_scpt = (np.unique([int(i) for i in df_frame['ScripCode']])).tolist()[0]

#st.subheader('Shown are the stock closing price and volume of "'+str(select_symbol) + '" for 50 Days Data')
st.subheader(':green[Candle]:red[stick] Pattern Technical Analysis of "'+str(select_symbol)+ '" with :tea: :coffee:')
st.sidebar.markdown("#### Date Range Selection")
print(select_symbol)

col1,col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(label="Start Date:", value=datetime(2023,9,1))
with col2:
    end_date = st.date_input(label="End Date:", value=current_trading_day)

print(start_date,end_date)

close_line = st.sidebar.checkbox(label="Close Price Line")
volume = st.sidebar.checkbox(label="Include ADX & Trading Volume")


@st.cache_data
def load_dataset(scpt):
    df = client.historical_data('N', 'C', scpt, '1d',start_date,end_date)
    df = df.astype({"Datetime": "datetime64[ns]"})    
    df["Date"] = df["Datetime"].dt.date
    df["BarColor"] = df[['Open','Close']].apply(lambda o:'red' if o.Open > o.Close else 'green',axis=1)
    df['Date_str'] = df['Date'].astype(str)
    df['EMA_21'] = np.round((pta.ema(df['Close'],length=21)),2)
    df['SMA_21'] = np.round((pta.sma(df['Close'],length=21)),2)
    df['DEMA_21'] = np.round((pta.dema(df['Close'],length=21)),2)
    ADX = pta.adx(high=df['High'],low=df['Low'],close=df['High'],length=14)
    df['ADX_14'] = np.round((ADX[ADX.columns[0]]),2)
    #df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
    return df

df1 = load_dataset(df_scpt)
dff = df1[50:]
print(dff.head(2))
indicator_colors = {"SMA_21":"blue","DEMA_21":"yellow","EMA_21":"red"}


def create_chart(df,close_line=False,include_vol=False,indicators=[]):
    candle=figure(x_axis_type="datetime",height=400,width=1200,
                  tooltips=[("Date","@Date_str"),("Open","@Open"),("High","@High"),("Low","@Low"),("Close","@Close"),("SMA_21","@SMA_21"),("DEMA_21","@DEMA_21"),("EMA_21","@EMA_21")],)
    candle.segment("Date","Low","Date","High",color="black",line_width=0.5,source=df)
    candle.segment("Date","Open","Date","Close",color="BarColor",line_width=3 if len(df)>100 else 6,source=df)

    candle.xaxis.axis_label="Date"
    candle.yaxis.axis_label="Price"
    if close_line:
        candle.line("Date","Close",color="black",source=df)

    for indicator in indicators:
        candle.line("Date",indicator,color=indicator_colors[indicator],line_width=2,source=df,legend_label=indicator)

    adx=None
    if include_vol:
        adx = figure(x_axis_type="datetime",height=200,width=1200)
        adx.segment("Date",0,"Date","ADX_14",line_width=2 if len(df)>100 else 6,line_color="BarColor",alpha=0.8,source=df)
        adx.yaxis.axis_label="ADX_14"

    volume=None
    if include_vol:
        volume = figure(x_axis_type="datetime",height=200,width=1200)
        volume.segment("Date",0,"Date","Volume",line_width=2 if len(df)>100 else 6,line_color="BarColor",alpha=0.8,source=df)
        volume.yaxis.axis_label="volume"

    return column(children=[candle,adx,volume],sizing_mode="scale_width") if volume else candle

talib_indicators = ["EMA_21","SMA_21","DEMA_21"]

indicators = st.sidebar.multiselect(label="Technical Indicators",options=talib_indicators)

sub_df = dff.set_index("Date").loc[start_date:end_date]
sub_df = sub_df.reset_index()

fig = create_chart(sub_df,close_line,volume,indicators)

st.bokeh_chart(fig,use_container_width=True)
xx = list(sub_df['Datetime'])
yy = list(sub_df['ADX_14'])
# st.line_chart(sub_df['ADX_14'],height=200,color="#ffaa00",use_container_width=True)
# st.line_chart(dff['Close'])

c = alt.Chart(sub_df, title='ADX Line Chart').mark_line().encode(
     x='Datetime', y='ADX_14')

st.altair_chart(c, use_container_width=True)

st.write('Data Dimension '+str(dff.shape[0])+ ' rows and ' + str(dff.shape[1])+ ' columns')
st.dataframe(dff)














# python -m streamlit run Streamlit_Charts.py