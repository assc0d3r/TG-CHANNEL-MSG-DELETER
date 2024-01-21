import asyncio
import os
from telethon import TelegramClient, events, types
import logging
import re
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession


import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.WARNING)

# Define environment variables if not provided in config file
API_ID = os.getenv("API_ID")
KEYWORD_PATTERN = os.getenv("KEYWORD_PATTERN")
SESSION = os.getenv("SESSION")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
API_HASH = os.getenv("API_HASH")

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    SESSION = client.session.save()
    await client.start()

    entity = await client.get_entity(CHANNEL_USERNAME)

    async def process_media(message):
        if message.media:
            file_name = message.file.name
            text = message.message

            if re.search(KEYWORD_PATTERN, text, flags=re.IGNORECASE):  # Case-insensitive match
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

#if __name__ == '__main__':
    asyncio.run(main())
