import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from five_paisa import *
import pandas_ta as pta
import numpy as np
import xlwings as xw
import time,json,datetime,sys

from_d = (date.today() - timedelta(days=35))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

print(from_d)
print(to_d)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

indexx = 'BANKNIFTY'
type = "FUT"

script_code_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_codee = pd.read_csv(script_code_url)
script_codee['text_new'] = script_codee['Name'].str.split(' ').str[0]
script_codee0 = script_codee[script_codee['text_new'] == indexx]
script_codee0.sort_values(['Expiry'], ascending=[True], inplace=True)

if type == "EQ":
    script_code = script_codee0[script_codee['CpType'] == 'XX']
    script_code1 = script_code[script_codee['Series'] == 'EQ']
    expiry = (pd.to_datetime(script_code1['Expiry']).dt.date).values.tolist()[0]
    symbol = (script_code1["Scripcode"]).values.tolist()[0]
    lotsize = (script_code1['LotSize']).values.tolist()
if type == "FUT":
    script_code = script_codee0[script_codee['CpType'] == 'XX']
    script_code1 = script_code[script_codee['Series'] == 'XX']
    expiry = (pd.to_datetime(script_code1['Expiry']).dt.date).values.tolist()[0]
    symbol = (script_code1["Scripcode"]).values.tolist()[0]
    lotsize = (script_code1['LotSize']).values.tolist()[0]
if type == "OPT":
    script_code = script_codee0[script_codee['CpType'] != 'XX']
    script_code1 = script_code[script_codee['Series'] == 'XX']
    expiry = pd.unique((pd.to_datetime(script_code1['Expiry']).dt.date).values.tolist())
    symbol = pd.unique((script_code1["Scripcode"]).values.tolist())
    lotsize = (script_code1['LotSize']).values.tolist()[0]

script_code2 = script_code1[["Exch","ExchType","Scripcode","Name","Series","Expiry","CpType","StrikeRate","LotSize"]]
# print(script_code2.head(6))
# print(lotsize)
# print(expiry)
# print(symbol)

df = client.historical_data('N', 'D', symbol, '5m', from_d, to_d) 
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.index = pd.DatetimeIndex(df['Datetime'])

def back(symbol):
    for sym in symbol:
        df["Symbol"] = sym
        df["MA_10"] = np.round((pta.ema(df["Close"], length=10)),2)
        df["MA_13"] = np.round((pta.ema(df["Close"], length=13)),2)
        df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
        df['Entry'] = np.where((df["MA_10"] > df["MA_13"]) & (df["RSI_14"] > 60), "Buy",np.where((df["MA_10"] < df["MA_13"]) & (df["RSI_14"] < 40), "Sell",""))
        df["Exit1"] = np.where((df['Date'].shift(-1) != df['Date']),"TimeExit",np.where((df["MA_10"] > df["MA_13"]) & (df["RSI_14"] > 60), "Buy",np.where((df["MA_10"] < df["MA_13"]) & (df["RSI_14"] < 40), "Sell","")))
        df['Exit'] = np.where((df["MA_10"] < df["MA_13"]) & (df["RSI_14"] < 40), "Buy_Exit",np.where((df["MA_10"] > df["MA_13"]) & (df["RSI_14"] > 60), "Sell_Exit",np.where(df["Exit1"] == "TimeExit", "Time_Exit","")))
    return df

bdk = back(indexx)
# print(bdk.tail(5))

class Golden(Strategy):


    def init(self):
        pass

    def next(self):
        current_signal = self.data.Exit1
        if current_signal == "Buy":
            if not self.position:
                self.buy()
        if current_signal == "Sell":
            if self.position:
                self.sell()
        # if (crossover(self.ema10,self.ema13 )) and self.rsi >60:
        #     self.buy()
        # elif (crossover(self.ema13,self.ema10)) and self.rsi < 40:
        #     self.sell()



bt = Backtest(bdk,Golden,cash=100000,commission=0.000,exclusive_orders=True)
#optim = bt.optimize(n1=range(50, 160, 10), n2=range(50, 160, 10),constraint=lambda x: x.n2 - x.n1 > 20,maximize='Return [%]' )
               
stats = bt.run()
bt.plot() 
stat = pd.DataFrame(stats)
print(stat)
print(stat.info())
trades = pd.DataFrame(stats['_trades'])
print(trades)
print(trades.info())


print("Excel Starting....")
if not os.path.exists("Backtest_new1.xlsx"):
    try:
        wb = xw.Book()
        wb.save("Backtest_new1.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Backtest_new1.xlsx')
for i in ["script","Data","stats","trades"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
st = wb.sheets("script")
dt = wb.sheets("Data")
stt = wb.sheets("stats")
tra = wb.sheets("trades")

st.range("a:w").value = None
dt.range("a:w").value = None
stt.range("a:w").value = None
tra.range("a:w").value = None


try:
    time.sleep(0.5)
    st.range("a1").value = script_codee
    dt.range("a1").value = bdk    
    stt.range("a1").value = stat
    tra.range("a1").value = trades
except Exception as e:
    print(e)









