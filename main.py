from telethon import TelegramClient, events, utils
from pymongo import MongoClient
import asyncio

class KeywordDeleter:
    def __init__(self, api_id, api_hash, token, db_uri, db_name):
        self.client = TelegramClient('bot', api_id, api_hash).start(bot_token=token)
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
        asyncio.get_event_loop().run_until_complete(self.delete_past_messages('YOUR_CHANNEL_NAME'))
        self.client.run_until_disconnected()

if __name__ == '__main__':
    kd = KeywordDeleter('YOUR_API_ID', 'YOUR_API_HASH', 'YOUR_BOT_TOKEN', 'mongodb://localhost:27017', 'telegram_bot')
    kd.run()
