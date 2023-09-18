import os
from kite_trade import *
# from kiteconnect import KiteConnect
import time,json,datetime,sys
import xlwings as xw
import pandas as pd
import copy
import numpy as np
import time
import dateutil.parser
import threading
from datetime import datetime,timedelta
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from time import sleep
# import urllib.parse as urlparse


from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

# api_key = 'xxxxxxxxxxxx'
# api_secret = 'xxxxxxxxxxxx'
# account_username = 'YR6706'
# account_password = 'vaa6762m'
# account_two_fa = int(111111)

# #kite = KiteConnect(api_key=api_key)

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(executable_path='/Users/entirety/Desktop/chromedriver',options=options)

# driver.get(kite.login_url())
# form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="login-form"]')))
# driver.find_element_by_xpath("//input[@type='text']").send_keys(account_username)
# driver.find_element_by_xpath("//input[@type='password']").send_keys(account_password)
# driver.find_element_by_xpath("//input[@type='submit']").click()
# sleep(1)
# form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="login-form"]//form')))
# driver.find_element_by_xpath("//input[@type='password']").send_keys(account_two_fa)
# driver.find_element_by_xpath("//input[@type='submit']").click()
# sleep(1)
# current_url = driver.current_url

# driver.close()

# parsed = urlparse.urlparse(current_url)
# request_token = urlparse.parse_qs(parsed.query)['request_token'][0]

# access_token = kite.generate_session(request_token=request_token,api_secret=api_secret)['access_token']

# kite.set_access_token(access_token)

# kite.ltp('MCX:CRUDEOIL21JUNFUT')

enctoken = "EpZ4/KZWMMHndjTI3rTLcWTJvKJkNKeJqeCwbZFpnbWIFiWzzk2OltgH+jiOgAMGkPtOi+g7jc4lhOpicrMYCLlcYyD9TZZfcNoEQdG037y2FS2xSU7ZiQ=="
kite = KiteApp(enctoken=enctoken)

print("----option chain----")

if not os.path.exists("optChan_kite.xlsx"):
    try:
        wb = xw.Book()
        wb.sheets.add("optionchain")
        wb.save("optChan_kite.xlsx")
        wb.close()
    except Exception as e:
        print(f"Error : {e}")
        sys.exit()
wb = xw.Book('optChan_kite.xlsx')
oc = wb.sheets("optionchain")
oc.range("a:b").value = oc.range("d6:e20").value = oc.range("g1:v4000").value = None

exchange = None
while True:
    if exchange is None: 
        try:
            exchange = pd.DataFrame(kite.instruments("NFO"))
            exchange = exchange[exchange["segment"] == "NFO-OPT"]
            break
        except:
            print("Exchange Download Error....")
            time.sleep(10)

df = pd.DataFrame({"FNO Symbol": list(exchange["name"].unique())})
df = df.set_index("FNO Symbol",drop=True)
oc.range("a1").value = df

oc.range("d2").value, oc.range("d3").value, oc.range("d4").value = "Symbol==>>", "Expiry==>>", "LotSize==>>",

pre_oc_symbol = pre_oc_expiry = ""
expiries_list = []
instrument_dict = {}
prev_day_oi = {}
stop_thread = False

def get_oi(data):
    global prev_day_oi,kite,stop_thread
    for symbol, v in data.items():
        if stop_thread:
            break
        while True:
            try:
                prev_day_oi[symbol]
                break
            except:
                try:
                    prev_day_data = kite.historical_data(v["token"],(datetime.now() - timedelta(days=5)).date(),
                                                         (datetime.now()-timedelta(days=1)).date(),"day",oi=True)
                    try:
                        prev_day_oi[symbol] = prev_day_data[-1]["oi"]
                    except:
                        prev_day_oi[symbol] = 0
                    break
                except Exception as e:
                    time.sleep(0.5)
