#import yfinance as yf
from contourpy import Mpl2005ContourGenerator
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import requests
import sqlalchemy
from io import BytesIO
from zipfile import ZipFile
#from five_paisa1 import *
from five_paisa import *
import time
import multiprocessing as mp

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


print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last 365 Day is :- "+str(days_365))

def bhavcopy(lastTradingDay):
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
    #bh_df = pd.DataFrame(bh_df)
    #bh_df.to_sql(name="full_bhavcopy", con=engine, if_exists="append", index=False)
    #print(bh_df.head(2))
    return bhav_eq

def bhavcopy_fno(lastTradingDay):
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
    #fo_df = pd.DataFrame(fo_df)
    #fo_df.to_sql(name="FO_bhavcopy", con=engine, if_exists="append", index=False)
    #print(fo_df.head(2))
    return bhav_fo

def fii_openint_down(lastTradingDay):
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
        #fii_op_int.to_sql(name="FII_DII_Open_Int", con=engine, if_exists="append", index=False)
        print(fii_op_int.head(1))
        print("Data Successfully updated for " + lastTradingDay)
    except:
        pass
    return fii_op_int

def fii_vol_down(lastTradingDay):
    try:
        dmyformat = datetime.strftime(lastTradingDay, '%d%m%Y')
        url = 'https://archives.nseindia.com/content/nsccl/fao_participant_vol_' + dmyformat + '.csv'
        # tablename = 'fii_dii_volume'
        fii_op_vol = pd.read_csv(url, skiprows=1)
        fii_op_vol = fii_op_vol.drop(fii_op_vol.index[4])
        fii_op_vol.insert(0, 'Date', lastTradingDay)
        fii_op_vol['Date'] = pd.to_datetime(fii_op_vol['Date'])
        fii_op_vol.columns = [c.strip() for c in fii_op_vol.columns.values.tolist()]
        #fii_op_vol.to_sql(name="FII_DII_Volume", con=engine, if_exists="append", index=False)
        print(fii_op_vol.head(1))
        print("Data Successfully updated for " + lastTradingDay)
    except:
        pass
    return fii_op_vol

# dfg = bhavcopy(last_trading_day)
# print(dfg.head(2))
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
    # print(exc_fo_list)
    # print(len(exc_fo_list))

    segment_eq = "nse_eq"
    exc_eq = f"https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/{segment_eq}"
    exc_eq1 = pd.read_csv(exc_eq,low_memory=False)
    # print(len(exc_eq1))
    # exc_eq2 = exc_eq1[(exc_eq1["Exch"] == "N") & (exc_eq1["Series"] == "XX")]# & (script_code_5paisa1['ExchType'].isin(['D']))]
    exc_eq2 = exc_eq1[(exc_eq1['SymbolRoot'].isin(exc_fo_list))]
    # print(exc_eq2)

    # print(exc_eq_list_scpt)
    # print(len(exc_eq_list_scpt))
    # print(exc_eq_list_sym)
    # print(len(exc_eq_list_sym))
    return exc_eq2



symb  = load_exc()
# print(symb)
# print(len(symb))
exc_eq_list_scpt = (np.unique(symb['ScripCode']).tolist())
exc_eq_list_sym = (np.unique(symb['SymbolRoot']).tolist())
# print(exc_eq_list_sym)
stock = 999920005



st.sidebar.header('User Input Features')
select_symbol = st.sidebar.selectbox('Symbol',list(exc_eq_list_sym))
#select_symbol = st.sidebar.multiselect('Symbol',exc_eq_list_sym,exc_eq_list_sym)
df_frame = symb[symb['SymbolRoot'] == select_symbol]
df_scpt = (np.unique([int(i) for i in df_frame['ScripCode']])).tolist()[0]

st.title("Simple Stock Price App")
st.subheader('Shown are the stock closing price and volume of "'+str(select_symbol) + '" for 50 Days Data')
st.markdown("""This app is simple web scraping""")
print(select_symbol)

def generate_new_data():
# loop = st.checkbox('Update Continuously')
# while loop:
    while True:
        time.sleep(5)
        df = client.historical_data('N', 'C', df_scpt, '1m', last_trading_day,current_trading_day)
        df = df.astype({"Datetime": "datetime64[ns]"})    
        df["Date"] = df["Datetime"].dt.date
        df.set_index("Datetime", inplace = True)
        print(df.tail(2))  
        return df
        

def load_data():
    # loop = st.checkbox('Update Continuously')
    # dff = generate_new_data()
    while True:
        dff = generate_new_data()
        st.line_chart(dff['Close'])
        st.line_chart(dff['Volume'])


        st.header('Display Stocks Stats of Selected Stocks')
        st.write('Data Dimension '+str(dff.shape[0])+ ' rows and ' + str(dff.shape[1])+ ' columns')
        st.dataframe(dff)

while True:
    load_data()






# python -m streamlit run Streamlit_Stock.py