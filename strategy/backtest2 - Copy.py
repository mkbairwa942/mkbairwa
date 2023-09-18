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
# from datetime import datetime, time, date
# import datetime
# import time,json,datetime,sys
# from datetime import timezone
from time import sleep
from datetime import date, datetime, timedelta
from dateutil.utils import today

from_d = (date.today() - timedelta(days=41))
# from_d = date(2022, 12, 29)

#to_d = (date.today())
to_d = date(2023, 4, 21)

to_days = (date.today()-timedelta(days=1))
# to_days = date(2023, 1, 20)

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
current_time = (datetime.now()).strftime("%H:%M")

# script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_code_5paisa = pd.read_csv(script_code_5paisa_url)

# enctoken = "ZEYTwpVbWDGxf91XntlGJEFfogKYV/Ltb4h0JgpQ9sn2lOhgfFpVaFC6TyuCfjLR19qpiVCyNEz4Sc0XW40hP6eBtPDQCHdq+l+jBWMSeJovzCmNnY6cqg=="
# kite = KiteApp(enctoken=enctoken)

#master_contract = pd.DataFrame(kite.instruments())
#print(master_contract.tail(10))

client.get_market_status()

symbol1 = '35018'
SL = 20
BuySl = SL*-1
SellSl = SL*1
print(BuySl,SellSl)

df = client.historical_data('N', 'D', symbol1, '5m', from_d, to_d)

opt_symbol = "ABB"

def expirt_date(opt_symbol):
    ep = []
    for ei in pd.DataFrame((client.get_expiry("N", opt_symbol))['Expiry'])['ExpiryDate']:
        left = ei[6:19]
        timestamp = pd.to_datetime(left, unit='ms')
        ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
        ep.append([ExpDate, left])

    ep1 = pd.DataFrame(ep)
    ep1.columns = ['ExpDate', 'DayFormat']
    expiry = (ep1['DayFormat'][0])

    return expiry