print("Excel : Started")
while True:
    oc_symbol,oc_expiry = oc.range("e2").value,oc.range("e3").value

    if pre_oc_symbol != oc_symbol or pre_oc_expiry != oc_expiry:
        oc.range("g:v").value = None
        instrument_dict = {}
        stop_thread = True
        time.sleep(2)
        if pre_oc_symbol != oc_symbol:
            oc.range("b:b").value = oc.range("d6:e20").value = None
            expiries_list = []
        pre_oc_symbol = oc_symbol
        pre_oc_expiry = oc_expiry
    if oc_symbol is not None:
        try:
            if not expiries_list:
                df = copy.deepcopy(exchange)
                df = df[df['name'] == oc_symbol]
                expiries_list = sorted(list(df["expiry"].unique()))
                df = pd.DataFrame({"Expiry Date": expiries_list})
                df = df.set_index("Expiry Date",drop=True)
                oc.range("b1").value = df

            if not instrument_dict and oc_expiry is not None:
                df = copy.deepcopy(exchange)
                df = df[df["name"] == oc_symbol]

                df = df[df["expiry"] == oc_expiry.date()]
                lot_size= list(df["lot_size"])[0]
                oc.range("e4").value = lot_size
                

                for i in df.index:
                    instrument_dict[f'NFO:{df["tradingsymbol"][i]}'] = {"strikePrice":float(df["strike"][i]),
                                                                        "instrumentType":df["instrument_type"][i],
                                                                        "token":df["instrument_token"][i]}
                    #print(instrument_dict)
                stop_thread = False
                thread = threading.Thread(target=get_oi,args=(instrument_dict,))
                thread.start()
            option_data = {}
            instrument_for_ltp = "NSE:NIFTY 50" if oc_symbol == "NIFTY" else (
                "NSE:NIFTY BANK" if oc_symbol == "BANKNIFTY" else f"NSE:{oc_symbol}")
            underlying_price = kite.quote(instrument_for_ltp)[instrument_for_ltp]["last_price"]
            for symbol,values in kite.quote(list(instrument_dict.keys())).items():
                try:
                    try:
                        option_data[symbol]
                    except:
                        option_data[symbol] = {}
                    option_data[symbol]["strikePrice"] = instrument_dict[symbol]["strikePrice"]
                    option_data[symbol]["instrumentType"] = instrument_dict[symbol]["instrumentType"]
                    option_data[symbol]["lastprice"] = values["last_price"]
                    option_data[symbol]["totalTradedVolume"] = int(values["volume"]/lot_size)
                    option_data[symbol]["openInterest"] = int(values["oi"]/lot_size)                    
                    option_data[symbol]["change"] = values["last_price"] - values["ohlc"]["close"] if values["last_price"] != 0 else 0
                    try:
                        option_data[symbol]["changeinOpenInterest"] = int((values["oi"] - prev_day_oi[symbol])/lot_size)
                    except:
                        option_data[symbol]["changeinOpenInterest"] = None

                    def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
                        try: 
                            t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
                            S = asset_price
                            K = strike_price
                            r = interest_rate
                            if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
                                raise Exception
                            flag = instrument_type[0].lower()
                            imp_v = implied_volatility(premium, S, K, t, r, flag)
                            return {"IV":imp_v,
                                    "Delta":delta(flag,S,K,t,r,imp_v),
                                    "Gamma":gamma(flag,S,K,t,r,imp_v),
                                    "Rho":rho(flag,S,K,t,r,imp_v),
                                    "Theta":theta(flag,S,K,t,r,imp_v),
                                    "Vega":vega(flag,S,K,t,r,imp_v)}
                        except:
                            return {"IV":0,
                                    "Delta":0,
                                    "Gamma":0,
                                    "Rho":0,
                                    "Theta":0,
                                    "Vega":0}
                    greek = greeks(values["last_price"],
                                   oc_expiry.date(),
                                   underlying_price,
                                   instrument_dict[symbol]["strikePrice"],
                                   0.1,
                                   instrument_dict[symbol]["instrumentType"])
                    option_data[symbol]["impliedVolatility"] = greek["IV"]
                except Exception as e:
                    pass
            df = pd.DataFrame(option_data).transpose()
            ce_df = df[df["instrumentType"] == "CE"]
            ce_df = ce_df[["totalTradedVolume","change","lastprice","impliedVolatility","changeinOpenInterest","openInterest","strikePrice"]]
            ce_df = ce_df.rename(columns={"openInterest":"CE OI","changeinOpenInterest":"CE Change in OI","impliedVolatility":"CE IV",
                                          "lastPrice":"CE LTP","change":"CE LTP Change","totalTradedVolume":"CE Volume"})
            ce_df.index = ce_df["strikePrice"]
            ce_df = ce_df.drop(["strikePrice"],axis=1)
            ce_df["Strike"] = ce_df.index
            pe_df = df[df["instrumentType"] == "PE"]
            
            pe_df = pe_df[["strikePrice","openInterest","changeinOpenInterest","impliedVolatility","lastprice","change","totalTradedVolume"]]
            pe_df = pe_df.rename(columns={"openInterest":"PE OI","changeinOpenInterest":"PE Change in OI","impliedVolatility":"PE IV",
                                          "lastPrice":"PE LTP","change":"PE LTP Change","totalTradedVolume":"PE Volume"})
            pe_df.index = pe_df["strikePrice"]
            pe_df = pe_df.drop(["strikePrice"],axis=1)
            df = pd.concat([ce_df,pe_df],axis=1).sort_index()
            df = df.replace(np.nan,0)
            df["Strike"] = df.index
            df.index = [np.nan] * len(df)

            oc.range("d6").value = [["Spot LTP",underlying_price],
                                    ["Total Call OI",sum(list(df["CE OI"]))],
                                    ["Total Put OI",sum(list(df["PE OI"]))],
                                    ["Total Call Change in OI",sum(list(df["CE Change in OI"]))],
                                    ["Total Put Change in OI",sum(list(df["PE Change in OI"]))],
                                    ["",""],
                                    ["Max Call OI",max(list(df["CE OI"]))],
                                    ["Max Put OI",max(list(df["PE OI"]))],
                                    ["Max Call OI Strike",list(df[df["CE OI"] == max(list(df["CE OI"]))]["Strike"])[0]],
                                    ["Max Put OI Strike",list(df[df["PE OI"] == max(list(df["PE OI"]))]["Strike"])[0]],
                                    ["",""],
                                    ["Max Call Change in OI",max(list(df["CE Change in OI"]))],
                                    ["Max Put Change in OI",max(list(df["PE Change in OI"]))],
                                    ["Max Call Change in OI Strike",list(df[df["CE Change in OI"] == max(list(df["CE Change in OI"]))]["Strike"])[0]],
                                    ["Max Put Change in OI Strike",list(df[df["PE Change in OI"] == max(list(df["PE Change in OI"]))]["Strike"])[0]],
                                    ]
            oc.range("g1").value = df

        except Exception as e:
            pass                       


            

                                    
    



