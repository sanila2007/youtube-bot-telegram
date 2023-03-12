from pyrogram import Client
from config import Config

plugins = dict(
    root="plugins"
)

print("I am awake")

bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins
)
bot.run()
