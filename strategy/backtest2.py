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
from kite_trade import *

from_d = (date.today() - timedelta(days=36))
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

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url)

enctoken = "ZEYTwpVbWDGxf91XntlGJEFfogKYV/Ltb4h0JgpQ9sn2lOhgfFpVaFC6TyuCfjLR19qpiVCyNEz4Sc0XW40hP6eBtPDQCHdq+l+jBWMSeJovzCmNnY6cqg=="
kite = KiteApp(enctoken=enctoken)

master_contract = pd.DataFrame(kite.instruments())
#print(master_contract.tail(10))

symbol1 = '35018'
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
def symbols_backtesting(symbol_list):
    all_trades = []
    position = None
    new_trade = pd.DataFrame()
    trade = {"Symbol": None, "Buy_Sell": None,"Entry_Date": None,"Entry_Time": None,  "Entry": None,"Exit_Date": None,"Exit_Time": None, "Exit": None, }
    for symbol in symbol_list:
        df["Symbol"] = symbol
        df["MA_10"] = np.round((pta.ema(df["Close"], length=10)),2)
        df["MA_13"] = np.round((pta.ema(df["Close"], length=13)),2)
        df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
        df['Entry'] = np.where((df["MA_10"] > df["MA_13"]) & (df["RSI_14"] > 60), "Buy",np.where((df["MA_10"] < df["MA_13"]) & (df["RSI_14"] < 40), "Sell",""))
        df["Exit1"] = np.where((df['Date'].shift(-1) != df['Date']),"TimeExit","")
        df['Exit'] = np.where((df["MA_10"] < df["MA_13"]) & (df["RSI_14"] < 40), "Buy_Exit",np.where((df["MA_10"] > df["MA_13"]) & (df["RSI_14"] > 60), "Sell_Exit",np.where(df["Exit1"] == "TimeExit", "Time_Exit","")))
        

        for i in df.index[14:]:
            if df["Entry"][i] == "Buy" and position != "Buy":
                trade["Symbol"] = symbol
                trade["Buy_Sell"] = "Buy"
                trade["Entry"] = df["Close"][i]
                trade["Entry_Date"] = df["Date"][i]
                trade["Entry_Time"] = df["Time"][i]
                trade["Entry_Volume"] = df["Volume"][i]
                trade["Entry_MA_10"] = df["MA_10"][i]
                trade["Entry_MA_13"] = df["MA_13"][i]
                trade["Entry_RSI_14"] = df["RSI_14"][i]
                all_trades.append(copy.deepcopy(trade)) 
                position = "Buy"
            if df["Exit1"][i] == "TimeExit" or df["Exit"][i] == "Buy_Exit" and position == "Buy":
                trade["Exit"] = df["Close"][i]
                trade["Exit_Date"] = df["Date"][i]
                trade["Exit_Time"] = df["Time"][i]
                trade["Exit_Volume"] = df["Volume"][i]
                trade["Exit_MA_10"] = df["MA_10"][i]
                trade["Exit_MA_13"] = df["MA_13"][i]
                trade["Exit_RSI_14"] = df["RSI_14"][i]
                all_trades.append(copy.deepcopy(trade)) 
                position = None
            if df["Entry"][i] == "Sell" and position != "Sell":
                trade["Symbol"] = symbol
                trade["Buy_Sell"] = "Sell"
                trade["Entry"] = df["Close"][i]
                trade["Entry_Date"] = df["Date"][i]
                trade["Entry_Time"] = df["Time"][i]
                trade["Entry_Volume"] = df["Volume"][i]
                trade["Entry_MA_10"] = df["MA_10"][i]
                trade["Entry_MA_13"] = df["MA_13"][i]
                trade["Entry_RSI_14"] = df["RSI_14"][i]
                all_trades.append(copy.deepcopy(trade)) 
                position = "Sell"
            if df["Exit1"][i] == "TimeExit" or df["Exit"][i] == "Sell_Exit" and position == "Sell":
                trade["Exit"] = df["Close"][i]
                trade["Exit_Date"] = df["Date"][i]
                trade["Exit_Time"] = df["Time"][i]
                trade["Exit_Volume"] = df["Volume"][i]
                trade["Exit_MA_10"] = df["MA_10"][i]
                trade["Exit_MA_13"] = df["MA_13"][i]
                trade["Exit_RSI_14"] = df["RSI_14"][i]
                all_trades.append(copy.deepcopy(trade)) 
                position = None  
    # sett = all_trades[-1]
    # sett1 = all_trades[-1]['Entry']
    # print(sett)      
    # print(type(sett))
    # print(sett1)      
    # print(type(sett1))
    all_trades1 = pd.DataFrame(all_trades)


    # or int((all_trades["Entry"][-1]) - StopLoss) > df["Close"][i]
    #or int((all_trades["Entry"][-1]) + StopLoss) > df["Close"][i] 
    new_trade = all_trades1[all_trades1['Entry_Date'] == all_trades1['Exit_Date']]
    new_trade1 = new_trade[new_trade['Entry'] != new_trade['Exit']]
    new_trade2 = new_trade1[new_trade1['Entry_Time'] < new_trade1['Exit_Time']]
  
    #new_trade3 = new_trade2.drop_duplicates(inplace=True)
    new_trade3 = new_trade2.drop_duplicates(ignore_index=True).copy()
    #all_trades1.drop_duplicates(inplace=True)

    j = -3
    if new_trade3['Buy_Sell'].iloc[j] == "Sell":
        print("Sell")
        print((new_trade3['Entry'].iloc[j]))
        print((new_trade3['Entry'].iloc[j]) + SellSl)
        #new_trade3['Exit'] = (new_trade3['Entry'].iloc[j]) + SellSl
    if new_trade3['Buy_Sell'].iloc[j] == "Buy" and (new_trade3['Exit'].iloc[j] - new_trade3['Entry'].iloc[j]) < -BuySl:
        print("new")
        print((new_trade3['Entry'].iloc[j]) + BuySl)        
    else:
        print("old")
        print((new_trade3['Entry'].iloc[j]))
        
        #print((new_trade3['Entry'].iloc[-2]))
        #new_trade3['Exit'] = (new_trade3['Entry'].iloc[-1]) + BuySl
    # print(new_trade3['Entry'].iloc[-1])
    # print(type(new_trade3['Entry'].iloc[-1]))
    return new_trade3

