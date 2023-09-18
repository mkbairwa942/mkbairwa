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
from backtesting import Strategy, Backtest

from_d = (date.today() - timedelta(days=27))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

symbol = 'MOTHERSUMI'
print(from_d)
print(to_d)
#print(to_days)

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

intradayy = intraday.date()
lastTradingDayy =  lastTradingDay.date()
print(dates)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url)
print(script_code_5paisa.tail(5))

symbol1 = '37834'
SL = 20
BuySl = SL*-1
SellSl = SL*1
print(BuySl,SellSl)

df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
df3 = df                        

#Check if NA values are in data
df=df[df['Volume']!=0]
df.isna().sum()
#df.reset_index(drop=True, inplace=True)

df['ATR'] = pta.atr(high=df['High'], low=df['Low'], close=df['Close'], length=14)


def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1['Low'][i]>df1['Low'][i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1['Low'][i]<df1['Low'][i-1]):
            return 0
    return 1

def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1['High'][i]<df1['High'][i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1['High'][i]>df1['High'][i-1]):
            return 0
    return 1

length = len(df)
high = list(df['High'])
low = list(df['Low'])
close = list(df['Close'])
open = list(df['Open'])
bodydiff = [0] * length

highdiff = [0] * length
lowdiff = [0] * length
ratio1 = [0] * length
ratio2 = [0] * length

# EurUSD set
mybodydiff = 0.000001
mybodydiffmin = 0.002

def isEngulfing(l):
    row=l
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row]<mybodydiff:
        bodydiff[row]=mybodydiff      

    bodydiffmin = mybodydiffmin
    if (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
        open[row-1]<close[row-1] and
        open[row]>close[row] and 
        (open[row]-close[row-1])>=-0e-5 and close[row]<open[row-1]): #+0e-5 -5e-5
        return 1

    elif(bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
        open[row-1]>close[row-1] and
        open[row]<close[row] and 
        (open[row]-close[row-1])<=+0e-5 and close[row]>open[row-1]):#-0e-5 +5e-5
        return 2
    else:
        return 0

def isStar(l):
    bodydiffmin = mybodydiffmin
    row=l
    highdiff[row] = high[row]-max(open[row],close[row])
    lowdiff[row] = min(open[row],close[row])-low[row]
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row]<mybodydiff:
        bodydiff[row]=mybodydiff
    ratio1[row] = highdiff[row]/bodydiff[row]
    ratio2[row] = lowdiff[row]/bodydiff[row]

    if (ratio1[row]>1 and lowdiff[row]<0.2*highdiff[row] and bodydiff[row]>bodydiffmin):# and open[row]>close[row]):
        return 1
    elif (ratio2[row]>1 and highdiff[row]<0.2*lowdiff[row] and bodydiff[row]>bodydiffmin):# and open[row]<close[row]):
        return 2
    else:
        return 0
    
