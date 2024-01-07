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
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from pandas import concat, DataFrame
from pandas_ta import Imports
from pandas_ta.overlap import ema
from pandas_ta.utils import get_offset, verify_series, signals

from_d = (date.today() - timedelta(days=4))
from_d = date(2023, 12, 1)

to_d = (date.today())
to_d = date(2024, 1, 5)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

symbol1 = '50481'

df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)

# df['Datetime'] = pd.to_datetime(df['Datetime'])
# df['Date'] = pd.to_datetime(df['Datetime']).dt.date
# df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
# df['Time'] = pd.to_datetime(df['Datetime']).dt.time
# df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
#df.set_index('Datetime',inplace=True)
df.ta.fisher(append=True)

a = pta.adx(df['High'], df['Low'], df['Close'], length = 14)
df = df.join(a)
b = pta.macd(df["Close"],12,26)
df = df.join(b)
df.rename(columns={'FISHERT_9_1': 'Fis_GRN','FISHERTs_9_1':'Fis_RED','MACD_12_26_9':'Macd_GRN','MACDs_12_26_9':'Macd_RED'}, inplace=True)
df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
df["EMA_9"] = np.round((pta.ema(df["Close"], length=9)),2)
df['Adx_curve'] = np.where(df['ADX_14'] > df['ADX_14'].shift(1),"YES","")
df['Pri_up_Ema'] = np.where(df['Close'] > df['EMA_9'],"YES","")
df['Fish_cross'] = np.where(df['Fis_GRN'] > df['Fis_RED'],"YES","")
df['Final'] = np.where((df['Adx_curve'] == "YES") & (df['Pri_up_Ema'] == "YES") & (df['Adx_curve'] == "YES"),"YES","")
df3 = df         
df = df[['Datetime','Open','High','Low','Close','Volume','Fis_GRN','Fis_RED','ADX_14','EMA_9','Final','Macd_GRN','Macd_RED','RSI_14']]

df['Buy'] = np.where((df['Final'].shift(1)=="") & (df['Final'] == "YES"),"Buy","")
df['Benchmark'] = df['High'].cummax()
df['TStopLoss'] = df['Benchmark'] * 0.98

df_buy = df[df['Buy'] == 'Buy']

buy_order_list = df_buy['Datetime'].tolist()

print(buy_order_list)

five_df1 = pd.DataFrame()
five_df2 = pd.DataFrame()
five_df3 = pd.DataFrame()
five_df4 = pd.DataFrame()
five_df5 = pd.DataFrame()
five_df6 = pd.DataFrame()
bhv_fo1 = pd.DataFrame()
one_day = pd.DataFrame()

SLL = 10
TGT = 20

