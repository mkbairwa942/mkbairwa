from telethon import TelegramClient, events
from telegram_read_msg import *

client = TelegramClient('mukesh', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

@client.on(events.NewMessage(chats=6432816471))
async def my_event_handler(event):
    print(event.raw_text)

x= 'BUY ASTRAL 1900 SL 1890 TRAGET 1950'


client.start()
client.run_until_disconnected()