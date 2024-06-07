#from py5paisa import FivePaisaClient
import pandas as pd
#from py5paisa.order import Order, OrderType, Exchange
from py5paisa1 import FivePaisaClient
import pyotp
import os
import pprint
from datetime import date, datetime, timedelta
from jugaad_data.nse import NSELive
from jugaad_data.holidays import holidays
import pandas
from datetime import datetime
import time
from dateutil.utils import today
import sqlalchemy

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

from_d = (date.today() - timedelta(days=30))
# from_d = date(2022, 12, 29)

to_d = (date.today())
# to_d = date(2023, 1, 23)

datess = pd.bdate_range(start=from_d, end=to_d, freq="C", holidays=holidays())
dates = datess[::-1]
intraday = datess[-1]
lastTradingDay = dates[1]

now = datetime.now()
intr_time1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
intr_time2 = now.replace(hour=15, minute=35, second=0, microsecond=0)

# print(lastTradingDay)
# print(intraday)

engine = sqlalchemy.create_engine('mysql+pymysql://mkbairwa942:vaa2829m@5.183.11.143:3306/capitalsscope')

def credentials (name):
    if name.upper() =='BHAVNA':
        cred = {
            "APP_NAME": "5P50464800",
            "APP_SOURCE": "16351",
            "USER_ID": "6vbYJ6PUjfE",
            "PASSWORD": "pbdJftZXd6t",
            "USER_KEY": "PpBMeomZDOiLMA7OJ8XfYqkf50cdRDec",
            "ENCRYPTION_KEY": "6FDPBQqiEJZjdlmoIJhGmXxfYcFaTest",
        }

        user = 'bhavnabairwa942@gmail.com'
        pwd = 'vaa6762m'
        dob = '19850602'
        TOTP=pyotp.TOTP("GUYDINRUHAYDAXZVKBDUWRKZ").now()
        print(user)
        print(TOTP)
        client_code='50464800'
        Pin='200200'
        RequestToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwODQwNDk1Iiwicm9sZSI6IkRrZldGQTFuUktoa0pMNG9MZnlubmwzYU50dzFBZzVmIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTcwOTkyMzAsImV4cCI6MTY5NzA5OTI5MCwiaWF0IjoxNjk3MDk5MjMwfQ.ZePYRN6mi7F_FRrgyujAQjQ4WKANUoQuiJJboLIgVDU'
        client = FivePaisaClient(cred=cred)
        client.get_totp_session(client_code,TOTP,Pin)
        #client.get_access_token(RequestToken)

    if name.upper() == 'MUKESH':
        cred = {
            "APP_NAME": "5P57141743",
            "APP_SOURCE": "9997",
            "USER_ID": "5SP0ws0uCmc",
            "PASSWORD": "C0VIQHnMEpI",
            "USER_KEY": "BT5DqKIGqnKmHiZnzGXKZ2aBql4oYBRp",
            "ENCRYPTION_KEY": "tTEQPwp3Gfh2l3LWqDb2UC1sD0IFvzV5",
        }

        user = 'mukeshbairwa942@gmail.com'
        pwd = 'navya@1234'
        dob = '19860518'
        TOTP=pyotp.TOTP("GU3TCNBRG42DGXZVKBDUWRKZ").now()
        print(user)
        print(TOTP)
        print("HI MUKESH")
        client_code='57141743'
        Pin='157359'
        RequestToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwODQwNDk1Iiwicm9sZSI6IkRrZldGQTFuUktoa0pMNG9MZnlubmwzYU50dzFBZzVmIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTcwOTkyMzAsImV4cCI6MTY5NzA5OTI5MCwiaWF0IjoxNjk3MDk5MjMwfQ.ZePYRN6mi7F_FRrgyujAQjQ4WKANUoQuiJJboLIgVDU'
        client = FivePaisaClient(cred=cred)
        client.get_totp_session(client_code,TOTP,Pin)
        #client.get_access_token(RequestToken)

    if name.upper() == 'HARESH':
        cred = {
            "APP_NAME": "5P50645842",
            "APP_SOURCE": "16771",
            "USER_ID": "mjrgk6c5MTu",
            "PASSWORD": "OJN4tsf3NUo",
            "USER_KEY": "5azZqigyoIRgTAnfoIbHVrvGpbnetUmu",
            "ENCRYPTION_KEY": "3jGC61GsOjZkTzfJQwkoTHT0aUbTBzjB",
        }

        user = 'hareshgnagar84@gmail.com'
        pwd = '1H825JV6'
        dob = '19920702'
        TOTP=pyotp.TOTP("GUYDMNBVHA2DEXZVKBDUWRKZ").now()
        print(user)
        print(TOTP)
        client_code='50645842'
        Pin='701570'
        RequestToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwODQwNDk1Iiwicm9sZSI6IkRrZldGQTFuUktoa0pMNG9MZnlubmwzYU50dzFBZzVmIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTcwOTkyMzAsImV4cCI6MTY5NzA5OTI5MCwiaWF0IjoxNjk3MDk5MjMwfQ.ZePYRN6mi7F_FRrgyujAQjQ4WKANUoQuiJJboLIgVDU'
        client = FivePaisaClient(cred=cred)
        client.get_totp_session(client_code,TOTP,Pin)
        #client.get_access_token(RequestToken)

    if name.upper() == 'ALPESH':
        cred = {
            "APP_NAME": "5P50840495",
            "APP_SOURCE": "19325",
            "USER_ID": "oVWgywCbqp4",
            "PASSWORD": "4hJ57QMiKEM",
            "USER_KEY": "DkfWFA1nRKhkJL4oLfynnl3aNtw1Ag5f",
            "ENCRYPTION_KEY": "GhyxDWjtOfOxjXjJnONTogFSYenULVVu",
        }

        user = 'agnagar300678@gmail.com'
        pwd = 'agnagar@123'
        dob = '19780630'        
        TOTP=pyotp.TOTP("GUYDQNBQGQ4TKXZVKBDUWRKZ").now()
        print(user)
        print(TOTP)
        client_code='50840495'
        Pin='200200'
        RequestToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwODQwNDk1Iiwicm9sZSI6IkRrZldGQTFuUktoa0pMNG9MZnlubmwzYU50dzFBZzVmIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTcwOTkyMzAsImV4cCI6MTY5NzA5OTI5MCwiaWF0IjoxNjk3MDk5MjMwfQ.ZePYRN6mi7F_FRrgyujAQjQ4WKANUoQuiJJboLIgVDU'
        client = FivePaisaClient(cred=cred)
        client.get_totp_session(client_code,TOTP,Pin)
        #client.get_access_token(RequestToken)

    if name.upper() == 'ASHWIN':
        cred = {
            "APP_NAME": "5P52997960",
            "APP_SOURCE": "20565",
            "USER_ID": "FElaBH50yu3",
            "PASSWORD": "553pD6kdtmr",
            "USER_KEY": "4H0ZtTsiy3H45EbLASavvsDKiakZPZEr",
            "ENCRYPTION_KEY": "mfTu3GGC28s0JTfV0JVRM2euCvAGL5ot",
        }

        user = 'ashwinpjoshi@gmail.com'
        pwd = '101010'
        dob = '19840905'
        TOTP=pyotp.TOTP("GUZDSOJXHE3DAXZVKBDUWRKZ").now()
        print(user)
        print(TOTP)
        client_code='52997960'
        Pin='101010'
        RequestToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwODQwNDk1Iiwicm9sZSI6IkRrZldGQTFuUktoa0pMNG9MZnlubmwzYU50dzFBZzVmIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTcwOTkyMzAsImV4cCI6MTY5NzA5OTI5MCwiaWF0IjoxNjk3MDk5MjMwfQ.ZePYRN6mi7F_FRrgyujAQjQ4WKANUoQuiJJboLIgVDU'
        client = FivePaisaClient(cred=cred)
        client.get_totp_session(client_code,TOTP,Pin)
        #client.get_access_token(RequestToken)


    return client


