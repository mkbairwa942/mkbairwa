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

pd.options.mode.copy_on_write = True

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)


live_market_keys = ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                        'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100',
                        'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200', 'NIFTY AUTO',
                        'NIFTY BANK', 'NIFTY ENERGY', 'NIFTY FINANCIAL SERVICES',
                        'NIFTY FINANCIAL SERVICES 25/50', 'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL',
                        'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY PRIVATE BANK',                        
                        'NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
                        'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30',
                        'NIFTY200 MOMENTUM 30',
                        'NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE',
                        'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                        'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15']#,'Securities in F&O', ]

class NseIndia:

    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple'
                                      'WebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("https://nseindia.com", headers=self.headers)
  
    def get_stock_info(self, symbol, trade_info=False):
        if trade_info:
            url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol + "&section=trade_info"
        else:
            url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol
        data = self.session.get(url, headers=self.headers).json()
        return data

    def get_stock_fno_info(self, symbol, trade_info=False):
        if trade_info:
            url = 'https://www.nseindia.com/api/quote-derivative?symbol=' + symbol + "&section=trade_info"
        else:
            url = 'https://www.nseindia.com/api/quote-derivative?symbol=' + symbol
        data = self.session.get(url, headers=self.headers).json()
        return data

    def live_market_data(self, key, symbol_list=False):
        data = self.session.get(
            f"https://www.nseindia.com/api/equity-stockIndices?index="
            f"{key.upper().replace(' ', '%20').replace('&', '%26')}",
            headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        df = df.drop(["meta"], axis=1)
        df = df.set_index("symbol", drop=True)
        df =  df[['identifier','open','dayHigh','dayLow',
            'lastPrice','previousClose','change','pChange',
            'totalTradedVolume','totalTradedValue','lastUpdateTime']]            
        if symbol_list:
            return list(df.index)
        else:
            return df

nse = NseIndia()

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
# live_data = get_live_data('N','C','HDFC')

# def place_trade(symbol,Qtyy,OrderTypee,ScripCodee,Pricee,StopLossPricee):
#     try:
#         order = client.place_order(
#                             OrderType='B' if OrderTypee == "BUY" else 'S',
#                             Exchange='N',
#                             ExchangeType='C',
#                             ScripCode = ScripCodee,
#                             Qty=Qtyy,
#                             Price=Pricee, 
#                             IsIntraday=True, 
#                             IsStopLossOrder=True, 
#                             StopLossPrice=StopLossPricee)
#         # order = kite.place_order(variety=kite.VARIETY_REGULAR,
#         #                  exchange=symbol[0:3],
#         #                  tradingsymbol=symbol[4:],
#         #                  transaction_type=kite.TRANSACTION_TYPE_BUY if direction == "Buy" else kite.TRANSACTION_TYPE_SELL,
#         #                  quantity=int(quantity),
#         #                  product=kite.PRODUCT_MIS,
#         #                  order_type=kite.ORDER_TYPE_MARKET,
#         #                  price=0.0,
#         #                  validity=kite.VALIDITY_DAY,
#         #                  tag="TA Python")
#         print(f"order : Symbol {symbol}, Qty {Qtyy}, Direction {OrderTypee}, Time {datetime.datetime.now().time()}{order}")
#         return order
#     except Exception as e:
#         return f"{e}"

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
        ordbook = ordbook[['Datetimeee','ScripName','Qty','Rate', 'BrokerOrderId', 'BuySell','OrderStatus', 'DelvIntra','PendingQty','RemoteOrderID','SLTriggerRate','WithSL','ScripCode','Reason', 'ExchType', 'MarketLot', 'OrderValidUpto','ord_type','AtMarket']]
        ordbook = ordbook[(ordbook["OrderStatus"] != "Rejected By 5P") & (ordbook["OrderStatus"] != "Rejected by Exch    ")] 
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
    if not os.path.exists("test1.xlsx"):
        try:
            wb = xw.Book()
            wb.save("test1.xlsx")
            wb.close()
        except Exception as e:
            print(f"Error : {e}")
            sys.exit()
    wb = xw.Book('test1.xlsx')
    for i in ["Data","Exchange","OrderBook","Position","Stat","Stat1","Stat2","Stat3","Stat4"]:
        try:
            wb.sheets(i)
        except:
            wb.sheets.add(i)
    dt = wb.sheets("Data")
    ex = wb.sheets("Exchange")
    ob = wb.sheets("OrderBook")
    pos = wb.sheets("Position")
    st = wb.sheets("Stat")
    st1 = wb.sheets("Stat1")
    st2 = wb.sheets("Stat2")
    st3 = wb.sheets("Stat3")
    st4 = wb.sheets("Stat4")
    #ex.range("a:u").value = None
    ob.range("a:s").value = None
    dt.range("e:o").value = None
    st.range("a:u").value = None
    st1.range("a:u").value = None
    st2.range("a:u").value = None
    st3.range("a:u").value = None
    st4.range("a:u").value = None
    pos.range("a:r").value = None
    wb.save("test1.xlsx")
    dt.range(f"a1:d1").value = ["Namee","Buy/Sell","Scripcode","Symbol_Conc"]#,"Open","high","Low","LTP","Volume","Vwap","Close","OI","NetChange","IV","Delta","Gamma","Rho","Theta","Vega","Qty","Direction","Entry Signal","Exit Signal","Entry","Exit"]
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
                # st.range("a1").value = new_dict
                # print("NFO Dict Download")
                break
            except Exception as e:
                time.sleep(1)
    
    while True:
        try:
            time.sleep(0.5)            
            scpt = dt.range(f"a{2}:c{500}").value            
            sym = dt.range(f"d{2}:d{500}").value
            # trading_info = dt.range(f"s{2}:x{10}").value
            trading_info = st.range(f"n{2}:x{10}").value  

            scpts = pd.DataFrame(scpt, columns=['Symbol','Buy/Sell','ScriptCode'])
            index = ['N:C:NIFTY','N:C:BANKNIFTY'] #999920000 999920005
            symbols = list(filter(lambda item: item is not None, sym))
            for li in index:                 
                symbols.append(li)
            symbols.reverse()

            subs_lst = symbols
            for i in subs_lst:   
                if i not in symbols:
                    subs_lst.remove(i)
                    try:
                        del live_data[i]
                    except Exception as e:
                        pass
            main_list = pd.DataFrame()
            idx = 0
            for i in symbols:
                # lst = [None,None,None,None,None,None,None,None,
                #         None,None,None,None,None,None,None,None]
                if i:
                    if i not in subs_lst:
                        subs_lst.append(i)
                    if i in subs_lst:
                        try:
                            main_li = pd.DataFrame()
                            inst1 = i.split(":")[0]
                            inst2 = i.split(":")[1]
                            inst3 = i.split(":")[2]
                            live_data = get_live_data(inst1,inst2,inst3)
                            main_li['Symbol'] = inst3,
                            main_li['Open'] = live_data['Data'][0]['Open'],
                            main_li['High'] = live_data['Data'][0]['High'],
                            main_li['Low'] = live_data['Data'][0]['Low'],
                            main_li['LTP'] = live_data['Data'][0]["LastTradedPrice"],
                            main_li['Volume'] = live_data['Data'][0]["Volume"],
                            main_li['Vwap'] = live_data['Data'][0]["AverageTradePrice"],
                            main_li['Close'] = live_data['Data'][0]["Close"],
                            main_li['OI'] = live_data['Data'][0]["OpenInterest"],
                            main_li['NetChange'] = live_data['Data'][0]["NetChange"] 
                            main_list = pd.concat([main_li, main_list])     
                            
                        except Exception as e:
                            pass                
                idx +=1
 
            #main_list.sort_values(['Symbol'], ascending=[True], inplace=True)
            main_list['Time'] = datetime.now()
            dt.range("e1").options(index=False).value = main_list      
        
            #odbook = pd.read_excel('E:/STOCK/Capital_vercel1/test1.xlsx', sheet_name='obook',index_col=False)
            # print(odbook.dtypes)

            live_market_keys.reverse()
            index_frame = pd.DataFrame()
            index_frame_one = pd.DataFrame()

            for idx in live_market_keys:
                print(idx)
                index_fra = nse.live_market_data(idx) 
                tot_valuee = index_fra["totalTradedValue"].iloc[0]               
                index_fra['Index'] = idx                
                index_fram = index_fra[1:]
                index_fram['Weitage'] = round(((index_fram["totalTradedValue"]*100)/tot_valuee),2)
                post = (index_fram['change'] > 0).sum().sum()
                negat = (index_fram['change'] < 0).sum().sum()
                index_frame = pd.concat([index_fram, index_frame])
                index_row = index_fra[:1] 
                idx_len = len(index_fram['Index'])
                index_row['Post'] = post
                index_row['Negat'] = negat
                index_row['Neutral'] = idx_len-(index_row['Post']+index_row['Negat'])
                index_row['Total'] = idx_len
                index_row['Calc'] = (index_row['Post']*100)/index_row['Total']
                index_row['Per'] = np.where(index_row['Calc']<50,index_row['Calc']*-1,index_row['Calc']*1)
                index_frame_one = pd.concat([index_row, index_frame_one],axis=0)

            index_frame_one.sort_values(['change','identifier'], ascending=[True,True], inplace=True)
            index_frame_one = index_frame_one[['Index','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','lastUpdateTime','Post','Negat','Neutral','Total','Per']]
            index_frame.sort_values(['Index','change'], ascending=[True,True], inplace=True)
            index_frame = index_frame[['Index','identifier','open','dayHigh','dayLow','lastPrice','previousClose','change','pChange','Weitage','totalTradedVolume','totalTradedValue','lastUpdateTime']]
            st3.range("a1").options(index=False).value = index_frame
            st2.range("a:n").value = None
            st2.range("a1").options(index=False).value = index_frame_one
            
            
            nift_50 = index_frame_one[index_frame_one['Index'] == "NIFTY 50"] 
            nift_bank = index_frame_one[index_frame_one['Index'] == "NIFTY BANK"] 
            niftt_50 = round(float(nift_50['Per']),2)
            niftt_bank = round(float(nift_bank['Per']),2)
            print("Nifty_50 Per is : "+str(niftt_50))
            print("BankNifty Per is : "+str(niftt_bank))
            
            main_list = pd.merge(scpts, main_list, on=['Symbol'], how='inner')
            main_list1 = main_list[main_list['Buy/Sell'] == "BUY"] 
            main_list2 = main_list[main_list['Buy/Sell'] == "SELL"] 
            
            funn = 14000
            Profit = 200
            Loss = -200

            funn = pd.DataFrame(client.margin())['AvailableMargin'] 
            fund1 = funn*2
            fund2 = funn         

            if main_list1.empty:
                print("main_list1 Is Empty")
                leght1 = 0
                main_list1['Exp_Qty'] = 0
            else:
                leght1 = fund1/(len(main_list1['LTP']))
                main_list1['Exp_Qty'] = (round((float(leght1)/(main_list1['LTP'])),0))

            if main_list2.empty:
                print("main_list2 Is Empty")
                leght2 = 0
                main_list2['Exp_Qty'] = 0
            else:
                leght2 = fund2/(len(main_list2['LTP']))
                main_list2['Exp_Qty'] = (round((float(leght2)/(main_list2['LTP'])),0))

            st.range("a1").options(index=False).value = main_list   
            
            st1.range("a1").options(index=False).value = main_list
            # sheet_length = len(main_list1['LTP'])
            # print(sheet_length)
            # for i in range(10000):
            #     sheet_length = i+1
            #st4.range("a1").ver
            rng = range('A1').vertical.last_cell

            #st4.range((rng.row + 1, rng.column)).value = main_list
            #st4.range("a1").vertical.last_cell.options(index=False).value = main_list
            Stat4 = main_list 
            #Stat4 = pd.read_excel('E:/STOCK/Capital_vercel1/test1.xlsx', sheet_name='Stat1')
            Stat5 = pd.concat([main_list, Stat4])  
            Stat5.sort_values(['Time'], ascending=[True], inplace=True)
            Stat6 = Stat5.drop_duplicates(subset=['Symbol'], keep='first')
            Stat6['Time_diff'] = (datetime.now() - Stat6['Time'])
            Stat6['Exp_Qty'] = np.where(Stat6['Buy/Sell'] == "BUY",(round((float(leght1)/(Stat6['LTP'])),0)),(round((float(leght2)/(Stat6['LTP'])),0)))
            Stat6.sort_values(['Time'], ascending=[True], inplace=True)
            st1.range("a1").options(index=False).value = Stat6        
            
            Buy_list_new = main_list1['Symbol']
            Sell_list_new = main_list2['Symbol']
            print("hjk")
            if (niftt_50 >= 60 and niftt_bank >= 60):
                for b in Buy_list_new: 
                    Buy_data = main_list1[main_list1['Symbol'] == b]
                    Buy_data = Buy_data.fillna(0)
                    Buy_ScripCodee = int(Buy_data['ScriptCode'])                    
                    Buy_Exp_Qty = int(Buy_data['Exp_Qty'])
                    Buy_ltp =  float(Buy_data['LTP'])
                    Buy_StopLossPri = round((Buy_ltp-((Buy_ltp*2)/100)),2)
                    Buy_StopLossPrice = round((round(Buy_StopLossPri / 0.05) * 0.05),2)
                    print(Buy_StopLossPri,Buy_StopLossPrice)
                    print("Market is Bullish")  
                    #order = client.place_order(OrderType="B",Exchange='N',ExchangeType='C', ScripCode = Buy_ScripCodee, Qty=Buy_Exp_Qty,Price=Buy_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Buy_StopLossPrice)
                    print("Buy Order Excecuted of : "+str(b)+" at Current Ltp is : "+str(Buy_ltp)+" and Qty is : "+str(Buy_Exp_Qty)+" and Stop Loss is : "+str(Buy_StopLossPrice))
 
            if (niftt_50 <= 40 and niftt_bank <= 40):
                for s in Sell_list_new: 
                    Sell_data = main_list2[main_list2['Symbol'] == s]
                    Sell_data = Sell_data.fillna(0)
                    Sell_ScripCodee = int(Sell_data['ScriptCode'])                    
                    Sell_Exp_Qty = int(Sell_data['Exp_Qty'])
                    Sell_ltp =  float(Sell_data['LTP'])
                    Sell_StopLossPri = round((Sell_ltp-((Sell_ltp*2)/100)),2)
                    Sell_StopLossPrice = round((round(Sell_StopLossPri / 0.05) * 0.05),2)
                    print(Sell_StopLossPri,Sell_StopLossPrice)
                    print("Market is Bearish")  
                    #order = client.place_order(OrderType="B",Exchange='N',ExchangeType='C', ScripCode = Sell_ScripCodee, Qty=Sell_Exp_Qty,Price=Sell_ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=Sell_StopLossPrice)
                    print("Sell Order Excecuted of : "+str(s)+" at Current Ltp is : "+str(Sell_ltp)+" and Qty is : "+str(Sell_Exp_Qty)+" and Stop Loss is : "+str(Sell_StopLossPrice))

            if ((niftt_50 > 40 and niftt_50 < 60) and (niftt_bank > 40 and niftt_bank < 60)):
                    print("Market is Sideways")
            else :
                print("Undeciced Market")
            odbook = get_orderbook() 
            odbook1 = pd.DataFrame(odbook)
            odbook1 = odbook1[odbook1["BuySell"] == "B"]
            odbook1['Value'] = odbook1['Qty']*odbook1['Rate']
            odbook1['Rate_Total'] = odbook1.groupby(['Symbol'])['Value'].transform('sum')
            odbook1['Qty_Total'] = odbook1.groupby(['Symbol'])['Qty'].transform('sum')
            odbook1['Avg_rate'] = np.round((np.where((odbook1['Qty'] == odbook1['Qty_Total']),odbook1['Rate'],(odbook1['Rate_Total']/odbook1['Qty_Total']))),2)
            ob.range("a1").options(index=False).value = odbook
            ob.range("a5").options(index=False).value = odbook1
            Stat7 = pd.merge(Stat6, odbook1, on=['Symbol'], how='outer')
            # Stat7 = [['Symbol','Buy/Sell','ScriptCode','Open','High','Low','LTP','Volume','Vwap','Close','OI','NetChange','Time','Time_diff','Exp_Qty',
            # 	'Datetimeee','Qty','Rate','DelvIntra','SLTriggerRate','WithSL',	'Value','Rate_Total','Qty_Total','Avg_rate',]]
            Stat7.sort_values(['Time'], ascending=[True], inplace=True)
            st1.range("a1").options(index=False).value = Stat7
            wb.save("test1.xlsx")
            # if (niftt_50 > 60 and niftt_bank > 60):
            #     print("Market is Bullish")

            #     if ordboook.empty:
            #         print("Order Book Is Empty_2")
            #         filt_data = main_list
            #         filt_data=filt_data[['ScriptCode','Symbol','Buy/Sell',"Open","High","Low","LTP","Volume","Vwap","Close","OI","NetChange","Exp_Qty"]]
            #         filt_data = filt_data[filt_data['Buy/Sell'] == "BUY"] 
            #         st.range("a1").options(index=False).value = filt_data
            #         ord_book_list = filt_data['Symbol']
    
            #         for j in ord_book_list:               
            #             eq_da = filt_data[filt_data['Symbol'] == j]
            #             ScripCodee = int(eq_da['ScriptCode'])
            #             Exp_Qty = int(eq_da['Exp_Qty'])
            #             ltp = float(eq_da['LTP'])
            #             StopLossPri = round((ltp-((ltp*2)/100)),2)
            #             StopLossPrice = round((float(round(StopLossPri / 0.05) * 0.05)),2)
            #             #order = client.place_order(OrderType="B",Exchange='N',ExchangeType='C', ScripCode = ScripCodee, Qty=Exp_Qty,Price=ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=StopLossPrice)
            #             print("Buy Order Excecuted of : "+str(j)+" at Current Ltp is : "+str(ltp)+" and Qty is : "+str(Exp_Qty)+" and Stop Loss is : "+str(StopLossPrice))
                
            #     else : 
            #         print("Order Book Is Not Empty")
            #         odbok = odbook1[odbook1["BuySell"] == "B"]
            #         filt_da = pd.merge(main_list, odbok, on=['Symbol'], how='outer')
            #         filt_da=filt_da[['ScriptCode','Symbol','Buy/Sell',"Open","High","Low","LTP","Volume","Vwap","Close","OI","NetChange","Exp_Qty",
            #             "Avg_rate","Qty","Datetimeee"]]
                    
            #         filt_da['P_L'] = filt_da["LTP"]-filt_da["Avg_rate"]
            #         filt_da['P_L_Per'] = (100*filt_da['P_L'])/filt_da['Avg_rate']
            #         filt_da['Value'] = filt_da["P_L"]*filt_da["Qty"]
            #         filt_da = filt_da.fillna(0)
            #         filt_da['Status'] = np.where(filt_da['P_L'] > Profit,"TGT", np.where(filt_da['P_L'] < Loss,"SL", ""))
            #         posit = pd.DataFrame(client.positions())
            #         print(posit)
            #         posit.rename(columns={'ScripName': 'Symbol'},inplace=True)
            #         print(posit)
            #         filt_data = pd.merge(filt_da, posit,  on=['Symbol'], how='inner')
            #         print(filt_data)
            #         filt_data = filt_da
            #         filt_data = filt_data[['ScriptCode','Symbol','Buy/Sell','Open','High','Low','LTP','Volume','Vwap','Close','OI','NetChange','Exp_Qty','Avg_rate','Qty','BookedPL','P_L','P_L_Per','Status','Datetimeee']]

            #         filt_data[['Open','High','Low','LTP_x','Volume','Vwap','Close','OI','NetChange']] = filt_data[['Open','High','Low','LTP_x','Volume','Vwap','Close','OI','NetChange']].apply(pd.to_numeric)
            #         filt_data['Time'] = pd.Timestamp("now")
            #         filt_data = filt_data[filt_data['Buy/Sell'] == "BUY"] 
            #         #hr_df.loc['Total'] = hr_df.iloc[:,1:4].sum()
            #         #filt_data.loc["BookedPL", "P_L"] = filt_data.BookedPL.sum()

            #         st.range("a1").options(index=False).value = filt_data   
            #         filt_data2 = filt_data
            #         #filt_data2 = filt_data2[['ScriptCode','Symbol','Buy/Sell','Open','High','Low','LTP','Volume','Vwap','Close','OI','NetChange','Time']]

            #         st1.range("a1").options(index=False).value = filt_data2
            #         Stat4 = pd.read_excel('E:/STOCK/Capital_vercel1/test1.xlsx', sheet_name='Stat1')
            #         Stat5 = pd.concat([filt_data2, Stat4])  
            #         #Stat5 = filt_data2.append(Stat4)
            #         Stat5.sort_values(['Time'], ascending=[True], inplace=True)
            #         Stat6 = Stat5.drop_duplicates(subset=['Symbol'], keep='first')
            #         st1.range("a1").options(index=False).value = Stat6

                
            #         filt_data1 = filt_data
            #         result_df = filt_data1.drop_duplicates(subset=['Symbol'])
    
            #         buy_not_okk = result_df[result_df['Avg_rate'] == 0]
            #         buy_not_sym = buy_not_okk['Symbol']

            #         for j in buy_not_sym:      
            #             buy_not_ok = buy_not_okk[buy_not_okk['Symbol'] == j]
            #             ScripCodee = int(buy_not_ok['ScriptCode'])
            #             Exp_Qty = int(buy_not_ok['Exp_Qty'])
            #             ltp =  float(buy_not_ok['LTP'])
            #             StopLossPri = round((ltp-((ltp*2)/100)),2)
            #             StopLossPrice = round((round(StopLossPri / 0.05) * 0.05),2)
            #             print("Buy Order Excecuted of : "+str(j)+" at Current Ltp is : "+str(ltp)+" and Qty is : "+str(Exp_Qty)+" and Stop Loss is : "+str(StopLossPrice))
            #             #order = client.place_order(OrderType="B",Exchange='N',ExchangeType='C', ScripCode = ScripCodee, Qty=Exp_Qty,Price=ltp, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=StopLossPrice)
            
            # else :
            #     print("Market is Bearish")  

            pos.range("a4").options(index=False).value = pd.DataFrame(client.positions()) 
            pos.range("a1").options(index=False).value = pd.DataFrame(client.margin())
            #pos.range("a4").options(index=False).value = pd.DataFrame(client.positions())

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

    # enctoken = "gQ/zLVyhmVCyuSSga5+qu+44S7z7kcKiOfb1eww3FYFrhVfgG/0pUuTcpc5Kz0yYWInqvFG1XZT+9CKGNf8Za4LEWssj1r0UnZcaQnO/NiuuvETXs9trrA=="
    # kite = KiteApp(enctoken=enctoken)
    # get_orderbook()
    # quote('NIFTY')
    start_excel()



