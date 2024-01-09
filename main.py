from telethon import TelegramClient, events, utils, errors
from pymongo import MongoClient
import asyncio
from decouple import config
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename='logfile.log',
)
logging.getLogger("pyrogram").setLevel(logging.DEBUG)

API_ID = config("API_ID")
API_HASH = config("API_HASH")
BOT_TOKEN = config("BOT_TOKEN")
CHANNEL_NAME = config("CHANNEL_NAME")
DB_URI = config("DB_URI")
DB_NAME = config("DB_NAME")                

class KeywordDeleter:
    def __init__(self, API_ID, API_HASH, BOT_TOKEN, DB_URI, DB_NAME):
        self.client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
        self.db = MongoClient(db_uri)[db_name]
        self.keywords = set(self.db.keywords.find_one()['keywords'])

    async def start(self, event):
        await event.respond("I'm a bot, please talk to me!")

    async def add_keyword(self, event):
        keyword = event.raw_text.split(' ', 1)[1]
        self.keywords.add(keyword)
        self.db.keywords.update_one({}, {'$set': {'keywords': list(self.keywords)}})
        await event.respond(f"Added keyword: {keyword}")

    async def delete_message(self, event):
        message_text = event.raw_text
        for keyword in self.keywords:
            if keyword in message_text:
                await event.delete()
                break

    async def delete_past_messages(self, channel):
        async for message in self.client.iter_messages(channel):
            for keyword in self.keywords:
                if keyword in message.text:
                    await self.client.delete_messages(channel, message.id)
                    break

    def run(self):
        self.client.add_event_handler(self.start, events.NewMessage(pattern='/start'))
        self.client.add_event_handler(self.add_keyword, events.NewMessage(pattern='/addkeyword'))
        self.client.add_event_handler(self.delete_message, events.NewMessage())
        asyncio.get_event_loop().run_until_complete(self.delete_past_messages('CHANNEL_NAME'))
        self.client.run_until_disconnected()

#if __name__ == '__main__':
    kd = KeywordDeleter(API_ID, 'API_HASH', BOT_TOKEN, 'DB_URI', 'telegram_bot')
    kd.run()