# con = urllib.parse.quote_plus(
#     'DRIVER={SQL Server Native Client 11.0};SERVER=MUKESH\SQLEXPRESS;DATABASE=Stock_data;trusted_connection=yes')
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(con))   

# client = credentials('alpesh','431070')


#Now Can directly call client.place_order()


index = 'SBIN'
# print(index)
# ltp = (client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"C","Symbol":index}])['Data'][0]['LastTradedPrice'])
# print(ltp)
# script_code_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
# script_codee = pd.read_csv(script_code_url)
# script_code = script_codee[script_codee['CpType'] == "CE"]
# script_code['text_new'] = script_code['Name'].str.split(' ').str[0]
# lotsize =((script_code[script_code['text_new'] == index])['LotSize']).values[-1]
# print(lotsize)

# Market Status
# market_status = client.get_market_status()

# Fetches holdings
# client.holdings()

# Fetches margin
# client.margin()

# Fetches positions
# client.positions()

# Fetches the order book of the client
# client.order_book()

# Fetches Trade book
# client.get_tradebook()


# pprint.pprint(client.get_market_status())
# pprint.pprint(client.holdings())
# pprint.pprint(client.margin())
# pprint.pprint(client.positions())
# pprint.pprint(client.order_book())
# pprint.pprint(client.get_tradebook())

