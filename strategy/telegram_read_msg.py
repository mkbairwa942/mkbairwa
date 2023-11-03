#import yfinance as yf
#import ta
#from ta import add_all_ta_features
#from ta.utils import dropna
# import pandas_ta as pta
#from finta import TA
# import talib
# import pandas as pd
# import copy
# import numpy as np
# import xlwings as xw
# from five_paisa import *
# from datetime import datetime,timedelta
# from numpy import log as nplog
# from numpy import NaN as npNaN
# from pandas import DataFrame, Series
# from pandas_ta.overlap import ema, hl2
# from pandas_ta.utils import get_offset, high_low_range, verify_series, zero
# from io import BytesIO
# import os
# from zipfile import ZipFile
# import requests
# import itertools

from telethon.sync import TelegramClient
import datetime
import pandas as pd
import requests
import time

first_name = "mkbairwa"
username = "mkbairwa_bot"
id = ":758543600"
zealous = "-4048562236"

api_id = 21176219
api_hash = "a427ae341f1376acb2691ae1101b91b8"


# print("hi")
# resp = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getMe")
# resp1 = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates")
# resp2 = requests.get("https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates?offset=6432816471")

# basr_url = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates"



# parameters = {
#     "offset" : ":758543600",
#     #"limit" : "2"
# }

# resp = requests.get(basr_url, data=parameters)
# #print(resp.text)

# basr_url1 = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/getUpdates"
# send_msg = "https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessags?chat_id=-4048562236"

# jokes = ["I Invented a New Bot","jokes1","jokes2","jokes3"]
# # for joke in jokes:
#     time.sleep(2)
#     parameters1 = {
#         "chat_id" : "6143172607",
#         "text" : joke
#     }

#     resp = requests.get(basr_url1, data=parameters1)
#     print(resp.text)

# print("hi_all")

# for joke in jokes:
#     #print(joke) 
#     urll = 'https://api.telegram.org/bot6432816471:AAG08nWywTnf_Lg5aDHPbW7zjk3LevFuajU/sendMessage?chat_id=-4048562236&text="{}"'.format(joke)
#     #print(urll)
#     requests.get(urll)


# Remember to use your own values from my.telegram.org!

client = TelegramClient('mukesh', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    #print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')
    # # ...to some chat ID
    await client.send_message(6432816471, 'Hello, group!')
    # ...to your contacts
    # await client.send_message('+919610033622', 'Hello, friend!')
    # # ...or even to any username
    # await client.send_message('username', 'Testing Telethon!')

    # # You can, of course, use markdown in your messages:
    # message = await client.send_message(
    #     'me',
    #     'This message has **bold**, `code`, __italics__ and '
    #     'a [nice website](https://example.com)!',
    #     link_preview=False
    # )

    # # Sending a message returns the sent message object, which you can use
    # print(message.raw_text)

    # # You can reply to messages directly if you have a message object
    # await message.reply('Cool!')

    # # Or send files, songs, documents, albums...
    # await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # # You can print the message history of any chat:
    # async for message in client.iter_messages('me'):
    #     print(message.id, message.text)

    #     # You can download media from messages, too!
    #     # The method will return the path where the file was saved.
    #     if message.photo:
    #         path = await message.download_media()
    #         print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())
