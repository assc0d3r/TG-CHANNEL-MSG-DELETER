import asyncio
from telethon import TelegramClient, events, types
import logging
import re
from telethon.sync import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession


import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.WARNING)

# Define environment variables if not provided in config file
api_id = os.getenv("API_ID")
keyword_pattern= os.getenv("KEYWORD_PATTERN")
session= os.getenv("SESSION")
channel_username= os.getenv("CHANNEL_USERNAME")
api_hash= os.getenv("API_HASH")

async def amogh():
    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.start()

    entity = await client.get_entity(channel_username)

    async def process_media(message):
        if message.media:
            file_name = message.file.name
            text = message.message

            if re.search(keyword_pattern, text, flags=re.IGNORECASE):  # Case-insensitive match
                try:
                    await message.delete()
                    print(f"Deleted message with filename: {file_name}")
                except Exception as e:
                    print(f"Error deleting message: {e}")
                    await asyncio.sleep(45)  # Longer wait for potential flood wait errors

    @client.on(events.NewMessage(chats=entity, incoming=True))
    async def handler(event):
        await process_media(event.message)

    async def process_history():
        offset_id = 0
        limit = 100

        while True:
            messages = await client.get_messages(entity, limit=limit, offset_id=offset_id)
            if not messages:
                break

            for message in messages:
                await process_media(message)

            offset_id = messages[-1].id + 1
            await asyncio.sleep(9)  # Sleep for 9 seconds between batches
            
    async def monitor_new_messages():
        @client.on(events.NewMessage(chats=entity, incoming=True))
        async def handler(event):
            await process_media(event.message)

    await process_history()
    await monitor_new_messages()  # Then start live monitoring
    await client.run_until_disconnected()

if __name__ == '__amogh__':
    asyncio.run(amogh())