# pt = pd.DataFrame(client.get_tradebook())
# print(pt)

# Note: This is an indicative order.

# You can pass scripdata either you can pass scripcode also.
# please use price = 0 for market Order
# use IsIntraday= true for intraday orders

# Using Scrip Data :-

# #Using Scrip Code :-
# client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=260)
# #Sample For SL order
# client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=350, IsIntraday=False, IsStopLossOrder=True, StopLossPrice=345)
# #Derivative Order
# client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = 57633, Qty=50, Price=1.5)
#
# Please refer below documentation link for paramaters to be passed in cleint.place_order function
# https://www.5paisa.com/developerapi/order-request-place-order

# client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=325, AHPlaced="Y")

# client.modify_order(ExchOrderID="1100000017861430", Qty=2,Price=261)

# client.cancel_order(exch_order_id="1100000017795041")

# cancel_bulk=[{"ExchOrderID": "<Exchange Order ID 1>"},{"ExchOrderID": "<Exchange Order ID 2>"}],
# client.cancel_bulk_order(cancel_bulk)

# test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=205,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=215.0,TriggerPriceForSL=203,LimitPriceForSL=202,ExchType='C',Exch='N',RequestType='P',AtMarket=False)
# client.bo_order(test_order)


# # Live Market Feed Streaming
# req_list = [{"Exch": "N", "ExchType": "C", "ScripCode": 3045},]
# req_data = client.Request_Feed('mf', 's', req_list)


# def on_message(ws, message):
#     print(message)
# client.connect(req_data)
# client.receive_data(on_message)

# Live Market Depth Streaming (Depth 20)

# a={"method": "subscribe", "operation": "20depth", "instruments": ["NC2885"]}
# print(client.socket_20_depth(a))
# def on_message(ws, message):
#     print(message)
# client.receive_data(on_message)

# Note:- Instruments in payload above is a list(array) in format as <exchange><exchange type><scrip code>

# # Full Market Snapshot
#
# a=[{"Exchange": "N", "ExchangeType": "C", "ScripCode": "3045"},
#    {"Exchange": "N", "ExchangeType": "C", "ScripCode": "1660"},
#    ]
# print(client.fetch_market_depth(a))

# Full Market Snapshot(By Symbol)

# a=[
#     {"Exchange":"N","ExchangeType":"C","Symbol":"NIFTY"},
#     {"Exchange":"N","ExchangeType":"C","Symbol":"BANKNIFTY"},
#     {"Exchange":"N","ExchangeType":"C","Symbol":"FINNIFTY"},
    # {"Exchange":"N","ExchangeType":"D","Symbol":"BANKNIFTY 31 Feb 2022 CE 41600.00"},
    # ]
# print(client.fetch_market_depth_by_symbol(a))
# print(client.fetch_market_depth_by_symbol([{"Exchange":"N","ExchangeType":"D","Symbol":"BANKNIFTY 04 May 2023 PE 43200.00"}])['Data'][0])

#     dfg1 = client.fetch_market_depth_by_symbol(a)
#     dfg2 = dfg1['Data']
#     dfg3 = pd.DataFrame(dfg2)
#     dfg3['TimeNow'] = datetime.now()
#     dfg3.to_sql(name="tick_data", con=engine, if_exists="append", index=False)
#     #print(dfg3.tail(1))
           

# print(Niftys())


# fo_bhav = (f"SELECT * FROM capitalsscope.live_Index;")
# fo_bhav = pd.read_sql(sql=fo_bhav, con=engine)
# print(fo_bhav)

# # Option Chain
# opt_symbol1 = "SBIN"

# # Returns list of all active expiries

# # client.get_option_chain("N","NIFTY",<Pass expiry timestamp from get_expiry response>)
# opt = pd.DataFrame(client.get_option_chain("N", "NIFTY", expiry)['Options'])
# print(opt)

# print(live_option_chain("NIFTY"))

# Historical Data

# historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)
# df = client.historical_data('N', 'C', 3045, '5m', '2023-09-29','2023-10-02')
# print(df)

# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']

# # To get actionable buy trades use:-
# print(client.get_buy())
#
#
# # To get list of current trades use:-
# print(client.get_trade())

# req_list=[
#             { "Exch":"N","ExchType":"C","ScripCode":1660},
#             ]

# req_data=client.Request_Feed('mf','s', req_list)
# def on_message(ws, message):
#     print(message)


# client.connect(req_data)

# client.receive_data(on_message)
# print(req_data)