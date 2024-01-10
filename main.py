import asyncio
from telethon import TelegramClient, events, types
from bson import ObjectId
import pymongo
import logging
from decouple import config

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Load configuration from environment or config file
config = {}
for key, value in os.environ.items():
    config[key] = value

# Define environment variables if not provided in config file
TG_BOT_TOKEN = config("TG_BOT_TOKEN")
KEYWORDS_COLLECTION= config("KEYWORDS_COLLECTION")
TG_SESSION_STRING= config("TG_SESSION_STRING")
CHANNEL_ID = config("CHANNEL_ID")
    
# Create a MongoDB client
try:
    client = pymongo.MongoClient(config["MONGODB_URI"])
except pymongo.MongoClientError as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    exit(1)

database = client["your_database"]
keywords_collection = database[config["KEYWORDS_COLLECTION"]]

# Define a helper function to delete a media file from a channel
async def delete_media_file(channel_id, media_file_path):
    try:
        await client(
            types.InputFileRequest(
                type=types.InputFileType.FILE,
                id=await client.get_file_id(media_file_path)
            )
        ).delete()
        logger.info(f"Deleted media file in channel {channel_id}: {media_file_path}")
    except Exception as e:
        logger.error(f"Error deleting media file: {e}")

# Define a helper function to add a keyword to the MongoDB collection
async def add_keyword(message):
    keyword = message.text.split()[1]
    try:
        keywords_collection.insert_one({"text": keyword})
        logger.info(f"Added keyword '{keyword}' to MongoDB collection")
        await message.reply(f"Keyword '{keyword}' added successfully")
    except pymongo.errors.DuplicateKeyError:
        logger.info(f"Keyword '{keyword}' already exists in MongoDB collection")
        await message.reply(f"Keyword '{keyword}' already exists.")
    except Exception as e:
        logger.error(f"Error adding keyword to MongoDB: {e}")
        await message.reply(f"Error adding keyword: {e}")

# Define a helper function to delete a keyword from the MongoDB collection
async def delete_keyword(message):
    keyword = message.text.split()[1]
    try:
        keywords_collection.delete_one({"text": keyword})
        logger.info(f"Deleted keyword '{keyword}' from MongoDB collection")
        await message.reply(f"Keyword '{keyword}' deleted successfully")
    except pymongo.errors.NotFoundError:
        logger.info(f"Keyword '{keyword}' not found in MongoDB collection")
        await message.reply(f"Keyword '{keyword}' not found.")
    except Exception as e:
        logger.error(f"Error deleting keyword from MongoDB: {e}")
        await message.reply(f"Error deleting keyword: {e}")

# Define a helper function to handle user commands
async def handle_command(message):
    if message.text.startswith("/addkeyword"):
        await add_keyword(message)
    elif message.text.startswith("/deletekeyword"):
        await delete_keyword(message)
    else:
        await message.reply("Invalid command.")

# Create a Telegram client instance
async def bardmsgdel():
    async with TelegramClient(config["TG_SESSION_STRING"], config["TG_BOT_TOKEN"]) as client:
        # Get all keywords from the MongoDB collection
        keywords = list(keywords_collection.find())

        # Process each channel and search for media matching the keywords
        for channel in await client.get_dialogs(limit=200):
            if channel.type != types.InputChannelType.CHANNEL:
                continue

            channel_id = channel.id

            for keyword in keywords:
                keyword_text = keyword["text"]
                media_files = await client.get_messages(channel_id)

                # Search for media files containing the specified keyword
                for media_file in media_files:
                    if keyword_text in media_file.caption and media_file.media:
                        media_file_path = media_file.media.document.file_path
                        logger.info(f"Found media matching keyword '{keyword_text}' in channel {channel_id}: {media_file_path}")

                        # Delete the media file
                        await delete_media_file(channel_id, media_file_path)
            logger.error(f"Error during execution: {e}")
        exit(1)
    client.run_until_disconnected(bardmsgdel())
