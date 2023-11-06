from telethon import TelegramClient, events
from telegram_read_msg import *
import re
import numpy as np
from five_paisa import *

clientt = TelegramClient('mukesh', api_id, api_hash)

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)
exc_equity = pd.DataFrame(script_code_5paisa)
exc_equity = exc_equity[(exc_equity["Exch"] == "N") & (exc_equity["ExchType"] == "C")]
exc_equity = exc_equity[exc_equity["Series"] == "EQ"]
exc_equity = exc_equity[exc_equity["CpType"] == "XX"]
exc_equity["Watchlist"] = exc_equity["Exch"] + ":" + exc_equity["ExchType"] + ":" + exc_equity["Name"]
exc_equity.sort_values(['Name'], ascending=[True], inplace=True)


def placeOrder(transType,symbol,scriptcode,Qty,isBuy,SL,target):
    order = client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = scriptcode, Qty=Qty,Price=isBuy, IsIntraday=True, IsStopLossOrder=True, StopLossPrice=SL)
    print(f'Place {transType} Order of {symbol} AT {isBuy} SL {SL} Target {target}')


def check_stat(statment):
    regex = r'\b\b.*\bLOOKS GOOD ABOVE\b.*\bADD TILL\b.*\bSUPPORT\b'
    match = re.search(regex,statment,re.IGNORECASE)
    if match:
        return True
    else:
        return False

def find_stat(statment,target_word):

    global symbol3,scriptcode2
    regex = r'\b{}\b\s+(\w+)'.format(target_word)
    match = re.search(regex,statment,re.IGNORECASE)
    symbol = statment[0:statment.find("LOOKS")]
    res = symbol.split() 
        
    ignore_list = ['FOR','TOMORROW','BREAKOUT','STOCK']

    list1 = []
    for i in res: 
        if i in ignore_list:
            pass
        else: 
            list1.append(i)
    resss = "".join([str(item) for item in list1])
    ressss = str(resss)
    #exc_equity1 = exc_equity[exc_equity.select_dtypes(object).apply(lambda row: row.str.contains('ZYDUSWELL'), axis=1).any(axis=1)]
    exc_equity1 = exc_equity[exc_equity['Root'].astype(str).str.contains((str(ressss)), regex=False)]
    if exc_equity1.empty:
        print('Symbol Not Matched')
    else:
        symbol1 = np.unique([str(i) for i in exc_equity1['Root']]).tolist()
        symbol2 = symbol1[0]
        symbol3 = str(symbol2)
        scriptcode = np.unique([int(i) for i in exc_equity1['Scripcode']]).tolist()
        scriptcode1 = scriptcode[0]
        scriptcode2 = int(scriptcode1)
        #symbol1 = str(exc_equity1['Root'][0])
        print(symbol3)
        print(scriptcode2)

    if match:
        return match.group(1)
    else:
        return None

@clientt.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

@clientt.on(events.NewMessage(chats=-1001762746549))
async def my_event_handler(event):
    statmen = event.raw_text
    statment = " ".join(line.strip() for line in statmen.splitlines())
    #statment.split()
    if check_stat(statment):
        print(check_stat(statment))
        await clientt.send_message(-4048562236,f'Got Signal {statment}')
        print(f'Pattern match for entry {statment}')
        isBuy = find_stat(statment,'LOOKS GOOD ABOVE')
        add_till = find_stat(statment,'ADD TILL')
        sl = find_stat(statment,'SUPPORT')
        target = find_stat(statment,'TARGET')
        isSell = ''
        isBuy = float(isBuy)
        sl = float(sl)


        if isBuy < 100:
            Qtyy = 200
        if isBuy > 100 and isBuy < 200:
            Qtyy = 100                        
        if isBuy > 200 and isBuy < 300:
            Qtyy = 80
        if isBuy > 300:
            Qtyy = 50
        Req_Amount = Qtyy*isBuy  
        print("Required Amount is "+str(Req_Amount))
        
        if isBuy:
            placeOrder('BUY',symbol3,scriptcode2,Qtyy,isBuy,sl,target)
        elif isSell:
            placeOrder('SELL',symbol3,scriptcode2,Qtyy,isBuy,sl,target)

clientt.start()
clientt.run_until_disconnected()