def market_depth(opt_symbol):
    # if now > intr_time1 and now < intr_time2 and (date.today()) == intradayy:
    eq_df = []
    Open = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['Open'])
    High = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['High'])
    Low = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['Low'])
    Close = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['Close'])
    Ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['LastTradedPrice'])
    Chg = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":opt_symbol}])['Data'][0]['NetChange'])
    Time = current_time
    Date = today()
    if opt_symbol == 'NIFTY':
        Spot = round(Ltp/50,0)*50
    else:
        Spot = round(Ltp/100,0)*100

    eq_df.append([Date, Time, Open, High, Low, Close, Ltp, Chg, Spot])
    df3 = pd.DataFrame(eq_df)
    df3.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg', 'Spot']
    df3['Symbol'] = 'NIFTY'
    df3 = df3[['Symbol', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Ltp', 'Chg','Spot']]
    return df3

        # print(df3.tail(2))
def option(opt_symbol):
    ep = []
    for ei in pd.DataFrame((client.get_expiry("N", opt_symbol))['Expiry'])['ExpiryDate']:
        left = ei[6:19]
        timestamp = pd.to_datetime(left, unit='ms')
        ExpDate = datetime.strftime(timestamp, '%d-%m-%Y')
        ep.append([ExpDate, left])

    ep1 = pd.DataFrame(ep)
    ep1.columns = ['ExpDate', 'DayFormat']
    expiry = (ep1['DayFormat'][0])

    opt = pd.DataFrame(client.get_option_chain("N", "NIFTY", expiry)['Options'])
    CE = []
    PE = []
    for i in opt:
        ce_data = opt[opt['CPType'] == 'CE']
        ce_data = ce_data.sort_values(['StrikeRate'])
        CE.append(ce_data)

        pe_data = opt[opt['CPType'] == 'PE']
        pe_data = pe_data.sort_values(['StrikeRate'])
        PE.append(pe_data)

    option = pd.DataFrame(client.get_option_chain("N", opt_symbol, expiry)['Options'])
    # pe_values = pd.DataFrame(client.get_option_chain("N", opt_symbol, expiry)['Options'])
    ce_values1 = option[option['CPType'] == 'CE']
    pe_values1 = option[option['CPType'] == 'PE']
    ce_data = ce_values1.sort_values(['StrikeRate'])
    pe_data = pe_values1.sort_values(['StrikeRate'])
    df1 = pd.merge(ce_data, pe_data, on='StrikeRate')
    df1['Date'] = today()
    df1['Time'] = current_time

    df1.rename(
        {'ChangeInOI_x': 'CE_Chg_OI', 'ChangeInOI_y': 'PE_Chg_OI', 'LastRate_x': 'CE_Ltp', 'LastRate_y': 'PE_Ltp',
        'OpenInterest_x': 'CE_OI', 'OpenInterest_y': 'PE_OI', 'Prev_OI_x': 'CE_Prev_OI', 'Prev_OI_y': 'PE_Prev_OI',
        'PreviousClose_x': 'CE_Prev_Ltp', 'PreviousClose_y': 'PE_Prev_Ltp', 'ScripCode_x': 'CE_Script',
        'ScripCode_y': 'PE_Script', 'Volume_x': 'CE_Volume', 'Volume_y': 'PE_Volume'}, axis=1, inplace=True)

    df1 = df1[['Date', 'Time', 'CE_Script', 'CE_Volume', 'CE_Prev_OI', 'CE_Chg_OI', 'CE_OI', 'CE_Prev_Ltp', 'CE_Ltp', 'StrikeRate',
            'PE_Ltp', 'PE_Prev_Ltp', 'PE_OI', 'PE_Chg_OI', 'PE_Prev_OI', 'PE_Volume', 'PE_Script']]

    print('live_option_chain_nifty',to_d,now)
    return df1
   

df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = pd.to_datetime(df['Datetime']).dt.date
df['Date'] = df['Date'].apply(lambda x: str(x)).apply(lambda x: pd.to_datetime(x))
df['Time'] = pd.to_datetime(df['Datetime']).dt.time
df['Time'] = df['Time'].apply(lambda x: str(x)).apply(lambda x: pd.Timestamp(x))
df = df[['Date', 'Time','Open','High', 'Low', 'Close', 'Volume','Datetime']]
df["MA_5"] = np.round((pta.ema(df["Close"], length=5)),2)
print(df.tail(2))
#df["El_Fish"] = np.round((pta.fisher(df["High"],df["Low"],length=10,signal=5,offset=2)),2)
#df['Sell_Entry'] = np.where((df['Low'].shift(1))>(df['MA_5'].shift(1)),"Sell","")
#df['Sell_Entry1'] = np.where(df['Close']<df['MA_5'],"Sell","")
df['Sell_Entry'] = np.where(((np.where((df['Low'].shift(1))>(df['MA_5'].shift(1)),"Sell",""))=="Sell") & ((np.where(df['Close']<df['MA_5'],"Sell",""))=="Sell"),"Sell","")
#df['Buy_Entry'] = np.where((df['High'].shift(1))<(df['MA_5'].shift(1)),"Buy","")
#df['Buy_Entry1'] = np.where(df['Close']>df['MA_5'],"Buy","")
df['Buy_Entry'] = np.where(((np.where((df['High'].shift(1))<(df['MA_5'].shift(1)),"Buy",""))=="Buy") & ((np.where(df['Close']>df['MA_5'],"Buy",""))=="Buy"),"Buy","")
#df['SL'] = (df.High.rolling(4).max())
#df['SL1'] = (df.High.rolling(4).max().shift(-4))
#df['SL2'] = np.where(df['Sell_Entry']=="Sell","SL","")
#df['SL3'] = np.where((df['SL1'])>(df['SL']),"SL","")
df['Sell_SL'] = np.where(((np.where(df['Sell_Entry']=="Sell","SL",""))=="SL") & ((np.where((df.High.rolling(4).max().shift(-4))>(df.High.rolling(4).max()),"SL",""))=="SL"),"SL","")
df['Sell_SL_PT'] = np.where((df['Sell_SL']=="SL"),(df['Close'])-((df.High.rolling(4).max().shift(-4))),"")


# trs = ta.indicators()
# print(trs)


df = df[4:]   
df3 = df   
#print(df3.tail(2))        

lengt = round((df3.shape[0])/2)
#print(lengt)
#print(type(lengt))
re1 = df3['Close'].iloc[lengt]
re2 = df3['Close'].iloc[lengt+1]
#print(re1,re2)
diff = (re2-re1)
#print(diff)

symbol_list = ["35018"]
       
print("Excel Starting....")
if not os.path.exists("Backtesting11.xlsx"):
    try:
        wb = xw.Book()
        wb.save("Backtesting11.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Backtesting11.xlsx')
for i in ["Data","stats","Exchange","Expiry","Mkt_Dep","Option"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
st = wb.sheets("stats")
exc = wb.sheets("Exchange")
exp = wb.sheets("Expiry")
mktdp = wb.sheets("Mkt_Dep")
opt = wb.sheets("Option")
dt.range("a:z").value = None
st.range("a:z").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
mktdp.range("a:z").value = None
opt.range("a:z").value = None
dt.range(f"a1:q1").value = ["Symbol","Buy_Sell","Entry","Entry Date","Exit","Exit Date",
                            "Entry Volume","Entry MA_10","Entry MA_13","Entry RSI_14","Exit Volume","Exit MA_10","Exit MA_13","Exit RSI_14"]
                            #" P/L","Probability","Return","Drawdown"]

try:
    time.sleep(0.5)
    dt.range("a1").value = df3
    st.range("a1").value = df
    exp.range("a1").value = expirt_date(opt_symbol)
    exp.range("d1").value = "Symbol"
    exp.range("d2").value = opt_symbol
    mktdp.range("a1").value = market_depth(opt_symbol)
    opt.range("a1").value = option(opt_symbol)
    #ex.range("a1").value = master_contract
except Exception as e:
    print(e)








