import os
from telethon import TelegramClient, events

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION = os.getenv('SESSION')
blacklisted_words = os.getenv('BLACKLISTED_WORDS').split(',')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')

client = TelegramClient(stringsession(SESSION), API_ID, API_HASH)

async def main():
    async for message in client.iter_messages(CHANNEL_LINK):
        if any(word in message.text for word in blacklisted_words):
            await message.delete()

with client:
    client.loop.run_until_complete(main())
