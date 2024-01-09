import os
from telethon import TelegramClient, events
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv('SESSION")
blacklisted_words = os.getenv("BLACKLISTED_WORDS")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

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
