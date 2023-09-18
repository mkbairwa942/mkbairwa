#import yfinance as yf
import ta
import pandas_ta as pta
from finta import TA
# import talib
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from five_paisa import *
from datetime import datetime
import datetime
import time,json,datetime,sys
from datetime import timezone
# from kite_trade import *

from_d = (date.today() - timedelta(days=1))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=10))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
print(from_d)
print(to_d)
#print(to_days)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

symbol1 = '3045'

df = client.historical_data('N', 'C', symbol1, '5m', date(2023, 5, 10), date(2023, 5, 10))
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Date', 'Time','Open','High', 'Low', 'Close',]]
df['Open_per'] = np.round(100-(100*(df['Close'].shift(1))/df['Open']),1)
df['High_per'] = np.round(100-(100*(df['Close'].shift(1))/df['High']),1)
df['Low_per'] = np.round(100-(100*(df['Close'].shift(1))/df['Low']),1)
df['Close_per'] = np.round(100-(100*(df['Close'].shift(1))/df['Close']),1)

df_copy = df[-11:] 
# df_copy_close = df_copy['Close'].iloc[-11]
# print(df_copy_close)       

df1 = client.historical_data('N', 'C', symbol1, '5m', date(2021, 1, 1), date(2021, 6, 30))
df2 = client.historical_data('N', 'C', symbol1, '5m', date(2021, 7, 1), date(2021, 12, 31))
df3 = client.historical_data('N', 'C', symbol1, '5m', date(2022, 1, 1), date(2022, 6, 30))
df4 = client.historical_data('N', 'C', symbol1, '5m', date(2022, 7, 1), date(2022, 12, 31))
df5 = client.historical_data('N', 'C', symbol1, '5m', date(2023, 1, 1), date(2023, 5, 9))
dff = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