def closeResistance(l,levels,lim):
    if len(levels)==0:
        return 0
    #!!!
    #lim=df.ATR[l]/2
    
    #diff between high and closest level among levels
    c1 = abs(df['High'][l]-min(levels, key=lambda x:abs(x-df['High'][l])))<=lim
    #diff between higher body and closest level to high
    c2 = abs(max(df['Open'][l],df['Close'][l])-min(levels, key=lambda x:abs(x-df['High'][l])))<=lim
    #min body less than closest level to high
    c3 = min(df['Open'][l],df['Close'][l])<min(levels, key=lambda x:abs(x-df['High'][l]))
    #low price less than closest level to high
    c4 = df['Low'][l]<min(levels, key=lambda x:abs(x-df['High'][l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0
    
def closeSupport(l,levels,lim):
    if len(levels)==0:
        return 0
    #!!!
    #lim=df.ATR[l]/2
    c1 = abs(df['Low'][l]-min(levels, key=lambda x:abs(x-df['Low'][l])))<=lim
    c2 = abs(min(df['Open'][l],df['Close'][l])-min(levels, key=lambda x:abs(x-df['Low'][l])))<=lim
    c3 = max(df['Open'][l],df['Close'][l])>min(levels, key=lambda x:abs(x-df['Low'][l]))
    c4 = df['High'][l]>min(levels, key=lambda x:abs(x-df['Low'][l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0

n1=2
n2=2
backCandles=45
signal = [0] * length

for row in range(backCandles, len(df)-n2):
    ss = []
    rr = []
    for subrow in range(row-backCandles+n1, row+1):
        if support(df, subrow, n1, n2):
            ss.append(df['Low'][subrow])
        if resistance(df, subrow, n1, n2):
            rr.append(df['High'][subrow])
    
    #!!!! parameters
    myclosedistance = 150e-5 #EURUSD
    if ((isEngulfing(row)==1 or isStar(row)==1) and closeResistance(row, rr, myclosedistance) ):#and df.RSI[row]<30
        signal[row] = 1
    elif((isEngulfing(row)==2 or isStar(row)==2) and closeSupport(row, ss, myclosedistance)):#and df.RSI[row]>70
        signal[row] = 2
    else:
        signal[row] = 0

df['signal']=signal
# print(df.tail(20))

# print(df[df['signal']==1].count(),df[df['signal']==2].count())
print(df[df['signal']==1],df[df['signal']==2])

def SIGNAL():
    return df['signal']

# Trader fixed SL and TP
class MyCandlesStrat(Strategy):  
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next() 
        if self.signal1==2:
            sl1 = self.data.Close[-1] -30 # 550e-4 #EURUSD
            tp1 = self.data.Close[-1] +50 # 600e-4
            self.buy(sl=sl1, tp=tp1)
        elif self.signal1==1:
            sl1 = self.data.Close[-1] +50#  550e-4 #EURUSD
            tp1 = self.data.Close[-1] -30#  600e-4
            self.sell(sl=sl1, tp=tp1)
bt = Backtest(df, MyCandlesStrat, cash=100000, commission=.000)
stat = bt.run()
bt.plot()
print(stat)
print()

# # ATR related SL and TP
# class MyCandlesStrat(Strategy): 
#     atr_f = 0.2
#     ratio_f = 1
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next() 
#         if self.signal1==2:
#             sl1 = self.data.Close[-1] - self.data.ATR[-1]/self.atr_f
#             tp1 = self.data.Close[-1] + self.data.ATR[-1]*self.ratio_f/self.atr_f
#             self.buy(sl=sl1, tp=tp1)
#         elif self.signal1==1:
#             sl1 = self.data.Close[-1] + self.data.ATR[-1]/self.atr_f
#             tp1 = self.data.Close[-1] - self.data.ATR[-1]*self.ratio_f/self.atr_f
#             self.sell(sl=sl1, tp=tp1)
# bt = Backtest(df, MyCandlesStrat, cash=100000, commission=.000)
# stat = bt.run()
# print(stat)

# #fixed distance Trailing SL
# class MyCandlesStrat(Strategy):
#     sltr=500e-4 #EURUSD
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next()
#         sltr = self.sltr
#         for trade in self.trades: 
#             if trade.is_long: 
#                 trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - sltr)
#             else:
#                 trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + sltr) 

#         if self.signal1==2 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] - sltr
#             self.buy(sl=sl1)
#         elif self.signal1==1 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] + sltr
#             self.sell(sl=sl1)


# bt = Backtest(df, MyCandlesStrat, cash=10_000, commission=.000)
# stat = bt.run()
# stat

# #ATR distance Trailing SL
# class MyCandlesStrat(Strategy):
#     atr_f = 1
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next()
#         for trade in self.trades: 
#             if trade.is_long: 
#                 trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.data.ATR[-1]/self.atr_f)
#             else:
#                 trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.data.ATR[-1]/self.atr_f)

#         if self.signal1==2 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] - self.data.ATR[-1]/self.atr_f
#             self.buy(sl=sl1)
#         elif self.signal1==1 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] + self.data.ATR[-1]/self.atr_f
#             self.sell(sl=sl1)
# bt = Backtest(df, MyCandlesStrat, cash=10_000, commission=.000)
# stat = bt.run()
# stat

# df['signal']=signal

# df[df['signal']==2].count()

# df_test=df.iloc[:]
# df_test.columns = ['Local time','Open', 'High', 'Low', 'Close', 'Volume', 'signal']
# df_test

# def SIGNAL():
#     return df_test.signal

# #fixed distance Trailing SL
# from backtesting import Strategy, Backtest
# import numpy as np

# class MyCandlesStrat(Strategy):
#     sltr=500e-4
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next()
#         sltr = self.sltr
#         for trade in self.trades: 
#             if trade.is_long: 
#                 trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - sltr)
#             else:
#                 trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + sltr) 

#         if self.signal1==2 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] - sltr
#             self.buy(sl=sl1)
#         elif self.signal1==1 and len(self.trades)==0: # trades number change!
#             sl1 = self.data.Close[-1] + sltr
#             self.sell(sl=sl1)


# bt = Backtest(df_test, MyCandlesStrat, cash=10_000, commission=.000)
# stat = bt.run()
# stat

# bt.plot()