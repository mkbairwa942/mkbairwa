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
import os, time, json, sys
import xlwings as xw
import pandas as pd
from datetime import datetime
from time import sleep
import logging
import pyotp

excel_name = xw.Book('PythonTrader_Terminal.xlsx')

#logging.basicConfig(level=logging.DEBUG)

# def Shoonya_login():
#     global api
#     isConnected = 0
#     try:
#         class ShoonyaApiPy(NorenApi):
#             def __init__(self):
#                 NorenApi.__init__(self, host='https://shoonyatrade.finvasia.com/NorenWClientTP/', websocket='wss://shoonyatrade.finvasia.com/NorenWSTP/', eodhost='https://shoonya.finvasia.com/chartApi/getdata/')

#         api = ShoonyaApiPy()

#         Credential_sheet = excel_name.sheets['User_Credential']

#         userid = Credential_sheet.range('B2').value.strip()
#         password = Credential_sheet.range('B3').value.strip()
#         TotpKey = str(Credential_sheet.range('B4').value)
#         pin = pyotp.TOTP(TotpKey).now()
#         twoFA = f"{int(pin):06d}" if len(pin) <=5 else pin    
#         vendor_code = Credential_sheet.range('B5').value.strip()
#         api_secret = Credential_sheet.range('B6').value.strip()
#         imei = 'abcd1234'
        
#         print(f"userid={userid},password={password},twoFA={twoFA},vendor_code={vendor_code},api_secret={api_secret}, imei={imei}")
#         login_status = api.login(userid=userid, password=password, twoFA=twoFA, vendor_code=vendor_code, api_secret=api_secret, imei=imei)
        
#         client_name = login_status.get('uname')
        
#         Credential_sheet.range('c2').value = 'Login Successful, Welcome ' + client_name
#         isConnected = 1
            
        
#     except Exception as e:
#         print(f"Error : {e}")
#         Credential_sheet.range('c2').value = 'Wrong credential'

#     return isConnected

feed_opened = False
SYMBOLDICT = {}
live_data = {}
def event_handler_quote_update(inmessage):
    global live_data
       
    global SYMBOLDICT
    #e   Exchange
    #tk  Token
    #lp  LTP
    #pc  Percentage change
    #v   volume
    #o   Open price
    #h   High price
    #l   Low price
    #c   Close price
    #ap  Average trade price

    fields = ['ts', 'lp', 'pc', 'c', 'o', 'h', 'l', 'v', 'ltq', 'ltp','bp1','sp1','ap','oi','ap']    
    
    message = { field: inmessage[field] for field in set(fields) & set(inmessage.keys())}
    
    key = inmessage['e'] + '|' + inmessage['tk']

    if key in SYMBOLDICT:
        symbol_info =  SYMBOLDICT[key]
        symbol_info.update(message)
        SYMBOLDICT[key] = symbol_info
        live_data[key] = symbol_info
    else:
        SYMBOLDICT[key] = message
        live_data[key] = message
       
def event_handler_order_update(tick_data):
    print(f"Order update {tick_data}")

def open_callback():
    global feed_opened
    feed_opened = True

def get_order_book():

    global api
    order_book = api.get_order_book()
    order_book = pd.DataFrame(order_book)
    order_book = order_book.sort_values(by=['norenordno']).reset_index(drop=True)
    return order_book
    
def order_status (orderid):
    AverageExecutedPrice = 0
    try:
        order_book = get_order_book()
        order_book = order_book[order_book.norenordno == str(orderid)]
        
        status = order_book.iloc[0]['status']
        if(status == 'COMPLETE'):
            AverageExecutedPrice = order_book.iloc[0]['avgprc']
    except Exception as e:
        Message = str(e) + " : Exception occur in order_status"
        print(Message)
    return AverageExecutedPrice
    
def place_trade(symbol,quantity,buy_or_sell):
    global api        
    tradingsymbol = symbol[4:]
    exchange = symbol[:3]
    price_type = 'MKT'
    price = 0.0
    
    if(exchange == 'NSE'):  
        product_type = 'C'
        #price = round(float(price),1)
    else:        
        product_type = 'M'
        
        
    ret = api.place_order(buy_or_sell = buy_or_sell[0], 
                            product_type = product_type,
                            exchange = exchange,
                            tradingsymbol = tradingsymbol, 
                            quantity = quantity,
                            discloseqty=0,
                            price_type = price_type,
                            price = price,
                            trigger_price=None,
                            retention='DAY', 
                            remarks='Python_Trader').get('norenordno')  

    ExecutedPrice = order_status (ret)
    
    Message = "Placed order id :" + ret + ", Executed @ " + str(ExecutedPrice)
    print(Message)
    
    return ExecutedPrice

def GetToken(exchange,tradingsymbol):
    global api
    Token = api.searchscrip(exchange=exchange, searchtext=tradingsymbol).get('values')[0].get('token')
    return Token

def subscribe_new_token(exchange,Token):
    global api
    symbol = []
    symbol.append(f"{exchange}|{Token}")
    api.subscribe(symbol)
    
def start_excel():
    global api, live_data
    global SYMBOLDICT
    dt = excel_name.sheets("Data")
    ob = excel_name.sheets("OrderBook")
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


if __name__ == '__main__':
    if(Shoonya_login() == 1 ):   
    
        api.start_websocket( order_update_callback=event_handler_order_update,
                         subscribe_callback=event_handler_quote_update, 
                         socket_open_callback=open_callback)

        while(feed_opened==False):
            print(feed_opened)
            pass
        print("Connected to WebSocket...")

        start_excel()
    else:
        print("Credential is not correct")