# def get_live_data(instruments):
#     global kite, live_data
#     try:
#         live_data
#     except:
#         live_data = {}
#     try:
#         live_data = kite.quote(instruments)
#     except Exception as e:
#         #print(f"Get live data Failed {{{e}}}")
#         pass
#     return live_data

# def place_trade(symbol, quantity, direction):
#     try:
#         order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=symbol[0:3],
#                          tradingsymbol=symbol[4:],
#                          transaction_type=kite.TRANSACTION_TYPE_BUY if direction == "Buy" else kite.TRANSACTION_TYPE_SELL,
#                          quantity=int(quantity),
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=0.0,
#                          validity=kite.VALIDITY_DAY,
#                          tag="TA Python")
#         print(f"order : Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
#         return order
#     except Exception as e:
#         return f"{e}"

# def get_orderbook():
#     global orders
#     try:
#         orders
#     except:
#         orders = {}
#     try:
#         data = pd.DataFrame(kite.orders())
#         data = data[data["tag"] == "TA Python"]
#         data = data.filter(["order_timestamp","exchange","tradingsymbol","transaction_type","quantity","average_price","status","status_message_raw"])
#         data.columns = data.columns.str.replace("_"," ")
#         data.columns = data.columns.str.title()
#         data = data.set_index(["Order Timestamp"],drop=True)
#         print(data)
#         data = data.sort_index(ascending=True)
#         orders = data
#     except Exception as e:
#         print(e)
#         pass
#     return orders

# def greeks(premium,expiry,asset_price,strike_price,interest_rate,instrument_type):
#     t = ((datetime.datetime(expiry.year,expiry.month,expiry.day,15,30) - datetime.datetime.now()) / datetime.timedelta(days=1)) / 365
#     S = asset_price
#     K = strike_price
#     r = interest_rate
#     if premium == 0 or t <= 0 or S <= 0 or K <= 0 or r<= 0:
#         raise Exception
#     flag = instrument_type[0].lower()
#     imp_v = implied_volatility(premium, S, K, t, r, flag)
#     return [imp_v,
#             delta(flag,S,K,t,r,imp_v),
#             gamma(flag,S,K,t,r,imp_v),
#             rho(flag,S,K,t,r,imp_v),
#             theta(flag,S,K,t,r,imp_v),
#             vega(flag,S,K,t,r,imp_v)]

# Exchange = None
# prev_info = {"Symbol": None, "Expiry": None}
# instruments_dict = {}
# option_data = {}

