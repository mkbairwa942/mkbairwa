from telethon import TelegramClient, events
from telegram_read_msg import *
import re

client = TelegramClient('mukesh', api_id, api_hash)

script_code_5paisa_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
script_code_5paisa = pd.read_csv(script_code_5paisa_url,low_memory=False)
exc_equity = pd.DataFrame(script_code_5paisa)
exc_equity = exc_equity[(exc_equity["Exch"] == "N") & (exc_equity["ExchType"] == "C")]
exc_equity = exc_equity[exc_equity["Series"] == "EQ"]
exc_equity = exc_equity[exc_equity["CpType"] == "XX"]
exc_equity["Watchlist"] = exc_equity["Exch"] + ":" + exc_equity["ExchType"] + ":" + exc_equity["Name"]
exc_equity.sort_values(['Name'], ascending=[True], inplace=True)
#print(exc_equity)


# statment1= 'LINCOLN PHARMA LOOKS GOOD ABOVE 515 ADD TILL 510 SUPPORT 505'
# statment1.split()
# print(statment1)
# print("hi")

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

def placeOrder(transType,symbol,isBuy,SL,target):
    print(f'Place {transType} Order of {symbol} AT {isBuy} SL {SL} Target {target}')


def check_stat(statment):
    regex = r'\b\b.*\bLOOKS GOOD ABOVE\b.*\bADD TILL\b.*\bSUPPORT\b'
    match = re.search(regex,statment,re.IGNORECASE)
    if match:
        return True
    else:
        return False

def find_stat(statment,target_word):

    global symbol
    regex = r'\b{}\b\s+(\w+)'.format(target_word)
    match = re.search(regex,statment,re.IGNORECASE)
    symbol = statment[0:statment.find("LOOKS")]
    exc_equity['ExerciseDay'] = exc_equity['Root'].str.contains(symbol).astype(int)
    print(exc_equity['ExerciseDay'])

    if match:
        return match.group(1)
    else:
        return None

# statment = statment1
# isBuy = find_stat(statment,'LOOKS GOOD ABOVE')
# add_till = find_stat(statment,'ADD TILL')
# sl = find_stat(statment,'SUPPORT')
# target = find_stat(statment,'TARGET')
# isSell = ''

# print(symbol,isBuy,add_till,sl,target)

# if isBuy:
#     placeOrder('BUY',symbol,isBuy,sl,target)
# elif isSell:
#     placeOrder('SELL',symbol,isBuy,sl,target)

@client.on(events.NewMessage(chats=-4048562236))
async def my_event_handler(event):
    statmen = event.raw_text
    statment = " ".join(line.strip() for line in statmen.splitlines())
    #statment.split()
    print(statment)
    if check_stat(statment):
        print(check_stat(statment))
        await client.send_message(6432816471,f'Got Signal {statment}')
        print(f'Pattern match for entry {statment}')
        isBuy = find_stat(statment,'LOOKS GOOD ABOVE')
        add_till = find_stat(statment,'ADD TILL')
        sl = find_stat(statment,'SUPPORT')
        target = find_stat(statment,'TARGET')
        isSell = ''
        if isBuy:
            placeOrder('BUY',symbol,isBuy,sl,target)
        elif isSell:
            placeOrder('SELL',symbol,isBuy,sl,target)




client.start()
client.run_until_disconnected()