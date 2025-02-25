import os
from imp_strategy.kite_trade import *
# from kiteconnect import KiteConnect
from five_paisa import *
import time,json,datetime,sys
import xlwings as xw
import pandas as pd
import numpy as np
import copy
import time
import dateutil.parser
import threading
from datetime import datetime,timedelta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)

# def get_login_credentials():
#     global login_credential

#     def login_credentials():
#         print("----Enter your Zerodha Login Credentials ----")
#         login_credential = {"api_key": str(input("Enter API Key :")),
#                             "api_secret": str(input("Enter API Secret :"))
#                             }
#         if input("press Y to save login credential and any key to bypass : ").upper() =="Y":
#             with open(f"Login Credentials.txt", "w")as f:
#                 json.dump(login_credential, f)
#             print("Data saved...")
#         else:
#             print("Data save cancelled !!!!")
    
#     while True:
#         try:
#             with open(f"Login Credentials.txt", "r") as f:
#                 login_credential = json.load(f)
#             break
#         except:
#             login_credentials()
#     return login_credential

# def get_access_token():
#     global access_token

#     def login():
#         global login_credential
#         print("Trying Log in...")
#         kite = KiteConnect(api_key=login_credential["api_key"])
#         print("Login url : ",kite.login_url())
#         request_tkn = input("Login and enter your request token here : ")
#         try:
#             access_token = kite.generate_session(request_token=request_tkn, api_secret=login_credential["api_secret"])['access_token']
#             os.makedirs(f"AccessToken", exist_ok=True)
#             with open(f"AccessToken/{datetime.datetime.now().date()}.json","w") as f:
#                 json.dump(access_token, f)
#             print("Login successful...")
#         except Exception as e:
#             print(f"Login Failed {{{e}}}")
#     print("Loading access token...")
#     while True:
#         if os.path.exists(f"AccessToken/{datetime.datetime.now().date()}.json"):
#             with open(f"AccessToken/{datetime.datetime.now().date()}.json","r") as f:
#                 access_token = json.load(f)
#             break
#         else:
#             login()
#     return access_token

# def get_kite():
#     global kite, login_credential,access_token
#     try:
#         kite = KiteConnect(api_key=login_credential["api_key"])
#         kite.set_access_token(access_token)
#     except Exception as e:
#         print(f"Error : {e}")
#         os.remove(f"AccessToken/{datetime.datetime.now().date()}.json") if os.path.exists(
#             f"AccessToken/{datetime.datetime.now().date()}.json") else None
#         sys.exit()


def get_live_data(Exchange,ExchangeType,Symbol):

    try:
        live_data
    except:
        live_data = {}
    try:
        live_data = client.fetch_market_depth_by_symbol([{"Exchange":Exchange,"ExchangeType":ExchangeType,"Symbol":Symbol}])
    except Exception as e:
        pass
    return live_data

# gfgg = get_live_data('N','C','HDFC')
# print(gfgg)
live_data = get_live_data('N','C','HDFC')

def place_trade(symbol, quantity, direction):
    try:
        order = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=symbol[0:3],
                         tradingsymbol=symbol[4:],
                         transaction_type=kite.TRANSACTION_TYPE_BUY if direction == "Buy" else kite.TRANSACTION_TYPE_SELL,
                         quantity=int(quantity),
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=0.0,
                         validity=kite.VALIDITY_DAY,
                         tag="TA Python")
        print(f"order : Symbol {symbol}, Qty {quantity}, Direction {direction}, Time {datetime.datetime.now().time()}{order}")
        return order
    except Exception as e:
        return f"{e}"

def get_orderbook():
    global orders
    try:
        orders
    except:
        orders = {}
    try:
        data = pd.DataFrame(client.order_book())
        # data = data[data["tag"] == "TA Python"]
        # data = data.filter(["order_timestamp","exchange","tradingsymbol","transaction_type","quantity","average_price","status","status_message_raw"])
        # data.columns = data.columns.str.replace("_"," ")
        # data.columns = data.columns.str.title()
        # data = data.set_index(["Order Timestamp"],drop=True)
        # print(data)
        # data = data.sort_index(ascending=True)
        orders = data
    except Exception as e:
        print(e)
        pass
    return orders

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

Exchange = None
prev_info = {"Symbol": None, "Expiry": None}
instruments_dict = {}
option_data = {}

