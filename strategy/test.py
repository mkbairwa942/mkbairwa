import os
from kite_trade import *
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


if 0 > 0 :
    print("yes")
else :
    print("no")

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

def place_trade(symbol,Qtyy,OrderTypee,ScripCodee,Pricee,StopLossPricee):
    try:
        order = client.place_order(
                            OrderType='B' if OrderTypee == "BUY" else 'S',
                            Exchange='N',
                            ExchangeType='C',
                            ScripCode = ScripCodee,
                            Qty=Qtyy,
                            Price=Pricee, 
                            IsIntraday=True, 
                            IsStopLossOrder=True, 
                            StopLossPrice=StopLossPricee)
        # order = kite.place_order(variety=kite.VARIETY_REGULAR,
        #                  exchange=symbol[0:3],
        #                  tradingsymbol=symbol[4:],
        #                  transaction_type=kite.TRANSACTION_TYPE_BUY if direction == "Buy" else kite.TRANSACTION_TYPE_SELL,
        #                  quantity=int(quantity),
        #                  product=kite.PRODUCT_MIS,
        #                  order_type=kite.ORDER_TYPE_MARKET,
        #                  price=0.0,
        #                  validity=kite.VALIDITY_DAY,
        #                  tag="TA Python")
        print(f"order : Symbol {symbol}, Qty {Qtyy}, Direction {OrderTypee}, Time {datetime.datetime.now().time()}{order}")
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
        # data = pd.DataFrame(client.order_book())

        ordbook = pd.DataFrame(client.order_book())
        # ordbook = ordbook[0:37]
        ordbook1 = ordbook    
        Datetimeee = []
        ord_type = []
        for i in range(len(ordbook)):
            ord_typ = ordbook['ScripName'][i]
            ord_type1 = ord_typ[22:24]
            ord_type.append(ord_type1)
            datee = ordbook['BrokerOrderTime'][i]
            timestamp = pd.to_datetime(datee[6:19], unit='ms')
            ExpDate = datetime.strftime(timestamp, '%d-%m-%Y %H:%M:%S')
            d1 = datetime(int(ExpDate[6:10]),int(ExpDate[3:5]),int(ExpDate[0:2]),int(ExpDate[11:13]),int(ExpDate[14:16]),int(ExpDate[17:19]))
            d2 = d1 + timedelta(hours = 5.5)
            Datetimeee.append(d2)
        ordbook['Datetimeee'] = Datetimeee
        ordbook['ord_type'] = ord_type   
        #ordbook = ordbook[ordbook["OrderStatus"] != "Rejected By 5P"]
        ordbook = ordbook[['Datetimeee', 'BrokerOrderId', 'BuySell','OrderStatus', 'DelvIntra','PendingQty','Qty','Rate','RemoteOrderID','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ScripName','ord_type','AtMarket']]
        ordbook = ordbook[ordbook["BuySell"] == "B"] 
        ordbook.rename(columns={'ScripName': 'Symbol'},inplace=True)
          
        orders = ordbook
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
       
def quote(instruments):
    if instruments:
        try:
            data = kite.quote(instruments)
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

# gfg = quote('NSE:SBIN')
# print(gfg)

