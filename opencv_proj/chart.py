import pandas as pd
import matplotlib.pyplot as plt
#from five_paisa1 import *
from five_paisa import *
import numpy as np
import xlwings as xw
import sys
import os
import mplfinance as mpf

month = 4
from_d = date(year=2024, month=month, day=1)
to_d = date(year=2024, month=month, day=30)

to_days = (date.today()-timedelta(days=1))
days_365 = (date.today() - timedelta(days=365)) 
print("1")
holida = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
print("2")
holida["Date"] = holida["Date1"].dt.date
holida1 = np.unique(holida['Date'])
print(holida1)

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holida1)
trading_dayss = trading_days_reverse[::-1]
# trading_dayss1 = ['2024-01-20', '2024-01-19','2024-01-18']
# trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[0]
second_last_trading_day = trading_days[2]
time_change = timedelta(minutes=870) 
upto_df = timedelta(minutes=930) 
new_current_trading_day = current_trading_day + time_change
df_upto_datetime = current_trading_day + upto_df
print(new_current_trading_day)
print(df_upto_datetime)

print("Trading_Days_Reverse is :- "+str(trading_days_reverse))
print("Trading Days is :- "+str(trading_dayss))
print("Last Trading Days Is :- "+str(trading_days))
print("Current Trading Day is :- "+str(current_trading_day))
print("Last Trading Day is :- "+str(last_trading_day))
print("Second Last Trading Day is :- "+str(second_last_trading_day))
print("Last 365 Day is :- "+str(days_365))

symbol = 'MOTHERSUMI'

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

print("Excel Starting....")

if not os.path.exists("chart.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("chart.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('chart.xlsx')
for i in ["Exchange","Filt_Exc","Stat","Stat1","Stat2","Stat3","Stat4"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
exc = wb.sheets("Exchange")
flt_exc = wb.sheets("Filt_Exc")
st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")

exc.range("a:u").value = None
flt_exc.range("a:u").value = None

stk_list = [999920005]

def data_download(stk_nm):
    df = client.historical_data('N', 'C', stk_nm, '5m', from_d,to_d)
    #print(df.head(5))
    df = df[['Datetime','Open','High', 'Low', 'Close', 'Volume']]
    #df = df.astype({"Datetime": "datetime64[ns]"})
    df['Name'] = np.where(stk_nm == 999920005,"BANKNIFTY",np.where(stk_nm == 999920000,"NIFTY",""))
    return df

df1 = data_download(999920000)
for x in range(1, 1674):
    print(x)
    df = df1.iloc[0+x:50+x]

    last_dt = str(list(df['Datetime'])[-1])
    print(last_dt)
    try:
        if df.empty:
            pass
        else:
            try:
                df.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
                st.range("a1").options(index=False).value = df
            except Exception as e:
                print(e)
        if df1.empty:
            pass
        else:
            try:
                df1.sort_values(['Name','Datetime'], ascending=[True,True], inplace=True)
                st1.range("a1").options(index=False).value = df1
            except Exception as e:
                print(e)
    except Exception as e:
        print(e) 

    folder = "D:\STOCK\Capital_vercel_new\opencv_proj\Scanned\chartImages"

    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)

    folder_path = folder  # Replace with your desired folder path

    replace_name = last_dt.replace(":","-")

    file_name = f'image_{replace_name}.jpg'
    full_path = os.path.join(folder_path, file_name)

    os.makedirs(folder_path, exist_ok=True)

    mpf.plot(
        df,
        type='candle',          # Candlestick chart
        style='charles',        # Chart style
        # title='Candlestick Chart Example',
        ylabel='Price',
        savefig=full_path,  
        axisoff=True     # Full path to save the image

    )

    print(f"Candlestick chart saved at: {full_path}")