dff['Datetime'] = pd.to_datetime(dff['Datetime'])
dff['Date'] = pd.to_datetime(dff['Datetime']).dt.date
dff['Date'] = dff['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
dff['Time'] = pd.to_datetime(dff['Datetime']).dt.time
dff['Time'] = dff['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
dff = dff[['Date', 'Time','Open','High', 'Low', 'Close']]
dff['Open_per'] = np.round(100-(100*(dff['Close'].shift(1))/dff['Open']),1)
dff['High_per'] = np.round(100-(100*(dff['Close'].shift(1))/dff['High']),1)
dff['Low_per'] = np.round(100-(100*(dff['Close'].shift(1))/dff['Low']),1)
dff['Close_per'] = np.round(100-(100*(dff['Close'].shift(1))/dff['Close']),1)
# dff['o_m_1'] = np.where(df_copy['Open_per'].iloc[-10] == dff['Open_per'], "yes","")
# dff['h_m_1'] = np.where(df_copy['High_per'].iloc[-10] == dff['High_per'], "yes","")
# dff['l_m_1'] = np.where(df_copy['Low_per'].iloc[-10] == dff['Low_per'], "yes","")
# dff['c_m_1'] = np.where(df_copy['Close_per'].iloc[-10] == dff['Close_per'], "yes","")
dff['match_1'] = np.where(((np.where(df_copy['Open_per'].iloc[-10] == dff['Open_per'], "yes","")) == "yes") & 
                          ((np.where(df_copy['High_per'].iloc[-10] == dff['High_per'], "yes","")) == "yes") & 
                          ((np.where(df_copy['Low_per'].iloc[-10] == dff['Low_per'], "yes","")) == "yes") & 
                          ((np.where(df_copy['Close_per'].iloc[-10] == dff['Close_per'], "yes","")) == "yes"),
                          "yes","")
# dff['o_m_2'] = np.where(df_copy['Open_per'].iloc[-9] == dff['Open_per'].shift(-1), "yes","")
# dff['h_m_2'] = np.where(df_copy['High_per'].iloc[-9] == dff['High_per'].shift(-1), "yes","")
# dff['l_m_2'] = np.where(df_copy['Low_per'].iloc[-9] == dff['Low_per'].shift(-1), "yes","")
# dff['c_m_2'] = np.where(df_copy['Close_per'].iloc[-9] == dff['Close_per'].shift(-1), "yes","")
dff['match_2'] = np.where(((np.where(df_copy['Open_per'].iloc[-9] == dff['Open_per'].shift(-1), "yes","")) == "yes")
                    & ((np.where(df_copy['High_per'].iloc[-9] == dff['High_per'].shift(-1), "yes","")) == "yes")
                    & ((np.where(df_copy['Low_per'].iloc[-9] == dff['Low_per'].shift(-1), "yes","")) == "yes")
                    & ((np.where(df_copy['Close_per'].iloc[-9] == dff['Close_per'].shift(-1), "yes","")) == "yes"),
                    "yes","")
# dff['o_m_3'] = np.where(df_copy['Open_per'].iloc[-8] == dff['Open_per'].shift(-2), "yes","")
# dff['h_m_3'] = np.where(df_copy['High_per'].iloc[-8] == dff['High_per'].shift(-2), "yes","")
# dff['l_m_3'] = np.where(df_copy['Low_per'].iloc[-8] == dff['Low_per'].shift(-2), "yes","")
# dff['c_m_3'] = np.where(df_copy['Close_per'].iloc[-8] == dff['Close_per'].shift(-2), "yes","")
dff['match_3'] = np.where(((np.where(df_copy['Open_per'].iloc[-8] == dff['Open_per'].shift(-2), "yes","")) == "yes")
                    & ((np.where(df_copy['High_per'].iloc[-8] == dff['High_per'].shift(-2), "yes","")) == "yes")
                    & ((np.where(df_copy['Low_per'].iloc[-8] == dff['Low_per'].shift(-2), "yes","")) == "yes")
                    & ((np.where(df_copy['Close_per'].iloc[-8] == dff['Close_per'].shift(-2), "yes","")) == "yes"),
                    "yes","")
# dff['o_m_4'] = np.where(df_copy['Open_per'].iloc[-7] == dff['Open_per'].shift(-3), "yes","")
# dff['h_m_4'] = np.where(df_copy['High_per'].iloc[-7] == dff['High_per'].shift(-3), "yes","")
# dff['l_m_4'] = np.where(df_copy['Low_per'].iloc[-7] == dff['Low_per'].shift(-3), "yes","")
# dff['c_m_4'] = np.where(df_copy['Close_per'].iloc[-7] == dff['Close_per'].shift(-3), "yes","")
dff['match_4'] = np.where(((np.where(df_copy['Open_per'].iloc[-7] == dff['Open_per'].shift(-3), "yes","")) == "yes")
                    & ((np.where(df_copy['High_per'].iloc[-7] == dff['High_per'].shift(-3), "yes","")) == "yes")
                    & ((np.where(df_copy['Low_per'].iloc[-7] == dff['Low_per'].shift(-3), "yes","")) == "yes")
                    & ((np.where(df_copy['Close_per'].iloc[-7] == dff['Close_per'].shift(-3), "yes","")) == "yes"),
                    "yes","")
# dff['o_m_5'] = np.where(df_copy['Open_per'].iloc[-6] == dff['Open_per'].shift(-4), "yes","")
# dff['h_m_5'] = np.where(df_copy['High_per'].iloc[-6] == dff['High_per'].shift(-4), "yes","")
# dff['l_m_5'] = np.where(df_copy['Low_per'].iloc[-6] == dff['Low_per'].shift(-4), "yes","")
# dff['c_m_5'] = np.where(df_copy['Close_per'].iloc[-6] == dff['Close_per'].shift(-4), "yes","")
dff['match_5'] = np.where(((np.where(df_copy['Open_per'].iloc[-6] == dff['Open_per'].shift(-4), "yes","")) == "yes")
                    & ((np.where(df_copy['High_per'].iloc[-6] == dff['High_per'].shift(-4), "yes","")) == "yes") 
                    & ((np.where(df_copy['Low_per'].iloc[-6] == dff['Low_per'].shift(-4), "yes","")) == "yes") 
                    & (np.where(df_copy['Close_per'].iloc[-6] == dff['Close_per'].shift(-4), "yes","") == "yes"),
                    "yes","")

print("Excel Starting....")
if not os.path.exists("hist_analysis.xlsx"):
    try:
        wb = xw.Book()
        wb.save("hist_analysis.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('hist_analysis.xlsx')
for i in ["Data","stats","stats1","Exchange"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
st = wb.sheets("stats")
st1 = wb.sheets("stats1")
ex = wb.sheets("Exchange")
dt.range("a:k").value = None
st.range("a:k").value = None
st1.range("a:aj").value = None
ex.range("a:k").value = None

try:
    time.sleep(0.5)
    dt.range("a1").value = df
    st.range("a1").value = df_copy
    st1.range("a1").value = dff
    #ex.range("a1").value = script_code_5paisa
    #ex.range("a1").value = master_contract
except Exception as e:
    print(e)