for a in buy_order_list:
    orderboo = df[(df['Datetime'] == a)]
    orderboo.sort_values(['Datetime'], ascending=[True], inplace=True)
    #print(orderboo.head(1))
    dfgg_up_1 = orderboo.iloc[[0]]
    #print(dfgg_up_1)
    #Buy_Scriptcodee = int(dfgg_up_1['Scripcode'])
    #Buy_Name = list(dfgg_up_1['Name'])[0]
    Buy_price = float(dfgg_up_1['Close'])                 
    Buy_Stop_Loss = float(round((dfgg_up_1['Close'] - (dfgg_up_1['Close']*SLL)/100),1))  
    Buy_Target = float(round((((dfgg_up_1['Close']*TGT)/100) + dfgg_up_1['Close']),1))
    # Buy_Exc = 'N' #list(dfgg_up_1['Exch'])[0]
    # Buy_Exc_Type = 'D' #list(dfgg_up_1['ExchType'])[0]
    # Buy_Qty = int(dfgg_up_1['LotSize'])
    
    Buy_timee = list(dfgg_up_1['Datetime'])[0]
    # print(Buy_timee)
    # print(Buy_timee)
    #Buy_timee1 = str(Buy_timee).replace(' ','T')

    dfg1 = client.historical_data('N', 'D', symbol1, '1m',from_d, to_d) 
    print(dfg1.head(1))
    # print(dfg1.tail(2))
    #dfg1['Scripcode'] = a
    #dfg1['ScripName'] = Buy_Name
    dfg1['Entry_Date'] = Buy_timee
    dfg1['Entry_Price'] = Buy_price
    # print(dfg1.head(2))
    dfg1.sort_values(['Datetime'], ascending=[True], inplace=True)
    dfg1['OK_DF'] = np.where(dfg1['Entry_Date'] < dfg1['Datetime'],"OK","")
    dfg1['StopLoss'] = Buy_Stop_Loss
    dfg1['Target'] = Buy_Target

    dfg2 = dfg1[(dfg1["OK_DF"] == "OK")]
    dfg2['Benchmark'] = dfg2['High'].cummax()
    dfg2['TStopLoss'] = dfg2['Benchmark'] * 0.95
    dfg2['BValue'] = dfg2['Entry_Price']*15
    
    dfg2['TGT_SL'] = np.where(dfg2['High'] > Buy_Target,"TGT",np.where(dfg2['Low'] < Buy_Stop_Loss,"SL",""))
    dfg2['SValue'] = np.where(dfg2['TGT_SL'] == "SL",Buy_Stop_Loss*15,np.where(dfg2['TGT_SL'] == "TGT",Buy_Target*15,""))  
    
    dfg2['P&L_SL'] = pd.to_numeric(dfg2['SValue']) - dfg2['BValue']
    dfg2['Qty'] = 15
    dfgg2 = dfg2.copy()
    five_df2 = pd.concat([dfg2, five_df2])
    dfg3 = dfg2[(dfg2['TGT_SL'] != '')]    
    dfg4 = dfg3.iloc[0:1]
    five_df1 = pd.concat([dfg4, five_df1])

    dfgg2['TGT_TSL'] = np.where(dfgg2['Low'] < dfgg2['TStopLoss'],"TSL",np.where(dfgg2['Low'] < Buy_Stop_Loss,"SL",""))
    
    five_df4 = pd.concat([dfgg2, five_df4])
    dfgg3 = dfgg2[(dfgg2['TGT_TSL'] != '')] 
    dfgg4 = dfgg3.iloc[0:1]
    #dfgg4['P&L'] = (dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*Buy_Qty
    dfgg4['P&L_TSL'] = np.where(dfgg4['TGT_TSL'] == "SL",(dfgg4['StopLoss'] - dfgg4['Entry_Price'])*15,np.where(dfgg4['TGT_TSL'] == "TSL",(dfgg4['TStopLoss'] - dfgg4['Entry_Price'])*15,"" ))
    five_df3 = pd.concat([dfgg4, five_df3])

# SLL = 20
# TGG = 70
# # BuySl = SL*-1
# # SellSl = SL*1
# # print(BuySl,SellSl)
# df['TP'] = df.Close + TGG
# df['SL'] = df.Close - SLL


print("Excel Starting....")
if not os.path.exists("haresh_backtest.xlsx"):
    try:
        wb = xw.Book()
        wb.save("haresh_backtest.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('haresh_backtest.xlsx')
for i in ["Data","Buy","Sale","Final","DF1","DF2","DF3","DF4","DF5","DF6"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
fl = wb.sheets("Final")
by = wb.sheets("Buy")
sl = wb.sheets("Sale")
df1 = wb.sheets("DF1")
df2 = wb.sheets("DF2")
df3 = wb.sheets("DF3")
df4 = wb.sheets("DF4")
df5 = wb.sheets("DF5")
df6 = wb.sheets("DF6")


dt.range("a:z").value = None
by.range("a:z").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
df1.range("a:az").value = None
df2.range("a:az").value = None
df3.range("a:az").value = None
df4.range("a:az").value = None
df5.range("a:az").value = None
df6.range("a:az").value = None


try:
    time.sleep(0.5)
    dt.range("a1").value = df
    by.range("a1").value = df_buy
    five_df1.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df1.range("a1").value = five_df1
    five_df2.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df2.range("a1").value = five_df2
    five_df3.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df3.range("a1").value = five_df3
    five_df4.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df4.range("a1").value = five_df4
    five_df5.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df5.range("a1").value = five_df5
    five_df6.sort_values(['Entry_Date'], ascending=[True], inplace=True)
    df6.range("a1").value = five_df6
    # sl.range("a1").value = Selling
    # fl.range("a1").value = new_df1
except Exception as e:
    print(e)
