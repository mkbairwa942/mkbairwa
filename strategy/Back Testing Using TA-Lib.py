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

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url)

symbol1 = '37834'

df = client.historical_data('N', 'D', symbol1, '5m', '2023-03-01', '2023-03-23')
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
                         
def symbols_backtesting(symbol_list):
    all_trades = []
    
    for symbol in symbol_list:
        #df = yf.Ticker(f"{symbol}.NS").history(period="5y", interval="1d")
        
        # df.columns = df.columns.str.replace(" ","")
        # df["Datetime"] = df["Datetime"].replace('T', " ")

        # df['Dates'] = pd.to_datetime(df['Datetime']).dt.date
        # df['Time'] = pd.to_datetime(df['Datetime']).dt.time
        df["Symbol"] = symbol
        df["MA_10"] = np.round((pta.ema(df["Close"], length=10)),2)
        df["MA_13"] = np.round((pta.ema(df["Close"], length=13)),2)
        df["RSI_14"] = np.round((pta.rsi(df["Close"], length=14)),2)
        print(df.head(3))
        # df["ATR_14"] = talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)
        # df["Upper_Band"], df["Middle_Band"], df["Lower_Band"] = talib.BBANDS(df["Close"], timeperiod=20,
        #                                                                      nbdevup=2,nbdevdn=2)

        trade = {"Symbol": None, "Buy/Sell": None,"Entry Date": None,"Entry Time": None,  "Entry": None,"Exit Date": None,"Exit Time": None, "Exit": None, }
        position = None
        for i in df.index[15:]:
            if df["MA_10"][i] > df["MA_13"][i] and df["RSI_14"][i] > 60 and position != "Buy":
                
                if trade["Symbol"] is not None:
                    trade["Exit"] = df["Close"][i]
                    trade["Exit Date"] = df["Date"][i]
                    trade["Exit Time"] = df["Time"][i]
                    trade["Exit Volume"] = df["Volume"][i]
                    trade["Exit MA_10"] = df["MA_10"][i]
                    trade["Exit MA_13"] = df["MA_13"][i]
                    trade["Exit RSI_14"] = df["RSI_14"][i]
                    all_trades.append(copy.deepcopy(trade))
                if position is not None:
                    trade["Symbol"] = symbol
                    trade["Buy/Sell"] = "Buy"
                    trade["Entry"] = df["Close"][i]
                    trade["Entry Date"] = df["Date"][i]
                    trade["Entry Time"] = df["Time"][i]
                    trade["Entry Volume"] = df["Volume"][i]
                    trade["Entry MA_10"] = df["MA_10"][i]
                    trade["Entry MA_13"] = df["MA_13"][i]
                    trade["Entry RSI_14"] = df["RSI_14"][i]
                position = "Buy"
            if df["MA_10"][i] < df["MA_13"][i] and df["RSI_14"][i] < 40 and position != "Sell":
                if trade["Symbol"] is not None:
                    trade["Exit"] = df["Close"][i]
                    trade["Exit Date"] = df["Date"][i]
                    trade["Exit Time"] = df["Time"][i]
                    trade["Exit Volume"] = df["Volume"][i]
                    trade["Exit MA_10"] = df["MA_10"][i]
                    trade["Exit MA_13"] = df["MA_13"][i]
                    trade["Exit RSI_14"] = df["RSI_14"][i]
                    all_trades.append(copy.deepcopy(trade))
                if position is not None:
                    trade["Symbol"] = symbol
                    trade["Buy/Sell"] = "Sell"
                    trade["Entry"] = df["Close"][i]
                    trade["Entry Date"] = df["Date"][i]
                    trade["Entry Time"] = df["Time"][i]
                    trade["Entry Volume"] = df["Volume"][i]
                    trade["Entry MA_10"] = df["MA_10"][i]
                    trade["Entry MA_13"] = df["MA_13"][i]
                    trade["Entry RSI_14"] = df["RSI_14"][i]
                position = "Sell"

    #all_trades['Dates'] = pd.to_datetime(df['Datetime']).dt.date
    #all_trades['Time'] = pd.to_datetime(df['Datetime']).dt.time
    return all_trades

symbol_list = ["37834"]

data = symbols_backtesting(symbol_list)
data1 = pd.DataFrame(data)

if data:
    risk_percent = 100
    df = pd.DataFrame(data)
    df["P/L"] = np.round((np.where(df["Buy/Sell"] == "Buy", (100*(df["Exit"] - df["Entry"])/df["Entry"])*risk_percent,
                        (100*(df["Entry"] - df["Exit"])/df["Entry"])*risk_percent)),2)
    df["Probability"] = np.round((100*(np.where(df["P/L"] > 0, 1, 0).cumsum())/(np.where(df["P/L"] != np.NaN, 1, 0).cumsum())),2)
    df["Return"] = np.round((df["P/L"].cumsum()),2)
    df["Drawdown"] = np.round((df["Return"] - (df["Return"].cummax().apply(lambda x: x if x > 0 else 0))),2)

    
    print(df1.tail(5))
    print(df1.info())
else:
    print("No Trades")
       
print("Excel Starting....")
if not os.path.exists("Backtesting_TAL.xlsx"):
    try:
        wb = xw.Book()
        wb.save("Backtesting_TAL.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Backtesting_TAL.xlsx')
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
dt.range(f"a1:q1").value = ["Symbol","Buy/Sell","Entry","Entry Date","Exit","Exit Date",
                            "Entry Volume","Entry MA_10","Entry MA_13","Entry RSI_14","Exit Volume","Exit MA_10","Exit MA_13","Exit RSI_14"]
                            #" P/L","Probability","Return","Drawdown"]

try:
    time.sleep(0.5)
    dt.range("a1").value = data1
    st.range("a1").value = df
    ex.range("a1").value = script_code_5paisa
except Exception as e:
    print(e)








