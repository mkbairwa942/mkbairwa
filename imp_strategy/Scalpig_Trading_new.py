# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:13:23 2022

Here i coded how to trade in finvasia broker using excel, all the trading data (o,h,l,c,..) will stream in excel.

Contact details :
Telegram Channel:  https://t.me/pythontrader
Developer Telegram ID : https://t.me/pythontrader_admin
Gmail ID:   mnkumar2020@gmail.com 
Whatsapp : 9470669031 

Disclaimer: The information provided by the Python Traders channel is for educational purposes only, so please contact your financial adviser before placing your trade. Developer is not responsible for any profit/loss happened due to coding, logical or any type of error.
"""

#from NorenRestApiPy.NorenApi import  NorenApi
import logging
import time
from jugaad_data.nse import *
from sqlalchemy import create_engine
import urllib.parse
import urllib
from io import BytesIO
from zipfile import ZipFile
import pandas_ta as pta
#from finta import TA
# import talib
import pandas as pd
import copy
import numpy as np
import xlwings as xw
from datetime import datetime,timedelta
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
from io import BytesIO
import os
import sys
from zipfile import ZipFile
import requests
import itertools
import math 
from telethon.sync import TelegramClient
#from notifypy import Notify
#from plyer import notification
import inspect
import time
from five_paisa1 import *
import threading
from dateutil.parser import parse
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

if not os.path.exists("Scalping_Trading_new.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("Scalping_Trading_new.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('Scalping_Trading_new.xlsx')
for i in ["stats","Exchange","Expiry","Position","OrderBook","OrderBook_New","Option","Data","Buy","Sale","Final",
            "Stat","Stat1","Stat2","Stat3","Stat4"]:
    try:
        wb.sheets(i)
    except:
        wb.sheets.add(i)
dt = wb.sheets("Data")
by = wb.sheets("Buy")
sl = wb.sheets("Sale")
fl = wb.sheets("Final")
st = wb.sheets("stats")
exc = wb.sheets("Exchange")
exp = wb.sheets("Expiry")
pos = wb.sheets("Position")
ob = wb.sheets("OrderBook")
ob1 = wb.sheets("OrderBook_New")
oc = wb.sheets("Option")
st = wb.sheets("Stat")
st1 = wb.sheets("Stat1")
st2 = wb.sheets("Stat2")
st3 = wb.sheets("Stat3")
st4 = wb.sheets("Stat4")
dt.range("a:x").value = None
by.range("a:x").value = None
sl.range("a:ab").value = None
fl.range("a:az").value = None
exc.range("a:z").value = None
exp.range("a:z").value = None
pos.range("a:z").value = None
ob.range("a:aj").value = None
ob1.range("a:al").value = None
st.range("a:u").value = None

credi_har = credentials("HARESH")

def get_live_data(Exchange,ExchangeType,Symbol):

    try:
        live_data
    except:
        live_data = {}
    try:
        live_data = credi_har.fetch_market_depth_by_symbol([{"Exchange":Exchange,"ExchangeType":ExchangeType,"Symbol":Symbol}])
    except Exception as e:
        pass
    return live_data

def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
    t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
    S = asset_price
    K = strike_price
    r = interest_rate
    if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
        raise Exception
    flag = instrument_type[0].lower()
    imp_v = implied_volatility(premium, S, K, t, r, flag)
    return [imp_v,
            delta(flag,S,K,t,r,imp_v),
            gamma(flag,S,K,t,r,imp_v),
            rho(flag,S,K,t,r,imp_v),
            theta(flag,S,K,t,r,imp_v),
            vega(flag,S,K,t,r,imp_v)]


def place_trade(Exche,ExchTypee,symbol,scripte,quantity,price,direction):
    try:
        order = credi_har.place_order(OrderType=direction,
                        Exchange=Exche,
                        ExchangeType=ExchTypee,
                        ScripCode = scripte,
                        Qty=int(quantity),
                        Price=0.0,
                        IsIntraday=True,)
                        #IsStopLossOrder=True
                        #StopLossPrice=StopLossPrice)
        print("CALL PLACE TRADE")
        print(f"order :Exche {Exche},ExchTypee {ExchTypee},scripte {scripte}, Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
        return order
    except Exception as e:
        return f"{e}"

        
       
# feed_opened = False
# SYMBOLDICT = {}
# live_data = {}
# def event_handler_quote_update(inmessage):
#     global live_data
       
#     global SYMBOLDICT
#     #e   Exchange
#     #tk  Token
#     #lp  LTP
#     #pc  Percentage change
#     #v   volume
#     #o   Open price
#     #h   High price
#     #l   Low price
#     #c   Close price
#     #ap  Average trade price

#     fields = ['ts', 'lp', 'pc', 'c', 'o', 'h', 'l', 'v', 'ltq', 'ltp','bp1','sp1','ap','oi','ap']    
    
#     message = { field: inmessage[field] for field in set(fields) & set(inmessage.keys())}
    
#     key = inmessage['e'] + '|' + inmessage['tk']

#     if key in SYMBOLDICT:
#         symbol_info =  SYMBOLDICT[key]
#         symbol_info.update(message)
#         SYMBOLDICT[key] = symbol_info
#         live_data[key] = symbol_info
#     else:
#         SYMBOLDICT[key] = message
#         live_data[key] = message
       
# def event_handler_order_update(tick_data):
#     print(f"Order update {tick_data}")

# def open_callback():
#     global feed_opened
#     feed_opened = True

# def get_order_book():

#     global api
#     order_book = api.get_order_book()
#     order_book = pd.DataFrame(order_book)
#     order_book = order_book.sort_values(by=['norenordno']).reset_index(drop=True)
#     return order_book
    
# def order_status (orderid):
#     AverageExecutedPrice = 0
#     try:
#         order_book = get_order_book()
#         order_book = order_book[order_book.norenordno == str(orderid)]
        
#         status = order_book.iloc[0]['status']
#         if(status == 'COMPLETE'):
#             AverageExecutedPrice = order_book.iloc[0]['avgprc']
#     except Exception as e:
#         Message = str(e) + " : Exception occur in order_status"
#         print(Message)
#     return AverageExecutedPrice
    
# def place_trade(symbol,quantity,buy_or_sell):
#     global api        
#     tradingsymbol = symbol[4:]
#     exchange = symbol[:3]
#     price_type = 'MKT'
#     price = 0.0
    
#     if(exchange == 'NSE'):  
#         product_type = 'C'
#         #price = round(float(price),1)
#     else:        
#         product_type = 'M'
        
        
#     ret = api.place_order(buy_or_sell = buy_or_sell[0], 
#                             product_type = product_type,
#                             exchange = exchange,
#                             tradingsymbol = tradingsymbol, 
#                             quantity = quantity,
#                             discloseqty=0,
#                             price_type = price_type,
#                             price = price,
#                             trigger_price=None,
#                             retention='DAY', 
#                             remarks='Python_Trader').get('norenordno')  

#     ExecutedPrice = order_status (ret)
    
#     Message = "Placed order id :" + ret + ", Executed @ " + str(ExecutedPrice)
#     print(Message)
    
#     return ExecutedPrice

# def GetToken(exchange,tradingsymbol):
#     global api
#     Token = api.searchscrip(exchange=exchange, searchtext=tradingsymbol).get('values')[0].get('token')
#     return Token

# def subscribe_new_token(exchange,Token):
#     global api
#     symbol = []
#     symbol.append(f"{exchange}|{Token}")
#     api.subscribe(symbol)
    
def start_excel():
    global api, live_data
    global SYMBOLDICT
    # dt = excel_name.sheets("Data")
    # ob = excel_name.sheets("OrderBook")
    ob.range("a:az").value = dt.range("n:q").value = None
    dt.range(f"a1:q1").value = [ "Symbol", "Open", "High", "Low", "Close", "VWAP", "Best Buy Price",
                                "Best Sell Price","Volume", "LTP","Percentage change", "Qty", "Direction", "Entry Signal", "Exit Signal", "Entry Price",
                                "Exit Price"]


    subs_lst = []
    Symbol_Token = {}

    while True:
        try:
            #time.sleep(.5)

            symbols = dt.range(f"a{2}:a{250}").value
            trading_info = dt.range(f"l{2}:q{250}").value
            main_list = []
            
            idx = 0
            for i in symbols:
                lst = [None, None, None, None,None, None, None, None, None,None]
                if i:
                    if i not in subs_lst:
                        subs_lst.append(i)
                        try:
                            exchange = i[:3]
                            tradingsymbol = i[4:]
                            Token = GetToken(exchange,tradingsymbol)
                            Symbol_Token[i] = exchange + '|' + str(Token)
                            subscribe_new_token(exchange,Token)
                            print(f"Symbol = {i}, Token={Token} subscribed")
                            
                        except Exception as e:
                            print(f"Subscribe error {i} : {e}")
                    if i in subs_lst:
                        try:
                            TokenKey = Symbol_Token[i]
                            
                            
                            lst = [live_data[TokenKey].get("o", "-"),
                                   live_data[TokenKey].get("h", "-"),
                                   live_data[TokenKey].get("l", "-"),
                                   live_data[TokenKey].get("c", "-"),
                                   live_data[TokenKey].get("ap", "-"),
                                   live_data[TokenKey].get("bp1", "-"),
                                   live_data[TokenKey].get("sp1", "-"),
                                   live_data[TokenKey].get("v", "-"),
                                   live_data[TokenKey].get("lp", "-"),
                                   live_data[TokenKey].get("pc", "-")]
                            trade_info = trading_info[idx]
                            
                            if trade_info[0] is not None and trade_info[1] is not None:
                                if type(trade_info[0]) is float and type(trade_info[1]) is str:
                                    if trade_info[1].upper() == "BUY" and trade_info[2] is True:
                                        if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                                            dt.range(f"p{idx + 2}").value = place_trade(i, int(trade_info[0]), "Buy")
                                        elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and \
                                                trade_info[5] is None:
                                            dt.range(f"q{idx + 2}").value = place_trade(i, int(trade_info[0]), "Sell")
                                    if trade_info[1].upper() == "SELL" and trade_info[2] is True:
                                        if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                                            dt.range(f"p{idx + 2}").value = place_trade(i, int(trade_info[0]), "Sell")
                                        elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and \
                                                trade_info[5] is None:
                                            dt.range(f"q{idx + 2}").value = place_trade(i, int(trade_info[0]), "Buy")
                            
                        except Exception as e:
                            # print(e)
                            pass
                main_list.append(lst)
                
                idx += 1

            dt.range("b2:k250").value = main_list
            if excel_name.sheets.active.name == "OrderBook":
                ob.range("a1").value = get_order_book()
        except Exception as e:
            # print(e)
            pass
start_excel()

# if __name__ == '__main__':
#     if(Shoonya_login() == 1 ):   
    
#         api.start_websocket( order_update_callback=event_handler_order_update,
#                          subscribe_callback=event_handler_quote_update, 
#                          socket_open_callback=open_callback)

#         while(feed_opened==False):
#             print(feed_opened)
#             pass
#         print("Connected to WebSocket...")

#         start_excel()
#     else:
#         print("Credential is not correct")