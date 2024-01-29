#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install python-telegram-bot --upgrade


# In[ ]:



pip install dataframe_image


# In[ ]:



apikey = 'angel_api_key'
username = 'angel_username'
pwd = 'angel_pwd'
CHAT_ID = 'chat_id'
BOT_TOKEN = 'bot_token'


# In[ ]:


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# In[ ]:


from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from smartapi import SmartConnect
import pandas as pd
import dataframe_image
import threading

ANGEL_OBJ =None
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def loginAngel():
    global ANGEL_OBJ
    obj=SmartConnect(api_key=apikey)
    data = obj.generateSession(username,pwd)
    refreshToken= data['data']['refreshToken']
    res = obj.getProfile(refreshToken)
    ANGEL_OBJ = obj
    return res['data']['exchanges'] 
    
def isValidUser(chat_id):
     return CHAT_ID == str(chat_id)
    
def echo(update: Update, context: CallbackContext):
    if isValidUser(update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Nothing to say')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"unauthorized access")

        
def orderbook(update: Update, context: CallbackContext):
    global ANGEL_OBJ
    if ANGEL_OBJ is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Login First')
        return
    
    orderRes= ANGEL_OBJ.orderBook()
    if orderRes['data'] and len(orderRes['data']) > 0:
        orderdf = pd.DataFrame(orderRes['data'])
        orderdf = orderdf[['tradingsymbol','transactiontype','variety','ordertype','producttype','quantity','status']]
        dataframe_image.export(orderdf, "order.png")
        
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo= open("C:/Users/hari/order.png", 'rb')  , caption="OrderBook")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Orderbook Empty')

def holding(update: Update, context: CallbackContext):
    global ANGEL_OBJ
    if ANGEL_OBJ is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Login First')
        return
    
    holdres= ANGEL_OBJ.holding() 
    
    if holdres['data'] and len(holdres['data']) > 0:
        holdingDf = pd.DataFrame(holdres['data'])
        dataframe_image.export(holdingDf, "holding.png")
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo= open("C:/Users/hari/holding.png", 'rb')  , caption="Holding")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Orderbook Empty')
    
    
def login(update: Update, context: CallbackContext):
    if isValidUser(update.effective_chat.id):
        res = loginAngel()
        context.bot.send_message(chat_id=update.effective_chat.id, text=res)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unauthorized access")

def error_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Something is Wrong")


def stopBot():
    updater.stop()
    updater.is_idle = False
    
    
def stop(update: Update, context: CallbackContext):
    if isValidUser(update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Stopping Bot......')
        threading.Thread(target=stopBot).start()
        
        
def start(update: Update, context: CallbackContext):
    if isValidUser(update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id, text='To get status first login \n /login \n /orderbook \n /holding \n /stop')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"unauthorized access")



login_handler = CommandHandler('login', login)
dispatcher.add_handler(login_handler)

orderBook_handler = CommandHandler('orderbook', orderbook)
dispatcher.add_handler(orderBook_handler)

stopBot_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stopBot_handler)

holding_handler = CommandHandler('holding', holding)
dispatcher.add_handler(holding_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

dispatcher.add_error_handler(error_handler)
    


# In[ ]:


updater.start_polling()


# In[ ]:


updater.stop()


# In[ ]:





# In[ ]:





# In[ ]:


import pandas as pd

data = {'Name':['A', 'B', 'C', 'D'],
        'Age':[34, 12, 56, 7]}
 
# Create DataFrame
df = pd.DataFrame(data)
df


# In[ ]:


import dataframe_image
dataframe_image.export(df, "demmo.png")

