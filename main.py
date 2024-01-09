import os
from telethon import TelegramClient, events
import logging
from telethon.sessions import StringSession
from decouple import config

#logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)

API_ID = config("API_ID")
API_HASH = config("API_HASH")
SESSION = config("SESSION")
blacklisted_words = config("BLACKLISTED_WORDS")
CHANNEL_LINK = config("CHANNEL_LINK")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def main():
    async for message in client.iter_messages(CHANNEL_LINK):
         blacklisted_words = item.get('blacklisted_words')
    if blacklisted_words is not None:
        if any(word in message.text for word in blacklisted_words):
            await message.delete()
    else:
        print("Blacklisted_words is missing or None.")

with client:
    client.loop.run_until_complete(main())
