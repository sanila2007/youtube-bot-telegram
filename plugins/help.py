# Copyright ©️ 2022 Sanila Ranatunga. All Rights Reserved
# You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [YouTube-Bot](https://github.com/sanila2007/YouTube_bot_telegram)

# Read GNU General Public License v3.0: https://github.com/sanila2007/YouTube_bot_telegram/blob/mai/LICENSE
# Don't forget to follow github.com/sanila2007 because I am doing these things for free and open source
# Star, fork, enjoy!


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔍Search YouTube", switch_inline_query_current_chat="")
        ]
    ]
)


@Client.on_message(filters.command("help") & filters.private)
async def help(bot, message):
    await message.reply(
        "This bot can search for YouTube videos & download YouTube videos, playlists and more. Use below methods to do these\n\n"
        "◉ Search for videos - <i>Use inline mode</i>\n"
        "◉ Download videos - <i>Send any link of a Youtube video and select a quality</i>\n"
        "◉ Download videos from playlist - <i>Send any link of a YouTube playlist</i>\n\nThis is quite simple. ||Enjoy it!!||",
        reply_markup=BUTTONS
    )