# # def instruments(symbol, expiry):
# #     instruments_dict = {}
# #     option_data = {}
# #     if Exchange is None:
# #         while True:
# #             try:
# #                 Exchange = pd.DataFrame(kite.instruments("NFO"))
# #                 break
# #             except:
# #                 pass
# #     if symbol and not expiry is None:
# #         try:
# #             df = copy.deepcopy(Exchange)
# #             df = df[(df["segment"] == "NFO-OPT") &
# #                         (df["name"] == symbol.upper())]
# #             df = df[df["expiry"] == sorted(list(df["expiry"].unique()))[expiry]]
# #             for i in df.index:
# #                 instruments_dict[f'NFO:{df["tradingsymbol"][i]}'] = {"Strike": float(df["strike"][i]),
# #                                                                               "Segment": df["segment"][i],
# #                                                                  "Instrument Type": df["instrument_type"][i],
# #                                                                  "Expiry": df["expiry"][i],
# #                                                                  "Lot": df["lot_size"][i]}
# #         except:
# #             pass
# #     prev_info = {"Symbol": symbol, "Expiry": expiry}
# #     return instruments_dict

# # pfe = instruments('NIFTY','29-03-2023')
# # print(pfe)

        
# def quote(instruments):
#     if instruments:
#         try:
#             data = kite.quote(instruments)
#             print(data.tail(50))
#             for symbol, values in data.items():
#                 try:
#                     option_data[symbol[4:]]
#                 except:
#                     option_data[symbol[4:]] = {}
#                 option_data[symbol[4:]]["Strike"] = instruments_dict[symbol]["Strike"]
#                 option_data[symbol[4:]]["Lot"] = instruments_dict[symbol]["Lot"]
#                 option_data[symbol[4:]]["Expiry"] = instruments_dict[symbol]["Expiry"]
#                 option_data[symbol[4:]]["Instument Type"] = instruments_dict[symbol]["Instrument Type"]
#                 option_data[symbol[4:]]["Open"] = values["ohlc"]["open"]
#                 option_data[symbol[4:]]["High"] = values["ohlc"]["high"]
#                 option_data[symbol[4:]]["Low"] = values["ohlc"]["low"]
#                 option_data[symbol[4:]]["Ltp"] = values["last_price"]
#                 option_data[symbol[4:]]["Close"] = values["ohlc"]["close"]
#                 option_data[symbol[4:]]["Volume"] = values["volume"]
#                 option_data[symbol[4:]]["Vwap"] = values["average_price"]
#                 option_data[symbol[4:]]["OI"] = values["oi"]
#                 option_data[symbol[4:]]["OI High"] = values["oi_day_high"]
#                 option_data[symbol[4:]]["OI Low"] = values["oi_day_low"]
#                 option_data[symbol[4:]]["Buy Qty"] = values["buy_quantity"]
#                 option_data[symbol[4:]]["Sell Qty"] = values["sell_quantity"]
#                 option_data[symbol[4:]]["Ltq"] = values["last_quantity"]
#                 option_data[symbol[4:]]["Change"] = values["net_change"]
#                 option_data[symbol[4:]]["Bid Price"] = values["depth"]["buy"][0]["price"]
#                 option_data[symbol[4:]]["Bid Qty"] = values["depth"]["buy"][0]["quantity"]
#                 option_data[symbol[4:]]["Ask Price"] = values["depth"]["sell"][0]["price"]
#                 option_data[symbol[4:]]["Ask Qty"] = values["depth"]["sell"][0]["quantity"]
#         except:
#             pass
#     return option_data

# gfg = quote('NSE:NIFTY 50')
# print(gfg)

# def start_excel():
#     global kite, live_data
#     print("Excel Starting....")
#     if not os.path.exists("TA_Python.xlsx"):
#         try:
#             wb = xw.Book()
#             wb.save("TA_Python.xlsx")
#             wb.close()
#         except Exception as e:
#             print(f"Error : {e}")
#             sys.exit()
#     wb = xw.Book('TA_Python.xlsx')
#     for i in ["Data","Exchange","OrderBook"]:
#         try:
#             wb.sheets(i)
#         except:
#             wb.sheets.add(i)
#     dt = wb.sheets("Data")
#     ex = wb.sheets("Exchange")
#     ob = wb.sheets("OrderBook")
#     ex.range("a:n").value = ob.range("a:h").value = dt.range("p:q").value = None
#     dt.range(f"a1:q1").value = ["Sr No","Symbol","Open","high","Low","LTP","Volume","Vwap","Best Bid Price",
#                                 "Best Ask Price","Close","OI","IV","Delta","Gamma","Rho","Theta","Vega","Qty","Direction","Entry Signal","Exit Signal","Entry","Exit"]
    
#     subs_lst = []
#     while True:
#         try:
#             master_contract = pd.DataFrame(kite.instruments())
#             #master_contract = master_contract.drop(["instrument_token","exchange_token","last_price","tick_size"],axis=1)
#             master_contract["watchlist_symbol"] = master_contract["exchange"] + ":" + master_contract["tradingsymbol"]
#             master_contract.columns = master_contract.columns.str.replace("_"," ")
#             master_contract.columns = master_contract.columns.str.title()
#             ex.range("a1").value = master_contract