# def instruments(symbol, expiry):
#     instruments_dict = {}
#     option_data = {}
#     if Exchange is None:
#         while True:
#             try:
#                 Exchange = pd.DataFrame(kite.instruments("NFO"))
#                 break
#             except:
#                 pass
#     if symbol and not expiry is None:
#         try:
#             df = copy.deepcopy(Exchange)
#             df = df[(df["segment"] == "NFO-OPT") &
#                         (df["name"] == symbol.upper())]
#             df = df[df["expiry"] == sorted(list(df["expiry"].unique()))[expiry]]
#             for i in df.index:
#                 instruments_dict[f'NFO:{df["tradingsymbol"][i]}'] = {"Strike": float(df["strike"][i]),
#                                                                               "Segment": df["segment"][i],
#                                                                  "Instrument Type": df["instrument_type"][i],
#                                                                  "Expiry": df["expiry"][i],
#                                                                  "Lot": df["lot_size"][i]}
#         except:
#             pass
#     prev_info = {"Symbol": symbol, "Expiry": expiry}
#     return instruments_dict

# pfe = instruments('NIFTY','29-03-2023')
# print(pfe)

        
def quote(instruments):
    if instruments:
        try:
            data = kite.quote(instruments)
            print(data.tail(50))
            for symbol, values in data.items():
                try:
                    option_data[symbol[4:]]
                except:
                    option_data[symbol[4:]] = {}
                option_data[symbol[4:]]["Strike"] = instruments_dict[symbol]["Strike"]
                option_data[symbol[4:]]["Lot"] = instruments_dict[symbol]["Lot"]
                option_data[symbol[4:]]["Expiry"] = instruments_dict[symbol]["Expiry"]
                option_data[symbol[4:]]["Instument Type"] = instruments_dict[symbol]["Instrument Type"]
                option_data[symbol[4:]]["Open"] = values["ohlc"]["open"]
                option_data[symbol[4:]]["High"] = values["ohlc"]["high"]
                option_data[symbol[4:]]["Low"] = values["ohlc"]["low"]
                option_data[symbol[4:]]["Ltp"] = values["last_price"]
                option_data[symbol[4:]]["Close"] = values["ohlc"]["close"]
                option_data[symbol[4:]]["Volume"] = values["volume"]
                option_data[symbol[4:]]["Vwap"] = values["average_price"]
                option_data[symbol[4:]]["OI"] = values["oi"]
                option_data[symbol[4:]]["OI High"] = values["oi_day_high"]
                option_data[symbol[4:]]["OI Low"] = values["oi_day_low"]
                option_data[symbol[4:]]["Buy Qty"] = values["buy_quantity"]
                option_data[symbol[4:]]["Sell Qty"] = values["sell_quantity"]
                option_data[symbol[4:]]["Ltq"] = values["last_quantity"]
                option_data[symbol[4:]]["Change"] = values["net_change"]
                option_data[symbol[4:]]["Bid Price"] = values["depth"]["buy"][0]["price"]
                option_data[symbol[4:]]["Bid Qty"] = values["depth"]["buy"][0]["quantity"]
                option_data[symbol[4:]]["Ask Price"] = values["depth"]["sell"][0]["price"]
                option_data[symbol[4:]]["Ask Qty"] = values["depth"]["sell"][0]["quantity"]
        except:
            pass
    return option_data

gfg = quote('NSE:SBIN')
print(gfg)

