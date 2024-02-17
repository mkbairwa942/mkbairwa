import pandas as pd
import numpy as np
from five_paisa1 import *
import calendar

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.options.mode.copy_on_write = True

credi_har = credentials("HARESH")

from_d = (date.today() - timedelta(days=15))
# from_d = date(2022, 12, 29)

to_d = (date.today())
#to_d = date(2023, 2, 3)

to_days = (date.today()-timedelta(days=1))
# to_d = date(2023, 1, 20)

days_365 = (date.today() - timedelta(days=365))
print(days_365)

holida = pd.read_excel('D:\STOCK\Capital_vercel_new\strategy\holida.xlsx')
holida["Date"] = holida["Date1"].dt.date
holida1 = np.unique(holida['Date'])

trading_days_reverse = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holida1)
trading_dayss = trading_days_reverse[::-1]
# trading_dayss1 = ['2024-01-20', '2024-01-19','2024-01-18']
# trading_dayss = [parse(x) for x in trading_dayss1]

trading_days = trading_dayss[1:]
current_trading_day = trading_dayss[0]
last_trading_day = trading_days[0]
second_last_trading_day = trading_days[1]
last_day = date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1])

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

exchange = None
while True:
    if exchange is None: 
        try:
            
            exchange = pd.DataFrame(script_code_5paisa)
            exchange["Watchlist"] = exchange["Exch"] + ":" + exchange["ExchType"] + ":" + exchange["Name"]
            exchange_cash = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['C'])) & (exchange["Series"] == "EQ")]
            exchange_opt = exchange[(exchange["Exch"] == "N") & (exchange['ExchType'].isin(['D'])) & (exchange['CpType'].isin(['CE','PE']))]
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

Expiry_exc = (np.unique(exchange_opt['Expiry']).tolist())   
F_O_List = (np.unique(exchange_opt['Root']).tolist())
F_O_List_exc = []
for dttg in F_O_List:
    ag={"Exchange": "N", "ExchangeType": "C", "Symbol": f"{dttg}"}
    F_O_List_exc.append(ag) 

scpt_listtt = []

for i in F_O_List:
    print(i)
    Fo_dfg1 = credi_har.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":f"{i}"}])['Data'][0]['LastTradedPrice']
    Spot = round(Fo_dfg1/100,0)*100
    dfc2 = exchange_opt[exchange_opt['Root'] == i]
    dfc3 = dfc2[(dfc2['Expiry'].apply(pd.to_datetime) >= current_trading_day)]
    Expiryyy = (np.unique(dfc3['Expiry']).tolist())[0]        
    dfc = dfc3[dfc3['Expiry'] == Expiryyy]
    dfc.sort_values(['StrikeRate','Expiry'], ascending=[True,True], inplace=True)

    dfgg_CE1 = dfc[(dfc["CpType"] == 'CE')] 
    dfgg_CE2 = dfgg_CE1[(dfgg_CE1['StrikeRate'] >= Spot)] 
    dfgg_CE3 = dfgg_CE2.head(3)
    dfgg_CE_scpt = (np.unique([int(i) for i in dfgg_CE3['Scripcode']])).tolist()
    scpt_listtt.append(dfgg_CE_scpt)

    dfgg_PE1 = dfc[(dfc["CpType"] == 'PE')]        
    dfgg_PE2 = dfgg_PE1[(dfgg_PE1['StrikeRate'] <= Spot)]                        
    dfgg_PE3 = dfgg_PE2.tail(3)
    dfgg_PE_scpt = (np.unique([int(i) for i in dfgg_PE3['Scripcode']])).tolist()
    scpt_listtt.append(dfgg_PE_scpt)
# print(scpt_listtt)

scpt_listtt1 = []
for list in scpt_listtt:
    for number in list:
        scpt_listtt1.append(number)

scpt_listtt2 = np.unique(scpt_listtt1)
#print(len(scpt_listtt2))

exchange_opt = exchange_opt[(exchange_opt['Scripcode'].isin(scpt_listtt2))]
exchange_opt.sort_values(['Name','StrikeRate'], ascending=[True,True], inplace=True)
print(exchange_opt.shape[0])
print(exchange_cash.shape[0])
# print(exc_new.head(20))
exchange_new = pd.concat([exchange_cash, exchange_opt], ignore_index=True, sort=False)
#exchange_new = exchange_cash.append(exchange_opt)
print(exchange_new.head(10))
print(exchange_new.shape[0])