def start_excel():
    global kite, live_data
    print("Excel Starting....")
    if not os.path.exists("test.xlsx"):
        try:
            wb = xw.Book()
            wb.save("test.xlsx")
            wb.close()
        except Exception as e:
            print(f"Error : {e}")
            sys.exit()
    wb = xw.Book('test.xlsx')
    for i in ["Data","Exchange","OrderBook","Position","Extra"]:
        try:
            wb.sheets(i)
        except:
            wb.sheets.add(i)
    dt = wb.sheets("Data")
    ex = wb.sheets("Exchange")
    ob = wb.sheets("OrderBook")
    pos = wb.sheets("Position")
    ext = wb.sheets("Extra")
    #ex.range("a:u").value = None
    ob.range("a:s").value = None
    dt.range("e:m").value = None
    dt.range(f"a1:q1").value = ["Symbol","Buy/Sell","Scripcode","Symbol_Conc","Open","high","Low","LTP","Volume","Vwap","Close","OI","NetChange",
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
            sym = dt.range(f"d{2}:d{500}").value
            symbols = list(filter(lambda item: item is not None, sym))
            # trading_info = dt.range(f"s{2}:x{10}").value
            trading_info = ext.range(f"n{2}:x{10}").value


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
                            # if trade_info[0] is not None and trade_info[1] is not None:
                            #     if type(trade_info[0]) is float and type(trade_info[1]) is str:
                            #         if trade_info[1].upper() == "BUY" and trade_info[2] is True:
                            #             if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                            #                 dt.range(f"w{idx + 2}").value = place_trade(i,int(trade_info[0]),"Buy")
                            #             elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
                            #                 dt.range(f"x{idx +2}").value = place_trade(i, int(trade_info[0]), "Sell")
                            #         if trade_info[1].upper() == "SELL" and trade_info[2] is True:
                            #             if trade_info[2] is True and trade_info[3] is not True and trade_info[4] is None and trade_info[5] is None:
                            #                 dt.range(f"w{idx +2 }").value = place_trade(i, int(trade_info[0]), "Sell")
                            #             elif trade_info[2] is True and trade_info[3] is True and trade_info[4] is not None and trade_info[5] is None:
                            #                 dt.range(f"x{idx + 2}").value = place_trade(i, int(trade_info[0]),"Buy")
                            if trade_info[0] is not None and trade_info[1] is not None:
                                if type(trade_info[0]) is int and type(trade_info[1]) is str:
                                    if trade_info[0] > 0 and trade_info[1].upper() == "Buy" :
                                        #place_trade(symbol,Qtyy,OrderTypee,ScripCodee,Pricee,StopLossPricee)
                                        ext.range(f"w{idx + 2}").value = place_trade(i,int(trade_info[0]),int(trade_info[1]),int(trade_info[2]),int(trade_info[3]),int(trade_info[4]))

                                    if trade_info[0] > 0 and trade_info[1].upper() == "SELL":                                        
                                        ext.range(f"w{idx +2 }").value = place_trade(i, int(trade_info[0]), "Sell")

                        except Exception as e:
                            pass

                main_list.append(lst)
                idx +=1

            main_list2 = pd.DataFrame(main_list, columns =['Open','high','Low','LTP','Volume','Vwap','Close','OI','NetChange','IV','Delta','Gamma','Rho','Theta','Vega'])
            main_list2['column'] = i
            print(main_list2)

            
            dt.range("e1").options(index=False).value = main_list2
            
            data_excel = pd.read_excel('E:/STOCK/Capital_vercel1/test.xlsx', sheet_name='Data')
            odbook = get_orderbook() 

            filt_data = pd.merge(data_excel, odbook, on=['Symbol'], how='inner')
            pos.range("a10").options(index=False).value = filt_data
            main_list1 = pd.DataFrame(main_list, columns =['Open','high','Low','LTP','Volume','Vwap','Close','OI','NetChange','IV','Delta','Gamma','Rho','Theta','Vega'])

            
            fun = pd.DataFrame(client.margin())
            fund = fun['AvailableMargin']
            fund = 28000
            print(fund)
            leght = fund/(len(main_list1['LTP']))
            print(leght)
            main_list1['Qty'] = round((leght/(main_list1['LTP'])),0)
            main_list1 = main_list1[['Open','high','Low','LTP','Volume','Vwap','Close','OI','NetChange','Qty']]
            ext.range("e1:n20").value = None
            ext.range("e1").options(index=False).value = main_list1
            ob.range("a1").options(index=False).value = get_orderbook() 
            pos.range("a1").options(index=False).value = pd.DataFrame(client.margin())
            pos.range("a4").options(index=False).value = pd.DataFrame(client.positions())
            
            wb.save("test.xlsx")                       
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



