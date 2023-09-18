# from ta import add_all_ta_features as ta
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from five_paisa import *
import pandas_ta as pta
#from kite_trade import *
#import talib

from_d = (date.today() - timedelta(days=36))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

print(from_d)
print(to_d)
#print(to_days)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# enctoken = "ZEYTwpVbWDGxf91XntlGJEFfogKYV/Ltb4h0JgpQ9sn2lOhgfFpVaFC6TyuCfjLR19qpiVCyNEz4Sc0XW40hP6eBtPDQCHdq+l+jBWMSeJovzCmNnY6cqg=="
# kite = KiteApp(enctoken=enctoken)

symbol = '35018'
df = client.historical_data('N', 'D', symbol, '5m', from_d, to_d) 
#df = pd.DataFrame(df)
# df['Daate'] = (pd.to_datetime(df['Datetime']))                               

# for d in df['Daate']:
#    df['date'] = d.date()
#    df['time'] = d.time()
# df1 = df.set_index(['Daate'])   

df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = (pd.to_datetime(df['Datetime']).dt.time).astype(str)
#df['Time'] = (df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))).astype(str)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.index = pd.DatetimeIndex(df['Datetime'])
print(df.tail(5))
print(df.info())     
#exittime = datetime.strptime("15:25:00", '%H:%M:%S')
exittime = "15:25:00"
print(exittime)
print(type(exittime))


class SMAcross(Strategy):
    n1 = 10
    n2 = 13
    n3 = 14
    upb = 60
    lob = 40
    
    def init(self):
        close = self.data.Close
        self.ema10 = self.I(ta.trend.ema_indicator,pd.Series(close),self.n1)
        self.ema13 = self.I(ta.trend.ema_indicator,pd.Series(close),self.n2)
        self.rsi = self.I(ta.momentum.rsi,pd.Series(close),self.n3)

    def next(self):
        price = self.data.Close
        sl = 50

        if self.ema10 > self.ema13  and self.rsi > self.upb:
            if not self.position :
                #self.buy() 
                self.buy(sl = price - sl)               
        if self.data.Time == "15:20:00" or self.ema10 < self.ema13  and self.rsi < self.lob:
            if self.position.is_long:
                self.position.close()
        if self.ema10 < self.ema13  and self.rsi < self.lob:
            if not self.position :
                #self.sell() 
                self.sell(sl = price + sl)               
        if self.data.Time == "15:20:00" or self.ema10 > self.ema13  and self.rsi > self.upb:
            if self.position.is_short:
                self.position.close()



bt = Backtest(df,SMAcross,cash=100000,commission=0.000,exclusive_orders=True)
#optim = bt.optimize(n1=range(50, 160, 10), n2=range(50, 160, 10),constraint=lambda x: x.n2 - x.n1 > 20,maximize='Return [%]' )
               
stats = bt.run()
bt.plot() 
print(stats)
print(stats['_trades'])