#             df = copy.deepcopy(master_contract)
#             df = df[df["Segment"] == "NFO-OPT"]
#             nfo_dict = {}
#             for i in df.index:
#                 nfo_dict[f'NFO:{df["Tradingsymbol"][i]}'] = [df["Expiry"][i],df["Strike"][i],df["Name"][i]]
#             break
#         except Exception as e:
#             time.sleep(1)
#     while True:
#         try:
#             time.sleep(0.5)
#             get_live_data(subs_lst)
#             symbols = dt.range(f"b{2}:b{500}").value
#             trading_info = dt.range(f"s{2}:x{500}").value

#             for i in subs_lst:
#                 if i not in symbols:
#                     subs_lst.remove(i)
#                     try:
#                         del live_data[i]
#                     except Exception as e:
#                         pass
#             main_list = []
#             idx = 0
#             for i in symbols:
#                 lst = [None,None,None,None,None,None,None,None,
#                         None,None,None,None,None,None,None,None]
#                 if i:
#                     if i not in subs_lst:
#                         subs_lst.append(i)
#                     if i in subs_lst:
#                         try:
#                             lst = [live_data[i]["ohlc"]["open"],
#                                    live_data[i]["ohlc"]["high"],
#                                    live_data[i]["ohlc"]["low"],
#                                    live_data[i]["last_price"]]
#                             try:
#                                 lst += [live_data[i]["volume"],
#                                         live_data[i]["average_price"],
#                                         live_data[i]["depth"]["buy"][0]["price"],
#                                         live_data[i]["depth"]["sell"][0]["price"],
#                                         live_data[i]["ohlc"]["close"],
#                                         live_data[i]["oi"]]
#                                 try:
#                                     lst += greeks(premium=live_data[i]["last_price"],
#                                                     expiry=nfo_dict[i][0],
#                                                     asset_price=live_data["NSE:NIFTY 50" if nfo_dict[i][2] == "NIFTY" else ("NSE:NIFTY BANK" if nfo_dict[i][2] == "BANKNIFTY" else f"NSE:{nfo_dict[i][2]}")]["last_price"],
#                                                     strike_price=nfo_dict[i][1],
#                                                     interest_rate=0.1,
#                                                     instrument_type=i[-2:])
#                                 except Exception as e:
#                                     lst += ["-","-","-","-","-","-"]

#                             except:
#                                 lst += [0,0,0,0,live_data[i]["ohlc"]["close"],0,"-","-","-","-","-","-"]
#                             trade_info = trading_info[idx]
#                             if trade_info[0] is not None and trade_info[1] is not None:
#                                 if type(trade_info[0]) is float and type(trade_info[1]) is str:
#                                     if trade_info[1].upper() == "BUY" and trade_info[2] is True:
#                                         if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
#                                             dt.range(f"w{idx + 2}").value = place_trade(i,int(trade_info[0]),"Buy")
#                                         elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
#                                             dt.range(f"x{idx +2}").value = place_trade(i, int(trade_info[0]), "Sell")
#                                     if trade_info[1].upper() == "SELL" and trade_info[2] is True:
#                                         if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
#                                             dt.range(f"w{idx +2 }").value = place_trade(i, int(trade_info[0]), "Sell")
#                                         elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
#                                             dt.range(f"x{idx + 2}").value = place_trade(i, int(trade_info[0]),"Buy")
#                         except Exception as e:
#                             pass
#                 main_list.append(lst)
#                 idx +=1
            
#             dt.range("c2").value = main_list
#             if wb.sheets.active.name == "OrderBook":
#                 ob.range("a1").value = get_orderbook()
#         except Exception as e:
#             print(e)

# if __name__=='__main__':
#     # get_login_credentials()
#     # get_access_token()
#     # get_kite()

#     # user_id = "YR6706"       # Login Id
#     # password = "vaa6762m"      # Login password
#     # twofa = "274957"         # Login Pin or TOTP
#     # enctoken = get_enctoken(user_id, password, twofa)
#     # kite = KiteApp(enctoken=enctoken)

#     enctoken = "pl2QjIkbYC21S2iKAYEE7JBKF2gMnvj2SoXPBvsblM27blj4R3YorWzyJphfuefkfbtfxlBvm50nbcKcjNvJrUs5bCUelQLL+SPbgaPFTeMtNXOzSGJFAQ=="
#     kite = KiteApp(enctoken=enctoken)
#     get_orderbook()
#     # quote('NIFTY')
#     start_excel()