symbol_list = ["35018"]

data = symbols_backtesting(symbol_list)
data1 = pd.DataFrame(data)
data2 = data.values.tolist()

if data2:
    risk_percent = 100
    df = pd.DataFrame(data)
    df["P/L"] = np.round((np.where(df["Buy_Sell"] == "Buy", (100*(df["Exit"] - df["Entry"]))/risk_percent,
                        (100*(df["Entry"] - df["Exit"]))/risk_percent)),2)
    df["Probability"] = np.round((100*(np.where(df["P/L"] > 0, 1, 0).cumsum())/(np.where(df["P/L"] != np.NaN, 1, 0).cumsum())),2)
    df["Return"] = np.round((df["P/L"].cumsum()),2)
    df["Drawdown"] = np.round((df["Return"] - (df["Return"].cummax().apply(lambda x: x if x > 0 else 0))),2)

else:
    print("No Trades")
       
print("Excel Starting....")
if not os.path.exists("Backtesting1.xlsx"):
    try:
        wb = xw.Book()
        wb.save("Backtesting1.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Backtesting1.xlsx')
for i in ["Data","stats","Exchange"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
st = wb.sheets("stats")
ex = wb.sheets("Exchange")
dt.range("a:w").value = None
st.range("a:w").value = None
ex.range("a:w").value = None
dt.range(f"a1:q1").value = ["Symbol","Buy_Sell","Entry","Entry Date","Exit","Exit Date",
                            "Entry Volume","Entry MA_10","Entry MA_13","Entry RSI_14","Exit Volume","Exit MA_10","Exit MA_13","Exit RSI_14"]
                            #" P/L","Probability","Return","Drawdown"]

try:
    time.sleep(0.5)
    dt.range("a1").value = df3
    st.range("a1").value = df
    #ex.range("a1").value = script_code_5paisa
    ex.range("a1").value = master_contract
except Exception as e:
    print(e)








