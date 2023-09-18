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
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
# print(from_d)
# print(to_d)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

symbol1 = '35002'


df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
df.set_index('Datetime',inplace=True)
df3 = df         

def fisher1(high, low, length=None, signal=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    hl2_ = hl2(high, low)
    highest_hl2 = hl2_.rolling(length).max()
    lowest_hl2 = hl2_.rolling(length).min()

    #hlr = high_low_range(highest_hl2, lowest_hl2)
    hlr  = highest_hl2-lowest_hl2
    hlr[hlr < 0.001] = 0.001

    position = ((hl2_ - lowest_hl2) / hlr) - 0.5
    v = 0
    m = high.size
    result = [npNaN for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        v = 0.66 * position[i] + 0.67 * v
        if v < -0.99: v = -0.999
        if v >  0.99: v =  0.999
        result.append(0.5 * (nplog((1 + v) / (1 - v)) + result[i - 1]))
    fisher = Series(result, index=high.index)
    signalma = fisher.shift(signal)


    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    props = f"{length}_{signal}"
    fisher.name = f"FISHERT{props}"
    signalma.name = f"FISHERTs{props}"
    fisher.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {fisher.name: fisher, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"FISHERT{props}"
    df.category = fisher.category
    return df

def macd(close, fast=None, slow=None, signal=None, talib=None, offset=None, **kwargs):
    """Indicator: Moving Average, Convergence/Divergence (MACD)"""
    # Validate arguments
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast
    close = verify_series(close, max(fast, slow, signal))
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None: return

    as_mode = kwargs.setdefault("asmode", False)

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import MACD
        macd, signalma, histogram = MACD(close, fast, slow, signal)
    else:
        fastma = ema(close, length=fast)
        slowma = ema(close, length=slow)

        macd = fastma - slowma
        signalma = ema(close=macd.loc[macd.first_valid_index():,], length=signal)
        histogram = macd - signalma

    if as_mode:
        macd = macd - signalma
        signalma = ema(close=macd.loc[macd.first_valid_index():,], length=signal)
        histogram = macd - signalma

    # Offset
    if offset != 0:
        macd = macd.shift(offset)
        histogram = histogram.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        macd.fillna(kwargs["fillna"], inplace=True)
        histogram.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        macd.fillna(method=kwargs["fill_method"], inplace=True)
        histogram.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _asmode = "AS" if as_mode else ""
    _props = f"_{fast}_{slow}_{signal}"
    macd.name = f"MACD{_asmode}{_props}"
    histogram.name = f"MACD{_asmode}h{_props}"
    signalma.name = f"MACD{_asmode}s{_props}"
    macd.category = histogram.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {macd.name: macd, histogram.name: histogram, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"MACD{_asmode}{_props}"
    df.category = macd.category

    signal_indicators = kwargs.pop("signal_indicators", False)
    if signal_indicators:
        signalsdf = concat(
            [
                df,
                signals(
                    indicator=histogram,
                    xa=kwargs.pop("xa", 0),
                    xb=kwargs.pop("xb", None),
                    xserie=kwargs.pop("xserie", None),
                    xserie_a=kwargs.pop("xserie_a", None),
                    xserie_b=kwargs.pop("xserie_b", None),
                    cross_values=kwargs.pop("cross_values", True),
                    cross_series=kwargs.pop("cross_series", True),
                    offset=offset,
                ),
                signals(
                    indicator=macd,
                    xa=kwargs.pop("xa", 0),
                    xb=kwargs.pop("xb", None),
                    xserie=kwargs.pop("xserie", None),
                    xserie_a=kwargs.pop("xserie_a", None),
                    xserie_b=kwargs.pop("xserie_b", None),
                    cross_values=kwargs.pop("cross_values", False),
                    cross_series=kwargs.pop("cross_series", True),
                    offset=offset,
                ),
            ],
            axis=1,
        )

        return signalsdf
    else:
        return df

macdd = (macd(df["Close"],fast=12, slow=26, signal=9, talib=None, offset=None))

fisher_transform = (fisher1(high=df['High'],low=df['Low'],length=20))
# fisher_transform1 = fisher_transform
# FISHERT9_1 = fisher_transform1.columns[0]
# FISHERT9_11 = FISHERT9_1
# FISHERTs9_1 = fisher_transform1.columns[1]
# FISHERTs9_11 = FISHERTs9_1

df["MA_5"] = np.round((pta.ema(df["Close"], length=5)),2)
#df["MA_20"] = np.round((pta.ema(df["Close"], length=20)),2)
df['MACD_WH'] = np.round((macdd[macdd.columns[0]]),2)
df['MACD_RED'] = np.round((macdd[macdd.columns[2]]),2)
df['MACD_HIST'] = np.round((macdd[macdd.columns[1]]),2)

# df['FISHERT_WH'] = np.round((fisher_transform[fisher_transform.columns[0]]),2)
# df['FISHERTs_RED'] = np.round((fisher_transform[fisher_transform.columns[1]]),2)
print(df.tail(5))
# for i in (10,13):
#     df['EMA_'+str(i)] = np.round((ta.trend.ema_indicator(df.Close, window=i)),2)
# df['atr'] = np.round((ta.volatility.average_true_range(df.High,df.Low,df.Close)),2)


SLL = 20
TGG = 70
# BuySl = SL*-1
# SellSl = SL*1
# print(BuySl,SellSl)
df['TP'] = df.Close + TGG
df['SL'] = df.Close - SLL

# df['TP'] = df.Close + (df.atr * 2)
# df['SL'] = df.Close - (df.atr * 3)






df['Entry'] = np.where(((np.where((df['High'].shift(1))<(df['MA_5'].shift(1)),"B_E",""))=="B_E") & ((np.where(df['Close']>df['MA_5'],"B_E",""))=="B_E"),"B_E",
                  np.where(((np.where((df['Low'].shift(1))>(df['MA_5'].shift(1)),"S_E",""))=="S_E") & ((np.where(df['Close']<df['MA_5'],"S_E",""))=="S_E"),"S_E",""))
#df['Entry'] = np.where((df.FISHERT_WH > df.FISHERTs_RED),"B_E",np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E",npNaN))
df['Entry'] = df['Entry'].ffill()
df['Entry1'] = np.where((df['Entry'] == "B_E") & (df['Entry'].shift(1) != "B_E"),"B_E",np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E",""))
df['Ent_A'] = (np.where(df['Entry1'] == "B_E",df['Close'],(np.where(df['Entry1'] == "S_E",df['Close'],npNaN))))
df['Ent_A'] = df['Ent_A'].ffill()
df['Ent_B'] = df['Close']-df['Ent_A']
df['Ent_B'] = np.where(df['Entry'] == "B_E",(df['Close']-df['Ent_A']),np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0))
df['Ent_C'] = np.where(((df['Entry'] == "B_E") & (df['Ent_B'] <= - SLL)),"B_SL",np.where(((df['Entry'] == "B_E") & (df['Ent_B'] >= TGG)),"B_TP",
              np.where(((df['Entry'] == "S_E") & (df['Ent_B'] <= - SLL)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_B'] >= TGG)),"S_TP",""))))

# df['Entry'] = np.where((df.FISHERT_WH < df.FISHERTs_RED),"S_E","")
# df['Entry1'] = np.where((df['Entry'] == "S_E") & (df['Entry'].shift(1) != "S_E"),"S_E","")
# df['Ent_A'] = (np.where(df['Entry1'] == "S_E",df['Close'],npNaN))
# df['Ent_A'] = df['Ent_A'].ffill()
# df['Ent_Bb'] = np.where(df['Entry'] == "S_E", (df['Ent_A'] - df['Close']),0)
# df['Ent_Cb'] = np.where(((df['Entry'] == "S_E") & (df['Ent_Bb'] <= - SLL)),"S_SL",np.where(((df['Entry'] == "S_E") & (df['Ent_Bb'] >= TGG)),"S_TP",""))

df.dropna(inplace=True)

length = len(df)-1

Buying = pd.DataFrame()
Selling = pd.DataFrame()
new_df1 = pd.DataFrame()    

for i in range(len(df)):
    if [i+1][0] <= length:
        if df['Entry1'].iloc[i + 1] == "B_E":
            bay = (df['Ent_A'].iloc[i + 1])
            buyy = df[i+1:i+2]
            Buying = pd.concat([buyy, Buying])
            sal = df[df['Ent_A'] == bay]
            sal1 = (sal[(sal['Ent_C'] == "B_SL") | (sal['Ent_C'] == "B_TP")])
            sal1['Sell_Date'] = (df.Date.iloc[i + 1])
            sal1['Sell_Time'] = (df.Time.iloc[i + 1])
            Selling = pd.concat([sal1[:1], Selling])

        if df['Entry1'].iloc[i + 1] == "S_E":
            bay1 = (df['Ent_A'].iloc[i + 1])
            buyy1 = df[i+1:i+2]
            Buying = pd.concat([buyy1, Buying])
            sal1 = df[df['Ent_A'] == bay1]
            sal11 = (sal1[(sal1['Ent_C'] == "S_SL") | (sal1['Ent_C'] == "S_TP")])
            sal11['Sell_Date'] = (df.Date.iloc[i + 1])
            sal11['Sell_Time'] = (df.Time.iloc[i + 1])
            Selling = pd.concat([sal11[:1], Selling])

Buying.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True) 
Buying.rename(columns={'Date': 'Datee', 'Time': 'Timee'}, inplace=True)
Selling.sort_values(['Date', 'Time'], ascending=[True, True], inplace=True)  
Selling.rename(columns={'Sell_Date': 'Datee', 'Sell_Time': 'Timee'}, inplace=True)
new_df1 = pd.merge(Buying, Selling,on=["Datee", "Timee"])

# selldates = []
# outcome = []

# for i in range(length):
#     if df.Buysignal.iloc[i]:
#         k = 1
#         SL = df.SL.iloc[i]     
#         TP = df.TP.iloc[i]
#         in_position = True
#         while in_position:
#             if [i+k][0] <= length:
#                 looping_close = df.Close.iloc[i + k]
#                 if looping_close >= TP:
#                     selldates.append(df.iloc[i+k].name)
#                     outcome.append('TP')
#                     in_position = False
#                 elif looping_close <= SL:
#                     selldates.append(df.iloc[i+k].name)
#                     outcome.append('SL')                         
#                 k += 1
#                 in_position = False           

# df.loc[selldates, "Sellsignal"] = 1
# df.Sellsignal = df.Sellsignal.fillna(0).astype(int)
# df['Sellsignal1'] = np.where((df['Sellsignal'] == 1) & (df['Sellsignal'].shift(1) == 0),1,0)
# df.loc[selldates, "outcome"] = outcome
# buyyy = df[(df.Buysignal1 == 1)]
# mask2 = df[(df.Sellsignal1 == 1)]
# print(mask2.outcome.value_counts().sum())
# print(mask2.outcome.value_counts())

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
for i in ["Data","Buy","Sale","Final"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
by = wb.sheets("Buy")
sl = wb.sheets("Sale")
fl = wb.sheets("Final")
dt.range("a:z").value = None
by.range("a:z").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None

try:
    time.sleep(0.5)
    dt.range("a1").value = df
    by.range("a1").value = Buying
    sl.range("a1").value = Selling
    fl.range("a1").value = new_df1
except Exception as e:
    print(e)