def start_excel():
    global kite, live_data
    print("Excel Starting....")
    if not os.path.exists("Excel_TA_Python_5paisa.xlsx"):
        try:
            wb = xw.Book()
            wb.save("Excel_TA_Python_5paisa.xlsx")
            wb.close()
        except Exception as e:
            print(f"Error : {e}")
            sys.exit()
    wb = xw.Book('Excel_TA_Python_5paisa.xlsx')
    for i in ["Data","Exchange","OrderBook","Extra"]:
        try:
            wb.sheets(i)
        except:
            wb.sheets.add(i)
    dt = wb.sheets("Data")
    ex = wb.sheets("Exchange")
    ob = wb.sheets("OrderBook")
    ext = wb.sheets("Extra")
    #ex.range("a:u").value = ob.range("a:h").value = None
    dt.range("c:l").value = None
    dt.range(f"a1:q1").value = ["Sr No","Symbol","Open","high","Low","LTP","Volume","Vwap","Close","OI","NetChange",
                                "IV","Delta","Gamma","Rho","Theta","Vega","Qty","Direction","Entry Signal","Exit Signal","Entry","Exit"]
    master_contract = None
    subs_lst = []
    while True:
        if master_contract is None: 
            try:
                master_contract = pd.DataFrame(script_code_5paisa)
                master_contract = master_contract[(master_contract["Exch"] == "N")]
                # master_contract = master_contract[(master_contract["Exch"] == "N") & (master_contract["ExchType"] == "C")]
                master_contract["Watchlist_Symbol"] = master_contract["Exch"] + ":" + master_contract["ExchType"] + ":" + master_contract["Name"]
                ex.range("a1").value = master_contract
                print("Exchange Download")
                df = copy.deepcopy(master_contract)
                df = df[(df["CpType"] != "EQ") & (df["CpType"] != "XX") & (df["ExchType"] == "D")]
                # nfo_dict = {}
                # for i in df.index:
                #     print(i)
                #     nfo_dict[f'NFO:{df["Name"][i]}'] = [df["Expiry"][i],df["StrikeRate"][i],df["Root"][i]]                          
                # new_dict = pd.DataFrame.from_dict(nfo_dict)
                # ext.range("a1").value = new_dict
                # print("NFO Dict Download")
                break
            except Exception as e:
                time.sleep(1)
    
    while True:
        try:
            time.sleep(0.5)  
            sym = dt.range(f"b{2}:b{500}").value
            symbols = list(filter(lambda item: item is not None, sym))
            trading_info = dt.range(f"s{2}:x{500}").value

            subs_lst = symbols
            for i in subs_lst:   
                if i not in symbols:
                    subs_lst.remove(i)
                    try:
                        del live_data[i]
                    except Exception as e:
                        pass
            main_list = []
            idx = 0
            for i in symbols:
                lst = [None,None,None,None,None,None,None,None,
                        None,None,None,None,None,None,None,None]
                if i:
                    if i not in subs_lst:
                        subs_lst.append(i)
                    if i in subs_lst:
                        try:
                            inst1 = i.split(":")[0]
                            inst2 = i.split(":")[1]
                            inst3 = i.split(":")[2]
                            live_data = get_live_data(inst1,inst2,inst3)
                            lst = [
                                   live_data['Data'][0]['Open'],
                                   live_data['Data'][0]['High'],
                                   live_data['Data'][0]['Low'],
                                   live_data['Data'][0]["LastTradedPrice"],
                                   live_data['Data'][0]["Volume"],
                                   live_data['Data'][0]["AverageTradePrice"],
                                   live_data['Data'][0]["Close"],
                                   live_data['Data'][0]["OpenInterest"],
                                   live_data['Data'][0]["NetChange"]]                                   

                            try:
                                lst += greeks(
                                    premium=live_data['Data'][0]["LastTradedPrice"],
                                                # expiry=nfo_dict[i][0],
                                                # asset_price=live_data["N:D:NIFTY 50" if nfo_dict[i][2] == "NIFTY" else ("N:D:NIFTY BANK" if nfo_dict[i][2] == "BANKNIFTY" else f"N:D:{nfo_dict[i][2]}")]["last_price"],
                                                # strike_price=nfo_dict[i][1],
                                                # interest_rate=0.1,
                                                # instrument_type=i[-2:]
                                                )
                            except Exception as e:
                                    lst += ["-","-","-","-","-","-"]

                            except:
                                lst += [0,0,0,0,live_data[i]["ohlc"]["close"],0,"-","-","-","-","-","-"]
                            trade_info = trading_info[idx]
                            if trade_info[0] is not None and trade_info[1] is not None:
                                if type(trade_info[0]) is float and type(trade_info[1]) is str:
                                    if trade_info[1].upper() == "BUY" and trade_info[2] is True:
                                        if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                                            dt.range(f"w{idx + 2}").value = place_trade(i,int(trade_info[0]),"Buy")
                                        elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
                                            dt.range(f"x{idx +2}").value = place_trade(i, int(trade_info[0]), "Sell")
                                    if trade_info[1].upper() == "SELL" and trade_info[2] is True:
                                        if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                                            dt.range(f"w{idx +2 }").value = place_trade(i, int(trade_info[0]), "Sell")
                                        elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
                                            dt.range(f"x{idx + 2}").value = place_trade(i, int(trade_info[0]),"Buy")
                        except Exception as e:
                            pass

                main_list.append(lst)
                idx +=1
                # print(main_list)
                # print(idx)
            
            dt.range("c2").value = main_list
            if wb.sheets.active.name == "OrderBook":
                ob.range("a1").options(index=False).value = get_orderbook()                
        except Exception as e:
            print(e)

if __name__=='__main__':
    # get_login_credentials()
    # get_access_token()
    # get_kite()

    # user_id = "YR6706"       # Login Id
    # password = "vaa6762m"      # Login password
    # twofa = "274957"         # Login Pin or TOTP
    # enctoken = get_enctoken(user_id, password, twofa)
    # kite = KiteApp(enctoken=enctoken)

    enctoken = "gQ/zLVyhmVCyuSSga5+qu+44S7z7kcKiOfb1eww3FYFrhVfgG/0pUuTcpc5Kz0yYWInqvFG1XZT+9CKGNf8Za4LEWssj1r0UnZcaQnO/NiuuvETXs9trrA=="
    kite = KiteApp(enctoken=enctoken)
    # get_orderbook()
    # quote('NIFTY')
    start_excel()



