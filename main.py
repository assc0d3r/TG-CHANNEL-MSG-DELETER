import asyncio
from telethon import TelegramClient, events, types
import logging
from decouple import config
import re
from telethon.sync import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession


import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.WARNING)

# Define environment variables if not provided in config file
api_id = config("API_ID")
keywords= config("KEYWORDS")
#amogh= config("TG_SESSION_STRING")
channel_id= config("CHANNEL_ID")
api_hash= config("API_HASH")
bot_token= config("BOT_TOKEN")

client = TelegramClient('amogh', api_id, api_hash).start(bot_token=bot_token)

async def delete_messages(keyword):
    async for message in client.iter_messages(channel_id):
        if message.media:
            if hasattr(message.media, 'document') and message.media.document.mime_type.startswith('video'):
                if message.text and re.search(keyword, message.text):
                    print(message.stringify())
                    try:
                        await client.delete_messages(channel_id, message.id)
                        await asyncio.sleep(9)  # Sleep for 3 seconds
                    except FloodWaitError as e:
                        print('We have to wait', e.seconds, 'seconds before continuing')
                        await asyncio.sleep(e.seconds)

async def main():
    tasks = [delete_messages(keyword) for keyword in keywords]
    await asyncio.gather(*tasks)

with client:
    client.loop.run_until_complete(main())

